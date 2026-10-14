# v4_hook.jpg の中央の文字を消して、夜空だけの背景を作る（調和補間＋星の描き足し）
import sys, numpy as np
from PIL import Image, ImageFilter
src, out = sys.argv[1], sys.argv[2]
im = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
H, W, _ = im.shape
x0, x1, y0, y1 = 460, 2105, 365, 1095
mask = np.zeros((H, W), bool); mask[y0:y1, x0:x1] = True
# 1/4 解像度で調和補間
s = 4
small = np.asarray(Image.fromarray(im.astype(np.uint8)).resize((W // s, H // s), Image.LANCZOS)).astype(np.float32)
m = np.zeros((H // s, W // s), bool); m[y0 // s:y1 // s + 1, x0 // s:x1 // s + 1] = True
f = small.copy()
# 初期値：行ごとに左右の境界を線形補間
for c in range(3):
    ch = f[..., c]
    for yy in range(ch.shape[0]):
        if m[yy].any():
            xs = np.where(m[yy])[0]; a, b = xs[0] - 1, xs[-1] + 1
            ch[yy, xs] = np.interp(xs, [a, b], [ch[yy, a], ch[yy, b]])
for it in range(6000):
    nb = (np.roll(f, 1, 0) + np.roll(f, -1, 0) + np.roll(f, 1, 1) + np.roll(f, -1, 1)) / 4
    f[m] = nb[m]
fill = np.asarray(Image.fromarray(np.clip(f, 0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)).astype(np.float32)
# 細かいざらつき（周りの空のノイズに合わせる）
rng = np.random.default_rng(5)
ref = im[60:380, 600:2000]
hf = ref - np.asarray(Image.fromarray(ref.astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))).astype(np.float32)
sd = np.clip(np.median(np.abs(hf)) * 1.4, 1, 6)
noise = rng.normal(0, sd, (H, W, 1)).astype(np.float32)
noise = np.asarray(Image.fromarray(np.clip(noise[..., 0] * 8 + 128, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))).astype(np.float32)
noise = (noise - 128) / 8
fill = fill + noise[..., None]
# 星
stars = np.zeros((H, W), np.float32)
n = int((x1 - x0) * (y1 - y0) / 3400)
for _ in range(n):
    x, y = rng.integers(x0, x1), rng.integers(y0, y1)
    b = min(1.0, rng.pareto(2.2) * .35 + .15)
    r = 0.6 + b * 1.4
    yy, xx = np.ogrid[max(0, y - 6):y + 7, max(0, x - 6):x + 7]
    stars[max(0, y - 6):y + 7, max(0, x - 6):x + 7] += b * np.exp(-((xx - x) ** 2 + (yy - y) ** 2) / (2 * r * r))
star_col = np.array([255, 247, 228], np.float32)
fill = fill * (1 - np.clip(stars, 0, 1)[..., None]) + star_col * np.clip(stars, 0, 1)[..., None]
# なじませる（ぼかしたマスクで合成）
mk = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(18))
a = (np.asarray(mk).astype(np.float32) / 255)[..., None]
res = im * (1 - a) + fill * a
Image.fromarray(np.clip(res, 0, 255).astype(np.uint8)).save(out, quality=95)
print('ok', H, W, 'stars', n, 'sd', sd)
