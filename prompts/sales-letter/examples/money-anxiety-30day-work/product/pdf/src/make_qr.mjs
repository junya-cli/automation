// QRコードをSVGで作る: node src/make_qr.mjs
import QRCode from 'qrcode';
import fs from 'node:fs';
const items = {
  qr_note: 'https://docs.google.com/document/d/1MtiOOO_1daacIk8Mfc6gGC205H8gvT42gDvBLhSxJ6o/copy',
  qr_line: 'https://lin.ee/zx8oP4j',
};
for (const [k, url] of Object.entries(items)) {
  const svg = await QRCode.toString(url, { type: 'svg', margin: 0, errorCorrectionLevel: 'M', color: { dark: '#283265', light: '#ffffff' } });
  fs.writeFileSync(new URL(`../assets/${k}.svg`, import.meta.url), svg);
  console.log(k, svg.length);
}
