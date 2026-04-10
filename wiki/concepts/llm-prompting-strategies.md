# LLMプロンプティング戦略 (LLM Prompting Strategies)

> タグ: #llm #prompting #argument-mining

## 主要手法と比較

| 手法 | 概要 | コスト | 性能 | 用途 |
|------|------|--------|------|------|
| **Zero-shot** | 例示なし、タスク説明のみ | 最低 | 低〜中 | 基線評価 |
| **Few-shot** | ラベル付き例を数件与える | 低 | 中〜高 | プレ研究に最適 |
| **Chain-of-Thought** | 推論ステップを明示させる | 低 | 高 | 複雑なタスク |
| **RAG** | 外部知識を検索・付加 | 中 | 高 | ドメイン特化 |
| **Fine-tuning** | タスク専用データで追加学習 | 高 | 最高 | 本番システム |
| **LoRA** | 効率的なfine-tuning | 中 | 高 | リソース制約下 |

## 議論マイニングでの知見

- **GPT-4のfew-shot** ≈ fine-tunedモデルの性能
- CoTは関係分類（support/attack判定）で特に有効
- few-shotの例の選び方が性能に大きく影響

## プレ研究での推奨アプローチ

**Step 2（プロンプト設計）の指針:**

```
1. まずzero-shotで基線を把握
2. few-shot (3〜5例) で性能を上げる
3. CoTを組み合わせて推論を可視化
4. 出力フォーマットを構造化JSON等で指定
```

**プロンプトテンプレート案（主張・根拠抽出）:**
```
以下の議論テキストから主張と根拠を抽出してください。

例:
テキスト: "〜なぜなら〜だから"
出力: {"claim": "〜", "premise": "〜だから", "relation": "support"}

テキスト: {INPUT}
出力:
```

## 関連記事

- [[concepts/argument-mining]] — 適用タスクの詳細
- [[papers/llm-argument-mining-survey]] — 手法の包括的比較
