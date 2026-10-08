// LINE登録特典「お金のクセ診断」PDFを、ワークブックのページから作る
// 使い方: python3 src/build.py && node src/make_shindan.mjs ../../launch/okane-no-kuse-shindan.pdf
import { chromium } from 'playwright-core';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spacePages } from './layout_pass.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const out = process.argv[2] || path.join(ROOT, 'build', 'shindan.pdf');
const shots = process.argv[3];
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const page = await (await browser.newContext({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 1.2 })).newPage();
await page.goto('file://' + path.join(ROOT, 'build', 'book.html'), { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);

await page.evaluate(() => {
  const pages = [...document.querySelectorAll('.page')];
  const find = t => pages.find(p => [...p.querySelectorAll('h2.sec')].some(h => h.textContent.trim() === t));
  const keep = [find('最近1か月のあなたに、0〜3で答えてください'), find('点数を足して、あなたの2タイプを見つけます'), find('お金のクセは、5つのタイプに分かれます')];
  keep[0].before(keep[1]); keep[1].before(keep[0]); keep[1].after(keep[2]);
  if (keep.some(k => !k)) throw new Error('page not found');
  const RUN = 'お金のクセ診断（20問）';
  keep.forEach(p => {
    p.querySelectorAll('.run .run-l').forEach(r => { r.lastChild.textContent = RUN; });
    p.querySelectorAll('.kicker').forEach(k => { if (k.textContent.includes('第2章')) k.textContent = k.textContent.includes('Day0') ? 'STEP 1' : (k.closest('.page') === keep[1] ? 'STEP 2' : 'STEP 3'); });
  });
  // セルフチェック：書き込みノートの案内を消す
  [...keep[0].querySelectorAll('.small')].filter(e => e.textContent.includes('書き込みノート')).forEach(e => e.remove());
  // 5タイプ一覧：ワークのページ番号の列を消す
  keep[2].querySelectorAll('table.tbl tr').forEach(tr => { const c = tr.lastElementChild; if (c && (c.textContent.trim().startsWith('p.') || c.textContent.trim() === '')) c.remove(); });
  [...keep[2].querySelectorAll('.tb')].forEach(t => { if (t.textContent.includes('次のページから')) t.textContent = 'タイプは、混ざっていてあたりまえ。どのタイプかで、30日でやることが変わります。'; });

  const aoiCircle = (size) => `<div style="width:${size}mm;height:${size}mm;border-radius:50%;margin:0 auto;background:#fff url(../assets/aoi_circle_600.png) center/cover no-repeat;box-shadow:0 0 0 2px var(--gold-l),0 0 0 5px #fff,0 0 0 6px var(--gold-l),0 8px 20px rgba(40,50,101,.14)"></div>`;
  const cover = document.createElement('section');
  cover.className = 'page wk-loosen';
  cover.innerHTML = `<div class="run"><span class="run-l"><i></i>${RUN}</span><span>毒親育ちのお金の不安がなくなる小さな習慣</span></div>
  <div class="body" style="display:flex;flex-direction:column;justify-content:center;gap:9mm;text-align:center">
    <div><div class="kicker" style="letter-spacing:.4em">FREE CHECK</div>
    <div class="mg" style="font-weight:700;color:var(--navy);font-size:34pt;letter-spacing:.08em;margin-top:2mm">お金のクセ診断</div>
    <div class="mg" style="font-weight:700;color:var(--wk);font-size:13pt;margin-top:1mm">20問・5分で、あなたの「2タイプ」が分かります</div></div>
    ${aoiCircle(64)}
    <div class="box tint" style="text-align:left;max-width:150mm;margin:0 auto">
      <h4>やり方</h4>
      <ol class="nlist"><li>最近1か月のあなたに、20問を0〜3で答える（STEP 1）</li><li>タイプごとに、決まった番号の点数を足す（STEP 2）</li><li>点数が高い2つが、あなたの2タイプ（STEP 3で、5つのタイプを確かめる）</li></ol>
    </div>
    <p class="small" style="max-width:150mm;margin:0 auto">この診断は、「お金についての思い込みには、いくつかの型がある」という研究（Klontz ほか, 2011）を参考に、アオが作ったものです。医学的・心理学的な診断ではありません。今のあなたの「傾向」を知るためのものです。</p>
  </div><div class="folio">1</div>`;
  const end = document.createElement('section');
  end.className = 'page wk-loosen';
  end.innerHTML = `<div class="run"><span class="run-l"><i></i>${RUN}</span><span>毒親育ちのお金の不安がなくなる小さな習慣</span></div>
  <div class="body" style="display:flex;flex-direction:column;gap:7mm;padding-top:10mm">
    <div class="kicker">NEXT</div>
    <h2 class="sec" style="font-size:20pt">あなたの2タイプは、何でしたか？</h2>
    <div class="talk"><div class="aoi l" style="background-image:url(../assets/aoi_face.png)"></div><div class="bubble"><div class="who">アオより</div>
      <p>診断、おつかれさまでした。</p>
      <p>よかったら、あなたの2タイプを、LINEのトークに送ってください（例：「人に出しすぎ・見ないふり」）。送らなくても、もちろん大丈夫です。</p>
      <p>このあとLINEでは、毒親育ちの人の「足りない」がどこから来るのか、そしてどうゆるめていくのかを、3回に分けてお届けします。</p></div></div>
    <div class="box tint"><h4>2タイプが分かると、何が変わるの？</h4>
      <p style="margin:0">たとえば「お金を見る」練習。見ないふりタイプは「少しだけ見る」練習、ため込みタイプは逆に「決めた日以外は見なくていい」練習です。同じ「お金の見直し」でも、タイプによって、やることが逆になることがあります。</p></div>
    <div class="warn"><h4>こんなときは、先に相談を</h4>
      <ul class="ilist" style="--wk:#C25B6A;--wk-t:#FBE3E6"><li><span class="ib">!</span><span>買い物をやめたいのにやめられず、隠したり、うそをついたりしている</span></li><li><span class="ib">!</span><span>借金やリボ払いの返済のために、別の借り入れをしている</span></li><li><span class="ib">!</span><span>眠れない・食べられないなどの不調が、2週間以上続いている</span></li></ul>
      <p style="margin:2mm 0 0;font-size:9.8pt">当てはまるときは、ひとりで抱えずに、医療機関や専門の窓口に相談してください。</p></div>
    <p class="small" style="text-align:center;margin-top:auto">『毒親育ちのお金の不安がなくなる小さな習慣 〜心と財布に余裕が生まれる30日ワーク〜』より　アオ</p>
  </div><div class="folio">5</div>`;
  const body = document.body;
  pages.forEach(p => { if (!keep.includes(p)) p.remove(); });
  body.insertBefore(cover, keep[0]);
  body.appendChild(end);
  keep.forEach((p, i) => { const f = p.querySelector('.folio'); if (f) f.textContent = String(i + 2); });
});

await spacePages(page);
const over = await page.evaluate(() => [...document.querySelectorAll('.page')].map((p, i) => { const b = p.querySelector('.body'); return b && b.scrollHeight > b.clientHeight + 1 ? i + 1 : null; }).filter(Boolean));
console.log('pages:', await page.evaluate(() => document.querySelectorAll('.page').length), 'overflow:', JSON.stringify(over));
if (shots) {
  const els = await page.$$('.page');
  for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: path.join(shots, `shindan_${i + 1}.png`) });
}
await page.emulateMedia({ media: 'print' });
await page.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
console.log('PDF:', out);
await browser.close();
