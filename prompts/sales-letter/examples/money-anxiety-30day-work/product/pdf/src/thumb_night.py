"""高級感のある夜景サムネ（1280×670）のHTMLを作る: python3 src/thumb_night.py
書き出し: node src/shoot.mjs build/thumb_night.html ../../note/images thumb:2:00_midashi.png
"""
import math, random, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import ROOT

W, H = 1280, 670
rnd = random.Random(7)
FONTS = ['@fontsource/shippori-mincho-b1/700.css', '@fontsource/shippori-mincho-b1/800.css',
         '@fontsource/noto-serif-jp/500.css', '@fontsource/noto-serif-jp/700.css', '@fontsource/noto-serif-jp/900.css',
         '@fontsource/cinzel/700.css', '@fontsource/zen-maru-gothic/700.css']

GOLD = '#F3D788'
GOLD_D = '#B98B3A'
NAVY = '#101538'


def star4(cx, cy, r, color='#FFF6D5', op=1.0):
    k = r * 0.28
    return (f'<path d="M{cx} {cy - r} Q{cx + k} {cy - k} {cx + r} {cy} Q{cx + k} {cy + k} {cx} {cy + r} '
            f'Q{cx - k} {cy + k} {cx - r} {cy} Q{cx - k} {cy - k} {cx} {cy - r}Z" fill="{color}" opacity="{op}"/>')


def stars():
    out = []
    for _ in range(260):
        x, y = rnd.uniform(0, W), rnd.uniform(0, 380)
        r = rnd.choice([0.7, 0.9, 1.1, 1.4, 1.8, 2.2])
        op = rnd.uniform(0.35, 1.0) * (1 - y / 520)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#FFFBEA" opacity="{op:.2f}"/>')
    for _ in range(18):
        x, y = rnd.uniform(40, W - 40), rnd.uniform(20, 300)
        r = rnd.uniform(4, 11)
        out.append(f'<g filter="url(#glow)">{star4(x, y, r, "#FFF3C4", 0.95)}</g>')
    # 流れ星
    for x, y, L, a in [(120, 70, 220, 28), (980, 40, 160, 22), (330, 20, 130, 30)]:
        out.append(f'<g transform="translate({x} {y}) rotate({a})"><rect x="0" y="-1.2" width="{L}" height="2.4" rx="1.2" fill="url(#shoot)"/>'
                   f'{star4(0, 0, 5, "#FFFFFF")}</g>')
    return ''.join(out)


def moon():
    return ('<g><circle cx="1140" cy="62" r="230" fill="url(#moonhalo)"/>'
            '<circle cx="1140" cy="62" r="118" fill="url(#moon)"/>'
            '<circle cx="1105" cy="40" r="14" fill="#E9D8A6" opacity=".35"/><circle cx="1170" cy="95" r="22" fill="#E9D8A6" opacity=".3"/>'
            '<circle cx="1118" cy="110" r="9" fill="#E9D8A6" opacity=".3"/></g>')


def mountains():
    far = 'M0 300 C 90 250 200 262 300 292 C 380 316 440 330 520 352 L520 430 L0 430 Z'
    far_r = 'M760 352 C 860 330 930 286 1040 262 C 1120 246 1200 258 1280 300 L1280 430 L760 430 Z'
    near = 'M0 340 C 110 300 220 318 330 346 C 400 364 450 386 500 400 L500 450 L0 450 Z'
    near_r = 'M780 400 C 860 384 920 350 1010 330 C 1100 312 1200 330 1280 346 L1280 450 L780 450 Z'
    return (f'<path d="{far}" fill="#241D5C"/><path d="{far_r}" fill="#241D5C"/>'
            f'<path d="{near}" fill="#191546"/><path d="{near_r}" fill="#191546"/>')


def trees(xs, base, color='#141238'):
    out = []
    for x, h in xs:
        out.append(f'<path d="M{x} {base} L{x - h * .28} {base} L{x} {base - h} L{x + h * .28} {base}Z" fill="{color}"/>'
                   f'<path d="M{x - h * .22} {base - h * .42} L{x} {base - h * .95} L{x + h * .22} {base - h * .42}Z" fill="{color}"/>')
    return ''.join(out)


def town_left():
    """左の丘の街：建物のシルエット＋あたたかい窓明かり"""
    sil, win = [], []
    x = 18
    while x < 470:
        slope = 318 + (x / 470) * 96  # 丘の斜面
        w = rnd.uniform(16, 34)
        h = rnd.uniform(26, 70) * (1 - x / 900)
        y = slope - h
        sil.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h + 30:.0f}" fill="#1A1646"/>')
        if rnd.random() < .7:
            sil.append(f'<path d="M{x - 2:.0f} {y:.0f} L{x + w / 2:.0f} {y - w * .55:.0f} L{x + w + 2:.0f} {y:.0f}Z" fill="#1A1646"/>')
        for wy in range(int(y + 7), int(slope - 6), 11):
            for wx in range(int(x + 4), int(x + w - 4), 8):
                if rnd.random() < .55:
                    c = rnd.choice(['#FFD98A', '#FFC66B', '#FFE7B0'])
                    win.append(f'<rect x="{wx}" y="{wy}" width="3.2" height="4" fill="{c}" opacity="{rnd.uniform(.6, 1):.2f}"/>')
        x += w + rnd.uniform(2, 9)
    # ドーム
    sil.append('<ellipse cx="150" cy="286" rx="30" ry="22" fill="#1A1646"/><rect x="118" y="286" width="64" height="40" fill="#1A1646"/>'
               '<rect x="147" y="256" width="6" height="14" fill="#1A1646"/>')
    tr = trees([(40, 60), (95, 48), (210, 54), (300, 44), (380, 38), (440, 34)], 420)
    return f'<g>{"".join(sil)}{tr}</g><g filter="url(#blur3)" opacity=".8">{"".join(win)}</g><g>{"".join(win)}</g>'


def castle_right():
    """右の城と街"""
    sil, win = [], []
    towers = [(1020, 42, 150), (1062, 28, 118), (1105, 54, 196), (1160, 30, 124), (1195, 40, 160), (1240, 26, 108), (985, 22, 96)]
    base = 352
    for x, w, h in towers:
        y = base - h
        sil.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h + 40}" fill="#191546"/>'
                   f'<path d="M{x - 3} {y} L{x + w / 2} {y - w * 1.1} L{x + w + 3} {y}Z" fill="#191546"/>'
                   f'<rect x="{x + w / 2 - 1}" y="{y - w * 1.1 - 10}" width="2" height="12" fill="#191546"/>')
        for wy in range(int(y + 10), int(base - 6), 13):
            for wx in range(int(x + 5), int(x + w - 5), 9):
                if rnd.random() < .45:
                    win.append(f'<rect x="{wx}" y="{wy}" width="3" height="5" rx="1.5" fill="{rnd.choice(["#FFD98A", "#FFE9B8", "#F7C465"])}" opacity="{rnd.uniform(.6, 1):.2f}"/>')
    # 城下町
    x = 800
    while x < 1280:
        slope = 400 - (x - 800) / 480 * 50
        w = rnd.uniform(14, 28); h = rnd.uniform(18, 42)
        y = slope - h
        sil.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h + 30:.0f}" fill="#1A1646"/>')
        for wy in range(int(y + 6), int(slope - 4), 10):
            for wx in range(int(x + 3), int(x + w - 3), 7):
                if rnd.random() < .5:
                    win.append(f'<rect x="{wx}" y="{wy}" width="2.6" height="3.6" fill="#FFD98A" opacity="{rnd.uniform(.5, 1):.2f}"/>')
        x += w + rnd.uniform(2, 8)
    tr = trees([(830, 40), (900, 46), (960, 36), (1250, 44)], 418)
    return f'<g>{"".join(sil)}{tr}</g><g filter="url(#blur3)" opacity=".8">{"".join(win)}</g><g>{"".join(win)}</g>'


def lake():
    out = ['<rect x="0" y="418" width="1280" height="70" fill="url(#lake)"/>']
    # 光の映り込み
    for _ in range(70):
        x = rnd.uniform(0, W)
        if 300 < x < 980 and rnd.random() < .7:
            continue
        w = rnd.uniform(1.5, 5); h = rnd.uniform(14, 48)
        c = rnd.choice(['#FFD98A', '#F7B8D8', '#C9A8FF', '#FFE9B8'])
        out.append(f'<rect x="{x:.0f}" y="420" width="{w:.1f}" height="{h:.0f}" fill="{c}" opacity="{rnd.uniform(.15, .5):.2f}"/>')
    # 月の映り込み
    out.append('<ellipse cx="1140" cy="432" rx="150" ry="10" fill="url(#moonref)"/>')
    for _ in range(28):
        x = rnd.uniform(1010, 1270); y = rnd.uniform(422, 470)
        out.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{rnd.uniform(6, 26):.0f}" height="1.4" fill="#FFF0C4" opacity="{rnd.uniform(.15, .5):.2f}"/>')
    # 橋
    arches = ''.join(f'<path d="M{x} 442 a 24 24 0 0 1 48 0 L{x + 48} 452 L{x} 452Z" fill="#2B2466"/>' for x in range(880, 1130, 58))
    out.append('<rect x="860" y="404" width="320" height="40" fill="#1A1646"/>' + arches +
               ''.join(f'<circle cx="{x}" cy="400" r="2.2" fill="#FFE2A0"/>' for x in range(880, 1170, 36)))
    return f'<g filter="url(#blur1)">{"".join(out[:1] + out[1:-1])}</g>{out[-1]}'


def flower(cx, cy, s, pet='#B6A2EA', hi='#E6DBFF', core='#F6D37C', rot=0):
    petals = ''.join(f'<ellipse cx="0" cy="{-s * .62:.1f}" rx="{s * .34:.1f}" ry="{s * .62:.1f}" fill="{pet}" transform="rotate({a + rot})"/>' for a in range(0, 360, 72))
    hil = ''.join(f'<ellipse cx="0" cy="{-s * .66:.1f}" rx="{s * .14:.1f}" ry="{s * .34:.1f}" fill="{hi}" opacity=".55" transform="rotate({a + rot})"/>' for a in range(0, 360, 72))
    return f'<g transform="translate({cx:.0f} {cy:.0f})">{petals}{hil}<circle r="{s * .17:.1f}" fill="{core}"/></g>'


def leaf(cx, cy, s, rot, color='#2E4A4E'):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{s * .3}" ry="{s}" fill="{color}" transform="rotate({rot} {cx} {cy})"/>'


def vines():
    out = []
    # 左上：つる
    for i in range(16):
        t = i / 15
        cx = 6 + t * 250 + rnd.uniform(-10, 10); cy = 16 + math.sin(t * 3.2) * 56 + t * 110
        if i % 2:
            out.append(leaf(cx + 18, cy + 10, rnd.uniform(16, 24), rnd.uniform(-60, 60)))
        out.append(flower(cx, cy, rnd.uniform(12, 24) * (1 - t * .4) + 6, rnd.choice(['#B6A2EA', '#C8B4F4', '#9F87D8']), rot=rnd.uniform(0, 72)))
    # 左端の縦のつる
    for i in range(7):
        cy = 150 + i * 42
        out.append(leaf(28 + rnd.uniform(-8, 8), cy + 18, 18, rnd.uniform(20, 70)))
        out.append(flower(18 + rnd.uniform(-10, 14), cy, rnd.uniform(10, 18), rnd.choice(['#B6A2EA', '#C8B4F4']), rot=rnd.uniform(0, 72)))
    # 右端：つる（月の下から）
    for i in range(12):
        t = i / 11
        cx = 1270 - rnd.uniform(0, 30) - math.sin(t * 2.6) * 30; cy = 180 + t * 300
        out.append(leaf(cx - 16, cy + 8, rnd.uniform(14, 22), rnd.uniform(-70, -20)))
        out.append(flower(cx, cy, rnd.uniform(11, 20), rnd.choice(['#B6A2EA', '#C8B4F4', '#9F87D8']), rot=rnd.uniform(0, 72)))
    # 左下・右下の小花
    for cx, cy in [(300, 650), (262, 662), (330, 640), (210, 612), (1010, 662), (1250, 648), (1180, 672)]:
        out.append(flower(cx, cy, rnd.uniform(10, 16), '#C8B4F4', rot=rnd.uniform(0, 72)))
    return ''.join(out)


def books_and_lantern():
    titles = ['KNOW YOUR PATTERN', 'SMALL HABITS', 'A LIGHTER TOMORROW']
    out = []
    y0 = 530
    for i, t in enumerate(titles):
        y = y0 + i * 46; x = 34 + (i % 2) * 8 - i * 4; w = 250 - (i % 2) * 12 + i * 6
        d = 12  # 奥行き
        out.append(f'<g><path d="M{x + w} {y} L{x + w + d} {y - d * .55} L{x + w + d} {y + 44 - d * .55} L{x + w} {y + 44}Z" fill="#0F1438"/>'
                   f'<path d="M{x} {y} L{x + d} {y - d * .55} L{x + w + d} {y - d * .55} L{x + w} {y}Z" fill="#EFE6CF"/>'
                   + ''.join(f'<line x1="{x + 2 + k * .5}" y1="{y - k * .5 * .55:.1f}" x2="{x + w - 2 + k * .5}" y2="{y - k * .5 * .55:.1f}" stroke="#CFC3A4" stroke-width=".6"/>' for k in range(1, 12, 2)) +
                   f'<rect x="{x}" y="{y}" width="{w}" height="44" rx="3" fill="url(#book{i % 2})"/>'
                   f'<rect x="{x + 1.5}" y="{y + 1.5}" width="{w - 3}" height="41" rx="2.5" fill="none" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1"/>'
                   f'<rect x="{x + 7}" y="{y + 6}" width="{w - 14}" height="32" rx="2" fill="none" stroke="{GOLD}" stroke-opacity=".35" stroke-width=".8"/>'
                   f'<rect x="{x}" y="{y}" width="{w}" height="44" rx="3" fill="url(#sheen)"/>'
                   f'<text x="{x + w / 2}" y="{y + 29}" text-anchor="middle" font-family="Cinzel" font-weight="700" font-size="14.5" letter-spacing="2" fill="{GOLD}">{t}</text></g>')
    # ランタン
    lx, ly = 118, 440
    out.append(f'<ellipse cx="{lx}" cy="{ly + 50}" rx="90" ry="70" fill="url(#lanternglow)"/>'
               f'<g><path d="M{lx - 20} {ly - 26} L{lx} {ly - 48} L{lx + 20} {ly - 26}Z" fill="url(#goldv)"/>'
               f'<rect x="{lx - 24}" y="{ly - 27}" width="48" height="6" rx="2" fill="url(#goldv)"/>'
               f'<circle cx="{lx}" cy="{ly - 54}" r="6" fill="none" stroke="{GOLD}" stroke-width="2.5"/>'
               f'<rect x="{lx - 19}" y="{ly - 21}" width="38" height="68" rx="5" fill="url(#glass)"/>'
               f'<rect x="{lx - 22}" y="{ly - 22}" width="44" height="70" rx="6" fill="none" stroke="url(#goldv)" stroke-width="3.5"/>'
               f'<line x1="{lx}" y1="{ly - 20}" x2="{lx}" y2="{ly + 46}" stroke="{GOLD_D}" stroke-width="1.6"/>'
               f'<line x1="{lx - 20}" y1="{ly + 13}" x2="{lx + 20}" y2="{ly + 13}" stroke="{GOLD_D}" stroke-width="1.6"/>'
               f'<ellipse cx="{lx}" cy="{ly + 24}" rx="7" ry="13" fill="#FFF3C2" filter="url(#blur2)"/>'
               f'<rect x="{lx - 26}" y="{ly + 48}" width="52" height="7" rx="2" fill="url(#goldv)"/>'
               f'<rect x="{lx - 14}" y="{ly + 55}" width="28" height="5" rx="2" fill="{GOLD_D}"/></g>')
    # 水晶玉
    ox, oy = 236, 486
    out.append(f'<ellipse cx="{ox}" cy="{oy + 10}" rx="64" ry="50" fill="url(#orbglow)"/>'
               f'<path d="M{ox - 30} {oy + 46} Q{ox} {oy + 30} {ox + 30} {oy + 46} L{ox + 26} {oy + 54} L{ox - 26} {oy + 54}Z" fill="url(#goldv)"/>'
               f'<circle cx="{ox}" cy="{oy}" r="40" fill="url(#orb)"/>'
               f'<circle cx="{ox}" cy="{oy}" r="40" fill="none" stroke="#FFFFFF" stroke-opacity=".5" stroke-width="1.2"/>'
               f'<ellipse cx="{ox - 14}" cy="{oy - 18}" rx="12" ry="7" fill="#FFFFFF" opacity=".55" transform="rotate(-30 {ox - 14} {oy - 18})"/>'
               + ''.join(star4(ox + rnd.uniform(-22, 22), oy + rnd.uniform(-20, 22), rnd.uniform(2, 5), '#FFF6D5', rnd.uniform(.6, 1)) for _ in range(9)) +
               ''.join(f'<circle cx="{ox + rnd.uniform(-26, 26):.0f}" cy="{oy + rnd.uniform(-26, 26):.0f}" r="{rnd.uniform(.6, 1.5):.1f}" fill="#FFF" opacity=".8"/>' for _ in range(16)))
    return ''.join(out)


def aoi_right():
    cx, cy, r = 1095, 486, 146
    rings = ''.join(f'<ellipse cx="{cx}" cy="{cy}" rx="{r + 34}" ry="{(r + 34) * k}" fill="none" stroke="url(#goldh)" stroke-width="2" opacity=".75" transform="rotate({a} {cx} {cy})"/>'
                    for k, a in [(.32, -18), (.5, 32), (.22, 70)])
    return (f'<ellipse cx="{cx + 10}" cy="{cy + r + 12}" rx="200" ry="40" fill="url(#cushion)"/>'
            f'<ellipse cx="{cx + 10}" cy="{cy + r + 12}" rx="200" ry="40" fill="none" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1.5"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r + 90}" fill="url(#aoiglow)"/>{rings}'
            f'<circle cx="{cx}" cy="{cy}" r="{r + 9}" fill="url(#goldv)"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r + 3}" fill="#FFFDF6"/>'
            f'<clipPath id="aoiclip"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
            f'<image href="../assets/aoi_circle_600.png" x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" clip-path="url(#aoiclip)"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r + 6}" fill="none" stroke="{GOLD}" stroke-width="1.2" opacity=".9"/>'
            + ''.join(star4(cx + dx, cy + dy, s, '#FFF6D5') for dx, dy, s in [(-150, -120, 10), (160, -90, 7), (-170, 40, 6), (150, 110, 9), (-120, 150, 5)]))


def bokeh():
    out = []
    for _ in range(40):
        x, y = rnd.uniform(0, W), rnd.uniform(60, H)
        if 330 < x < 950 and 60 < y < 600 and rnd.random() < .8:
            continue
        r = rnd.uniform(3, 14)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{rnd.choice(["#FFD98A", "#FFE9B8", "#E3C7FF"])}" opacity="{rnd.uniform(.08, .3):.2f}"/>')
    return f'<g filter="url(#blur2)">{"".join(out)}</g>'


def flourish(cx, cy, w, flip=1):
    """見出しの下の金の飾り罫"""
    h = w / 2
    return (f'<g transform="translate({cx} {cy}) scale({flip} 1)" fill="none" stroke="url(#goldh)" stroke-width="2" stroke-linecap="round">'
            f'<path d="M{-h} 0 C{-h * .6} 0 {-h * .5} -10 {-h * .3} -10 S{-h * .12} 0 {-h * .12} 0"/>'
            f'<path d="M{-h * .12} 0 C{-h * .16} 8 {-h * .3} 12 {-h * .42} 6"/>'
            f'<path d="M{h} 0 C{h * .6} 0 {h * .5} -10 {h * .3} -10 S{h * .12} 0 {h * .12} 0"/>'
            f'<path d="M{h * .12} 0 C{h * .16} 8 {h * .3} 12 {h * .42} 6"/>'
            f'<circle cx="{-h}" cy="0" r="2.2" fill="{GOLD}" stroke="none"/><circle cx="{h}" cy="0" r="2.2" fill="{GOLD}" stroke="none"/></g>'
            + star4(cx, cy, 9, GOLD) + star4(cx - w * .36, cy - 1, 4, GOLD, .9) + star4(cx + w * .36, cy - 1, 4, GOLD, .9))


DEFS = f'''<defs>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="blur1" x="-5%" y="-20%" width="110%" height="140%"><feGaussianBlur stdDeviation="1"/></filter>
<filter id="blur2" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.5"/></filter>
<filter id="blur3" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3"/></filter>
<linearGradient id="shoot" x1="0" x2="1"><stop offset="0" stop-color="#FFF" stop-opacity=".95"/><stop offset="1" stop-color="#FFF" stop-opacity="0"/></linearGradient>
<radialGradient id="moon" cx=".4" cy=".35" r=".75"><stop offset="0" stop-color="#FFFDF2"/><stop offset=".7" stop-color="#F6E8B8"/><stop offset="1" stop-color="#E4CB8E"/></radialGradient>
<radialGradient id="moonhalo"><stop offset="0" stop-color="#FFF4CF" stop-opacity=".55"/><stop offset=".45" stop-color="#FFE7B0" stop-opacity=".18"/><stop offset="1" stop-color="#FFE7B0" stop-opacity="0"/></radialGradient>
<linearGradient id="lake" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5A3B95"/><stop offset=".5" stop-color="#3A2A75"/><stop offset="1" stop-color="#1F1750"/></linearGradient>
<radialGradient id="moonref"><stop offset="0" stop-color="#FFF0C4" stop-opacity=".7"/><stop offset="1" stop-color="#FFF0C4" stop-opacity="0"/></radialGradient>
<linearGradient id="goldv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF2C4"/><stop offset=".35" stop-color="#E9C66E"/><stop offset=".6" stop-color="#B8862B"/><stop offset=".8" stop-color="#F3D788"/><stop offset="1" stop-color="#9E7322"/></linearGradient>
<linearGradient id="goldh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9E7322"/><stop offset=".25" stop-color="#F7DE94"/><stop offset=".5" stop-color="#FFF6D0"/><stop offset=".75" stop-color="#E2BC63"/><stop offset="1" stop-color="#9E7322"/></linearGradient>
<linearGradient id="book0" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1B2358"/><stop offset=".5" stop-color="#2A3474"/><stop offset="1" stop-color="#161C4A"/></linearGradient>
<linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF" stop-opacity=".16"/><stop offset=".5" stop-color="#FFF" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".25"/></linearGradient>
<linearGradient id="book1" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2A1F5C"/><stop offset=".5" stop-color="#3B2D78"/><stop offset="1" stop-color="#221A4C"/></linearGradient>
<radialGradient id="lanternglow"><stop offset="0" stop-color="#FFD98A" stop-opacity=".55"/><stop offset="1" stop-color="#FFD98A" stop-opacity="0"/></radialGradient>
<linearGradient id="glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF6D8" stop-opacity=".9"/><stop offset=".5" stop-color="#FFD98A" stop-opacity=".85"/><stop offset="1" stop-color="#F0A94A" stop-opacity=".9"/></linearGradient>
<radialGradient id="orbglow"><stop offset="0" stop-color="#D8CCFF" stop-opacity=".5"/><stop offset="1" stop-color="#D8CCFF" stop-opacity="0"/></radialGradient>
<radialGradient id="orb" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="#F4EEFF" stop-opacity=".95"/><stop offset=".45" stop-color="#9C86E0" stop-opacity=".85"/><stop offset="1" stop-color="#2E2270" stop-opacity=".95"/></radialGradient>
<linearGradient id="cushion" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6A49B0"/><stop offset="1" stop-color="#2E1E62"/></linearGradient>
<radialGradient id="aoiglow"><stop offset="0" stop-color="#FFF0C4" stop-opacity=".5"/><stop offset=".55" stop-color="#FFE7B0" stop-opacity=".12"/><stop offset="1" stop-color="#FFE7B0" stop-opacity="0"/></radialGradient>
<radialGradient id="horizon" cx=".5" cy=".6" r=".6"><stop offset="0" stop-color="#F2A4E0" stop-opacity=".7"/><stop offset=".35" stop-color="#B57AE0" stop-opacity=".4"/><stop offset=".7" stop-color="#8E5BC8" stop-opacity=".12"/><stop offset="1" stop-color="#8E5BC8" stop-opacity="0"/></radialGradient>
</defs>'''

CSS = f'''
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: #222; }}
#thumb {{ position: relative; width: {W}px; height: {H}px; overflow: hidden; margin: 20px;
  background: linear-gradient(180deg, #05071E 0%, #0E1340 26%, #2A2070 46%, #5A3B95 60%, #2B1C5E 72%, #140F33 100%); }}
#thumb svg.scene {{ position: absolute; inset: 0; width: {W}px; height: {H}px; }}
.vig {{ position: absolute; inset: 0; background:
  radial-gradient(ellipse 72% 70% at 50% 48%, rgba(0,0,0,0) 55%, rgba(4,5,22,.72) 100%),
  linear-gradient(180deg, rgba(0,0,0,0) 78%, rgba(6,5,24,.55) 100%); }}
.col {{ position: absolute; left: 0; right: 0; top: 0; display: flex; flex-direction: column; align-items: center; }}
.mincho {{ font-family: 'Shippori Mincho B1', 'Noto Serif JP', serif; }}
.serif {{ font-family: 'Noto Serif JP', 'Shippori Mincho B1', serif; }}
.pill {{ display: inline-flex; align-items: center; gap: 10px; background: rgba(12,14,46,.78); border: 1.5px solid rgba(243,215,136,.85);
  border-radius: 999px; padding: 6px 30px; color: #FFF8E6; font-weight: 700; letter-spacing: .1em; box-shadow: 0 4px 18px rgba(0,0,0,.35), inset 0 0 0 1px rgba(255,255,255,.06); }}
.pill.top {{ margin-top: 26px; font-size: 21px; }}
.pill .x {{ color: {GOLD}; font-size: 18px; }}
.kicker {{ margin-top: 12px; font-size: 27px; font-weight: 800; letter-spacing: .28em; color: #FFE9A8;
  text-shadow: 0 2px 2px rgba(0,0,0,.6), 0 0 18px rgba(255,220,130,.45); }}
.title {{ position: relative; display: grid; line-height: 1.06; font-weight: 800; letter-spacing: .02em; text-align: center; margin-top: 4px; }}
.title > span {{ grid-area: 1 / 1; white-space: nowrap; position: relative; }}
.title .shadow {{ z-index: 1; }} .title .glow {{ z-index: 2; }} .title .edge {{ z-index: 3; }} .title .face {{ z-index: 4; }}
.title .l1 {{ font-size: 106px; }} .title .l2 {{ font-size: 92px; display: block; margin-top: 4px; }}
.fl {{ display: block; width: 560px; height: 30px; margin-top: 6px; overflow: visible; }}
.title .shadow {{ color: #1A0E00; transform: translate(4px, 6px); filter: blur(1.5px); opacity: .85; }}
.title .glow {{ color: rgba(255, 222, 140, .9); filter: blur(16px); opacity: .9; }}
.title .edge {{ -webkit-text-stroke: 5px #3a2600; color: #3a2600; opacity: .95; }}
.title .face {{ background: linear-gradient(180deg, #FFFBE6 0%, #FDE9A6 22%, #F0C65E 42%, #C7922F 54%, #FFF3C9 66%, #E9C470 82%, #A9772A 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent; }}
.sub {{ margin-top: 10px; font-size: 42px; line-height: 1.22; font-weight: 900; color: #FFFFFF; text-align: center; letter-spacing: .04em;
  text-shadow: 0 2px 0 rgba(0,0,0,.35), 0 3px 10px rgba(10,5,40,.85), 0 0 26px rgba(90,40,140,.9); }}
.pill.mid {{ margin-top: 20px; font-size: 20px; padding: 8px 32px; }}
.cta {{ margin-top: 20px; display: inline-flex; align-items: center; gap: 16px; padding: 12px 60px 12px 52px; border-radius: 999px;
  background: linear-gradient(180deg, #FFF3C9 0%, #F4D783 25%, #D9A83E 60%, #F6DD94 100%); color: #1C1230; font-size: 40px; font-weight: 800; letter-spacing: .12em;
  box-shadow: 0 0 0 2px rgba(255,248,220,.6), 0 0 0 5px rgba(201,151,46,.9), 0 10px 26px rgba(0,0,0,.45), 0 0 40px rgba(255,214,120,.45); text-shadow: 0 1px 0 rgba(255,255,255,.5); }}
.cta .ar {{ font-size: 30px; font-weight: 700; margin-top: 2px; }}
.cta .st {{ color: #B8862B; font-size: 24px; }}
.name {{ position: absolute; left: 1052px; top: 640px; width: 86px; text-align: center; font-size: 15px; letter-spacing: .5em; color: #FFE9A8; font-weight: 700; text-shadow: 0 1px 3px rgba(0,0,0,.7); }}
'''


def page():
    scene = (f'<svg class="scene" viewBox="0 0 {W} {H}">{DEFS}'
             f'<rect width="{W}" height="{H}" fill="url(#horizon)"/>{stars()}{moon()}{mountains()}{town_left()}{castle_right()}{lake()}'
             f'<rect x="0" y="470" width="{W}" height="200" fill="#120E33"/>'
             f'{bokeh()}{aoi_right()}{vines()}{books_and_lantern()}'
             + ''.join(f'<g filter="url(#glow)">{star4(x, y, r, "#FFF3C4")}</g>' for x, y, r in [(292, 172, 13), (990, 142, 9), (214, 296, 8), (1066, 284, 12), (640, 118, 6), (960, 236, 5), (330, 262, 5)])
             + '</svg>')
    links = ''.join(f'<link rel="stylesheet" href="../node_modules/{f}">' for f in FONTS)
    html = f'''<!doctype html><html lang="ja"><head><meta charset="utf-8">{links}<style>{CSS}</style></head><body>
<div id="thumb">{scene}<div class="vig"></div>
<div class="col">
  <div class="pill serif top"><span>毒親育ち</span><span class="x">×</span><span>お金の不安</span><span class="x">×</span><span>1日5分</span></div>
  <div class="kicker mincho">毒親育ちの</div>
  <div class="title mincho">
    <span class="shadow"><span class="l1">お金の不安が</span><span class="l2">なくなる小さな習慣</span></span>
    <span class="glow"><span class="l1">お金の不安が</span><span class="l2">なくなる小さな習慣</span></span>
    <span class="edge"><span class="l1">お金の不安が</span><span class="l2">なくなる小さな習慣</span></span>
    <span class="face"><span class="l1">お金の不安が</span><span class="l2">なくなる小さな習慣</span></span>
  </div>
  <svg class="fl" viewBox="0 0 560 30">{DEFS}{flourish(280, 14, 540)}</svg>
  <div class="sub serif">もう、お金のことで<br>自分を責めなくていい。</div>
  <div class="pill serif mid">心と財布に余裕が生まれる、書き込み式の30日ワーク</div>
  <div class="cta mincho"><span class="st">✦</span>詳しく見る<span class="ar">›</span></div>
</div>
<div class="name mincho">アオ</div>
</div></body></html>'''
    out = ROOT / 'build' / 'thumb_night.html'
    out.write_text(html, encoding='utf-8')
    print(out)


if __name__ == '__main__':
    page()
