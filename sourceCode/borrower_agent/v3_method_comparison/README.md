# V3: 既存話法比較 × 記事情報豊富度

逆さま不動産の借り手記事をもとに、既存の自己アピール話法を再現し、記事情報豊富度との組み合わせを比較する実験版。

## 条件

- 話法：`plain`, `prep`, `star`, `aida`
- 記事情報豊富度：`small`, `medium`, `large`
- 陶作家ケース：4 × 3 = 12条件

## 実行

```bash
python scripts/run_experiment.py \
  --cases case01_ceramic_atelier \
  --methods plain,prep,star,aida \
  --information-levels small,medium,large \
  --repetitions 3 \
  --order-seed 42
```

詳細は [設計書.md](設計書.md) を参照。

証拠在庫は記事レベルごとに初回だけ抽出され、`evidence_inventories/` に固定保存される。同じ在庫ID・ハッシュが全話法と全反復で使われる。

## 集計

```bash
python scripts/summarize_method_audits.py
python scripts/summarize_method_audits.py --output runs/method_audits.csv
```

人手評価項目は [eval/rubric.md](eval/rubric.md) を参照。
