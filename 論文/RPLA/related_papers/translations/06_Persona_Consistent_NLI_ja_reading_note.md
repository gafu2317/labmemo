# NLIによるPersona Consistency 日本語読解ノート

PDF: [06_Persona_Consistent_NLI_1911.05889.pdf](../pdfs/06_Persona_Consistent_NLI_1911.05889.pdf)  
原題: Generating Persona Consistent Dialogues by Exploiting Natural Language Inference  
著者: Haoyu Song et al. / AAAI 2020

## 一言まとめ

発話とpersona文の関係をNLIで判定し、矛盾しない発話生成に使う研究。今回の **記事にないこと・矛盾することを言わない評価** に直接近い。

## Abstractの要点

対話エージェントでは自然な応答だけでなく、一貫したpersonaを保つことが重要。本論文は、Natural Language Inferenceを利用して、応答とpersonaの整合性を扱う。応答とpersona文のペアをentailment / neutral / contradictionとして判定し、その信号を強化学習の報酬として使う。

## 何が近いか

- 発話とpersonaの矛盾検出。
- 自然さと一貫性を分けて扱う点。
- NLIを評価器・学習信号として使う点。

## 今回との接続

借り手AIでは、発話と借り手記事の間に矛盾がないかを見たい。記事から抽出した「制約」や「希望」と発話をNLI的に比較し、contradictionを検出する仕組みが考えられる。

## 注意点

NLIで「矛盾」は見つけやすいが、「記事に書かれていない新情報を勝手に足した」ケースはneutralになりやすい。そのため、今回のFaithfulness評価ではNLIだけでは不十分かもしれない。

## 発表で使える一言

NLIを使うと、発話がpersonaと矛盾していないかを自動評価できる。借り手AIでも、記事から抽出した希望や制約と発話の矛盾チェックに使える可能性がある。

