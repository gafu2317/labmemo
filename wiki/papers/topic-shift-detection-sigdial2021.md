# Topic Shift Detection for Mixed Initiative Response

> タグ: #topic-shift #dialogue #xlnet #mixed-initiative #annotation
> 著者: Konigari, Chand, Alluri & Shrivastava (IIIT Hyderabad)
> 年: 2021
> ソース: SIGDIAL 2021 (ACL Anthology)
> raw: [[raw/papers/topic-shift-detection-for-mixed-initiative-response.pdf]]

## 一行要約

オープンドメイン対話でのトピック逸脱をXLNet-baseで検出（Precision 84%）し、システムイニシアチブ（話題修正促し）を自動生成する手法を提案。

## 問題設定

- バーチャルアシスタントとの対話で、ユーザーが主要話題から逸脱することが頻繁に発生
- 既存手法は事前定義のトピックセットを前提とするが、オープンドメインではそれが不可能
- 事前定義なしでの主要話題逸脱検出が課題

## アノテーションフレームワーク

Switchboardコーパス（電話音声書き起こし）74会話に3ラベルでアノテーション：

| ラベル | 説明 |
|--------|------|
| Major Topic (MT) | 会話の主要トピックに属する発話 |
| Minor Topic (MiT) | 主要トピックの延長上にある副話題 |
| Off-topic (OT) | 主要トピックからの完全な逸脱 |

- Cohen's kappa = 0.64（信頼性あり）
- MiTとOTの区別が困難 → 二値分類（Major vs Rest）に統合

## モデル

- SVM / LightGBM をベースライン
- BERT / RoBERTa / **XLNet-base** を比較

| モデル | Precision | Recall | F1 |
|--------|----------|--------|----|
| LightGBM | 0.65 | 0.69 | 0.66 |
| BERT-base | 0.69 | 0.69 | 0.69 |
| RoBERTa-base | 0.77 | 0.63 | 0.69 |
| **XLNet-base** | **0.84** | **0.72** | **0.77** |

- XLNetが512トークン制限なしで長文文脈をカバーできる点が有効

## システムイニシアチブ（ケーススタディ）

- 最初K=15発話から単語重要度スコア（BiLSTM）で主要トピックをBoWとして抽出
- XLNetで逸脱を検出したタイミングでシステムが話題修正を促す応答を生成
- 例: "Do you want to go back to topic of fishing?"

## 我々の研究への示唆

議論支援システムでの**議論の脱線検知**に直接応用可能。主要議論テーマからの逸脱をXLNetで検出し、システムが議論を元のテーマに戻す「ファシリテーター機能」として実装できる。事前トピックセット不要な点が実用的。Switchboardコーパスのアノテーション手法（Major/Minor/OT）は議論支援での逸脱分類設計の参考になる。

## バックリンク

- [[concepts/topic-shift-detection]]
- [[concepts/llm-prompting-strategies]]
