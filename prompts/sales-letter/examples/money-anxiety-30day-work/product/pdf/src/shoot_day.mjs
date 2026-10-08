// ワークの「Dayの読むページ」を、紙の影つきの画像にする（LINEやXで中身を見せる用）
// 使い方: python3 src/build.py && node src/shoot_day.mjs 1 ../../launch/images/day1.png
import { chromium } from 'playwright-core';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spacePages } from './layout_pass.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const [day = '1', out = path.join(ROOT, 'build', `day${day}.png`)] = process.argv.slice(2);
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const ctx = await browser.newContext({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 1.5 });
const page = await ctx.newPage();
await page.goto('file://' + path.join(ROOT, 'build', 'book.html'), { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await spacePages(page);

const idx = await page.evaluate(d => [...document.querySelectorAll('.page')]
  .findIndex(p => p.classList.contains('rp') && p.querySelector('.daynum .n')?.textContent.trim() === d), day);
if (idx < 0) throw new Error(`Day${day} の読むページが見つかりません`);
const shot = await page.locator('.page').nth(idx).screenshot({ type: 'png' });

await page.setContent(`<body style="margin:0;background:#F4EDDD"><div id="w" style="display:inline-block;padding:40px;background:#F4EDDD">
  <img src="data:image/png;base64,${shot.toString('base64')}" style="display:block;width:794px;border-radius:4px;box-shadow:0 2px 6px rgba(40,50,101,.10),0 12px 32px rgba(40,50,101,.16)"></div></body>`);
await page.locator('#w').screenshot({ path: out });
console.log(out);
await browser.close();
