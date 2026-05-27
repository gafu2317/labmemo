# Increasing Faithfulness 日本語読解ノート

PDF: [08_Increasing_Faithfulness_2021.acl-long.58.pdf](../pdfs/08_Increasing_Faithfulness_2021.acl-long.58.pdf)  
原題: Increasing Faithfulness in Knowledge-Grounded Dialogue with Controllable Features  
著者: Hannah Rashkin et al. / ACL 2021

## 一言まとめ

根拠文に忠実な対話を生成するため、応答のinformativenessやobjectivityを制御する研究。今回の「自然だけど言いすぎない」借り手AIに近い。

## Abstractの要点

Knowledge-grounded dialogueは、与えられた根拠文に基づいて情報を伝えるべきだが、既存データには根拠に忠実な応答と、主観的・雑談的な応答が混在している。本論文は、informativenessやobjectivityを測る評価指標を提案し、それらを制御特徴としてモデルに与えることで、根拠に忠実な応答を生成しやすくする。

## 何が近いか

- 根拠に忠実な対話生成。
- 主観的・雑談的応答と、根拠に基づく情報提供を分ける点。
- 生成時にfaithfulnessを促す制御を入れる点。

## 今回との接続

借り手AIでは、人間らしく自然に話す必要はあるが、記事にない個人的体験や希望を作ってはいけない。つまり、自然さと根拠忠実性のバランスが重要。

## 注意点

この論文は外部文書に基づく知識提供が中心。借り手AIでは、根拠文は借り手記事であり、さらに対話の目的は情報提供だけでなく大家から情報を得ること。

## 発表で使える一言

Increasing Faithfulnessは、自然な対話の中でも根拠文に忠実な情報だけを話すよう制御する考え方を示している。借り手AIでも、記事に基づく主張と自然な会話のバランスが課題になる。

