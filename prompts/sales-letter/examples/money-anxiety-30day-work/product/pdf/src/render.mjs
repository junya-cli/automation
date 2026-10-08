// HTML → PDF 書き出しと品質チェック
// 使い方: node src/render.mjs [--pdf out.pdf] [--shots 1-5,48] [--scale 1.4]
import { chromium } from 'playwright-core';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';
import { spacePages } from './layout_pass.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const pdfOut = opt('--pdf', null);
const shots = opt('--shots', null);
const scale = parseFloat(opt('--scale', '1.3'));

const exe = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const browser = await chromium.launch({ executablePath: exe });
const ctx = await browser.newContext({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: scale });
const page = await ctx.newPage();
await page.goto('file://' + path.join(ROOT, 'build', 'book.html'), { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);

await spacePages(page);

// 書くページのメモ欄：狭すぎるものは隠す
const notes = await page.evaluate(() => [...document.querySelectorAll('.page')].map((p, i) => {
  const n = p.querySelector('.notes');
  if (!n) return null;
  const mm = n.getBoundingClientRect().height / 3.7795;
  if (mm < 28) n.classList.add('tiny');
  return { page: i + 1, mm: Math.round(mm) };
}).filter(Boolean));
const small = notes.filter(n => n.mm < 28);
if (small.length) console.log('メモ欄を省略:', JSON.stringify(small));

// はみ出しチェック
const over = await page.evaluate(() => [...document.querySelectorAll('.page')].map((p, i) => {
  const b = p.querySelector('.body');
  if (!b) return null;
  const d = b.scrollHeight - b.clientHeight;
  const wide = [...p.querySelectorAll('*')].some(e => e.scrollWidth > e.clientWidth + 2 && getComputedStyle(e).overflow === 'hidden' && e.classList.contains('body'));
  return d > 1 || wide ? { page: i + 1, over_px: d } : null;
}).filter(Boolean));
// 余白が多すぎるページ（本文の使用率）
const fill = await page.evaluate(() => [...document.querySelectorAll('.page')].map((p, i) => {
  const b = p.querySelector('.body');
  if (!b || p.querySelector('.notes')) return null;
  const top = b.getBoundingClientRect().top, h = b.clientHeight;
  let max = 0;
  for (const c of b.children) max = Math.max(max, c.getBoundingClientRect().bottom - top);
  return { page: i + 1, pct: Math.round(max / h * 100) };
}).filter(x => x && x.pct < 82));
console.log('余白が多いページ(<82%):', fill.map(x => `${x.page}:${x.pct}%`).join(' '));
const total = await page.evaluate(() => document.querySelectorAll('.page').length);
console.log(`ページ数: ${total}`);
console.log(over.length ? `はみ出し: ${JSON.stringify(over)}` : 'はみ出し: なし');

// 欠けた文字（フォントが無い字）チェック用に使用フォントを確認
const fonts = await page.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight).filter((v, i, a) => a.indexOf(v) === i));
console.log('読み込まれたフォント:', fonts.join(', '));

if (shots) {
  const want = new Set();
  for (const part of shots.split(',')) {
    if (part === 'all') { for (let i = 1; i <= total; i++) want.add(i); continue; }
    const [a, b] = part.split('-').map(Number);
    for (let i = a; i <= (b || a); i++) want.add(i);
  }
  const dir = path.join(ROOT, 'build', 'shots');
  fs.mkdirSync(dir, { recursive: true });
  const els = await page.$$('.page');
  for (const i of want) {
    if (els[i - 1]) await els[i - 1].screenshot({ path: path.join(dir, `p${String(i).padStart(3, '0')}.png`) });
  }
  console.log(`スクリーンショット: ${[...want].length}枚 → build/shots`);
}

if (pdfOut) {
  await page.emulateMedia({ media: 'print' });
  await page.pdf({ path: pdfOut, preferCSSPageSize: true, printBackground: true });
  console.log('PDF:', pdfOut);
}
await browser.close();
