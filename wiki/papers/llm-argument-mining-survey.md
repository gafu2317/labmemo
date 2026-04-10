# LLMs in Argument Mining: A Survey

> タグ: #survey #argument-mining #llm
> 著者: Hao Li, Viktor Schlegel, et al.
> 年: 2025
> ソース: arXiv
> raw: [[論文/論文データ/Large Language Models in Argument Mining A Survey]]

## 一行要約

LLM時代の議論マイニング技術を250論文・40データセットで体系的にまとめたサーベイ。

## 主要な知見

- **GPT-4のfew-shot ≈ fine-tunedモデルの性能**（従来手法との比較で同等以上）
- 議論品質評価で人間評価者との高相関（ρ = .46〜.93）
- Chain-of-Thought・RAG・LoRAなどの2021年以降の手法を体系化
- 統合データセット（IAM, ARIES）の活用が進む

## 手法の整理

| カテゴリ | 代表手法 |
|---------|---------|
| プロンプティング | Few-shot, CoT, RAG |
| 効率的学習 | LoRA, PEFT |
| データ拡張 | 合成データ生成 |

## 残る課題

- LLMのブラックボックス性・バイアス
- 多言語・クロスドメイン性能の不十分さ
- 計算コスト

## 次に読むべき論文

- Lawrence & Reed (2019) — 議論マイニングの基礎
- Chen et al. (2024) — LLM応用実験
- Ivanova et al. (2024) — 品質評価

## 我々の研究への示唆

プレ研究でのプロンプトエンジニアリングアプローチの理論的根拠。「few-shotで十分な性能が出る」というエビデンスになる。

## バックリンク

- [[concepts/argument-mining]]
- [[concepts/llm-prompting-strategies]]
