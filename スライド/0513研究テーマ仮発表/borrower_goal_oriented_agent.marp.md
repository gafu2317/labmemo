---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section {
    font-family: "Hiragino Sans", "Yu Gothic", "Noto Sans JP", sans-serif;
    color: #111827;
    background: #ffffff;
    padding: 54px 64px;
  }
  h1 {
    color: #1d4ed8;
    font-size: 38px;
    line-height: 1.35;
  }
  h2 {
    color: #1d4ed8;
    font-size: 32px;
    border-bottom: 3px solid #bfdbfe;
    padding-bottom: 8px;
  }
  h3 {
    color: #1f2937;
    font-size: 24px;
  }
  p, li {
    font-size: 24px;
    line-height: 1.55;
  }
  ul {
    margin-top: 18px;
  }
  strong {
    color: #1d4ed8;
  }
  table {
    font-size: 21px;
  }
  th {
    background: #eff6ff;
    color: #1d4ed8;
  }
  .small {
    font-size: 18px;
    color: #4b5563;
  }
  .center {
    text-align: center;
  }
  .box {
    border: 2px solid #bfdbfe;
    border-radius: 8px;
    padding: 18px 22px;
    background: #f8fbff;
  }
  .flow {
    display: grid;
    grid-template-columns: 1fr 42px 1fr 42px 1fr;
    gap: 10px;
    align-items: center;
    margin-top: 28px;
  }
  .flow .node {
    border: 2px solid #93c5fd;
    border-radius: 8px;
    padding: 18px;
    background: #eff6ff;
    text-align: center;
    font-size: 22px;
    min-height: 78px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .arrow {
    text-align: center;
    color: #1d4ed8;
    font-size: 28px;
    font-weight: bold;
  }
---

# 逆さま不動産における<br>借り手AIエージェントの検討

<br>

先行研究調査と今後の方向性

<br>

<span class="small">発表者: 福富隆大　　日付: 2026年5月13日</span>

<!--
発表者ノート:
今日は、逆さま不動産における借り手AIエージェントという方向性について話します。
まだ研究テーマとして確定したものではなく、関連する先行研究を調べた上で、今の時点で面白そうだと思っている方針を共有する発表です。
-->

---

## 逆さま不動産とAIエージェント

従来の不動産では、物件を持っている側が情報を出し、  
借り手がその中から選ぶ形式が中心だった。

| 従来の不動産 | 逆さま不動産 |
|---|---|
| 物件情報を掲載する | 借り手の夢ややりたいことを掲載する |
| 借り手が物件を探す | 大家が借り手に関心を持つ |
| 条件から選ぶ | 想いや使い方からつながる |

<div class="box">
借り手の記事をもとに、本人の代わりに対話するAIを作れないか。
</div>

<!--
発表者ノート:
逆さま不動産は、空き家問題に対して、物件側からではなく借り手側から情報を出す仕組みです。
借り手が自分のやりたいことや夢を記事として掲載し、それに共感した大家さんとつながる、という形です。
ここで、借り手の記事情報を使って、本人の代わりに大家さんへアピールしたり質問したりするAIエージェントが考えられます。
-->


---

## 背景: 逆さま不動産で必要になる対話

逆さま不動産では、物件情報ではなく、  
借り手の「やりたいこと」や「夢」が先に公開される。

- 大家は、借り手の想いや使い方に関心を持つ
- 借り手は、自分のやりたいことなどを記事にする
- 借り手側から大家さんに質問する形をとる

<div class="box">
借り手の意図を正しく伝え、必要な情報を聞き出す対話AIが重要になる。
</div>

<!--
発表者ノート:
背景として、逆さま不動産では、通常の不動産のように物件条件だけを見て選ぶのではなく、借り手のやりたいことや夢が重要になります。
そのため、大家さんとのやり取りでは、借り手の意図を正しく伝えることと、物件が目的に合うかを確認することが必要になります。
-->


---

## やりたいことのイメージ

借り手の記事情報をもとに、AIが借り手として  
大家さんにアピールしたり、必要な質問をしたりする。

<div class="flow">
  <div class="node">借り手の記事<br><span class="small">夢・目的・背景</span></div>
  <div class="arrow">→</div>
  <div class="node">対話AI<br><span class="small">借り手として話す</span></div>
  <div class="arrow">→</div>
  <div class="node">大家さん<br><span class="small">アピール・質問</span></div>
</div>

### 考えたい要件

- 持っている情報と違うことを言わない
- 人間らしく自然に話す
- 使用目的に必要な情報を聞き出す

<!--
発表者ノート:
ここで考えているAIは、単に本人っぽい雑談をするAIではありません。
借り手の記事に書かれた情報に忠実でありながら、大家さんとの対話で必要な情報を取得することが目的です。
-->

---

## 先行研究1: persona研究の全体像

**Two Tales of Persona in LLMs**  
Tseng et al., EMNLP Findings 2024

| 分類 | persona の所在 | 目的 |
|---|---|---|
| LLM Role-Playing | AI側 | AIが与えられた役割として振る舞う |
| LLM Personalization | ユーザ側 | AIがユーザ情報に合わせて応答する |

今回の対話相手は大家さんなので
**借り手情報をpersonaとして与える role-playing** に近い。

<!--
発表者ノート:
この論文では、persona研究を2つに整理しています。
AI自身に役割を与える場合がRole-Playingで、ユーザ情報に合わせる場合がPersonalizationです。
今回のテーマでは、LLMが話す相手は大家さんです。そのため、大家さんに合わせるpersonalizationというより、借り手の記事情報をAI側のpersonaとして与え、借り手役として話すrole-playingに近いと考える方が正確です。
-->

---

## 先行研究2: RPLAの分類

**From Persona to Personalization: A Survey on RPLAs**  
Chen et al., TMLR 2024

| persona の種類 | 内容 | 今回との関係 |
|---|---|---|
| Demographic | 年齢・職業などの属性 | 直接の中心ではない |
| Character | 有名人・架空キャラクター | 深い再現は目的ではない |
| Individualized | 特定個人の履歴・好み | 借り手記事に近い |

借り手記事は、限られた情報から作る **Individualized Persona** と見なせる。

<!--
発表者ノート:
RPLAのサーベイではpersonaを3種類に分けています。
今回扱う借り手の記事は、キャラクター再現というより、特定の個人の目的や価値観に近いのでIndividualized Personaに近いです。
ただし、情報量が少ない点が課題になります。
-->

---

## 先行研究3: 評価の難しさ

RPLAでは「それらしく話せるか」だけでなく、  
評価そのものが難しいことが指摘されている。

| 研究 | 注目点 | 今回との関係 |
|---|---|---|
| TimeChara | その時点で知らないことを言う問題 | 根拠にない発話の問題 |
| PersonaEval | LLM評価器は人間のように評価できるか | 評価方法の妥当性 |
| PingPong | 多ターン対話で評価する | 大家との対話に近い |

<div class="box">
本研究でも「本人らしさ」だけでなく、根拠忠実性と情報獲得を評価する必要がある。
</div>

<!--
発表者ノート:
評価系の研究を見ると、RPLAでは単に自然に話せるかだけでは不十分です。
根拠にない情報を言っていないか、多ターンで目的を達成できるか、人間やLLMがそれをどう評価するかが課題になります。
-->

---

## 先行研究からわかったこと

調査から、今回のテーマに関係しそうな点は3つある。

1. **personaを与えるだけでは不十分**  
   一貫性や根拠忠実性が崩れる可能性がある

2. **情報が少ない個人の再現は難しい**  
   記事にないことを補いすぎる危険がある

3. **評価軸を分ける必要がある**  
   本人らしさ、自然さ、目的達成は別の観点

<!--
発表者ノート:
先行研究からわかったことを、今回の研究に引きつけて整理するとこの3つです。
特に重要なのは、借り手記事をそのままプロンプトに入れるだけでは、根拠にない発話や目的から外れた会話が起こりうる点です。
-->

---

## 研究の方向性

記事全文をそのまま入れるだけでなく、  
対話に必要な情報として構造化して使うことを考えている。

<div class="flow">
  <div class="node">借り手の記事</div>
  <div class="arrow">→</div>
  <div class="node">目的・希望・制約<br>質問項目を抽出</div>
  <div class="arrow">→</div>
  <div class="node">目的志向<br>対話エージェント</div>
</div>

<br>

| 構造化する情報 | 例 |
|---|---|
| 目的 | 何を実現したいか |
| 希望 | どんな場所・条件がよいか |
| 制約 | 言ってよいこと・言えないこと |
| 質問項目 | 大家に確認すべきこと |

<!--
発表者ノート:
研究の方向性としては、記事をそのままcontextに入れるだけでなく、目的、希望、制約、質問項目に分けて構造化することを考えています。
これにより、根拠に基づく発話と、目的達成のための質問を両立できないかと考えています。
-->

---

## 評価の方向性

仮にエージェントを作る場合、以下の観点で評価したい。

| 評価軸 | 見ること |
|---|---|
| Faithfulness | 記事にないこと・矛盾することを言っていないか |
| Persona Consistency | 借り手の目的や価値観と合っているか |
| Task Success | 必要な物件情報を聞き出せたか |
| Naturalness | 大家との会話として自然か |

比較対象として、まずは **記事をそのままpromptに入れたLLM** を考える。

<!--
発表者ノート:
評価では、本人らしさだけを見るのではなく、記事との矛盾がないか、必要な情報を聞けたか、自然に対話できたかを分けて見る必要があります。
比較対象としては、借り手記事をそのままプロンプトに入れたLLMをベースラインにするのがわかりやすいと考えています。
-->

---

## まとめ

- RPLA研究は、人物像に基づく対話AIを考える上で参考になる
- 借り手記事を使う場合、深いキャラクター再現より **根拠忠実性** が重要
- 今後は、記事情報の構造化と評価方法を検討したい

<div class="box">
借り手の記事情報に忠実で、自然に大家と対話し、必要な情報を集めるAIエージェントを方向性として考える。
</div>

<!--
発表者ノート:
まとめです。
今回の研究構想では、RPLAをそのままキャラクター再現として使うのではなく、借り手情報に基づく目的志向対話として考えます。
今後は、記事情報をどう構造化するか、そして発話をどう評価するかを詰めていきたいです。
-->
