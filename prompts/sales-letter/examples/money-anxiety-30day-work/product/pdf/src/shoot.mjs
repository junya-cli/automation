// HTMLの要素を画像にする: node src/shoot.mjs build/note_figs.html outdir id:scale ...
import { chromium } from 'playwright-core';
import path from 'node:path';
import fs from 'node:fs';
const [html, outDir, ...items] = process.argv.slice(2);
fs.mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
for (const it of items) {
  const [id, scale, name] = it.split(':');
  const ctx = await browser.newContext({ viewport: { width: 1400, height: 1000 }, deviceScaleFactor: parseFloat(scale) });
  const page = await ctx.newPage();
  await page.goto('file://' + path.resolve(html), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.locator('#' + id).screenshot({ path: path.join(outDir, name) });
  console.log(name);
  await ctx.close();
}
await browser.close();
