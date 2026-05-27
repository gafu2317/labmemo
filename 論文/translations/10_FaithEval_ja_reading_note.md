# FaithEval 日本語読解ノート

PDF: [10_FaithEval_2024.arxiv.2410.03727.pdf](../pdfs/10_FaithEval_2024.arxiv.2410.03727.pdf)  
原題: FaithEval: Can Your Language Model Stay Faithful to Context, Even If "The Moon is Made of Marshmallows"  
著者: Yifei Ming et al. / ICLR 2025

## 一言まとめ

LLM・RAG が **与えられた文脈（context）に忠実か** を測るベンチマーク。反事実・矛盾・答えられない文脈の3タスクで、**faithfulness hallucination**（文脈と不一致な生成）を評価する。借り手記事を根拠とする発話の評価に直結する。

## Abstractの要点

- **Faithfulness hallucination**: 提供 context と整合しない応答（factual hallucination とは別）。
- 3タスク: unanswerable / inconsistent / counterfactual contexts（検索が不完全・矛盾・誤情報を返す状況を模擬）。
- 4.9K 問題、4段階の context 構築と人手・LLM 検証。
- SOTA でも忠実性は低く、**モデルサイズが大きいほど忠実とは限らない**。

## Abstract 日本語訳（意訳）

LLM および RAG システムにおいて、与えられた文脈への忠実性は実運用上の信頼に不可欠である。しかし faithfulness hallucination、すなち応答が提供文脈とずれる問題は依然として深刻である。本論文は FaithEval を提案し、答えられない・矛盾する・反事実的な文脈の3タスクで LLM の忠実性を評価する。計4.9Kの高品質問題を4段階の検証パイプラインで構築した。多様なオープン・プロプライエタリモデルの実験では、最先端モデルでも文脈忠実性に苦戦し、大規模モデルが必ずしも改善するとは限らないことが示された。

## 何が近いか（今回の記事 grounding）

- 借り手記事＋構造化 profile が **context** に相当する。
- 大家の発話や検索結果が矛盾・不足する状況でも、記事外のことを言わない必要がある（FaithEval の inconsistent / unanswerable に類似）。
- Global Faithfulness (APC) が persona 制約向けなら、FaithEval は **一般の context faithfulness** のベンチマーク線引きになる。

## 今回との違い / 注意点

- タスクは QA/RAG 形式が中心で、多ターン交渉対話そのものではない。
- counterfactual は「文脈が世界知識と違うとき文脈に従うか」のテスト。借り手 AI では「記事が唯一の真実」という設定に近い。

## 使える示唆（実験設計に効かせる）

- Faithfulness 軸を「記事にない主張」「記事と矛盾」「記事から答えられない質問への適切な拒否」に分解できる。
- Baseline（長文記事）vs Structured（明示制約）で、文脈追従エラー率を比較する評価プロトコルの参考になる。

## 発表で使える一言

FaithEval は「与えられた文脈に張り付けるか」を体系評価する。借り手 AI の根拠忠実性は、記事を context とみなした faithfulness 問題として位置づけられる。
