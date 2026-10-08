"""スクリーンショットを並べた確認用シート: python3 src/sheet.py 1-8 [out.png]"""
import sys, pathlib
from PIL import Image, ImageDraw
ROOT = pathlib.Path(__file__).resolve().parents[1]
a, b = map(int, sys.argv[1].split('-'))
out = sys.argv[2] if len(sys.argv) > 2 else str(ROOT / 'build' / f'sheet_{a:03d}.png')
ims = [Image.open(ROOT / 'build' / 'shots' / f'p{i:03d}.png') for i in range(a, b + 1)]
w, h = 560, int(560 * 297 / 210)
cols = 4
rows = (len(ims) + cols - 1) // cols
sheet = Image.new('RGB', (cols * (w + 10) + 10, rows * (h + 30) + 10), '#bbbbbb')
d = ImageDraw.Draw(sheet)
for k, im in enumerate(ims):
    x, y = 10 + (k % cols) * (w + 10), 10 + (k // cols) * (h + 30)
    sheet.paste(im.convert('RGB').resize((w, h)), (x, y + 20))
    d.text((x, y + 4), f'p{a + k}', fill='black')
sheet.save(out)
print(out)
