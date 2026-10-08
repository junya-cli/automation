// 前付け・章・付録・Dayの読むページ：少し拡大し、残った余白をブロックの間に配る
export async function spacePages(page) {
  await page.evaluate(() => {
  const MM = 3.7795;
  const SEL = '.fig,.box,.grid2,.grid3,.cards,.conclusion,.memo,.sep2,.warn,.tbl,table,.stopbox,.talk,.offer,.abc,.type-hero,.kv,.blk,.ifthen,h3,.hd,.legend,.faq,.berg';
  for (const p of document.querySelectorAll('.page.fp, .page.rp')) {
    const rp = p.classList.contains('rp');
    const b = p.querySelector('.body');
    let kids = [...b.children];
    if (kids.length === 1 && kids[0].children.length > 1) kids = [...kids[0].children];
    const H = b.clientHeight;
    const used = () => { const t = b.getBoundingClientRect().top; let m = 0; for (const c of kids) m = Math.max(m, c.getBoundingClientRect().bottom - t); return m; };
    let u = used();
    if (u > H) continue;
    const z = rp ? 1 : Math.min(1.07, (H * 0.92) / u);
    if (z > 1.01) {
      kids.forEach(c => c.style.zoom = z);
      u = used();
      if (u > H * 0.985) { kids.forEach(c => c.style.zoom = ''); u = used(); }
    }
    const slots = kids.filter((c, i) => i > 0 && c.matches(SEL));
    if (!slots.length) continue;
    const extra = Math.min((rp ? 6 : 11) * MM, (H * 0.975 - u) / slots.length);
    if (extra <= 0) continue;
    for (const c of slots) {
      const prev = c.previousElementSibling;
      const pb = prev ? parseFloat(getComputedStyle(prev).marginBottom) || 0 : 0;
      const mt = parseFloat(getComputedStyle(c).marginTop) || 0;
      if (c.classList.contains('sep2')) {
        c.style.marginTop = (Math.max(pb, mt) + extra / 2) + 'px';
        c.style.marginBottom = (parseFloat(getComputedStyle(c).marginBottom) + extra / 2) + 'px';
      } else {
        c.style.marginTop = (Math.max(pb, mt) + extra) + 'px';
      }
    }
  }
});
}
