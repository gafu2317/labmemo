# Argument Mining on Twitter: A Survey

> タグ: #argument-mining #survey #social-media #twitter #stance-detection
> 著者: Schaefer & Stede
> 年: 2021
> ソース: it–Information Technology 63(1):45–58
> raw: [[raw/papers/argument-mining-on-twitter-a-survey.pdf]]

## 一行要約

Twitter上の議論マイニングに関するサーベイで、コーパス構築・議論要素/関係検出・スタンス検出の3タスクを体系的に整理。

## タスク分類

| タスク | 内容 | 代表的手法 |
|--------|------|----------|
| コーパス構築 | ツイートへの議論アノテーション | DART, DCV2017, AB2016, SS2020 |
| 議論要素/関係検出 | クレーム・前提の抽出、支持/攻撃関係の分類 | SVM, LR, XGBoost |
| スタンス検出 | 話者の立場（支持/反対/中立）を判定 | BiLSTM, BERT |

## 主要データセット

- **DART** (BCV2016a): Twitterの議論構造アノテーション
- **DCV2017**: 討論スレッドの賛否ラベル
- **AB2016**: 議論バウンダリー検出
- **SS2020**: スタンス検出ベンチマーク

## 主な知見

- 議論要素検出: SVM/LR/XGBoostが最良
- **関係検出は依然困難**（F1: 0.00–0.20）— Twitter特有のノイズ・略語が要因
- スタンス検出はBERTベースで改善が著しい
- Twitterの非形式的言語・140字制限が議論構造を複雑にする

## 課題

- 短文・略語・ハッシュタグによる意味の曖昧さ
- 文脈（スレッド構造）の活用が不十分
- 多言語対応の欠如

## 我々の研究への示唆

議論支援システムにおいてSNS上の非形式的議論を扱う際の基礎知識として有用。特に**関係検出の低性能**は、LLMを用いた議論支援においても克服すべき主要課題であり、few-shot/in-contextアプローチの可能性を示唆する。

## バックリンク

- [[concepts/argument-mining]]
