---
paper_id: "14"
status: read
relevance: medium
themes: [忠実性, 知識接地対話, 評価]
use_in: [評価設計, 関連研究]
---

# Q2 日本語読解ノート

PDF: [14_Q2_2021.emnlp-main.619.pdf](../pdfs/14_Q2_2021.emnlp-main.619.pdf)  
原題: Q2: Evaluating Factual Consistency in Knowledge-Grounded Dialogues via Question Generation and Question Answering  
著者: Or Honovich et al. / EMNLP 2021

## 一言まとめ

応答中の情報が根拠文に基づいているかを、質問生成と質問応答で評価する手法。今回のFaithfulness評価にかなり近い。

## Abstractの要点

Knowledge-grounded dialogueでは、生成モデルが根拠知識と矛盾する内容を言うことがある。Q2は、応答から質問を生成し、根拠文からその質問に答えられるかを確認することで、応答のfactual consistencyを評価する。回答の比較にはNLIを使う。

## 何が近いか

- 応答が根拠文に基づいているかを見る点。
- gold responseなしで評価できる点。
- 応答中の情報単位を質問に変換して検証する点。

## 今回との接続

借り手AIの発話について、「この発話内容は借り手記事から確認できるか」を評価したい。Q2の考え方を使えば、発話から質問を作り、借り手記事を根拠として答えられるかを確認する評価が考えられる。

## 注意点

借り手AIでは、記事に書かれていない質問を大家にすること自体は問題ない。問題は、借り手自身に関する新情報を断定すること。したがって、Q2的な評価では「借り手自身についての主張」と「大家への質問」を分ける必要がある。

## 発表で使える一言

Q2は、対話応答の事実が根拠文から支持されるかをQAで評価する手法である。借り手AIでも、発話中の借り手情報が記事から支持されるかを評価する参考になる。
