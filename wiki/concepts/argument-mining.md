# 議論マイニング (Argument Mining)

> タグ: #argument-mining #llm #nlp

## 定義

議論マイニングとは、テキストから**主張（claim）**・**根拠（premise）**・それらの**論理的関係**を自動的に抽出・分析する自然言語処理の分野。

## 主要タスク

1. **議論検出 (Argument Detection)** — 文が議論的発言かどうかの判定
2. **議論抽出 (Argument Extraction)** — 主張・根拠の境界と種類を特定
3. **関係分類 (Relationship Classification)** — 議論間の「支持(support)」「反対(attack)」を分類
4. **議論品質評価 (Argument Quality)** — 議論の説得力・論理的強度の評価

## LLM時代の主要手法

| 手法 | 説明 | 性能 |
|------|------|------|
| Few-shot prompting | ラベル付き例を少数与えてタスクを解かせる | GPT-4はfine-tunedモデルと同等以上 |
| Chain-of-Thought (CoT) | 推論ステップを段階的に出力させる | 複雑な関係分類で有効 |
| RAG | 外部知識を検索して付加 | ドメイン特化タスクで有効 |
| Fine-tuning / LoRA | タスク専用データで追加学習 | 最高性能だが計算コスト大 |

## LLMの弱点（既知の課題）

- 長文でニュアンスに富んだコメントの処理
- 感情的表現を含む言語の解釈
- **暗黙的な議論**（明示的でない主張・前提）の識別
- ブラックボックス性・バイアス・計算コスト

## 主要データセット

- **IAM** (Integrated Argument Mining dataset)
- **ARIES** — 統合的な議論評価データセット

## 我々の研究への接続

[[研究方針#仮説1]] の「論理構造の可視化」に直結。

- 主張・根拠・対立関係の抽出 = 議論マイニングの関係分類タスク
- プレ研究ではプロンプトエンジニアリングで検証（fine-tuningは将来課題）
- LLMの弱点（暗黙的議論）はStep3評価の観点として重要

## 関連記事

- [[papers/llm-argument-mining-survey]] — 包括的なサーベイ
- [[papers/llms-am-relationship-classification]] — 関係分類の実験的評価
- [[concepts/llm-prompting-strategies]] — 使用するプロンプト手法の詳細
- [[concepts/discussion-visualization]] — 抽出結果の可視化
