---
marp: true
theme: default
paginate: true
size: 16:9
footer: "借り手AIエージェント｜進捗共有"
style: |
  section {
    font-family: "Hiragino Sans", "Yu Gothic", "Noto Sans JP", sans-serif;
    color: #172033;
    background: #ffffff;
    padding: 48px 62px 52px;
  }
  section::after {
    color: #6b7280;
    font-size: 13px;
  }
  footer {
    color: #94a3b8;
    font-size: 12px;
  }
  h1 {
    color: #153b6b;
    font-size: 42px;
    line-height: 1.28;
    letter-spacing: .01em;
  }
  h2 {
    color: #153b6b;
    font-size: 31px;
    border-bottom: 3px solid #d8e8f8;
    padding-bottom: 9px;
    margin-bottom: 26px;
  }
  h3 {
    color: #153b6b;
    font-size: 21px;
    margin: 0 0 10px;
  }
  p, li {
    font-size: 21px;
    line-height: 1.5;
  }
  strong {
    color: #0f6a63;
  }
  .lead {
    font-size: 27px;
    line-height: 1.55;
    color: #334155;
  }
  .small {
    font-size: 15px;
    line-height: 1.45;
    color: #64748b;
  }
  .tag {
    display: inline-block;
    padding: 5px 11px;
    border-radius: 999px;
    background: #e8f3f1;
    color: #0f6a63;
    font-size: 15px;
    font-weight: 700;
  }
  .box {
    border: 1.5px solid #bdd4eb;
    border-radius: 12px;
    padding: 18px 22px;
    background: #f7fbff;
  }
  .accent {
    border-left: 7px solid #1b8a7d;
    border-radius: 8px;
    padding: 14px 20px;
    background: #f0faf8;
  }
  .warning {
    border-left: 7px solid #d98928;
    border-radius: 8px;
    padding: 14px 20px;
    background: #fff8ec;
  }
  .cols {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
  }
  .cols-40 {
    display: grid;
    grid-template-columns: .78fr 1.22fr;
    gap: 28px;
  }
  .card {
    border: 1.5px solid #d8e2ec;
    border-radius: 12px;
    padding: 18px 20px;
    background: #ffffff;
  }
  .card p, .card li {
    font-size: 18px;
    line-height: 1.47;
  }
  .card.good {
    border-top: 6px solid #1b8a7d;
  }
  .card.base {
    border-top: 6px solid #7b8ca4;
  }
  .quote {
    font-size: 18px;
    line-height: 1.55;
    color: #26364b;
    margin: 4px 0 0;
  }
  .landlord {
    border-radius: 10px;
    padding: 12px 17px;
    background: #edf2f7;
    color: #344256;
    font-size: 18px;
    margin-bottom: 18px;
  }
  mark {
    background: #dff4ef;
    color: #0d5a54;
    padding: 0 .12em;
  }
  .timeline {
    display: grid;
    grid-template-columns: 1fr 42px 1fr 42px 1.15fr;
    gap: 8px;
    align-items: stretch;
    margin-top: 28px;
  }
  .step {
    border: 1.5px solid #cad7e5;
    border-radius: 12px;
    padding: 18px;
    background: #f8fafc;
  }
  .step.current {
    border: 3px solid #1b8a7d;
    background: #f0faf8;
  }
  .arrow {
    align-self: center;
    text-align: center;
    color: #6f8eae;
    font-size: 29px;
    font-weight: 700;
  }
  .flow {
    display: grid;
    grid-template-columns: 1fr 38px 1fr 38px 1fr 38px 1fr;
    gap: 7px;
    align-items: center;
    margin-top: 24px;
  }
  .node {
    min-height: 112px;
    border: 1.5px solid #bcd1e6;
    border-radius: 12px;
    padding: 16px 13px;
    background: #f7fbff;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    line-height: 1.35;
  }
  .node.key {
    border: 3px solid #1b8a7d;
    background: #f0faf8;
  }
  .kpi {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-top: 24px;
  }
  .kpi > div {
    border-radius: 11px;
    padding: 18px 14px;
    background: #f3f7fb;
    text-align: center;
    font-size: 17px;
    line-height: 1.35;
  }
  .num {
    display: inline-flex;
    width: 31px;
    height: 31px;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: #153b6b;
    color: #fff;
    font-weight: 700;
    margin-right: 10px;
  }
  table {
    width: 100%;
    font-size: 17px;
  }
  th {
    background: #eaf3fb;
    color: #153b6b;
  }
  td, th {
    padding: 9px 12px;
  }
  section.cover-slide {
    background:
      linear-gradient(120deg, rgba(255,255,255,.97) 0%, rgba(255,255,255,.94) 60%, rgba(229,244,241,.96) 100%);
  }
  section.cover-slide h1 {
    margin-top: 82px;
    font-size: 48px;
  }
---

<!-- _class: cover-slide -->
<!-- _paginate: false -->
<!-- _footer: "" -->

# 借り手AIエージェントの現在地

<p class="lead">対話の試作状況と、<br>現場の視点で相談したいこと</p>

<br>

<span class="tag">逆さま不動産 × 対話AI</span>

<p class="small" style="margin-top: 38px;">福富 隆大　｜　2026年7月</p>

<!--
発表者ノート：
今日は、以前お話しした構想そのものの説明ではなく、
現在どのような会話が生成できていて、どこに課題があるのかをご共有します。
そのうえで、実際の大家さんとのやり取りとして違和感がないか、
現場の視点からご意見をいただきたいと考えています。
-->

---

## 今日お話ししたいこと

<div class="cols-40">
  <div class="box">
    <h3>現在地</h3>
    <p><strong>借り手の記事から、大家さんとの会話を生成する試作</strong>まで進んでいます。</p>
    <p class="small">本番サービスへの導入ではなく、まずは研究用の対話実験です。</p>
  </div>
  <div>
    <p><span class="num">1</span>研究の中で、考え方がどう変わったか</p>
    <p><span class="num">2</span>今、実際にどんな会話が出ているか</p>
    <p><span class="num">3</span>現場感とズレていないか相談したい</p>
  </div>
</div>

<div class="accent" style="margin-top: 26px;">
このAIの役割は、条件交渉ではなく、<strong>大家さんが「本人と話してみたい」と思うきっかけをつくること</strong>です。
</div>

<!--
発表者ノート：
現在は、借り手の記事と物件情報を与えて、4往復程度の会話を生成できます。
ただし、契約や条件交渉をAIに任せる想定ではありません。
本人同士が会う前のきっかけ作りに範囲を絞っています。
-->

---

## これまでの試作と、現在の方式

<div class="timeline">
  <div class="step">
    <span class="tag">v1</span>
    <h3 style="margin-top: 13px;">固定感情表現版</h3>
    <p class="small">対話段階ごとに、感情表現の方針を固定して生成</p>
  </div>
  <div class="arrow">→</div>
  <div class="step">
    <span class="tag">v2 初期</span>
    <h3 style="margin-top: 13px;">動的発話構成版</h3>
    <p class="small">大家さんの発話や対話段階に応じて、発話の構成を選択</p>
  </div>
  <div class="arrow">→</div>
  <div class="step current">
    <span class="tag">現行 v2</span>
    <h3 style="margin-top: 13px;">熱意証拠選択版</h3>
    <p class="small">記事から抽出・原文確認した証拠を、対話状況に応じて選択</p>
  </div>
</div>

<div class="accent" style="margin-top: 28px;">
現在は、<strong>記事のどの情報を、どの場面で伝えるか</strong>を主な比較対象にしています。
</div>

<!--
発表者ノート：
これまでに3段階の試作を行っています。
v1では対話段階ごとに感情表現の方針を固定していました。
v2初期では、大家さんの発話に応じて発話構成を変える方式を試しました。
現行版では、記事から原文確認できた情報を候補として持ち、
どの情報をどの場面で提示するかを選ぶ方式にしています。
-->

---

## 現在の試作：記事から「今伝える根拠」を選ぶ

<div class="flow">
  <div class="node">
    <strong>借り手の記事</strong>
    <span class="small">夢・背景・活動</span>
  </div>
  <div class="arrow">→</div>
  <div class="node key">
    <strong>熱意の根拠を抽出</strong>
    <span class="small">原点／行動／継続</span>
  </div>
  <div class="arrow">→</div>
  <div class="node key">
    <strong>会話に合わせて選択</strong>
    <span class="small">質問・懸念・段階</span>
  </div>
  <div class="arrow">→</div>
  <div class="node">
    <strong>大家さんへ伝える</strong>
    <span class="small">記事外の創作を確認</span>
  </div>
</div>

<div class="cols" style="margin-top: 28px;">
  <div class="card base">
    <h3>通常版</h3>
    <p>大家さんの質問に、記事にある事実で<strong>中立的に回答</strong></p>
  </div>
  <div class="card good">
    <h3>提案版</h3>
    <p>回答に加え、状況に合う<strong>未使用の熱意の根拠を1つ</strong>伝える</p>
  </div>
</div>

<p class="small">共通条件：同じ借り手記事、同じ物件情報、同じ大家側の質問・懸念、同じ事実確認処理</p>

<!--
発表者ノート：
借り手の記事から、本人にとっての意味、すでに行ったこと、
今後も続ける姿勢などを候補として取り出します。
大家さんからの質問や懸念に応じて、その時点で伝える根拠を1つ選びます。
比較のために、特別な熱意の指示をしない通常版も用意しています。
-->

---

## 会話ログ例 1/3：制作方法を尋ねられた場面

<div class="landlord"><strong>大家：</strong>ガス窯を含め、この物件でどのように作品を制作したいですか？</div>

<div class="cols">
  <div class="card base">
    <h3>通常版</h3>
    <p class="quote">ガス窯でいろいろな焚き方を試しながら、焼き締めの作品を制作していきたいです。［中略］試行錯誤しながら自分らしい作品を作ることが好きなので、落ち着いて制作できる環境が必要です。</p>
  </div>
  <div class="card good">
    <h3>提案版</h3>
    <p class="quote">ガス窯は、焼き締めという釉薬を使わない制作方法で、土の質感や色味を生かすのに適しています。［中略］<mark>技術向上と伝統技術継承のため、常滑市と四日市市で急須作りを教わり、制作もしています。</mark></p>
  </div>
</div>

<div class="accent" style="margin-top: 21px;">
提案版では、用途説明に加えて、<strong>現在行っている学習・制作活動</strong>が選ばれています。
</div>

<p class="small">出典：陶作家のアトリエ兼住居ケースで生成した会話ログ（2026年7月19日）</p>

<!--
発表者ノート：
これは現在のログの一例です。
通常版も用途にはきちんと答えています。
提案版では、それに加えて、本人がすでに常滑と四日市で学び、
制作しているという記事上の事実を選んでいます。
こうした違いが、大家さんの「本人と話したい」という判断につながるかを確かめたいです。
-->

---

## 会話ログ例 2/3：最初に用途を尋ねられた場面

<div class="landlord"><strong>大家：</strong>どのようなご利用をお考えか、聞かせていただけますか？</div>

<div class="cols">
  <div class="card base">
    <h3>通常版</h3>
    <p class="quote">陶作家の藤井ノゾミと申します。花器を中心に制作しており、最近は常滑市と四日市市で急須作りも学んでいます。</p>
    <p class="quote">アトリエ兼住居として使える一軒家を探しており、ガス窯が置ける小屋やガレージ、梱包材の保管と梱包作業ができるスペースも欲しいと考えています。</p>
  </div>
  <div class="card good">
    <h3>提案版</h3>
    <p class="quote">陶作家として、花器を中心に制作しており、最近は常滑市と四日市市で急須作りも学んでいます。アトリエ兼住居として、ガス窯が置ける環境で、落ち着いて作品制作を続けたいと考えています。</p>
    <p class="quote"><mark>海外からのご注文も少しずついただけるようになってきた</mark>ので、梱包材の保管や梱包作業のスペースも必要になってきました。</p>
  </div>
</div>

<div class="accent" style="margin-top: 20px;">
見てほしい点：最初の発話で、<strong>用途・必要条件・現在の活動状況をどこまで伝えると自然か</strong>。
</div>

<p class="small">出典：同一ケース・同一大家シナリオの会話ログ（2026年7月19日 11:11／11:12生成）</p>

<!--
発表者ノート：
こちらは最初に用途を尋ねられた場面です。
通常版は必要な条件を一度に整理して答えています。
提案版は、海外からの注文が増えているという現在の活動状況を、
梱包スペースが必要な理由として加えています。
最初の発話として、この情報量や順番が自然かを見ていただきたいです。
-->

---

## 会話ログ例 3/3：保管・梱包を尋ねられた場面

<div class="landlord"><strong>大家：</strong>離れをアトリエとして活用できますが、梱包材の保管と梱包作業は、別のスペースが必要になりますか？</div>

<div class="cols">
  <div class="card base">
    <h3>通常版</h3>
    <p class="quote">離れ（25㎡）でアトリエ兼制作スペースとして使用できるのであれば、<strong>梱包材の保管と梱包作業は別のスペースがあると効率的</strong>だと考えています。</p>
  </div>
  <div class="card good">
    <h3>提案版</h3>
    <p class="quote">離れでアトリエとして活用できるのであれば、梱包材の保管と梱包作業は居住棟で行いたいと考えています。</p>
    <p class="quote"><mark>海外への発送が増えてきた</mark>ので、作品制作とは別に梱包作業のスペースがあると、制作に集中しやすくなると考えています。</p>
  </div>
</div>

<div class="accent" style="margin-top: 22px;">
見てほしい点：質問への回答に加える情報が、<strong>必要性の理解につながるか／説明過多に感じるか</strong>。
</div>

<p class="small">出典：同一ケース・同一大家シナリオの会話ログ（2026年7月19日 11:11／11:12生成）</p>

<!--
発表者ノート：
こちらは具体的なスペースについて尋ねられた場面です。
提案版では、海外発送が増えているという背景をもう一度添えています。
必要性の理解にはつながる可能性がありますが、
すでに話した内容の繰り返しや、説明過多に感じないかも確認したい点です。
-->

---

## 現在のログで見えている応答上の課題

<div class="landlord"><strong>大家：</strong>周辺が住宅街なので、ガス窯の音や煙が近隣に影響しないか心配しています。</div>

<div class="card good">
  <h3>現在の提案版ログ</h3>
  <p class="quote">ご懸念ありがとうございます。<mark>そうした環境での制作は難しいということですね。</mark></p>
  <p class="quote">ただ、私が今求めているのは、落ち着いて作品制作を続けられる環境です。［中略］地域が可能性や希望のある場所であることをアピールし、協力してくださった方々に恩返ししたいと思っています。</p>
</div>

<div class="warning" style="margin-top: 20px;">
記事中の価値観は提示できているが、<strong>煙や音への配慮に直接答えられていない</strong>。大家さんの懸念を早合点している点も不自然。
</div>

<p class="small">現在の調整点：①質問・懸念への回答を最優先　②熱意を入れない方がよい場面を判断　③発話を短く保つ</p>

<!--
発表者ノート：
一方で、うまくいっていない例もあります。
このログでは、地域への恩返しという本人の価値観は出せていますが、
大家さんが知りたい煙や音への対応には答えられていません。
また、「制作は難しいということですね」と早合点しています。
記事中の情報を提示することと、相手の懸念に直接答えることのバランスが現在の課題です。
-->

---

## 次に確かめること

<p class="lead" style="margin-bottom: 20px;">同じケースの「通常版」と「提案版」を、条件名を隠して比較します。</p>

<div class="kpi">
  <div><strong>想い・熱意</strong><br><span class="small">活動の重要性や継続意思が伝わるか</span></div>
  <div><strong>会ってみたいか</strong><br><span class="small">本人から続きを聞きたいか</span></div>
  <div><strong>本人らしさ</strong><br><span class="small">その人固有の語りに感じるか</span></div>
  <div><strong>誠実さ・自然さ</strong><br><span class="small">創作がなく、会話として自然か</span></div>
</div>

<div class="timeline" style="grid-template-columns: 1fr 42px 1fr 42px 1fr; margin-top: 30px;">
  <div class="step current"><h3>現在</h3><p class="small">陶作家ケースで試作・ログ生成</p></div>
  <div class="arrow">→</div>
  <div class="step"><h3>次</h3><p class="small">会話品質を調整し、複数ケースを生成</p></div>
  <div class="arrow">→</div>
  <div class="step"><h3>評価</h3><p class="small">条件を隠した人手比較</p></div>
</div>

<!--
発表者ノート：
次は、同じ借り手・同じ大家側の流れで生成した2つの会話を、
どちらが提案版か分からない状態で比較します。
主に見たいのは、想いが伝わるか、本人に会ってみたいかです。
同時に、本人らしさ、記事にない創作がないこと、
会話の自然さも確認します。
-->

---

## ぜひ伺いたいこと

<div class="cols">
  <div>
    <p><span class="num">1</span><strong>最初の会話で、大家さんは何を気にするか</strong></p>
    <p><span class="num">2</span><strong>どんな話が「本人に会いたい」につながるか</strong></p>
    <p><span class="num">3</span><strong>今回の会話例に、現実とのズレはないか</strong></p>
  </div>
  <div class="box">
    <h3>あわせて相談したいこと</h3>
    <ul>
      <li>AIが拾うとよい記事情報</li>
      <li>AIに言わせない方がよい内容</li>
      <li>検証するなら、どの場面・対象が現実的か</li>
    </ul>
  </div>
</div>

<div class="accent" style="margin-top: 25px;">
研究上の「熱意」ではなく、現場で<strong>信頼や次の対話につながる材料</strong>になっているかを確かめたいです。
</div>

<!--
発表者ノート：
今日一番伺いたいのは、この3点です。
AIの技術的な評価だけではなく、実際の大家さんが何を気にするのか、
何を聞くと本人に会いたくなるのかを教えていただきたいです。
また、将来的に検証するとすれば、どの場面から始めるのが現実的かも相談できればと思います。
-->

---

<!-- _footer: "補足｜借り手AIエージェント" -->

## 補足：実験で固定しているもの／変えているもの

| | 内容 |
|---|---|
| **変えるもの** | 記事中の熱意の根拠を、意図的に選んで伝えるか |
| 固定するもの | 借り手の記事、物件情報、大家の質問・懸念の順序 |
| 共通の確認 | 記事にない事実を話していないか |
| 対話の長さ | 大家の挨拶＋借り手4発話程度 |
| 対象外 | 条件交渉、契約、最終的な貸与判断 |

<div class="box" style="margin-top: 26px;">
<strong>現在のケース：</strong>陶作家が、ガス窯を置けるアトリエ兼住居を探す場面<br>
<span class="small">物件側の主な懸念：住宅街における窯の音・煙、煙突工事、作業・保管スペース</span>
</div>

<p class="small">研究用実装：v2.2「根拠に基づく熱意伝達＋制御大家シナリオ」</p>

<!--
発表者ノート：
ここからは質問があった場合の補足です。
比較では、借り手の記事や物件情報、大家さんが何を聞くかを固定し、
熱意の根拠を意図的に選ぶかどうかだけを主な違いにしています。
-->
