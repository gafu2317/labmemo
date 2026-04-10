# labmemo — LLM知識ベース

研究テーマ「LLMを用いた議論支援システム」のための個人知識ベース。
rawデータをLLMがwikiにコンパイルし、Obsidianで閲覧・管理する。

---

## ディレクトリ構成

```
labmemo/
├── raw/                    ソースドキュメント（手動で追加）
│   ├── papers/             論文PDF・Webクリップ
│   └── articles/           Web記事のMarkdown
│
├── wiki/                   LLMがコンパイルしたwiki（自動管理）
│   ├── index.md            マスターインデックス
│   ├── concepts/           概念記事
│   └── papers/             論文記事（バックリンク・研究示唆付き）
│
├── queries/                Q&Aの出力が蓄積される
├── scripts/search.py       検索エンジン（唯一のスクリプト）
├── 論文/                   既存の論文メモ（rawとして参照）
├── スライド/               発表スライド
└── 研究方針.md             研究テーマの概要
```

---

## 使い方

コンパイル・Q&A・ヘルスチェックはすべて **Claude Codeに直接頼む**。

| 操作 | Claude Codeへの指示例 |
|------|----------------------|
| 新論文をwikiに追加 | 「`raw/papers/xxx.md` をwiki記事にして」 |
| Q&A | 「wikiを参照して〇〇について教えて」 |
| ヘルスチェック | 「wikiの壊れたリンクや孤立記事を探して」 |
| スライド生成 | 「〇〇についてMarp形式のスライドを作って」 |

---

## search.py — 検索エンジン

LLMに依存しない純粋なキーワード検索。Claude Codeが参照ファイルを探すときにも使う。

```bash
python scripts/search.py "クエリ"
python scripts/search.py "topic shift" --top 10
python scripts/search.py "仮説1" --dir wiki
```

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| `--top N` | 表示件数 | 5 |
| `--dir` | 検索対象（`wiki` / `raw` / `all`） | `all` |

---

## ワークフロー

### 新しい論文・記事を追加するとき

```bash
# キーワードでサーベイ論文を検索（◆=サーベイ, ★=PDF入手可）
python scripts/fetch_paper.py --search "argument mining" --survey

# キーワードで論文を検索（上位20件）
python scripts/fetch_paper.py --search "topic shift detection"

# URLから論文を取得し、引用論文も一覧表示（芋蔓式収集）
python scripts/fetch_paper.py https://arxiv.org/abs/2506.16383
```

- 番号を選ぶとPDFを `raw/papers/` にダウンロード（`1,3,5` / `1-10` / `all`）
- ダウンロード後: Claude Codeに「`raw/papers/` の新しいPDFをwiki記事にして、`wiki/index.md` も更新して」と頼む
- wiki記事になった論文のURLで再度実行 → 芋蔓式に収集が広がる

### 調べ物・Q&Aをするとき

Claude Codeに質問するだけ。出力を `queries/` に保存するよう指示すると知識が蓄積される。

### wikiを整理するとき

「wikiのヘルスチェックをして、結果を `queries/lint_日付.md` に保存して」とClaude Codeに頼む。

---

## wikiの記事フォーマット

```markdown
# 記事タイトル

> タグ: #タグ1 #タグ2
> 著者: ...（論文記事の場合）
> raw: [[rawファイルへのリンク]]

## 一行要約

## [内容セクション]

## 我々の研究への示唆

## バックリンク
- [[concepts/関連概念]]
```

---

## 注意

- `wiki/` 以下はLLMが管理する。手動編集は最小限に。
- `raw/` と `論文/論文データ/` は元データとして保持し、削除しない。
- `queries/` の出力は随時wikiに「ファイル」して知識を積み重ねる。
