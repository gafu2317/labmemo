#!/usr/bin/env python3
"""
tag_wordcloud.py — wiki/papers/ のタグを集計してワードクラウド画像を生成する

Usage:
    python scripts/tag_wordcloud.py
    python scripts/tag_wordcloud.py --output ~/Desktop/tags.png
    python scripts/tag_wordcloud.py --show
"""

import argparse
import re
from collections import Counter
from pathlib import Path

import numpy as np
from wordcloud import WordCloud

WIKI_PAPERS_DIR = Path(__file__).parent.parent / "wiki" / "papers"
OUTPUT_DEFAULT = Path(__file__).parent.parent / "output" / "tag_wordcloud.png"

# macOS NotoSansJP（日本語フォント）
FONT_PATH = str(Path.home() / "Library/Fonts/NotoSansJP-VariableFont_wght.ttf")

# タグ → 日本語表示名のマッピング
TAG_JA: dict[str, str] = {
    "llm": "LLM",
    "argument-mining": "議論マイニング",
    "dialogue": "対話",
    "survey": "サーベイ",
    "topic-shift": "話題転換",
    "dataset": "データセット",
    "multi-agent": "マルチエージェント",
    "evaluation": "評価",
    "rag": "RAG",
    "benchmark": "ベンチマーク",
    "meeting-summarization": "会議要約",
    "hci": "HCI",
    "speech": "音声",
    "summarization": "要約",
    "social-media": "ソーシャルメディア",
    "twitter": "Twitter",
    "prompting": "プロンプティング",
    "stance-detection": "スタンス検出",
    "feedback": "フィードバック",
    "multi-llm": "マルチLLM",
    "classification": "分類",
    "cognitive-bias": "認知バイアス",
    "argumentation-framework": "論証フレームワーク",
    "argumentation-frameworks": "論証フレームワーク",
    "argumentation-theory": "論証理論",
    "argumentation": "論証",
    "computational-argumentation": "計算論的論証",
    "dialogical-am": "対話的議論マイニング",
    "claim-detection": "クレーム検出",
    "claim-verification": "クレーム検証",
    "in-context-learning": "インコンテキスト学習",
    "discussion-summarization": "討論要約",
    "knowledge-grounded": "知識グラウンド",
    "note-taking": "メモ",
    "augmented-reality": "AR",
    "gaze-interaction": "視線操作",
    "user-in-the-loop": "ユーザー参加型",
    "contestable-ai": "コンテスタブルAI",
    "education": "教育",
    "essay-evaluation": "作文評価",
    "explainability": "説明可能性",
    "xai": "説明可能AI",
    "medical-summarization": "医療要約",
    "medical": "医療",
    "clinical-nlp": "臨床NLP",
    "quality-instrument": "品質評価器具",
    "sop": "SOP",
    "it-operations": "ITオペレーション",
    "root-cause-analysis": "根本原因分析",
    "synthetic-data": "合成データ",
    "active-learning": "能動学習",
    "hallucination": "ハルシネーション",
    "factuality": "事実性",
    "citation": "引用",
    "peer-review": "論文レビュー",
    "reasoning": "推論",
    "deductive-reasoning": "演繹推論",
    "uncertainty-quantification": "不確実性定量化",
    "rephrase": "言い換え",
    "rewriting": "書き換え",
    "political-discussion": "政治的討論",
    "persuasion": "説得",
    "debate": "討論",
    "ibm-debater": "IBM Debater",
    "argument-quality": "議論品質",
    "argllm": "ArgLLM",
    "qbaf": "QBAF",
    "rebuttal": "反論",
    "opinion-mining": "意見マイニング",
    "aspect-extraction": "側面抽出",
    "topic-segmentation": "トピック分割",
    "mixed-initiative": "混合主導",
    "annotation": "アノテーション",
    "shared-task": "共有タスク",
    "cross-domain": "クロスドメイン",
    "domain-specific": "ドメイン特化",
    "transformer": "Transformer",
    "bert": "BERT",
    "xlnet": "XLNet",
    "deberta": "DeBERTa",
    "t5": "T5",
    "longformer": "Longformer",
    "contrastive-learning": "対照学習",
    "instruction-tuning": "指示チューニング",
    "rlhf": "RLHF",
    "language-model": "言語モデル",
    "nlp": "NLP",
    "nli": "自然言語推論",
    "multimodal": "マルチモーダル",
    "relation-detection": "関係検出",
    "response-selection": "応答選択",
    "tod": "タスク指向対話",
    "proactive": "プロアクティブ",
    "sequential": "逐次処理",
    "memory": "メモリ",
    "recommendation": "推薦",
    "teacher-student": "教師学生モデル",
    "unsupervised": "教師なし学習",
    "attention": "アテンション",
    "legal-nlp": "法律NLP",
    "chinese": "中国語",
    "portuguese": "ポルトガル語",
    "municipal": "市議会",
    "multi-granularity": "多粒度",
    "odd": "場違い検出",
    "appropriateness": "適切性",
    "llm-judge": "LLM審判",
    "error-detection": "誤り検出",
    "visualization": "可視化",
    "multi-granularity": "多粒度",
}


def collect_tags(wiki_dir: Path) -> Counter:
    """タグを収集し、日本語表示名に変換して集計する。"""
    raw: Counter = Counter()
    for md_file in sorted(wiki_dir.glob("*.md")):
        for line in md_file.read_text(encoding="utf-8").splitlines():
            if line.startswith("> タグ:"):
                tags = re.findall(r"#([\w-]+)", line)
                raw.update(tags)

    # 日本語表示名でマージ集計
    counter: Counter = Counter()
    for tag, count in raw.items():
        ja_name = TAG_JA.get(tag, tag)  # マッピングがなければ英語のまま
        counter[ja_name] += count
    return counter


def make_circle_mask(size: int = 500) -> np.ndarray:
    x, y = np.ogrid[:size, :size]
    center = size // 2
    radius = center - 10
    mask = ((x - center) ** 2 + (y - center) ** 2 > radius ** 2).astype(np.uint8) * 255
    return mask


def generate(counter: Counter, output: Path, show: bool) -> None:
    if not counter:
        print("タグが見つかりませんでした。wiki/papers/ を確認してください。")
        return

    mask = make_circle_mask(500)

    wc = WordCloud(
        font_path=FONT_PATH,
        width=1000,
        height=1000,
        background_color="white",
        colormap="tab20",
        mask=mask,
        contour_width=0,
        prefer_horizontal=0.9,
        max_words=200,
        min_font_size=10,
    )
    wc.generate_from_frequencies(counter)

    output.parent.mkdir(parents=True, exist_ok=True)
    wc.to_file(str(output))
    print(f"保存しました: {output}")

    print("\n--- タグ頻度 Top 20 ---")
    for tag, count in counter.most_common(20):
        bar = "█" * count
        print(f"  #{tag:<30} {count:2d}  {bar}")

    if show:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(8, 8))
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.tight_layout()
        plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(description="wiki/papers/ のタグからワードクラウドを生成")
    parser.add_argument("--output", type=Path, default=OUTPUT_DEFAULT, help="出力先PNGパス")
    parser.add_argument("--show", action="store_true", help="生成後にウィンドウ表示")
    args = parser.parse_args()

    counter = collect_tags(WIKI_PAPERS_DIR)
    print(f"スキャン完了: {sum(counter.values())} タグ / {len(counter)} 種類")
    generate(counter, args.output, args.show)


if __name__ == "__main__":
    main()
