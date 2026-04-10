# Topic Shift Detection for Mixed Initiative Response

> タグ: #topic-shift #dialogue #classification #transformer
> 著者: Rachna Konigari et al.
> 会議: SIGDIAL 2021
> URL: https://aclanthology.org/2021.sigdial-1.29/
> raw: [[論文/論文データ/Topic_Shift_Detection_with_Classification]]

## 一行要約

XLNetに対話履歴を入力としてfine-tuningし、話題転換を「維持/転換/一時脱線」に分類するモデルを提案。従来のコサイン類似度ベースをF1スコアで大幅に上回った。

## 提案手法の核心

```
入力: [現在の発言] + [直前N発言の対話履歴]
      ↓
   XLNet (fine-tuned)
      ↓
出力: Maintain / Shift / Digress
```

**ポイント**: 対話履歴を入力に含めることが精度向上の鍵

## 従来手法との比較

| 手法 | F1スコア |
|------|---------|
| コサイン類似度ベース | 低 |
| **XLNetファインチューニング（提案）** | **大幅に高い** |

## 課題

- ラベル付き対話データの作成コストが高い
- 事前定義カテゴリ以外の転換パターンは検出不可

## 我々の研究への示唆

**仮説2の具体的な実装指針:**
1. 「ベクトル類似度でシンプルに実装」を基線として使う
2. 将来的にXLNetなど分類モデルへ発展させる
3. **「直前の対話履歴を入力に含める」** は基線実装でも取り入れるべきテクニック
4. 評価は2値でなく3カテゴリで設計するとより豊富な考察が可能

## バックリンク

- [[concepts/topic-shift-detection]]
- [[concepts/discussion-visualization]]
