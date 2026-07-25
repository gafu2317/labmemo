const fs = require("fs");
const path = require("path");
const { marked } = require("marked");
const { chromium } = require("playwright");

const sourcePath = path.resolve("借り手AIエージェント進捗共有.marp.md");
const htmlPath = path.resolve("借り手AIエージェント進捗共有.preview.html");
const pdfPath = path.resolve("借り手AIエージェント進捗共有.pdf");

const source = fs.readFileSync(sourcePath, "utf8");
const frontmatterMatch = source.match(/^---\n([\s\S]*?)\n---\n/);
if (!frontmatterMatch) throw new Error("Marp front matter was not found.");

const frontmatter = frontmatterMatch[1];
const styleMatch = frontmatter.match(/style: \|\n([\s\S]*)$/);
const deckStyle = styleMatch
  ? styleMatch[1].replace(/^  /gm, "")
  : "";
const body = source.slice(frontmatterMatch[0].length);
const slides = body.split(/\n---\n/);

const renderedSlides = slides.map((slide, index) => {
  const classMatch = slide.match(/<!--\s*_class:\s*([^\s]+)\s*-->/);
  const footerHidden = /<!--\s*_footer:\s*""\s*-->/.test(slide);
  const html = marked.parse(slide);
  const className = classMatch ? classMatch[1] : "";
  const pageNumber = footerHidden ? "" : `<span class="page-number">${index + 1}</span>`;
  const footer = footerHidden ? "" : "<footer>借り手AIエージェント｜進捗共有</footer>";
  return `<section class="${className}">${html}${footer}${pageNumber}</section>`;
}).join("\n");

const documentHtml = `<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<style>
  @page { size: 13.333333in 7.5in; margin: 0; }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; background: #d9dee5; }
  section {
    width: 1280px;
    height: 720px;
    overflow: hidden;
    position: relative;
    break-after: page;
    page-break-after: always;
  }
  section:last-child { break-after: auto; page-break-after: auto; }
  footer {
    position: absolute;
    left: 62px;
    bottom: 16px;
    padding: 0;
  }
  .page-number {
    position: absolute;
    right: 28px;
    bottom: 16px;
    color: #6b7280;
    font-size: 13px;
  }
${deckStyle}
</style>
</head>
<body>
${renderedSlides}
</body>
</html>`;

fs.writeFileSync(htmlPath, documentHtml);

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  await page.goto(`file://${htmlPath}`, { waitUntil: "networkidle" });

  const overflow = await page.locator("section").evaluateAll((sections) =>
    sections.map((section, index) => ({
      slide: index + 1,
      horizontal: section.scrollWidth > section.clientWidth,
      vertical: section.scrollHeight > section.clientHeight,
      scrollWidth: section.scrollWidth,
      scrollHeight: section.scrollHeight,
    }))
  );

  await page.pdf({
    path: pdfPath,
    width: "13.333333in",
    height: "7.5in",
    printBackground: true,
    margin: { top: "0", right: "0", bottom: "0", left: "0" },
  });

  console.log(JSON.stringify({ slides: slides.length, overflow, pdfPath }, null, 2));
  await browser.close();
})();
