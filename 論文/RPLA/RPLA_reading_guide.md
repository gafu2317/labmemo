# Role-Playing Language Agents (RPLA) 読書ガイド

調査日: 2026-05-12

## まず掴む全体像

RPLA は、LLM に「特定のペルソナ・キャラクター・個人像」を割り当て、その人物らしい知識、口調、感情、行動方針、記憶を保ちながら対話させる研究領域。

大きく見ると、論点は次の4つに分かれる。

1. Persona の種類: demographic / character / individualized
2. 作り方: prompting / retrieval-memory / instruction tuning / preference tuning / reward modeling / multi-agent generation
3. 評価: character consistency, behavioral alignment, attractiveness, human-likeness, hallucination, temporal consistency
4. リスク: stereotype, privacy, identity misuse, over-attachment, LLM-as-a-judge の妥当性

最初は `Two Tales` で persona 研究全体の地図を作り、次に `From Persona to Personalization` で RPLA という名前の体系を押さえるのがよい。

## 推奨読書順

### 1. サーベイで地図を作る

- [01_Two_Tales_of_Persona_in_LLMs_2406.01171.pdf](pdfs/01_Two_Tales_of_Persona_in_LLMs_2406.01171.pdf)
  - Persona を LLM Role-Playing と LLM Personalization の二系統に整理。
  - RPLA だけでなく、推薦・検索・LLM-as-a-judge まで射程に入る。

- [02_From_Persona_to_Personalization_RPLA_Survey_2404.18231.pdf](pdfs/02_From_Persona_to_Personalization_RPLA_Survey_2404.18231.pdf)
  - RPLA を前面に出したサーベイ。
  - Demographic Persona / Character Persona / Individualized Persona の3分類が読みどころ。

- [03_Oscars_of_AI_Theater_2407.11484.pdf](pdfs/03_Oscars_of_AI_Theater_2407.11484.pdf)
  - Role-playing with LMs の設計要素を data / models and alignment / agent architecture / evaluation に分類。
  - character consistency, behavioral alignment, attractiveness という評価軸を押さえる。

### 2. 基礎論文で「作り方」を見る

- [04_Character_LLM_2310.10158.pdf](pdfs/04_Character_LLM_2310.10158.pdf)
  - historical / fictional character を演じる trainable agent。
  - Experience Reconstruction によるデータ生成が重要。

- [05_RoleLLM_2310.00746.pdf](pdfs/05_RoleLLM_2310.00746.pdf)
  - benchmark, eliciting, enhancing の三本柱。
  - RoleBench, RoleGPT, RoCIT, RoleLLaMA / RoleGLM など、後続研究の語彙が多い。

### 3. 評価系を押さえる

- [06_CharacterEval_2401.01275.pdf](pdfs/06_CharacterEval_2401.01275.pdf)
  - 中国語 RPCA 評価ベンチマーク。多面的な評価軸の初期例。

- [07_CharacterBench_2412.11912.pdf](pdfs/07_CharacterBench_2412.11912.pdf)
  - character customization 能力の大規模 bilingual benchmark。

- [08_TimeChara_2405.18027.pdf](pdfs/08_TimeChara_2405.18027.pdf)
  - 物語内の時点を固定したときの character hallucination を扱う。
  - 「未来知識をうっかり話す」問題として理解しやすい。

- [09_PingPong_2409.06820.pdf](pdfs/09_PingPong_2409.06820.pdf)
  - user emulation と multi-model evaluation による多ターン評価。

- [10_PersonaEval_2508.10014.pdf](pdfs/10_PersonaEval_2508.10014.pdf)
  - LLM evaluator が人間のように role-play を評価できるかを疑う論文。
  - 評価研究をするなら重要。

- [11_FURINA_2510.06800.pdf](pdfs/11_FURINA_2510.06800.pdf)
  - multi-agent pipeline でカスタム可能な benchmark を作る。
  - reasoning と RP hallucination のトレードオフが面白い。

### 4. 学習・アライメント手法を見る

- [12_Persona_Aware_Contrastive_Learning_2503.17662.pdf](pdfs/12_Persona_Aware_Contrastive_Learning_2503.17662.pdf)
  - annotation-free な persona alignment。
  - role chain と contrastive learning が要点。

- [13_PsyMem_2505.12814.pdf](pdfs/13_PsyMem_2505.12814.pdf)
  - 26の心理学的指標と明示的 memory control。
  - キャラクターの内面・記憶をどう表現するかを見るのに良い。

- [14_Crab_RoleRM_ACL2025.pdf](pdfs/14_Crab_RoleRM_ACL2025.pdf)
  - configurable RP-LLM と RoleRM。
  - fine-grained evaluation と human perception alignment が中心。

- [15_ChARM_2505.23923.pdf](pdfs/15_ChARM_2505.23923.pdf)
  - character-based act-adaptive reward modeling。
  - RoleplayPref / RoleplayEval と DPO への接続が読みどころ。

## 日本語で近いもの

- [16_JSAI2024_Persona_Character_Emotion_4K1GS903.pdf](pdfs/16_JSAI2024_Persona_Character_Emotion_4K1GS903.pdf)
  - ペルソナ指定型キャラクターの感情ベクトル評価と発話意志判定。

- [17_NLP2025_P10-5_Character_Duality_Generation.pdf](pdfs/17_NLP2025_P10-5_Character_Duality_Generation.pdf)
  - キャラクターの2面性を表出する発話生成。

- [18_NLP2025_P10-6_Persona_Consistency_Pseudo_Preference_Tuning.pdf](pdfs/18_NLP2025_P10-6_Persona_Consistency_Pseudo_Preference_Tuning.pdf)
  - 擬似選好チューニングによるペルソナ一貫性向上。

- [19_NLP2025_P10-9_Character_Image_Evaluator_Agreement.pdf](pdfs/19_NLP2025_P10-9_Character_Image_Evaluator_Agreement.pdf)
  - なりきり雑談システム評価のためのキャライメージ一致。

- [20_NLP2025_P10-17_TRPG_Game_Master_Multi_Agent.pdf](pdfs/20_NLP2025_P10-17_TRPG_Game_Master_Multi_Agent.pdf)
  - LLM ベースのマルチエージェント TRPG ゲームマスター。

- [21_NLP2025_P10-20_Thought_Utterance_Personal_Traits.pdf](pdfs/21_NLP2025_P10-20_Thought_Utterance_Personal_Traits.pdf)
  - 思考発話を利用した個人の発話・性格特性再現。

## 読むときのメモ観点

各論文は、次の5点だけ埋めれば比較しやすい。

| 観点 | メモ |
|---|---|
| 何を persona と呼んでいるか | demographic / character / individualized / memory / psychology |
| どう作るか | prompt, retrieval, tuning, reward, multi-agent |
| 何を評価しているか | consistency, attractiveness, hallucination, human-likeness, preference |
| データ源 | fiction, scripts, profiles, synthetic dialogue, human annotation |
| 弱点 | judge validity, temporal leakage, stereotype, privacy, scale |

## 最短ルート

時間がない場合は、まずこの5本だけでよい。

1. Two Tales
2. From Persona to Personalization
3. Character-LLM
4. RoleLLM
5. CharacterBench または TimeChara

その後、研究テーマが「学習手法」なら PCL / PsyMem / Crab / ChARM へ、「評価方法」なら PingPong / PersonaEval / FURINA へ進む。

