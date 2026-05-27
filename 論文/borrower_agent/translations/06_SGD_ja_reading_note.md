# SGD（Schema-Guided Dialogue）日本語読解ノート

PDF: [06_SGD_2019.arxiv.1909.05855.pdf](../pdfs/06_SGD_2019.arxiv.1909.05855.pdf)  
原題: Towards Scalable Multi-Domain Conversational Agents: The Schema-Guided Dialogue Dataset  
著者: Abhinav Rastogi et al. / 2019

## 一言まとめ

巨大な仮想アシスタントを想定し、「サービスの schema（intent/slot のセット）」を入力として、動的に予測できる対話パラダイムを提示。そのベンチマークとして SGD データセットを構築（16ドメイン・1万6千超の会話）。  
構造化入力（slots を YAML で持つ今回の方式）を正当化しやすい “土台” の論文。

## Abstractの要点

- 仮想アシスタントは多ドメイン・多APIを扱う必要があるが、API は増え続け、訓練データが少ないものもある。
- 既存の公開 TOD データセットは
  - ドメイン数が少ない
  - ドメインごとに固定 ontology を前提にしている
  ため、現実の課題を十分に表現できない。
- 提案:
  - SGD データセット（16ドメイン、1.6万超、多サービスを含む）
  - schema-guided paradigm（schema を入力にして動的な intent/slot を予測）
  - このパラダイムに基づく dialogue state tracking モデル
- 提供する状態追跡モデルは、新しい API への zero-shot generalization も狙える。

## Abstract 日本語訳（意訳）

Google Assistant や Alexa のような仮想アシスタントは、複数領域にまたがる多数のサービス/API を自然言語の会話インターフェースとして提供する。こうしたシステムは、重なり合う機能を持つサービスが増え続ける環境において、それらを扱う必要がある。さらに、一部のサービスは学習データがほとんど存在しないこともある。しかし、タスク指向対話の既存データセットはドメイン数が限られ、かつ各ドメインに単一の固定オントロジーを仮定しているため、こうした課題を十分に捉えられていない。本研究では、16ドメインにまたがる1万6千超のマルチドメイン会話を含む SGD データセットを導入する。これは、既存の TOD コーパスより規模で上回り、大規模仮想アシスタントを作る際の課題を強く反映している。SGD は言語理解、slot filling、dialogue state tracking、応答生成など複数タスクに対する難度の高い試験台になる。同時に、schema-guided なタスク指向対話のパラダイムも提案し、入力として渡された schema の natural language description に基づき、動的に現れる intents/slots へ予測を行うことで、多数のサービスを追加学習なしで扱えるようにする。さらにこのパラダイム上に、動的な state tracking のためのモデルも提示し、新規 API への zero-shot 一般化と、通常設定での競争力を両立することを示す。

## 何が近いか（今回の `slots` / 構造化入力との対応）

- 今回の YAML の `slots` は、「この案件（物件）で重要になる属性集合」を schema 化している。
- SGD が言う「schema-guided により新 API/サービスを追加学習なしで扱える」という話は、
  - 既知条件の組み合わせだけでなく
  - 新しい property / case でも同じ会話運用ができる
  という今回の設計方針（実験の拡張性）と整合しやすい。

## 今回との違い / 注意点

- SGD は主に DST/slot filling を狙う dataset・枠組み。
- 今回は対話生成（借り手/大家）と評価（faithfulness, task success 等）が中心。
- ただし、構造化プロンプトの入力設計（slots を自然言語でどう渡すか）の根拠として使える。

## 使える示唆

- YAML schema 的な情報（slots/質問/制約）を、LLM の入力として “動的” に組み立てる発想は SGD の schema-guided paradigm と同型。
- 比較実験では、
  - Baseline: schema 情報なし（全文/生入力）
  - 構造化: schema 情報（slots）を明示
  を置き、SGD が示したような「一般化・拡張性が上がるなら成功率が上がるはず」という流れで議論できる。

## 発表で使える一言

SGDは「サービスの schema を入力として扱う」ことで、大規模な仮想アシスタントを扱えると示した。今回の構造化プロンプト（YAML slots）はこの schema-guided 発想を借りたものとして位置づけられる。

