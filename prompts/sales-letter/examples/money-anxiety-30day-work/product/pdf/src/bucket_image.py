"""note用の図「穴の空いたバケツ」: python3 src/bucket_image.py && node src/shoot.mjs build/bucket.html ../../note/images bucket:2:07_bucket.png"""
import random, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import icon, ROOT
from build import FONTS
from note_images import CSS

rnd = random.Random(3)
NAVY, GOLD, BLUE, BLUE_D, RED = '#283265', '#C9A14B', '#7FB6E8', '#3A74C2', '#C25B6A'


def bill(x, y, rot, s=1.0):
    w, h = 56 * s, 30 * s
    return (f'<g transform="translate({x} {y}) rotate({rot})"><rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="3" fill="#EFE9D6" stroke="#B8AD8C" stroke-width="1.2"/>'
            f'<rect x="{-w / 2 + 4}" y="{-h / 2 + 4}" width="{w - 8}" height="{h - 8}" rx="2" fill="none" stroke="#B8AD8C" stroke-width=".8"/>'
            f'<circle r="{8 * s}" fill="#DCD3B4"/><text y="{4 * s}" text-anchor="middle" font-size="{11 * s}" font-weight="700" fill="#6B6A80" font-family="Zen Maru Gothic">¥</text></g>')


def coin(x, y, s=1.0):
    return (f'<g transform="translate({x} {y})"><circle r="{11 * s}" fill="#E9C66E" stroke="#B8862B" stroke-width="1.5"/>'
            f'<text y="{4.5 * s}" text-anchor="middle" font-size="{12 * s}" font-weight="700" fill="#8A5A00" font-family="Zen Maru Gothic">¥</text></g>')


def drops(x, y0, n, spread=10):
    out = []
    for i in range(n):
        yy = y0 + i * 16 + rnd.uniform(-3, 3); xx = x + rnd.uniform(-spread, spread) * (i / n)
        out.append(f'<path d="M{xx} {yy} q-3 -6 0 -9 q3 3 0 9z" fill="{BLUE}" opacity="{.9 - i * .07:.2f}" transform="rotate(180 {xx} {yy - 4.5})"/>')
    return ''.join(out)


def scene():
    bx, by = 330, 150  # バケツの中心上
    out = []
    # ジョウロからの水（上の注ぎ）
    out.append(f'<path d="M158 96 C 200 120 250 140 {bx - 40} {by + 6}" stroke="{BLUE}" stroke-width="8" fill="none" stroke-linecap="round" opacity=".9"/>'
               f'<path d="M158 96 C 200 120 250 140 {bx - 40} {by + 6}" stroke="#D6EAFB" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
               + ''.join(f'<circle cx="{x}" cy="{y}" r="2.2" fill="{BLUE}" opacity=".8"/>' for x, y in [(205, 112), (238, 140), (262, 150), (290, 170)]))
    # ジョウロ
    out.append('<g transform="translate(50 30)">'
               f'<rect x="0" y="22" width="78" height="52" rx="8" fill="{BLUE_D}"/><rect x="0" y="22" width="78" height="10" rx="5" fill="#2E5FA3"/>'
               f'<path d="M74 34 L108 62 L100 70 L70 48Z" fill="{BLUE_D}"/><circle cx="106" cy="66" r="8" fill="#2E5FA3"/>'
               f'<path d="M12 22 C 12 4 56 4 56 22" stroke="{BLUE_D}" stroke-width="6" fill="none"/></g>')
    out.append(f'<text x="40" y="128" font-size="15" font-weight="700" fill="{BLUE_D}" font-family="Zen Maru Gothic">家計簿・節約</text>'
               f'<text x="40" y="147" font-size="12.5" fill="#6A6A7E" font-family="Noto Sans JP">＝ 注ぎ方の工夫（悪くない）</text>')
    # バケツ
    out.append(f'<defs><linearGradient id="metal" x1="0" x2="1"><stop offset="0" stop-color="#9AA3B2"/><stop offset=".35" stop-color="#E3E8EF"/><stop offset=".6" stop-color="#B9C2CF"/><stop offset="1" stop-color="#7E8797"/></linearGradient>'
               f'<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A9D1F4"/><stop offset="1" stop-color="{BLUE_D}"/></linearGradient>'
               f'<clipPath id="bk"><path d="M{bx - 110} {by} L{bx - 84} {by + 200} L{bx + 84} {by + 200} L{bx + 110} {by}Z"/></clipPath></defs>')
    out.append(f'<path d="M{bx - 110} {by} L{bx - 84} {by + 200} L{bx + 84} {by + 200} L{bx + 110} {by}Z" fill="url(#metal)"/>')
    # 中の水（少ししかたまらない）
    out.append(f'<g clip-path="url(#bk)"><rect x="{bx - 120}" y="{by + 130}" width="240" height="100" fill="url(#water)" opacity=".9"/>'
               f'<ellipse cx="{bx}" cy="{by + 130}" rx="94" ry="9" fill="#C9E3F8"/></g>')
    out.append(f'<ellipse cx="{bx}" cy="{by}" rx="110" ry="16" fill="#D7DDE6" stroke="#8E97A6" stroke-width="3"/>'
               f'<ellipse cx="{bx}" cy="{by}" rx="98" ry="10" fill="#6E7788"/>'
               f'<path d="M{bx - 104} {by - 2} C {bx - 100} {by - 120} {bx + 100} {by - 120} {bx + 104} {by - 2}" stroke="#8E97A6" stroke-width="5" fill="none"/>'
               f'<rect x="{bx - 86}" y="{by + 196}" width="172" height="8" rx="3" fill="#6E7788"/>')
    # 底の穴と、もれ出るお金と水
    holes = [(bx - 52, 'もれ口'), (bx - 8, ''), (bx + 44, '')]
    for hx, _ in holes:
        out.append(f'<ellipse cx="{hx}" cy="{by + 200}" rx="9" ry="4" fill="#2B2F3A"/>')
        out.append(drops(hx, by + 212, 6, 14))
    for x, y, r, s in [(bx - 150, by + 262, -28, 1), (bx - 100, by + 300, 14, .95), (bx - 40, by + 275, -8, 1), (bx + 10, by + 310, 20, 1), (bx + 60, by + 268, -16, .95),
                       (bx + 120, by + 300, 36, .9), (bx - 60, by + 335, 30, .85), (bx + 150, by + 335, -22, .85), (bx + 50, by + 345, 8, .9)]:
        out.append(bill(x, y, r, s))
    for x, y in [(bx - 110, by + 250), (bx + 30, by + 245), (bx + 100, by + 262), (bx - 20, by + 350), (bx + 160, by + 285), (bx - 140, by + 320)]:
        out.append(coin(x, y))
    # ラベル：穴
    out.append(f'<path d="M{bx + 150} {by + 196} L{bx + 92} {by + 203}" stroke="{RED}" stroke-width="1.6" fill="none" marker-end="url(#ah)"/>'
               f'<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8z" fill="{RED}"/></marker></defs>'
               f'<text x="{bx + 154}" y="{by + 188}" font-size="15" font-weight="700" fill="{RED}" font-family="Zen Maru Gothic">底の穴</text>'
               f'<text x="{bx + 154}" y="{by + 208}" font-size="12.5" fill="#6A6A7E" font-family="Noto Sans JP">＝ 家で覚えた</text>'
               f'<text x="{bx + 154}" y="{by + 225}" font-size="12.5" fill="#6A6A7E" font-family="Noto Sans JP">「お金のルール」</text>')
    # ラベル：たまらない
    out.append(f'<text x="{bx + 128}" y="{by + 100}" font-size="14" font-weight="700" fill="{NAVY}" font-family="Zen Maru Gothic">どれだけ注いでも</text>'
               f'<text x="{bx + 128}" y="{by + 120}" font-size="14" font-weight="700" fill="{NAVY}" font-family="Zen Maru Gothic">たまらない</text>')
    return ''.join(out)


def main():
    links = ''.join(f'<link rel="stylesheet" href="../node_modules/{f}">' for f in FONTS)
    html = (f'<!doctype html><html lang="ja"><head><meta charset="utf-8">{links}<style>{CSS}'
            '.card svg.sc { width: 580px; height: 520px; display: block; margin: 0 auto; }</style></head><body>'
            '<div class="shot card" id="bucket"><div class="mg ttl">穴の空いたバケツに、<br>水を足していませんか？</div>'
            '<div class="lead">家計簿や節約は「注ぎ方」の工夫。穴は、そこにはありません</div>'
            f'<svg class="sc" viewBox="0 0 580 520">{scene()}</svg>'
            '<div class="foot"><div class="face"></div><div class="bb mg">直す場所は、注ぎ方ではなく、底の穴。<br>このワークでは、この穴を「もれ口」と呼びます。</div></div></div></body></html>')
    out = ROOT / 'build' / 'bucket.html'
    out.write_text(html, encoding='utf-8')
    print(out)


if __name__ == '__main__':
    main()
