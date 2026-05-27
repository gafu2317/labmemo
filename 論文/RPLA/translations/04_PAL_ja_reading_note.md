# Persona-Aware Alignment Framework 日本語読解ノート

PDF: [04_Persona_Aware_Alignment_PAL_2025.tacl-1.77.pdf](../pdfs/04_Persona_Aware_Alignment_PAL_2025.tacl-1.77.pdf)  
原題: Persona-Aware Alignment Framework for Personalized Dialogue Generation  
著者: Guanrong Li et al. / TACL 2025

## 一言まとめ

personaを単に入力に入れるだけではなく、persona alignment自体を学習目標にする研究。今回の「記事をそのままpromptに入れるだけでは弱い」という問題意識に近い。

## Abstractの要点

Personalized dialogue generationはpersona profileと対話履歴を使って、personaに関連し一貫した応答を生成する。しかし既存モデルは、Next Token Predictionのようなtoken-level学習に依存しがちで、与えられたpersonaを無視して一般的な応答を生成しやすい。本論文は、persona alignmentを直接学習目標にするPALを提案する。

## 何が近いか

- personaを入力に入れるだけでは不十分という問題意識。
- 応答がpersonaに意味的に合っているかを重視する点。
- `Select then Generate` のように、関連personaを選んでから生成する点。

## 今回との接続

借り手記事には多くの情報が混ざる可能性がある。全情報を常に使うのではなく、今の対話状況に関連する目的・希望・制約を選んで発話する必要がある。これはPALの「関連persona選択」に近い。

## 今回との違い

PALは主にopen-domain personalized dialogue。今回の研究では、大家との目的志向対話で、情報獲得というタスク成功も重要になる。

## 発表で使える一言

PALは、personaをpromptに入れるだけではモデルが無視する可能性があるため、persona alignmentを明示的に扱う必要があることを示している。借り手AIでも、記事情報を構造化し、関連する情報を選んで使う設計が必要になりそう。

