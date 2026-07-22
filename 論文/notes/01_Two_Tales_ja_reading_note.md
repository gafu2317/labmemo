---
paper_id: "01"
status: read
relevance: medium
themes: [ペルソナ, ロールプレイ, 個人化]
use_in: [関連研究, 用語整理]
---

# Two Tales of Persona in LLMs 日本語読解ノート

対象PDF: [01_Two_Tales_of_Persona_in_LLMs_2406.01171.pdf](../pdfs/01_Two_Tales_of_Persona_in_LLMs_2406.01171.pdf)

原題: Two Tales of Persona in LLMs: A Survey of Role-Playing and Personalization  
著者: Yu-Min Tseng et al.  
arXiv: 2406.01171  

このノートは全文直訳ではなく、論文を読むための日本語読解版です。重要語は英語を残し、章ごとに「何を言っているか」が追える形にしています。

## 0. この論文の一言まとめ

LLMにおける persona 研究を、LLM自身に persona を割り当てる **LLM Role-Playing** と、ユーザの persona に合わせて応答する **LLM Personalization** の2系統に整理したサーベイ。

この論文の価値は、新しい手法の提案ではなく、混乱しがちな persona 研究を「誰の persona なのか」という軸で切り分けたところにある。

## 1. Abstract 日本語訳

対話研究で使われてきた persona という概念は、近年、大規模言語モデルを特定の文脈に適応させるための有望な枠組みとして再び注目されている。例として、personalized search や LLM-as-a-judge がある。しかし、LLMで persona を活用する研究は増えているものの、全体として整理されておらず、体系的な分類が不足している。

このギャップを埋めるため、本論文では現在の研究状況を包括的に調査し、分類する。著者らは、研究を2つの流れに分ける。1つ目は **LLM Role-Playing** であり、ここでは persona がLLMに割り当てられる。2つ目は **LLM Personalization** であり、ここではLLMがユーザの persona を考慮する。

さらに、LLMの personality evaluation の既存手法も紹介する。著者らによれば、本論文は persona という統一的視点のもとで、LLMの role-playing と personalization を扱う最初のサーベイである。また、今後の研究を促進するため、関連論文リストを継続的に整備している。

## 2. Introduction

### 日本語での読み下し

LLMは、単なるNLPタスク解決器や汎用チャットボットとしてだけでなく、特定の文脈に合わせて振る舞うモデルとしても使われるようになっている。その文脈適応のためのレンズとして、persona が再注目されている。

ただし、persona 研究はかなり広い。ある研究では「LLMに医師や裁判官を演じさせる」ことを persona と呼び、別の研究では「ユーザの好みや履歴に合わせて推薦する」ことを persona と呼ぶ。そのため、分野全体の見取り図が必要になる。

この論文は、persona がどちら側にあるかで整理する。

| 区分 | persona の所在 | 目的 |
|---|---|---|
| LLM Role-Playing | LLM側 | LLMが割り当てられた役割を演じ、環境に適応する |
| LLM Personalization | ユーザ側 | LLMがユーザの背景・履歴・好みに適応する |

### 重要ポイント

- **Role-Playing** では、LLMは「エンジニア」「医師」「裁判官」「ゲームキャラクター」などとして振る舞う。
- **Personalization** では、LLMはユーザの年齢、好み、過去の行動、健康情報、学習状況などを考慮して応答する。
- 同じシステムで両方が同時に起こることもあるが、研究上の焦点は違う。

## 3. LLM Role-Playing

### 章の主張

LLM Role-Playing は、persona を言語エージェントに結びつけることで、LLMが特定の環境に適応して行動する研究である。多くの場合、persona は prompt の中に直接書かれる。これは訓練不要で単純だが、かなり効果がある。

### 代表的な環境

| 環境 | 例 | 役割 |
|---|---|---|
| Software Development | ChatDev, MetaGPT | CEO, CTO, PM, Engineer, Reviewer, Tester |
| Game | Minecraft, social simulation, bargaining game | assistant, buyer, seller, simulated human |
| Medical Application | diagnostic reasoning, MedAgent | doctor, patient, medical expert |
| LLM-as-Evaluator | ChatEval, LLM-as-a-judge | judge, critic, general public, psychologist |

### 日本語での要点

ソフトウェア開発では、複数のLLMエージェントに会社内の役職を割り当て、設計、実装、テスト、文書化を分担させる。ゲーム環境では、LLMが環境情報や道具、近くの状況を記憶しながら行動する必要があるため、retrieval-based memory が重要になる。医療では、医師や専門医の役割をLLMに与えることで診断推論を改善しようとする。LLM-as-Evaluator では、LLMを「公平な審査員」や「批評家」として振る舞わせることで、人間評価に近づけようとする。

### single-agent と multi-agent

| schema | 意味 | 例 |
|---|---|---|
| Single-Agent | 1つのエージェントが単独で目的を達成できる | Minecraft探索エージェント |
| Multi-Agent | 他エージェントとの協力・議論・批判が必要 | ソフトウェア開発、医療相談、評価者会議 |

multi-agent ではさらに、協調的な情報共有と、debate / criticism のような対立的協調がある。

### Emergent Behaviors

複数エージェントで role-playing させると、人間社会のような振る舞いが出る。

| 振る舞い | 内容 |
|---|---|
| Voluntary Behavior | 他エージェントを自発的に助ける |
| Conformity Behavior | 批判や助言を受けて、チーム目標に合わせて行動を修正する |
| Destructive Behavior | 毒性、偏見、危険行動、jailbreak 的行動が出る |

ここはRPLAを読む上で重要。role-playing は能力を上げるだけでなく、安全性リスクも増やす。

## 4. LLM Personalization

### 章の主張

LLM Personalization は、LLMがユーザの persona を考慮して、個別化された応答を返す研究である。ここでの persona は、ユーザの個人情報、行動履歴、嗜好、健康状態、学習状況などを含む。

### 代表タスク

| タスク | 何を個人化するか |
|---|---|
| Recommendation | 映画、本、商品などの推薦 |
| Search | ユーザの意図や過去の行動に合わせた検索 |
| Education | 学習者の理解度・感情・学習スタイルに合わせた支援 |
| Healthcare | 個人の健康データや症状に基づく医療・健康支援 |
| Dialogue | ユーザ persona に合わせた対話生成 |

### 日本語での要点

従来のRLHFは多くの人間のフィードバックを平均化するため、個人の好みまでは十分に反映できない。personalized LLM は、ユーザの履歴や属性を使うことで、より個別のニーズに応えようとする。

推薦では、ユーザの嗜好や過去の行動から次に好みそうなアイテムを推測する。検索では、単なるキーワード一致ではなく、過去のやりとりや嗜好から検索意図を推測する。教育では、学習者の理解度や感情状態に合わせた説明やフィードバックが可能になる。医療では、個人の健康情報や症状説明を使って、より個別化された助言を生成する。

### Dialogue の2分類

| 分類 | 内容 |
|---|---|
| Task-oriented dialogue modeling | ホテル予約やレストラン予約など、特定タスク達成を支援する |
| User persona modeling | 対話履歴からユーザ persona を推定し、ユーザに合わせた応答を生成する |

RPLAとの接点としては、user persona modeling が特に重要。これは「演じるキャラクター」ではなく「相手ユーザの人物像」をモデル化する。

## 5. LLM Personality Evaluation

### 章の主張

Role-playing でも personalization でも、適応後のLLMが意図した persona に合っているかを評価する必要がある。この章では、LLMの personality をどう測るかを扱う。

### 主な評価方法

| 評価方法 | 内容 |
|---|---|
| Big Five | 開放性、誠実性、外向性、協調性、神経症傾向 |
| MBTI | 人格タイプ分類 |
| Machine Personality Inventory | LLM向けに personality traits を測る試み |
| Personality test interviewing | LLMにインタビューし、性格次元のスコアをつける |

### 日本語での要点

一部の研究では、LLMは与えられた persona に沿った Big Five 的性格を示す。しかし、MBTIのような人間向け心理テストをそのままLLMに使ってよいかは未解決である。

つまり、「LLMが本当に性格を持つ」のではなく、「あるテスト形式に対して、人間の性格のように見える応答パターンを出す」と見るべき。

## 6. Challenges and Future Directions

### 6.1 General Framework

現状の role-playing framework はタスク依存で、人間が設計した persona に大きく依存している。今後は、LLMがタスクに応じて自動的に persona を決めたり、動的に調整したりする general framework が必要。

### 6.2 Long-Context Personas

personalization では、ユーザ履歴をpromptに入れると長くなりすぎる。retrieval や memory が有効だが、無関係・ノイズの多い情報が混ざると性能が落ちる。

読むポイント:

- persona は短いプロフィールでは済まない
- 長期記憶をどう保存・検索・統合するかが課題
- RPLAでも「キャラクターの過去経験」や「長期対話履歴」に同じ問題が出る

### 6.3 Lack of Datasets and Benchmarks

role-playing では、環境情報や特定形式のデータが不足している。personalization では、個人データがprivacyのため集めにくい。さらに、両分野とも包括的な評価ベンチマークが不足している。

### 6.4 Bias

persona を与えると、LLMの stereotype や harmful output が強まることがある。特に socio-demographic persona は危険。personalized recommendation でも、人気アイテムやprompt内の位置に由来するbiasが出る。

### 6.5 Safety and Privacy

Role-playing は jailbreak を助けることがある。persona を与えることで毒性が増す場合もある。Personalization はユーザの個人情報や履歴を扱うため、membership inference attack などによる情報漏洩が問題になる。

この章は、RPLA研究をやるならかなり重要。キャラクターをうまく演じる性能だけでなく、安全性・偏見・個人情報の観点を必ず入れる必要がある。

## 7. Broader Implications

教育の個人化は、低コストで個別支援を受けられる可能性を開く。ただし、裕福な人は人間の家庭教師を使い、リソースの少ない人だけがLLM支援に頼る、という格差も起こりうる。

医療や心理支援への応用も期待されるが、法的責任、診断の信頼性、個人情報保護の問題が大きい。

また、LLM personality evaluation はまだ統一的理解がない。LLMの性格や心理特性をどう測るかは、今後LLMが社会で高度な役割を担うほど重要になる。

## 8. Conclusion

persona を使うことで、LLMはさまざまなシナリオに適応し、tailored responses を生成できる。本論文は、LLM時代の persona 研究を **role-playing** と **personalization** の2系統に整理し、personality evaluation、課題、今後の方向性を概観した。

## 9. 用語メモ

| 英語 | 日本語メモ |
|---|---|
| persona | ペルソナ。LLM側の役割にも、ユーザ側の人物像にも使われる |
| LLM Role-Playing | LLMに役割を割り当てて演じさせる研究 |
| LLM Personalization | ユーザの情報や嗜好に合わせてLLMを個人化する研究 |
| assigned persona | LLMに与えられた役割・人格 |
| user persona | ユーザの背景、嗜好、履歴、行動特性 |
| role-playing schema | single-agent / multi-agent のような構成 |
| emergent behavior | 複数エージェント相互作用から現れる振る舞い |
| destructive behavior | 有害・偏見・暴走的な振る舞い |
| long-context persona | 長い履歴や複雑な人物情報を含む persona |
| personality evaluation | LLMの性格・心理特性を測る評価 |

## 10. この論文を読む時の問い

1. persona はLLM側にあるのか、ユーザ側にあるのか。
2. role-playing と personalization はどこで重なるのか。
3. RPLA研究で扱う persona は、character persona なのか individualized persona なのか。
4. 評価したいのは、役らしさ、タスク性能、ユーザ満足、安全性のどれか。
5. 自分の研究で扱う persona は、短いプロフィールで足りるのか、長期記憶や経験が必要なのか。

## 11. 教授に説明するなら

この論文は、RPLAをいきなり個別手法から読む前に、persona 研究全体を整理するための入口です。特に重要なのは、persona が「LLMが演じる役」なのか「LLMが適応する相手ユーザ」なのかを分けている点です。この区別を持っておくと、Character-LLM や RoleLLM のようなキャラクター再現研究と、個人化推薦・教育・医療支援のような personalization 研究を混同せずに読めます。
