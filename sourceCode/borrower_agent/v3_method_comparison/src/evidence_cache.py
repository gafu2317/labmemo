from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from llm_client import get_model
from models import Case
from passion_evidence import extract_passion_evidence

ROOT = Path(__file__).parent.parent
PROMPT_PATH = ROOT / "prompts" / "passion_evidence_extractor.txt"
DEFAULT_CACHE_DIR = ROOT / "evidence_inventories"


@dataclass(frozen=True)
class EvidenceInventoryBundle:
    inventory_id: str
    inventory_sha256: str
    inventory: dict[str, list[dict[str, str]]]
    path: Path


def load_or_create_evidence_inventory(
    case: Case,
    information_level: str,
    temperature: float = 0,
    refresh: bool = False,
    cache_dir: Path = DEFAULT_CACHE_DIR,
) -> EvidenceInventoryBundle:
    """記事レベルごとの証拠在庫を一度だけ抽出し、話法間で共有する。"""
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"{case.id}_{information_level}.json"
    article_sha = _sha256_text(case.article)
    prompt_sha = _sha256_text(PROMPT_PATH.read_text(encoding="utf-8"))

    if path.exists() and not refresh:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("article_sha256") != article_sha:
            raise ValueError(
                f"{path.name} は現在の記事と一致しません。"
                "--refresh-evidence-cache を指定して明示的に更新してください。"
            )
        if data.get("extractor_prompt_sha256") != prompt_sha:
            raise ValueError(
                f"{path.name} は現在の抽出プロンプトと一致しません。"
                "--refresh-evidence-cache を指定して明示的に更新してください。"
            )
        return _bundle_from_data(path, data)

    inventory = extract_passion_evidence(case, temperature=temperature)
    inventory_sha = _sha256_json(inventory)
    inventory_id = (
        f"{case.id}:{information_level}:"
        f"{article_sha[:12]}:{prompt_sha[:12]}:{inventory_sha[:12]}"
    )
    data = {
        "inventory_id": inventory_id,
        "case_id": case.id,
        "information_level": information_level,
        "article_sha256": article_sha,
        "extractor_prompt_sha256": prompt_sha,
        "inventory_sha256": inventory_sha,
        "model": get_model(),
        "temperature": temperature,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "inventory": inventory,
    }
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return _bundle_from_data(path, data)


def _bundle_from_data(path: Path, data: dict) -> EvidenceInventoryBundle:
    inventory = data.get("inventory")
    if not isinstance(inventory, dict):
        raise ValueError(f"{path.name} の inventory が不正です。")
    actual_sha = _sha256_json(inventory)
    if data.get("inventory_sha256") != actual_sha:
        raise ValueError(f"{path.name} の証拠在庫ハッシュが一致しません。")
    return EvidenceInventoryBundle(
        inventory_id=str(data["inventory_id"]),
        inventory_sha256=actual_sha,
        inventory=inventory,
        path=path,
    )


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _sha256_json(value: object) -> str:
    canonical = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return _sha256_text(canonical)

