# RPLA 論文 5点メモ

作成日: 2026-05-12

読むときの共通観点:

| 観点 | 見ること |
|---|---|
| persona | 何を persona / character / individual として扱うか |
| 作り方 | prompt, retrieval, memory, tuning, reward, multi-agent など |
| 評価 | 何を良い role-play とみなすか |
| データ源 | profile, fiction, dialogue, synthetic data, human annotation など |
| 弱点 | 残る問題、評価の不安、倫理・実装上の制約 |

## 01. Two Tales of Persona in LLMs

PDF: [01_Two_Tales_of_Persona_in_LLMs_2406.01171.pdf](pdfs/01_Two_Tales_of_Persona_in_LLMs_2406.01171.pdf)

| 観点 | メモ |
|---|---|
| persona | persona を「LLMに割り当てるもの」と「ユーザ側の個人情報・嗜好」とに分ける。前者が role-playing、後者が personalization。 |
| 作り方 | サーベイなので特定手法ではなく、prompting, instruction tuning, memory, retrieval, user modeling などを整理する。 |
| 評価 | role-playing では persona consistency / character fidelity、personalization では user satisfaction / recommendation quality / task performance を見る。 |
| データ源 | 既存の persona dialogue dataset、キャラクター設定、ユーザ履歴、個人化タスクのログ、LLM-as-a-judge 系評価データ。 |
| 弱点 | role-playing と personalization が混同されやすい。persona が stereotype や privacy 問題を含むため、便利な分類である一方で倫理的整理が必要。 |

## 02. From Persona to Personalization: A Survey on RPLAs

PDF: [02_From_Persona_to_Personalization_RPLA_Survey_2404.18231.pdf](pdfs/02_From_Persona_to_Personalization_RPLA_Survey_2404.18231.pdf)

| 観点 | メモ |
|---|---|
| persona | Demographic Persona / Character Persona / Individualized Persona の3分類。RPLA を「assigned personas を模倣する specialized AI systems」と定義する。 |
| 作り方 | persona sourcing, agent construction, evaluation に分けて整理。prompt, profile construction, memory, fine-tuning, retrieval, product-level agent design を扱う。 |
| 評価 | human likeness, persona consistency, social intelligence, application usefulness。分類ごとに評価基準が変わる。 |
| データ源 | demographic attributes、歴史上人物・架空人物の資料、実ユーザとの継続対話・行動履歴。 |
| 弱点 | demographic persona は stereotype の危険が大きい。individualized persona は privacy と動的更新が難しい。character persona は知識漏れ・幻覚・版権問題が残る。 |

## 03. The Oscars of AI Theater

PDF: [03_Oscars_of_AI_Theater_2407.11484.pdf](pdfs/03_Oscars_of_AI_Theater_2407.11484.pdf)

| 観点 | メモ |
|---|---|
| persona | persona / character を「LMが演じる対象」として扱う。単純な一貫性から、魅力・行動・関係性まで含む character-driven simulation へ拡張。 |
| 作り方 | data, models and alignment, agent architecture, evaluation の分類。prompting だけでなく alignment、memory、agent design を含める。 |
| 評価 | character consistency, behavioral alignment, attractiveness が中心軸。単に正しい発話かではなく、演劇的・対話体験的な良さも評価対象。 |
| データ源 | persona profiles、キャラクター会話、物語・台本、合成対話、role-playアプリ由来データ、既存研究のベンチマーク。 |
| 弱点 | attractiveness のような主観評価は人によって揺れる。動的プロフィール管理、高次の一貫性、長期対話での崩れが未解決。 |

## 04. Character-LLM

PDF: [04_Character_LLM_2310.10158.pdf](pdfs/04_Character_LLM_2310.10158.pdf)

| 観点 | メモ |
|---|---|
| persona | Beethoven, Cleopatra, Caesar など、歴史上・物語上の「特定人物」。profile, experience, emotional states を persona の中核にする。 |
| 作り方 | Experience Reconstruction で人物経験を場面化し、その経験を用いて LLaMA 系モデルを訓練する。prompt だけでなく trainable agent にする点が特徴。 |
| 評価 | trained agent に interview し、人物の記憶・経験・感情が反映されるかを見る。character memorization と experience consistency が焦点。 |
| データ源 | 人物の経歴・経験・資料から抽出した scenes / memory flashes。LLMで経験場面を再構成して訓練データ化する。 |
| 弱点 | 再構成した経験には生成LLM由来の捏造が混ざりうる。歴史人物は検証可能性が限定され、本人らしさの評価も主観的。 |

## 05. RoleLLM

PDF: [05_RoleLLM_2310.00746.pdf](pdfs/05_RoleLLM_2310.00746.pdf)

| 観点 | メモ |
|---|---|
| persona | character-level role。職業など粗い persona ではなく、Sherlock Holmes のような細粒度の役を想定する。 |
| 作り方 | Role Profile Construction, Context-Instruct, RoleGPT, RoCIT の4段階。GPTで役らしいデータを作り、open-source LLMを role-conditioned instruction tuning する。 |
| 評価 | RoleBench で role-playing ability を測る。知識、発話スタイル、役らしさ、指示追従の総合評価。 |
| データ源 | 100 roles の profile、context-based instruction、GPT生成の role-specific QA / dialogue。RoleBench は168,093 samples。 |
| 弱点 | GPT生成データへの依存が大きく、データ品質・バイアスが上流モデルに引っ張られる。キャラクターの深い心理や長期記憶までは限定的。 |

## 06. CharacterEval

PDF: [06_CharacterEval_2401.01275.pdf](pdfs/06_CharacterEval_2401.01275.pdf)

| 観点 | メモ |
|---|---|
| persona | Role-Playing Conversational Agent の「キャラクター」。主に中国語環境で、知識・性格・発話スタイルを持つ対話相手として扱う。 |
| 作り方 | 評価ベンチマーク論文。モデル構築よりも、RPCA の性能を測るための多次元評価セットを設計する。 |
| 評価 | character consistency, conversational ability, knowledge, style など複数観点。人間評価と自動評価の接続が焦点。 |
| データ源 | 中国語キャラクター対話・プロフィール・評価質問。対象キャラクターに関する知識や会話例をもとに作る。 |
| 弱点 | 言語・文化圏が中国語に寄る。人間評価の主観性と、評価者が本当にキャラクターを知っているかという問題が残る。 |

## 07. CharacterBench

PDF: [07_CharacterBench_2412.11912.pdf](pdfs/07_CharacterBench_2412.11912.pdf)

| 観点 | メモ |
|---|---|
| persona | customized characters。特定キャラクターをどれだけ理解・再現できるかを対象にする。 |
| 作り方 | ベンチマーク論文。キャラクター理解・カスタマイズ能力を測る bilingual benchmark を構築する。 |
| 評価 | キャラクター属性、知識、行動、発話スタイル、状況に応じた応答の妥当性。CharacterEval より体系化された評価次元を志向。 |
| データ源 | キャラクター設定・作品情報・対話例・質問応答。英中 bilingual な評価データ。 |
| 弱点 | ベンチマークが対象キャラクターや言語に依存する。高得点でも長期対話・未知状況・感情推移の再現を保証しない。 |

## 08. TimeChara

PDF: [08_TimeChara_2405.18027.pdf](pdfs/08_TimeChara_2405.18027.pdf)

| 観点 | メモ |
|---|---|
| persona | 物語内のある時点に存在する character。キャラクター人格だけでなく「その時点で知っていること」を persona の一部として扱う。 |
| 作り方 | point-in-time character hallucination を検出する評価設定。モデルに時点を指定して会話させ、未来知識の漏れを見る。 |
| 評価 | temporal consistency、未来情報への言及、時点整合性。例として、まだ知らない将来の妻や事件を言ってしまうかを測る。 |
| データ源 | 物語作品の時系列情報、キャラクター知識、時点ごとの質問・対話。 |
| 弱点 | 作品の時系列アノテーションが必要。キャラクターらしさと時点整合性が衝突する場合の評価が難しい。 |

## 09. PingPong

PDF: [09_PingPong_2409.06820.pdf](pdfs/09_PingPong_2409.06820.pdf)

| 観点 | メモ |
|---|---|
| persona | role-playing agent が演じるキャラクター。単発応答ではなく、ユーザとの多ターン相互作用で維持される persona を見る。 |
| 作り方 | user emulation を使って動的な multi-turn evaluation を行う。評価用ユーザもモデルで生成し、対話を進めながら評価する。 |
| 評価 | 多ターンでの一貫性、応答の自然さ、破綻の起きにくさ、会話相手としての持続性。 |
| データ源 | キャラクター設定、シナリオ、ユーザエミュレータが生成する会話ログ、評価モデルの判定。 |
| 弱点 | user emulator と judge model の品質に依存する。人間ユーザの予測不能さや主観的満足をどこまで再現できるかが課題。 |

## 10. PersonaEval

PDF: [10_PersonaEval_2508.10014.pdf](pdfs/10_PersonaEval_2508.10014.pdf)

| 観点 | メモ |
|---|---|
| persona | role-play 応答を評価する対象としての persona。評価者が persona を理解できているかが主題。 |
| 作り方 | LLM-as-a-judge の妥当性を検証する評価研究。role-play の良し悪しを LLM evaluator が人間のように判定できるかを調べる。 |
| 評価 | judge-human agreement、推論能力と評価能力の関係、persona理解・比較判断の正確さ。 |
| データ源 | role-play 応答、persona/profile、human evaluation、複数LLM evaluator の判定。 |
| 弱点 | LLM judge は fluent な応答に引っ張られやすい可能性がある。評価用LLMの推論能力と role-play 感性が一致するとは限らない。 |

## 11. FURINA

PDF: [11_FURINA_2510.06800.pdf](pdfs/11_FURINA_2510.06800.pdf)

| 観点 | メモ |
|---|---|
| persona | 完全カスタム可能な role-playing benchmark の対象としての persona / character。 |
| 作り方 | multi-agent pipeline でベンチマークを生成・拡張する。キャラクター設定、質問、会話、評価軸を自動構成する方向。 |
| 評価 | role-playing hallucination、reasoning、persona adherence、custom benchmark 上の性能。reasoning と RP hallucination のトレードオフを観察する。 |
| データ源 | multi-agent で生成した設定・評価項目・対話データ、既存キャラクター情報。 |
| 弱点 | 自動生成ベンチマークなので、生成側のモデルバイアスが評価に入る。customizability は高いが、人手検証なしでは品質保証が難しい。 |

## 12. Persona-Aware Contrastive Learning

PDF: [12_Persona_Aware_Contrastive_Learning_2503.17662.pdf](pdfs/12_Persona_Aware_Contrastive_Learning_2503.17662.pdf)

| 観点 | メモ |
|---|---|
| persona | role profile と対話履歴に現れるキャラクター性。発話が persona と整合するかを中心に扱う。 |
| 作り方 | Persona-Aware Contrastive Learning。正しい persona-response と不整合な response を対比し、annotation-free に persona alignment を強める。 |
| 評価 | persona consistency、role-play response quality、既存手法との比較。 |
| データ源 | role-play dialogue、persona profile、role chain、positive/negative response pair。負例は persona 不一致を利用して作る。 |
| 弱点 | contrastive pair の作り方に性能が依存する。persona 一貫性は上がっても、魅力・創造性・長期記憶まで改善するとは限らない。 |

## 13. PsyMem

PDF: [13_PsyMem_2505.12814.pdf](pdfs/13_PsyMem_2505.12814.pdf)

| 観点 | メモ |
|---|---|
| persona | 心理学的指標と memory によって表される persona。Big Five のような性格特性だけでなく、記憶制御を含む。 |
| 作り方 | 26の心理学的指標と明示的 memory control を使い、role-play agent の内面・記憶を制御する。 |
| 評価 | psychological consistency、memory fidelity、role-play quality、人格特性の再現性。 |
| データ源 | 心理尺度、persona profile、対話履歴、memory items、評価用質問。 |
| 弱点 | 心理指標が本当に会話上の人格を十分に表すかは不明。指標数が増えるほど制御・評価・解釈が複雑になる。 |

## 14. Crab + RoleRM

PDF: [14_Crab_RoleRM_ACL2025.pdf](pdfs/14_Crab_RoleRM_ACL2025.pdf)

| 観点 | メモ |
|---|---|
| persona | configurable role-playing LLM が扱う役・キャラクター。細粒度の role attributes を設定可能にする。 |
| 作り方 | Crab で configurable RP-LLM を作り、RoleRM という reward model で role-play 品質を評価・改善する。 |
| 評価 | fine-grained role-play evaluation、human preference alignment、reward model の予測性能。 |
| データ源 | role profile、対話応答、選好データ、人間評価またはLLM支援アノテーション。 |
| 弱点 | reward model が評価軸を固定してしまう危険がある。人間の好み・キャラ解釈の多様性を1つの報酬に圧縮しすぎる可能性。 |

## 15. ChARM

PDF: [15_ChARM_2505.23923.pdf](pdfs/15_ChARM_2505.23923.pdf)

| 観点 | メモ |
|---|---|
| persona | character と act の組み合わせ。単なる人物設定ではなく、その場面でどの act を行うかに応じて評価を変える。 |
| 作り方 | Character-based Act-adaptive Reward Modeling。RoleplayPref / RoleplayEval を用い、DPO などの alignment に接続する。 |
| 評価 | act-aware reward、character consistency、preference prediction、DPO 後の role-play 品質。 |
| データ源 | role-play preference data、character profile、act labels、評価用応答ペア。 |
| 弱点 | act の定義やラベル付けが難しい。報酬設計が細かくなるほど汎用性とのトレードオフが出る。 |

## 16. JSAI2024: LLMを用いたペルソナ指定型キャラクターの感情解析

PDF: [16_JSAI2024_Persona_Character_Emotion_4K1GS903.pdf](pdfs/16_JSAI2024_Persona_Character_Emotion_4K1GS903.pdf)

| 観点 | メモ |
|---|---|
| persona | ペルソナ指定型キャラクター。キャラクターの感情ベクトルや発話意志を persona の振る舞いとして見る。 |
| 作り方 | LLM に persona を与え、感情ベクトル評価と発話意志判定を行う。生成よりも解析・評価寄り。 |
| 評価 | 感情推定の妥当性、発話意志判定、キャラクター設定と感情反応の整合性。 |
| データ源 | 日本語キャラクター設定、対話文、感情ラベルまたは感情ベクトル。 |
| 弱点 | 感情ベクトルがキャラクターらしさ全体を代表するわけではない。LLM の感情推定が評価器として妥当か検証が必要。 |

## 17. NLP2025 P10-5: キャラクターの2面性を表出する発話の生成

PDF: [17_NLP2025_P10-5_Character_Duality_Generation.pdf](pdfs/17_NLP2025_P10-5_Character_Duality_Generation.pdf)

| 観点 | メモ |
|---|---|
| persona | 既存キャラクターの「主に表出する性格」と、意外性を持つ「2面性」。ツンデレのような内的な振れ幅を扱う。 |
| 作り方 | GPT-4o にプロンプトで2面性を出す応答を生成させ、候補生成・リランキングで改善を試す。 |
| 評価 | キャラクター性、魅力、2面性の表出。人間が発話を見て2面性を感じるかを評価する。 |
| データ源 | キャラクター設定、2面性を出すべき状況、生成応答候補、人間評価。 |
| 弱点 | プロンプトだけでは2面性をうまく表出できない場合が多い。いつ2面性を出すべきかというタイミング問題は初期検討外。 |

## 18. NLP2025 P10-6: 擬似選好チューニングによる対話応答のペルソナ一貫性向上

PDF: [18_NLP2025_P10-6_Persona_Consistency_Pseudo_Preference_Tuning.pdf](pdfs/18_NLP2025_P10-6_Persona_Consistency_Pseudo_Preference_Tuning.pdf)

| 観点 | メモ |
|---|---|
| persona | 対話応答生成における話者 persona。例として「猫を飼っている」「キャンプが好き」などの自己情報。 |
| 作り方 | 他対話からランダムに抽出した persona で生成した応答を擬似負例、参照応答を正例として preference tuning する。 |
| 評価 | persona consistency と自然性。教師あり学習や Dialogue-NLI 報酬による強化学習と比較。 |
| データ源 | persona 情報付き対話データ、参照応答、ランダム別personaで作る擬似負例。 |
| 弱点 | 負例が「別personaで生成」なので、実際の微妙な矛盾や自然な逸脱をどこまで扱えるかが課題。応答の多様性を損なう可能性もある。 |

## 19. NLP2025 P10-9: なりきり雑談システム評価のためのキャライメージ一致

PDF: [19_NLP2025_P10-9_Character_Image_Evaluator_Agreement.pdf](pdfs/19_NLP2025_P10-9_Character_Image_Evaluator_Agreement.pdf)

| 観点 | メモ |
|---|---|
| persona | 創作上の架空人物の「キャラらしさ」。原作者、ファン、作品を知らない人でキャライメージが違う可能性を扱う。 |
| 作り方 | 評価方法の研究。ファンがキャラらしい/らしくないセリフを作り、4択クイズで評価者間一致を見る。 |
| 評価 | キャライメージの一致率、原作者とファンの違い、評価者の作品理解度。 |
| データ源 | 作中セリフ、ファン作成セリフ、4択クイズ、回答者の回答データ。 |
| 弱点 | キャラらしさが評価者集団に依存することを示す一方、どの集団を正解にすべきかは残る。クイズ形式が実際の対話評価を完全に代表するわけではない。 |

## 20. NLP2025 P10-17: LLMベースのマルチエージェントTRPGゲームマスター

PDF: [20_NLP2025_P10-17_TRPG_Game_Master_Multi_Agent.pdf](pdfs/20_NLP2025_P10-17_TRPG_Game_Master_Multi_Agent.pdf)

| 観点 | メモ |
|---|---|
| persona | TRPG のゲームマスターと NPC。単一キャラクターというより、進行役・ルール管理者・物語演出者としての role。 |
| 作り方 | LLM にシナリオとルールブックを与えてGMをさせ、複数エージェントによるフィードバックで応答を改善する。 |
| 評価 | ルール遵守、シナリオ整合性、自然な応答、プレイヤー要望への柔軟性。GM経験者による課題分析。 |
| データ源 | TRPGシナリオ、ルールブック、プレイ対話、マルチエージェントのフィードバック。 |
| 弱点 | ルール誤り、状態管理ミス、シナリオ逸脱が起こりやすい。ゲームごとにルールや関数設計が異なり、汎用化が難しい。 |

## 21. NLP2025 P10-20: 思考発話を利用した個人の発話及び性格特性再現

PDF: [21_NLP2025_P10-20_Thought_Utterance_Personal_Traits.pdf](pdfs/21_NLP2025_P10-20_Thought_Utterance_Personal_Traits.pdf)

| 観点 | メモ |
|---|---|
| persona | 多様な個人の発話・感情・思考・Big Five 性格特性。著名人や架空人物ではなく、個人の内面再現に寄せる。 |
| 作り方 | 既存対話データに LLM で対象人物の思考発話を付与し、その thinking + speaking データで fine-tuning する。 |
| 評価 | 発話スタイルの再現、感情・思考の再現、Big Five など性格特性の再現性。 |
| データ源 | 既存対話データ、LLM生成の思考発話、個人のBig Fiveスコア。 |
| 弱点 | LLMが付与した思考発話が本当に本人の内面を表すかは不確か。思考を明示すると説明らしさは増すが、実在個人の privacy と同意が重要になる。 |

