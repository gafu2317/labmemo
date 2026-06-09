# 論文フォルダ（PDF / 読解ノート）

`RPLA/` と `borrower_agent/` に分かれていた文献を **2026-05 に `論文/pdfs/` と `論文/translations/` へ統合**した。

## 構成

| パス | 内容 |
|------|------|
| `pdfs/` | 論文 PDF（`01_`〜`33_` の連番プレフィックス） |
| `translations/` | 日本語読解ノート（`*_ja_reading_note.md`）と途中メモ（`*.txt`） |

ファイル名の先頭番号は **PDF と読解ノートで対応**する（例: `05_PicPersona_...pdf` ↔ `05_PicPersona_TOD_ja_reading_note.md`）。

## 収録の出どころ（統合前）

- **RPLA**: Role-Playing / Persona / Character 周辺（キャラクター LLM、ベンチマーク、国内学会論文など）
- **borrower_agent**: 借り手 AI エージェント向け（faithfulness、目的志向対話、preference 遵守など）

同一論文の PDF は1本にまとめている。読解ノートはテーマごとに別内容のものがある場合のみ残す（重複していたものは統合時に整理）。

## 番号一覧（概要）

| # | テーマ | 代表論文 |
|---|--------|----------|
| 01–02 | サーベイ・整理 | Two Tales, RPLA Survey |
| 03–09 | 評価・TOD・RPLA | Oscars, PrefEval, PicPersona, PAL, TimeChara, PersonaEval, PingPong |
| 10–13 | 借り手 AI 直結 | FaithEval, Global Faithfulness, PersonaGym, PersonaMem |
| 14–17 | 忠実性・ grounding | Q2, Increasing Faithfulness, Grounded Minimal Edits, SG-USM |
| 18–27 | キャラクター / RPLA | Character LLM, RoleLLM, CharacterEval, … ChARM |
| 28–33 | 国内・NLP2025 | JSAI2024, NLP2025 P10 系 |
|| 34 | 感情表現 × 交渉 | EvoEmo (arXiv:2509.04310) — 進化的RLで感情ポリシーを最適化、感情なし/固定感情/EvoEmo の3条件比較 |
|| 35 | 感情 × ロールプレイ記憶 | Emotional RAG (arXiv:2410.23041) — 気分依存的記憶理論に基づく感情状態考慮の記憶検索フレームワーク |
|| 36 | 戦略 × 表現の統合 | DMNA (ACL 2025) — Dual-Mind: MCTS+DPOの直感モジュール × Reflexionの熟慮モジュールを統合 |

詳細は各 PDF ファイル名（arXiv ID / 会議名入り）を参照。

## メモの書き方

- **読解ノート**: Abstract 意訳・要点・研究への接続（Obsidian 用）
- **txt**: 翻訳途中・抜粋メモ（すべての PDF があるわけではない）

旧フォルダ `RPLA/`・`borrower_agent/` は README のみ残っている場合がある。実体はすべて本ディレクトリ配下に移動済み。
