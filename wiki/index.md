# Wiki Index

> このファイルはLLMによって自動メンテナンスされます。手動編集は最小限に。
> Last updated: 2026-05-08

## 研究テーマ
[[研究方針]] — LLMを用いた議論支援システムの研究
[[研究方針]] — 不動産賃借希望者ペルソナAIエージェント（記事ベースのキャラクター模倣）

---

## 概念記事 (concepts/)

| 記事 | 概要 | 関連論文 |
|------|------|---------|
| [[concepts/argument-mining]] | 議論マイニングの定義・タスク・手法の全体像 | LLM-AM-Survey, LLMs-AM-Relation |
| [[concepts/topic-shift-detection]] | 話題転換・脱線検知の手法と評価 | Topic-Shift-SIGDIAL |
| [[concepts/cognitive-bias-in-llm]] | LLMにおける認知バイアスの種類と検出手法 | MindScope, Cognitive-Bias-Search |
| [[concepts/llm-prompting-strategies]] | プロンプトエンジニアリング・CoT・few-shot等の手法 | LLM-AM-Survey |
| [[concepts/discussion-visualization]] | 議論の可視化・構造化手法 | LLMs-AM-Relation |

---

## 論文記事 (papers/)

| 記事 | 著者・年 | 概要1行 | タグ |
|------|---------|---------|------|
| [[papers/llm-argument-mining-survey]] | Li et al., 2025 | LLM時代の議論マイニング手法サーベイ（250論文分析） | #survey #argument-mining |
| [[papers/llms-am-relationship-classification]] | arXiv 2402.04330, 2024 | LLMによる議論の検出・抽出・関係分類の性能評価 | #argument-mining #classification |
| [[papers/topic-shift-detection-sigdial2021]] | Konigari et al., SIGDIAL 2021 | XLNetを用いた対話中の話題転換分類（Precision 84%） | #topic-shift #dialogue |
| [[papers/mindscope-cognitive-bias]] | 謝振涛 et al., 2024 | マルチエージェントで72種の認知バイアスを検出 | #cognitive-bias #multi-agent |
| [[papers/cognitive-bias-conversational-search]] | Ji et al., 2024 | 音声会話検索における認知バイアスの検出・軽減 | #cognitive-bias #speech |
| [[papers/2508.02584]] | Ng et al., 2025 | MArgE: QBAF/DF-QuADで複数LLMの論証証拠を統合 | #argument-mining #multi-agent #llm |
| [[papers/2510.02339]] | Zhou et al., 2025 | ArgLLMsにおける不確実性定量化手法の比較 | #argument-mining #llm #uncertainty |
| [[papers/2409.07453]] | Hong et al., 2025 | CAELF: 論証フレームワークで説明可能な学生作文評価 | #argumentation-framework #education #contestable-ai |
| [[papers/2412.05206]] | Dhole et al., 2024 | ConQRet: RAArgベンチマーク・LLMジャッジ評価 | #argument-mining #rag #benchmark |
| [[papers/2402.16063]] | Li et al., ACL 2024 | CEG: 引用強化生成でLLMチャットボットのハルシネーション検出 | #hallucination #rag #citation |
| [[papers/2503.08569]] | Zhu et al., 2025 | DeepReview: 3段階推論チェーンで論文レビューを自動生成 | #paper-review #reasoning #llm |
| [[papers/2602.13713]] | Uberna et al., 2026 | 論証理論をRAGで組込むMASで言い換え分類F1=0.67 | #argument-mining #multi-agent #rag |
| [[papers/2407.11919]] | Kirstein et al., 2024 | CoT MIP＋フィードバックで会議要約を2段階改善 | #meeting-summarization #llm #feedback |
| [[papers/2307.15793]] | Asthana et al., CSCW 2025 | Highlights＋Hierarchicalの2デザインで会議リキャップ | #meeting-summarization #hci #llm |
| [[papers/2406.12480]] | Wagner et al., ICLR 2025 | LLM合成データ＋SQBC能動学習でスタンス検出F1=0.754 | #stance-detection #synthetic-data #active-learning |
| [[papers/2505.12474]] | Zhou et al., 2025 | 背景知識＋討論からBG要約＋意見要約生成するKGDS | #discussion-summarization #knowledge-grounded #benchmark |
| [[papers/2407.01161]] | Tsai et al., 2025 | ARヘッドセット＋視線選択でLLMメモ提案を採択するGazeNoter | #note-taking #augmented-reality #hci |
| [[papers/2602.16607]] | Marques et al., WWW 2026 | ポルトガル語市議会議事録2880件要約ベンチマーク | #meeting-summarization #dataset #benchmark |
| [[papers/2501.08977]] | Moen et al., 2025 | 臨床文書要約の9属性品質評価器具PDSQI-9（医療ドメイン） | #medical-summarization #evaluation |
| [[papers/2502.08224]] | Pei et al., WWW 2025 | SOPフロー駆動の5エージェントITインフラ根本原因分析システム | #multi-agent #sop #it-operations |
| [[papers/2509.06602]] | Blondeel et al., 2025 | 腫瘍委員会向けLLMマルチエージェントHAOとTBFact評価（医療ドメイン） | #multi-agent #medical #summarization |
| [[papers/2301.09911]] | Alshomary et al., 2023 | マルチタスクBARTとスタンスランキングで反論のContrastiveness最大化 | #counter-argument #argument-mining #llm |
| [[papers/2503.05328]] | 2025 | Web検索RAGで動的知識統合し事実根拠付き反論を生成、LLM審判ρ=0.82 | #counter-argument #argument-mining #rag |
| [[papers/2402.08498]] | ICWSM 2025 | 3修辞スタイルの反論比較でスタイル-証拠トレードオフを実証（38,000ペア） | #counter-argument #persuasion #llm |
| [[papers/2404.10570]] | Heidelberg+Bielefeld, 2024 | PAKT知識グラフで討論のフレーム・価値観・概念をNeo4jで可視化 | #argumentation-framework #knowledge-grounded #debate |
| [[papers/2410.23724]] | Imperial+Ericsson+Liverpool, 2024 | Argumentation×MLの交差点を3タイプ・2目的で体系化したサーベイ | #survey #argument-mining #argumentation-framework |
| [[papers/2310.10158]] | Shao et al., EMNLP 2023 | キャラクタープロファイル学習でLLMを特定人物として振る舞わせる | #persona #role-playing #fine-tuning |
| [[papers/2301.02401]] | Lim et al., EMNLP 2022 | 外部知識とペルソナを同時グラウンディングする対話エージェント | #persona #knowledge-grounding #RAG |
| [[papers/2408.11779]] | Zhu et al., ICLR 2025 | Big Five等の性格特性でLLMを効率的にアライメント（PAPI） | #persona #personality #alignment |
| [[papers/2010.03205]] | Majumder et al., EMNLP 2020 | Commonsense拡張でペルソナから暗黙の好みを推論して対話 | #persona #commonsense #variational |
| [[papers/2109.07713]] | Wu et al., EMNLP 2021 | 最小編集でペルソナ一貫性を保ちながら新ドメインへ転移 | #persona #consistency #minimal-edit |
| [[papers/2305.17388]] | Ahn et al., ACL 2023 | テキスト＋画像のマルチモーダルペルソナに基づく対話 | #persona #multimodal #dataset |
| [[papers/2503.17662]] | Ji et al., ACL 2025 | アノテーション不要の対照学習でロールプレイ一貫性を向上（PCL） | #persona #consistency #contrastive-learning |
| [[papers/2302.06674]] | Oh et al., EMNLP 2023 | ペルソナ＋知識を同時検索するRAGフレームワーク（PK-ICR） | #persona #RAG #retrieval |
| [[papers/2407.03974]] | Tamoyan et al., 2024 | ペルソナLLMで人間-チャットボット対話を44%識別不能率でシミュレート | #persona #user-simulation #evaluation |
| [[papers/2401.12474]] | Lu et al., ACL 2024 | 自己アライメントで4000キャラクターのロールプレイデータを自動生成（Ditto） | #role-playing #self-alignment #dataset |
| [[papers/2502.09082]] | Wang et al., ICML 2025 | 17,966キャラクター＋GCA評価でペルソナシミュレーションのSOTA（CoSER） | #persona #role-playing #evaluation #dataset |
| [[papers/2010.03538]] | Cornell, 2020 | 議論構造特徴量＋BiLSTM+BERTでDDO討論勝者予測精度77.28% | #argument-mining #persuasion #debate #dataset |
| [[papers/2011.01589]] | Grammarly+Mannheim, 2020 | GAQCorpus: 3ドメイン5,285件を4軸（論理性・効果性・合理性）で品質評価 | #argument-quality #argument-mining #dataset |
| [[papers/2103.07769]] | Qatar+FullFact+Bologna, 2021 | 自動ファクトチェック4段階パイプラインの包括サーベイ | #survey #factuality #claim-verification |

---

## クエリ出力 (queries/)

*Q&Aの出力はこちらに蓄積されます*

---

## タグ一覧

- `#argument-mining` — 議論マイニング関連
- `#argumentation-framework` — 論証フレームワーク（QBAF・Dungなど）
- `#topic-shift` — 話題転換・脱線検知関連
- `#cognitive-bias` — 認知バイアス関連
- `#survey` — サーベイ論文
- `#classification` — 分類タスク
- `#dialogue` — 対話システム
- `#multi-agent` — マルチエージェント
- `#speech` — 音声・発話
- `#llm` — LLM活用
- `#visualization` — 可視化
- `#rag` — Retrieval-Augmented Generation
- `#benchmark` — ベンチマーク・データセット
- `#hallucination` — ハルシネーション検出・軽減
- `#meeting-summarization` — 会議・討論要約
- `#stance-detection` — スタンス検出（賛成/反対）
- `#synthetic-data` — LLM合成データ活用
- `#active-learning` — 能動学習
- `#discussion-summarization` — 討論要約・知識グラウンド
- `#note-taking` — リアルタイムメモ・支援
- `#hci` — ヒューマンコンピュータインタラクション
- `#contestable-ai` — 異議申し立て可能なAI
- `#education` — 教育・評価支援
- `#medical-summarization` — 医療文書要約（参考）
- `#sop` — 標準作業手順書活用
- `#it-operations` — ITオペレーション（参考）
- `#counter-argument` — 反論生成・反論支援
- `#argument-quality` — 議論品質評価（Cogency/Effectiveness/Reasonableness）
- `#persuasion` — 説得・議論の効果
- `#debate` — 討論・ディベート
- `#factuality` — 事実性・ファクトチェック
- `#claim-verification` — クレーム検証・事実検証
- `#knowledge-grounded` — 知識グラウンド型生成
- `#persona` — ペルソナ・キャラクター模倣
- `#role-playing` — ロールプレイ・キャラクターエージェント
- `#character-alignment` — キャラクターアライメント
- `#user-simulation` — ユーザーシミュレーション
- `#consistency` — ペルソナ一貫性
- `#personality` — 性格特性（Big Fiveなど）
- `#self-alignment` — 自己アライメント（アノテーション不要）
- `#contrastive-learning` — 対照学習
- `#commonsense` — 常識推論
