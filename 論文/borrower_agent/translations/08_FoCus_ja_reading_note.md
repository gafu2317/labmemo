# FoCus（Persona + Knowledge Grounding）日本語読解ノート

PDF: [08_FoCus_2022.arxiv.2112.08619.pdf](../pdfs/08_FoCus_2022.arxiv.2112.08619.pdf)  
原題: Customized Conversation Grounding Persona and Knowledge  
著者: Yoonna Jang et al. / AAAI? / arXiv 2022（論文本文より）

## 一言まとめ

「ユーザ persona」と「知識（Wikipedia）」を両方反映したカスタマイズ応答を作るデータセット FoCus。  
評価も persona grounding（persona を正しく使っているか）と knowledge grounding（知識を正しく使っているか）に分けて行う。  
今回の Borrower/landlord の “根拠分離”の考え方に直結する。

## Abstractの要点

- 問題: 既存の対話エージェントは
  - persona は扱うが知識との融合が弱い
  - 知識は扱うが persona との融合が弱い
  ため、「persona と knowledge が自然に融合した応答」を作るのが難しい。
- 提案: persona と Wikipedia 知識を使って customized answers を作る FoCus データセット。
- 評価:
  - 生成性能を自動指標＋人手で評価
  - persona grounding（PG）と knowledge grounding（KG）という2つの下位タスクで、
    モデルが適切なソース（persona/知識）を参照しているかを検証。

## Abstract 日本語訳（意訳）

人は会話するとき、話題に関する事前知識と、相手（話し手/話される側）の背景情報を利用して発話する。しかし既存の対話エージェントやデータセットは、こうした包括的な情報を考慮できていないため、知識と persona が適切に融合した発話を生成することに限界がある。そこで著者らは、ユーザの persona と Wikipedia の知識によって構築される custom answer を持つデータセット FoCus を提案する。事前学習済みモデル（BART, GPT-2, その他）について、情報量があり、かつ customized な応答を作れるかを評価するために、生成性能を自動スコアで測り、さらに定性的結果を人手評価でも確認する。モデルが persona と知識を適切に反映しているかは、提案する2つの下位タスクである persona grounding（PG）と knowledge grounding（KG）によって検討する。また、grounding quality assessment によって、データの発話が適切な知識と persona に基づいて構築されていることを示す。

## 何が近いか（今回の “根拠の分離”）

- 今回のランドロード案は「大家LLM + property_facts」で、**知識（fact）側の grounding**を厳密にする思想。
- FoCus は、persona 側と knowledge 側の grounding を別タスクとして測る。
- 今回の Borrower/landlord でも同様に、
  - Borrower 発話の grounding: 借り手記事/プロフィール（persona/constraints）への忠実性
  - Landlord 発話の grounding: property_facts への忠実性
  を切り分けて評価できる。

## 今回との違い / 注意点

- FoCus は persona と知識の統合を “データセットの性格” として扱う。
- 今回は「入力方式（構造化 vs 無構造）」の比較が主眼なので、
  FoCus の PG/KG を “評価観点” として参照する形になる。

## 使える示唆（構造化プロンプト vs Baseline）

- 構造化プロンプト条件では、Borrower に対して persona/constraints が YAML で明示されるため、
  - persona grounding（PG）に相当する指標が上がるはず
- Baseline は記事全文のままなので、
  - 必要な persona/constraints を取りこぼしたり、不要な推測を混ぜたりして PG が落ちる可能性
- Landlord 側でも property_facts だけを参照すれば KG に相当する評価が安定する。

## 発表で使える一言

FoCusは「persona grounding」と「knowledge grounding」を分けて評価できる。今回の構造化プロンプト vs Baseline比較でも、借り手側（persona/制約）と大家側（property facts）の grounding を分離して語れる。

