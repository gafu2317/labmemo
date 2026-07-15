# 借り手AIエージェント実験システム

逆さま不動産における借り手の熱意を代弁する交渉対話エージェントの実験コード。
バージョンごとにコード・プロンプト・ログを分離し、入力データ（ケース・物件）と評価軸だけを共有する。

## バージョン対応表

| 版 | 仮説 | 実験での位置づけ |
|---|---|---|
| `v1_fixed_emotion` | 感情表現指示の有無（phase固定の感情レシピ） | FIT2026 時点の手法 |
| `v2_adaptive_planner` | 面接・プレゼン由来の修辞ムーブを状況に応じて選択 | 次実験。Baseline=v1感情レシピ、Proposed=6ムーブ |

## ディレクトリ構成

```
borrower_agent/
├── README.md
├── shared/                     # バージョン共通
│   ├── data/                   # cases / eval_cases / properties
│   └── eval/                   # rubric など評価資料
├── v1_fixed_emotion/           # 固定感情表現版
│   ├── src/
│   ├── prompts/
│   ├── scripts/
│   ├── gpts/                   # FIT 用 Custom GPTs 資産
│   ├── runs/
│   └── 設計書.md
└── v2_adaptive_planner/        # 動的発話構成版
    ├── src/
    ├── prompts/
    ├── scripts/
    ├── runs/
    └── 設計書.md
```

## 実行方法

各バージョンのディレクトリで実行する。

```bash
cd v1_fixed_emotion
python scripts/run_experiment.py --all-cases --conditions baseline,proposed

cd ../v2_adaptive_planner
python scripts/run_experiment.py --all-cases --conditions baseline,proposed
```

ケース・物件は `../shared/data/` を参照する。ログは各版の `runs/` に保存される。

## 環境変数

各版に `.env`（または `.env.example` をコピー）を置く。

```
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-haiku-4-5-20251001
```
