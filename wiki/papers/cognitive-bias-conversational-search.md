# Cognitive Bias in Spoken Conversational Search

> タグ: #cognitive-bias #speech #dialogue #hci
> 著者: Kaixin Ji et al.
> 年: 2024
> ソース: arXiv
> raw: [[論文/論文データ/Towards Detecting and Mitigating Cognitive Bias in Spoken Conversational Search]]

## 一行要約

音声会話検索における認知バイアス（確証バイアス等）を脳波・皮膚電位などの生理データと行動データで検出し、軽減策を提案。

## 検出手法

| センサー | 検出シグナル |
|---------|------------|
| EEG（脳波） | 前頭葉活動 — 認知負荷の指標 |
| EDA（皮膚電位） | ストレス・覚醒レベル |
| 音声分析 | 発話内容・記憶テスト |

**発見**: 難しいトピックで前頭葉活動増加・ストレス上昇

## 軽減策

1. **話速調整** — 情報提示速度を下げる
2. **明示的な質問** — 反証情報を提示する質問（最も効果的）
3. ナッジ手法 — 偏りに気づかせる介入

## 課題

- 生理信号の個人差・解釈困難
- リアルタイム介入の倫理問題（認知の自由の侵害リスク）
- センサー信頼性は長時間実験でないと低い

## 我々の研究への関連度

**低**（方法論的に距離がある）

参考: 議論バイアスを軽減する介入設計の将来課題として。

## バックリンク

- [[concepts/cognitive-bias-in-llm]]
