# MindScope: Cognitive Biases in LLMs via Multi-Agent Systems

> タグ: #cognitive-bias #multi-agent #llm #evaluation
> 著者: 謝振涛、趙加宝 et al.
> 年: 2024
> ソース: arXiv
> raw: [[論文/論文データ/MindScope Exploring cognitive biases in LLMs through Multi-Agent Systems]]

## 一行要約

72種の認知バイアスを調べるマルチエージェントシステム（MindScope）で12モデルを評価し、GPT-4単体より検出精度35%向上。

## システム構成（RuleGenフレームワーク）

| モジュール | 役割 |
|-----------|------|
| 記憶 (Memory) | 対話履歴の保持 |
| 計画 (Planning) | シナリオ構築の設計 |
| 反省 (Reflection) | 自己評価・二重チェック |
| 行動 (Action) | 実際の発言生成 |

エージェント役割: **調査対象 / 協力者 / 司会者**

## 主要発見

- モデルサイズ大 → バイアス減少（Llama2-7b〜70bで確認）
- Fine-tuning → バイアス増加のリスクあり（Vicunaシリーズ）
- 対話シナリオで見えるバイアス（サンクコスト誤謬・計画誤謬）は静的テストでは見えない
- 全モデルでIKEA効果の検出性能が低い

## 検証精度

- GPT-4評価者 vs 人間評価者: Kappa=0.72、精度88%

## 我々の研究への関連度

**低〜中**（背景知識として有用）

議論支援システムへの直接的な応用は限定的だが：
- LLMが議論分析時に確証バイアスをかける可能性を認識しておく
- マルチエージェントアーキテクチャは将来の拡張候補

## バックリンク

- [[concepts/cognitive-bias-in-llm]]
