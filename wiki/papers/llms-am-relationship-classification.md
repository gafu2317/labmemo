# LLMs for Argument Mining: Relationship Classification

> タグ: #argument-mining #classification #llm
> URL: https://arxiv.org/abs/2402.04330
> 年: 2024
> raw: [[論文/論文データ/LLMs_for_Argument_Mining_Relationship_Classification]]

## 一行要約

オンラインコメントの議論マイニング3タスク（検出・抽出・関係分類）でLLMの性能を評価し、fine-tunedモデルが最高性能を示した。

## 評価タスク

1. **議論検出** — 発言が議論的かどうか
2. **議論抽出** — 主張・根拠の境界と種類
3. **関係分類** — support / attack の判定 ← **我々の仮説1に直結**

## 主要結果

| モデルタイプ | 性能 | コスト |
|------------|------|--------|
| Fine-tuned大型LLM | **最高** | 高 |
| Prompt-onlyLLM | 中〜高 | 低 |
| RoBERTaなど従来モデル | 中 | 低〜中 |

## LLMの系統的弱点

- **長文・ニュアンスに富んだコメント**の処理
- **感情的表現**を含む言語の解釈
- **暗黙的な議論**（明示されていない主張・前提）の識別

## 我々の研究への示唆

- **仮説1の検証計画と同等タスク** → 設計の直接参考になる
- fine-tuningのコストが大きい → プロンプトエンジニアリング先行の正当性
- LLMの弱点3点 → Step3評価での分析観点として明示的に使う

## バックリンク

- [[concepts/argument-mining]]
- [[concepts/llm-prompting-strategies]]
- [[wiki/index]]
