# PrefEval 日本語読解ノート

PDF: [04_PrefEval_2502.09597.pdf](../pdfs/04_PrefEval_2502.09597.pdf)  
原題: Do LLMs Recognize Your Preferences? Evaluating Personalized Preference Following in LLMs  
著者: Siyan Zhao et al. / ICLR 2025

## 一言まとめ

LLMが長い会話の中でユーザの好みを推論・記憶・遵守できるかを評価するベンチマーク。今回の借り手AIでは、**借り手記事の希望や制約を忘れず守れるか** の参考になる。

## Abstractの要点

LLMはチャットボットとして使われているが、ユーザの好みを反映した応答はまだ十分ではない。PrefEvalは、明示的・暗黙的なユーザ好みを含む3,000のペアからなり、LLMが好みを推論し、記憶し、長い文脈で守れるかを評価する。実験では、最新LLMでも長い会話で好みを維持するのが難しいことが示された。

## 何が近いか

- ユーザの希望・制約を会話中に守る評価。
- explicit preference と implicit preference の区別。
- long-context / multi-sessionで性能が落ちる問題。
- RAGやpromptingを比較している点。

## 今回との接続

借り手記事には、希望・価値観・避けたい条件が書かれる可能性がある。借り手AIは、それらを会話中に守る必要がある。たとえば「静かな制作場所がほしい」と書かれている人が、騒音のある物件でも問題ないように話してしまうと不適切。

## 今回との違い

PrefEvalはユーザ本人に向けて個人化応答する設定。今回のAIは借り手の好みを使って、第三者である大家と話す。つまり、preference followingを **代理対話** に使う点が違う。

## 発表で使える一言

PrefEvalは、LLMがユーザの好みを長い会話の中で守ることが難しいと示している。借り手AIでも、記事から抽出した希望や制約を会話中に維持できるかを評価する必要がある。

