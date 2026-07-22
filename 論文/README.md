# 文献管理

逆さま不動産の借り手AIエージェント研究で参照する文献の保管庫。
他者の文献と自分の論文原稿を混同しないため、このフォルダには参考文献だけを置く。

## フォルダ構成

| パス | 内容 |
|---|---|
| `pdfs/` | 番号付きの原論文PDF |
| `notes/` | 完成した日本語読解ノート |
| `extracts/` | PDFから抽出した本文や翻訳途中のテキスト |
| `inbox/` | 新しく入手し、まだ番号を付けていない文献 |
| `references.bib` | 原稿で実際に引用する文献のBibTeX |

ファイル名先頭の番号を文献IDとして使い、PDF・ノート・抽出テキストを対応させる。既存の `01`〜`36` は振り直さない。

## 文献台帳

凡例：`読了` = 読解ノートあり、`PDFのみ` = ノート未作成、`抽出あり` = 作業用テキストあり。

| ID | 文献 | 主な位置づけ | 状態 |
|---:|---|---|---|
| 01 | Two Tales of Persona in LLMs | サーベイ・概念整理 | 読了・抽出あり |
| 02 | From Persona to Personalization / RPLA Survey | サーベイ・概念整理 | 読了・抽出あり |
| 03 | Oscars of AI Theater | ロールプレイ評価 | PDFのみ |
| 04 | PrefEval | 選好追従評価 | 読了・抽出あり |
| 05 | PicPersona-TOD | 個人化・タスク指向対話 | 読了・抽出あり |
| 06 | Persona-Aware Alignment / PAL | ペルソナ整合 | 読了・抽出あり |
| 07 | TimeChara | 時点整合・幻覚評価 | 読了・抽出あり |
| 08 | PersonaEval | ロールプレイ評価 | 読了・抽出あり |
| 09 | PingPong | ユーザ模擬・マルチターン評価 | 読了・抽出あり |
| 10 | FaithEval | 文脈忠実性 | 読了 |
| 11 | Global Faithfulness / PRP | 制約への大域的忠実性 | 読了 |
| 12 | PersonaGym | ペルソナエージェント評価 | 読了 |
| 13 | PersonaMem | 動的ユーザ情報・記憶 | 読了 |
| 14 | Q2 | Grounded dialogueの事実整合性 | 読了・抽出あり |
| 15 | Increasing Faithfulness | 知識接地対話 | 読了・抽出あり |
| 16 | Grounded Minimal Edits | ペルソナ接地対話 | 読了・抽出あり |
| 17 | SG-USM | タスク指向対話の満足度 | 読了・抽出あり |
| 18 | Character-LLM | キャラクターLLM | PDFのみ |
| 19 | RoleLLM | ロールプレイLLM | PDFのみ |
| 20 | CharacterEval | キャラクター評価 | PDFのみ |
| 21 | Persona-Consistent NLI | ペルソナ一貫性 | 読了・抽出あり |
| 22 | CharacterBench | キャラクター評価 | PDFのみ |
| 23 | Persona-Aware Contrastive Learning | ペルソナ学習 | PDFのみ |
| 24 | FURINA | ロールプレイ | PDFのみ |
| 25 | PsyMem | 心理・記憶 | PDFのみ |
| 26 | Crab / RoleRM | ロールプレイ報酬モデル | PDFのみ |
| 27 | ChARM | キャラクター評価・学習 | PDFのみ |
| 28 | JSAI2024 Persona / Character / Emotion | 感情・キャラクター | PDFのみ |
| 29 | NLP2025 Character Duality Generation | キャラクター生成 | PDFのみ |
| 30 | NLP2025 Persona Consistency | ペルソナ一貫性 | PDFのみ |
| 31 | NLP2025 Character Image Evaluator Agreement | 評価者一致 | PDFのみ |
| 32 | NLP2025 TRPG Game Master Multi-Agent | マルチエージェント | PDFのみ |
| 33 | NLP2025 Thought / Utterance / Personal Traits | 内的状態・発話 | PDFのみ |
| 34 | EvoEmo | 感情表現・対話戦略 | 読了 |
| 35 | Emotional RAG | 感情・ロールプレイ記憶 | 読了 |
| 36 | DMNA | 戦略と表現の統合 | 読了 |

## 研究上の優先テーマ

この研究では、次の順で文献を接続する。

1. 感情表現によって借り手の熱意・動機を伝える設計
2. BaselineとProposedを比較する評価設計
3. 記事・物件ファクトに反しない忠実性
4. 適合確認の質問を含むタスク指向対話
5. ペルソナ一貫性とマルチターン対話

この対話は条件交渉ではなく、借り手が受動的な大家へ働きかけ、対面につながるきっかけを作るものとして文献との違いを記録する。

## 新しい文献を追加するとき

1. まず `inbox/` にPDFを置く。
2. 次の未使用番号を付けて `pdfs/` に移す。
3. `notes/_template.md` を複製し、同じ番号で読解ノートを作る。
4. この台帳の状態と位置づけを更新する。
5. 原稿で実際に引用すると決めた段階で `references.bib` に追加する。

## 読解ノートの状態

ノートの `status` には `unread`、`reading`、`read` のいずれかを使う。`relevance` は `high`、`medium`、`low` とし、フォルダ分けの代わりに `themes` を複数指定する。
