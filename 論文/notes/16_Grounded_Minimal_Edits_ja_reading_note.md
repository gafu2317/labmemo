---
paper_id: "16"
status: read
relevance: high
themes: [ペルソナ, 接地対話, 一貫性]
use_in: [手法設計, 関連研究]
---

# Grounded Minimal Edits 日本語読解ノート

PDF: [16_Grounded_Minimal_Edits_2021.emnlp-main.183.pdf](../pdfs/16_Grounded_Minimal_Edits_2021.emnlp-main.183.pdf)  
原題: Transferable Persona-Grounded Dialogues via Grounded Minimal Edits  
著者: Chen Henry Wu et al. / EMNLP 2021

## 一言まとめ

既存の自然な応答を最小限編集して、personaにgroundedな応答へ変える研究。今回の借り手AIでは、**自然さを保ちながら記事に忠実にする** 方向の参考になる。

## Abstractの要点

Grounded dialogue modelは、personaなどの概念に基づいて応答を生成する。しかし、grounded dialogue dataの分布に依存するため、転移性に課題がある。本論文は、既存応答を最小限編集して与えられたconceptにgroundするGrounded Minimal Editorを提案する。persona関連部分とpersona非依存部分を分離・再結合し、persona consistencyを改善しながら知識利用や共感を保つ。

## 何が近いか

- personaに基づく応答修正。
- 応答全体を作り直すのではなく、必要な部分だけ変える点。
- 自然さ、知識利用、共感を保ちながらpersona consistencyを上げる点。

## 今回との接続

借り手AIでも、LLMが作った自然な発話に対して「記事に根拠があるか」「言いすぎていないか」をチェックし、必要なら最小限修正する構成が考えられる。

## 今回との違い

この論文はpersona一貫性を主に扱う。今回の研究では、大家から必要情報を得るための質問生成や対話状態管理も必要。

## 発表で使える一言

Grounded Minimal Editsは、自然な応答を保ちながらpersonaに合うように修正する方向を示している。借り手AIでも、生成後に記事根拠に合わせて発話を修正する仕組みが考えられる。
