# Show, Don’t Tell 日本語読解ノート

PDF: [05_Show_Dont_Tell_2022.naacl-main.336.pdf](../pdfs/05_Show_Dont_Tell_2022.naacl-main.336.pdf)  
原題: Show, Don’t Tell: Demonstrations Outperform Descriptions for Schema-Guided Task-Oriented Dialogue  
著者: Raghav Gupta et al. / NAACL 2022

## 一言まとめ

スキーマ（intent/slot 等）の意味を、自然言語の説明（description）で渡すより、**状態アノテーション付きの短い対話例（demonstration）**で見せた方が、0-shot 一般化が強くなる、という主張。  
構造化入力（slot 情報）をどう LLM に理解させるか、の示唆になる。

## Abstractの要点

- 多ドメイン/多API を扱う universal な対話システムは重要。
- schema-guided modeling が効いているが、description ベースは
  - 記述作業が手間
  - セマンティクスを間接にしか伝えない
  - description の揺れに頑健でない
 という欠点がある。
- 提案: Show, Don’t Tell（SDT）で、**ラベル付きの1つの対話例**を入力にする。
- SDT は、Schema-Guided Dialogue（SGD）と MultiWOZ leave-one-out の2ベンチマークで SOTA。
- description よりもデータ効率が良く、schema variation に頑健。

## Abstract 日本語訳（意訳）

複数ドメインにまたがり、新しいサービスへ最小のオーバーヘッドで一般化できる汎用対話システムを作ることは重要な課題である。既存研究は、スキーマ要素の自然言語記述を使って汎用化を実現してきた。しかし記述はスキーマのセマンティクスを間接的にしか伝えない。そこで著者らは Show, Don’t Tell を提案する。これは seq2seq モデルに対し、スキーマ要素の意味を「説明して伝える」のではなく、「状態がラベル付けされた対話例」で示す（demonstration）という形でプロンプトする手法である。説明を作るのと同程度の手間が必要ではあるが、巨大言語モデルに対し短い例をスキーマ表現として与えると、0-shot 一般化を測る2つの対話状態追跡ベンチマークで SOTA 性能が出ることを示す。

## 何が近いか（今回の比較へのつなぎ）

- 今回の「構造化プロンプト」は `slots` / `questions` / `constraints` を整形して渡す方式。
- Show, Don’t Tell は「スロットの意味は、説明文より例で学ばせた方が強い」というメッセージなので、
  - 構造化プロンプトに、例（ミニ対話や期待する出力形式のデモ）を付与すると改善する可能性
  - Baseline との差がさらに明確になる可能性
  を示唆する。

## 今回との違い / 注意点

- SDT は主に DST（dialogue state tracking）の入力理解を強化する文脈。
- 今回は Borrower/landlord の生成（交渉・質問応答）なので、例の作り方（どの部分を示すか）を工夫する必要がある。

## 使える示唆（実装アイデア）

- 構造化プロンプト条件にだけ、短い「状態例」を1つ入れる（ただし公平性を保つため、Baseline側も同じ長さの雑な説明を入れる等が必要）。
- 例の内容は、今回の `slots` の意味に直結するようにする：
  - `location=駅徒歩` のとき、どんな質問や条件提示をするか
  - `budget` のとき、どんな譲歩をしてよいか
  - `constraints` のとき、NG理由の出し方

## 発表で使える一言

スロットの意味は説明よりデモ（例）で理解させた方が強い。構造化プロンプトが効く理由を「例を入れた理解の安定化」として補強できる。

