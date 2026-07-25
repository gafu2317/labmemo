from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from methods import INFORMATION_LEVELS
from models import Case


VARIANTS_DIR = Path(__file__).parent.parent / "article_variants"


def load_case_with_information_level(
    case_path: Path,
    information_level: str,
    variants_dir: Path = VARIANTS_DIR,
) -> Case:
    """同一人物の統制済み記事変種を読み込む。自動要約は行わない。"""
    if information_level not in INFORMATION_LEVELS:
        available = ", ".join(INFORMATION_LEVELS)
        raise ValueError(
            f"未知の情報量: {information_level!r}  使用可能: {available}"
        )

    base = Case.from_yaml(case_path)
    variant_path = variants_dir / f"{base.id}.yaml"
    if not variant_path.exists():
        raise FileNotFoundError(
            f"{base.id} の記事変種がありません: {variant_path}。"
            "V3では情報量操作を研究者が固定するため、自動生成へフォールバックしません。"
        )

    with open(variant_path, encoding="utf-8") as f:
        data: dict[str, Any] = yaml.safe_load(f) or {}

    if data.get("case_id") != base.id:
        raise ValueError(
            f"{variant_path.name} の case_id={data.get('case_id')!r} が "
            f"共有ケースID={base.id!r} と一致しません。"
        )
    levels = data.get("levels", {})
    level_data = levels.get(information_level)
    if not isinstance(level_data, dict):
        raise ValueError(
            f"{variant_path.name} に levels.{information_level} がありません。"
        )

    if level_data.get("use_shared_article") is True:
        article = base.article
    else:
        article = level_data.get("article")
        if not isinstance(article, str) or not article.strip():
            raise ValueError(
                f"{variant_path.name} の levels.{information_level}.article が空です。"
            )

    meta = dict(base.meta)
    meta.update(
        {
            "information_level": information_level,
            "article_variant_file": variant_path.name,
            "article_variant_label": level_data.get("label", information_level),
            "article_variant_design": data.get("design", {}),
        }
    )
    return Case(id=base.id, title=base.title, article=article.strip(), meta=meta)

