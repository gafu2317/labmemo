# PicPersona-TOD 日本語読解ノート

PDF: [01_PicPersona_TOD_2025.naacl-long.403.pdf](../pdfs/01_PicPersona_TOD_2025.naacl-long.403.pdf)  
原題: PicPersona-TOD: A Dataset for Personalizing Utterance Style in Task-Oriented Dialogue with Image Persona  
著者: Jihyun Lee et al. / NAACL 2025

## 一言まとめ

Task-Oriented Dialogueにpersonaを入れ、ユーザに合わせた応答スタイルを作る研究。今回の借り手AIに近いのは、**タスク達成とpersona適応を両立しようとしている点**。

## Abstractの要点

Task-Oriented Dialogueはユーザの要求を自然言語で達成するための対話システムだが、既存システムは一般的で単調な応答になりやすく、ユーザの個人的属性に適応できない。そこで本論文は、ユーザ画像をpersonaの一部として使うPicPersona-TODを提案する。年齢や感情的文脈などに合わせた応答を可能にし、外部知識を使ってhallucinationを減らす。

## 何が近いか

- TODにpersonaを入れる点。
- personalizationがユーザ体験を改善する点。
- 外部知識を使ってhallucinationを減らす点。
- タスク精度を落とさずに個別化応答を作る点。

## 今回との違い

PicPersona-TODでは、AIはユーザに合わせて応答する。今回の借り手AIでは、AIは大家に応答するが、personaは借り手側にある。つまり、今回の方が **借り手personaを持つ代理エージェント** という構造になる。

## 使える示唆

借り手AIでも、自然さだけでなく、タスクの正確性を落とさないことが重要。記事に基づく発話と、大家から情報を得るタスクの両立を評価する必要がある。

## 発表で使える一言

PicPersona-TODは、目的志向対話にpersonaを入れると応答の個別性が上がることを示している。ただし、今回の研究ではpersonaを「対話相手」ではなく「代理する借り手」に持たせる点が異なる。

