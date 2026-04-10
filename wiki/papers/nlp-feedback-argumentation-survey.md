# Teach Me How to Argue: NLP Feedback Systems for Argumentation

> タグ: #argument-mining #survey #feedback #education #nlp
> 著者: Guerraoui et al.
> 年: 2023
> ソース: ArgMining 2023 (ACL Workshop), pages 19–34
> raw: [[raw/papers/teach-me-how-to-argue-a-survey-on-nlp-feedback-systems-in-ar.pdf]]

## 一行要約

議論教育向けNLPフィードバックシステムを4次元（豊富さ・可視化・対話性・個別化）で分類したサーベイ。

## 4次元フレームワーク

| 次元 | 問い | 内容 |
|------|------|------|
| **Richness（豊富さ）** | What / Why | フィードバックの内容・粒度 |
| **Visualization（可視化）** | How | 議論構造の見せ方 |
| **Interactivity（対話性）** | Who | 人間vsシステムの役割分担 |
| **Personalization（個別化）** | To whom | 学習者プロファイルへの適応 |

## 対象とする議論理論

- **Toulminモデル**: クレーム・データ・ワラント
- **RST（修辞構造理論）**: 文間の修辞関係
- **CABLE（協調議論）**: 議論の社会的側面
- **ソクラテス的質問法**: 探索的対話

## 主要知見

- 既存システムの多くはRichnessに偏り、PersonalizationとInteractivityが弱い
- 可視化（グラフ・マップ）は理解促進に有効だが実装が複雑
- **将来の方向性**: 個別化されたチャットボット型フィードバック

## 我々の研究への示唆

LLMを用いた議論支援システムの設計において、このフレームワークは有用な評価軸となる。特に**Interactivity（誰が議論を主導するか）**と**Personalization（各参加者への適応）**は、我々のシステム設計における核心的課題。LLMによる個別化フィードバックの実現可能性を示す研究方向として参照できる。

## バックリンク

- [[concepts/argument-mining]]
- [[concepts/llm-prompting-strategies]]
