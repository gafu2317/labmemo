# 借り手AIエージェント実験システム

逆さま不動産における借り手の熱意を代弁し、大家に「この人に貸したい」と感じてもらうきっかけを作る対話エージェントの実験コード。条件交渉や契約の詳細は対象外とする。
バージョンごとにコード・プロンプト・ログを分離し、入力データ（ケース・物件）と評価軸だけを共有する。

## バージョン対応表

| 版 | 仮説 | 実験での位置づけ |
|---|---|---|
| `v1_fixed_emotion` | 感情表現指示の有無（phase固定の感情レシピ） | FIT2026 時点の手法 |
| `v2_adaptive_planner` | 記事中の個人的価値・既遂行行動・継続姿勢など、検証済みの熱意証拠を大家の対話行為に応じて選択 | 次実験。Baseline=熱意表現の特別指示なし、Proposed=根拠に基づく熱意伝達。大家はYAMLで行為を固定し文面のみLLM生成 |

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
    ├── scenarios/             # v2専用の大家対話行為と物件設計メモ
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
