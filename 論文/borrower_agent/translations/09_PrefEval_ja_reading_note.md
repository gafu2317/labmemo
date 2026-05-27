# PREFEVAL 日本語読解ノート

PDF: [09_PrefEval_2025.arxiv.2502.09597.pdf](../pdfs/09_PrefEval_2025.arxiv.2502.09597.pdf)  
原題: DO LLMS RECOGNIZE YOUR PREFERENCES? EVALUATING PERSONALIZED PREFERENCE FOLLOWING IN LLMS  
著者: Siyan Zhao et al. / ICLR 2025

## 一言まとめ

LLM がユーザの好み（preference）を**長い文脈で推論し、記憶し、守れるか**を測るベンチマーク PREFEVAL。  
構造化プロンプトで好みを明示する今回の設計は、「preference adherence（従順性/遵守）」を改善するかどうかに直結する。

## Abstractの要点

- LLM をチャットボットに使う際、ユーザの preference へのパーソナライズが弱い。
- PREFEVAL:
  - 20 トピック
  - preference と query のペアが 3000
  - 明示的/暗黙的の preference が含まれる
- 多セッション対話で文脈長を最大 100k tokens まで変えて評価。
- 生成（generation）と分類（classification）の2タスクで評価。
- ベンチマーク結果:
  - 多くのモデルがゼロショットでは、わずか 10 turns（約3k tokens）で preference following が 10% 未満に落ちる。
  - prompting / retrieval を強くしても長文脈で悪化する。
- fine-tuning をすると改善する。

## Abstract 日本語訳（意訳）

大規模言語モデルはチャットボットとして普及しているが、ユーザの好み（preference）に合わせて応答をパーソナライズする能力は依然として限定的である。そこで著者らは、長い文脈の会話設定で、LLM がユーザ preference を推論・記憶・遵守できるかを評価するためのベンチマーク PREFEVAL を提案する。PREFEVAL は 20 トピックにまたがる 3000 の、ユーザ preference とクエリの組を手作業で作成している。preference 情報は明示的/暗黙的の両方の形を含み、生成タスクと分類タスクを通して LLM の性能を評価する。PREFEVAL を用いて、10個のオープンソース/クローズド LLM を対象に、文脈長が最大 100k tokens になるような複数セッション会話で preference following 能力をベンチマークした。プロンプト、反復的フィードバック、retrieval augmented generation など様々な手法を比較した結果、最先端 LLM でも会話中に積極的にユーザ preference を守ることは困難であることが分かった。特にゼロショットでは、多くのモデルで 10 turns 程度で精度が 10% 未満に下がる。高度な prompting や retrieval を使っても、長文脈では悪化が続く。さらに、PREFEVAL で fine-tuning することで大きく性能が改善することも示す。以上より PREFEVAL は preference following 能力を測定し、理解し、改善するための価値ある資源になると主張する。

## 何が近いか（今回の “希望の遵守”）

- 今回の Borrower structured prompt は、「希望（wish）」「制約（constraints）」を明示するため、  
  PREFEVAL が扱う preference following と非常に近い。
- 特に
  - conversation が進むほど、明示情報の保持・遵守が落ちる
  - implicit な preference は難しい
 という観点が、借り手AIのタスク成功と persona 一貫性に関係する。

## 今回との違い / 注意点

- PREFEVAL は “ユーザの好みに対する応答” を主に評価しているが、今回のタスクは不動産条件・交渉であり、preference が形式的に “slot/constraint” になっている。
- ただし、評価概念としては preference following を「slot 充足」に読み替えることで転用できる。

## 使える示唆（実験設計に効かせる）

- もし評価で「希望に反する提案/質問が何回起きたか」などをカウントするなら、
  PREFEVAL の設計（明示/暗黙、長文脈）に寄せたプロトコルを追加できる。
- 構造化プロンプト条件が Baseline より上手くなるなら、
  - turns が進むにつれて compliance（遵守）が保たれる
  - implicit preference を拾う率が高い
  のような差が出る可能性がある。

## 発表で使える一言

PREFEVAL は「長い対話で preference を推論・記憶・遵守できるか」を実測する。構造化プロンプトで希望/制約を明示する今回の比較は、この preference adherence を改善できるかの検証として語れる。

