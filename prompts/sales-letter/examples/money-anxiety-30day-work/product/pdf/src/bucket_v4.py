"""note用の図「穴の空いたバケツ」（v4の夜空の世界観・2560×1440）
python3 src/bucket_v4.py && Playwrightで #scene を 2560×1440 で撮り、note/images/07_bucket.jpg に保存
背景は assets/bg_night_v4.jpg（v4の見出し画像から文字を消したもの。src/clean_bg.py）
"""
import math, random, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import ROOT

W, H = 2560, 1440
rnd = random.Random(11)
FONTS = ['@fontsource/shippori-mincho-b1/800.css', '@fontsource/zen-maru-gothic/700.css']

# バケツの形
CX, TY, BY = 1560, 660, 1160
RXT, RYT, RXB, RYB = 262, 48, 200, 36


def rx_at(y):
    t = (y - TY) / (BY - TY)
    return RXT + (RXB - RXT) * t, RYT + (RYB - RYT) * t


def star4(x, y, r, c='#FFF6D8', op=1.0):
    k = r * .22
    return (f'<path d="M{x:.1f} {y - r:.1f} Q{x + k:.1f} {y - k:.1f} {x + r:.1f} {y:.1f} Q{x + k:.1f} {y + k:.1f} {x:.1f} {y + r:.1f} '
            f'Q{x - k:.1f} {y + k:.1f} {x - r:.1f} {y:.1f} Q{x - k:.1f} {y - k:.1f} {x:.1f} {y - r:.1f}Z" fill="{c}" opacity="{op}"/>')


def bez(p0, p1, p2, t):
    return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
            (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])


def jet(p0, p1, p2, w0, w1, n=40):
    """先が細くなる水流の形"""
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        x, y = bez(p0, p1, p2, t)
        x2, y2 = bez(p0, p1, p2, min(1, t + 1e-3))
        dx, dy = x2 - x, y2 - y
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        w = (w0 + (w1 - w0) * t) / 2
        left.append((x + nx * w, y + ny * w)); right.append((x - nx * w, y - ny * w))
    pts = left + right[::-1]
    return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + 'Z'


def coin(x, y, r, tilt, rot, op=1.0):
    ry = r * max(.28, abs(math.cos(math.radians(tilt))))
    th = r * .16
    return (f'<g transform="translate({x:.0f} {y:.0f}) rotate({rot})" opacity="{op}">'
            f'<ellipse cx="0" cy="{th:.1f}" rx="{r}" ry="{ry:.1f}" fill="#7A5214"/>'
            f'<ellipse cx="0" cy="0" rx="{r}" ry="{ry:.1f}" fill="url(#coin)"/>'
            f'<ellipse cx="0" cy="0" rx="{r * .78:.1f}" ry="{ry * .78:.1f}" fill="none" stroke="#9A6B1E" stroke-width="{r * .07:.1f}" opacity=".7"/>'
            f'<text x="0" y="{ry * .32:.1f}" text-anchor="middle" font-family="Shippori Mincho B1" font-weight="800" font-size="{r * 1.0:.0f}" fill="#8A5A12" '
            f'transform="scale(1 {ry / r:.2f})" opacity=".85">¥</text>'
            f'<ellipse cx="{-r * .3:.1f}" cy="{-ry * .35:.1f}" rx="{r * .32:.1f}" ry="{ry * .18:.1f}" fill="#FFF6D0" opacity=".7"/></g>')


def bill(x, y, rot, s=1.0):
    w, h = 150 * s, 72 * s
    return (f'<g transform="translate({x:.0f} {y:.0f}) rotate({rot}) skewX({rnd.uniform(-8, 8):.0f})" filter="url(#soft)">'
            f'<path d="M{-w / 2} {-h / 2} Q0 {-h / 2 - 8 * s} {w / 2} {-h / 2} L{w / 2} {h / 2} Q0 {h / 2 + 6 * s} {-w / 2} {h / 2}Z" fill="url(#paper)"/>'
            f'<rect x="{-w / 2 + 7 * s}" y="{-h / 2 + 7 * s}" width="{w - 14 * s}" height="{h - 14 * s}" rx="{4 * s}" fill="none" stroke="#B08A45" stroke-width="{1.6 * s}" opacity=".75"/>'
            f'<circle cx="{w * .2}" cy="0" r="{h * .26}" fill="none" stroke="#B08A45" stroke-width="{1.4 * s}" opacity=".7"/>'
            f'<text x="{w * .2}" y="{h * .1}" text-anchor="middle" font-family="Shippori Mincho B1" font-weight="800" font-size="{h * .34:.0f}" fill="#9A7230" opacity=".8">¥</text>'
            f'<path d="M{-w * .38} {-h * .12} L{-w * .02} {-h * .12} M{-w * .38} {h * .04} L{-w * .08} {h * .04} M{-w * .38} {h * .2} L{-w * .14} {h * .2}" stroke="#B08A45" stroke-width="{2 * s}" opacity=".55"/></g>')


DEFS = '''<defs>
<linearGradient id="metal" gradientUnits="userSpaceOnUse" x1="1298" y1="0" x2="1822" y2="0">
  <stop offset="0" stop-color="#1B1840"/><stop offset=".06" stop-color="#36336B"/><stop offset=".17" stop-color="#7A7EB8"/><stop offset=".27" stop-color="#C8CCEA"/>
  <stop offset=".33" stop-color="#F3F3FC"/><stop offset=".40" stop-color="#C4C8E8"/><stop offset=".55" stop-color="#8B8FC4"/><stop offset=".72" stop-color="#5C5C97"/>
  <stop offset=".88" stop-color="#383770"/><stop offset="1" stop-color="#1B1840"/></linearGradient>
<linearGradient id="metalV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".10"/><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#0A0820" stop-opacity=".55"/></linearGradient>
<linearGradient id="inner" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4A4A86"/><stop offset=".6" stop-color="#1E1C48"/><stop offset="1" stop-color="#121035"/></linearGradient>
<linearGradient id="gold" gradientUnits="userSpaceOnUse" x1="1298" y1="0" x2="1822" y2="0">
  <stop offset="0" stop-color="#5C3D0E"/><stop offset=".12" stop-color="#A97A2B"/><stop offset=".26" stop-color="#F0CF7C"/><stop offset=".33" stop-color="#FFF4CC"/>
  <stop offset=".42" stop-color="#E2B95E"/><stop offset=".62" stop-color="#B0812E"/><stop offset=".84" stop-color="#7A5418"/><stop offset="1" stop-color="#4A300A"/></linearGradient>
<linearGradient id="goldV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF4CC"/><stop offset=".3" stop-color="#EBC572"/><stop offset=".55" stop-color="#A9792A"/><stop offset=".75" stop-color="#6E4A16"/><stop offset="1" stop-color="#D9AC55"/></linearGradient>
<linearGradient id="brass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF0C2"/><stop offset=".16" stop-color="#EAC46C"/><stop offset=".42" stop-color="#B0822F"/><stop offset=".62" stop-color="#6E4A16"/><stop offset=".8" stop-color="#9C6E24"/><stop offset="1" stop-color="#E2BC66"/></linearGradient>
<linearGradient id="brassH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6E4A16"/><stop offset=".3" stop-color="#D9AF58"/><stop offset=".5" stop-color="#FFF0C2"/><stop offset=".7" stop-color="#C99A42"/><stop offset="1" stop-color="#5C3D0E"/></linearGradient>
<radialGradient id="coin" cx=".38" cy=".32" r=".8"><stop offset="0" stop-color="#FFF5CF"/><stop offset=".35" stop-color="#F2CF77"/><stop offset=".75" stop-color="#C08B2E"/><stop offset="1" stop-color="#8A5C16"/></radialGradient>
<linearGradient id="paper" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFF9EC"/><stop offset=".6" stop-color="#EFE3C6"/><stop offset="1" stop-color="#D8C79F"/></linearGradient>
<linearGradient id="water" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E9F7FF"/><stop offset=".5" stop-color="#9FD6FA"/><stop offset="1" stop-color="#6FA9F0"/></linearGradient>
<radialGradient id="glowC"><stop offset="0" stop-color="#BFE6FF" stop-opacity=".85"/><stop offset=".45" stop-color="#8FC8F5" stop-opacity=".35"/><stop offset="1" stop-color="#8FC8F5" stop-opacity="0"/></radialGradient>
<radialGradient id="glowG"><stop offset="0" stop-color="#FFE7A6" stop-opacity=".95"/><stop offset=".4" stop-color="#F5C35E" stop-opacity=".45"/><stop offset="1" stop-color="#F5C35E" stop-opacity="0"/></radialGradient>
<radialGradient id="pool" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#CDEBFF" stop-opacity=".75"/><stop offset=".5" stop-color="#7DB4F0" stop-opacity=".35"/><stop offset="1" stop-color="#5A7FD8" stop-opacity="0"/></radialGradient>
<radialGradient id="halo"><stop offset="0" stop-color="#B9A4FF" stop-opacity=".35"/><stop offset=".6" stop-color="#8E73E0" stop-opacity=".12"/><stop offset="1" stop-color="#8E73E0" stop-opacity="0"/></radialGradient>
<linearGradient id="beam" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#CFEAFF" stop-opacity=".55"/><stop offset="1" stop-color="#CFEAFF" stop-opacity="0"/></linearGradient>
<filter id="b2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2"/></filter>
<filter id="b6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="b14" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="b30" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="30"/></filter>
<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation=".8"/></filter>
<filter id="brushed" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.0025 0.05" numOctaves="3" seed="4" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 1.4 -0.55"/></filter>
<filter id="grain" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="9" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.5  0 0 0 0 0.45  0 0 0 0 0.6  0 0 0 0.9 -0.35"/></filter>
<filter id="rough" x="-30%" y="-30%" width="160%" height="160%">
  <feTurbulence type="fractalNoise" baseFrequency="0.18" numOctaves="2" seed="3"/><feDisplacementMap in="SourceGraphic" scale="7"/></filter>
<clipPath id="bodyClip"><path id="bodyPath" d="BODY"/></clipPath>
</defs>'''


def body_path():
    return (f'M{CX - RXT} {TY} L{CX - RXB} {BY} A{RXB} {RYB} 0 0 0 {CX + RXB} {BY} '
            f'L{CX + RXT} {TY} A{RXT} {RYT} 0 0 1 {CX - RXT} {TY}Z')


def band(y, w, op=1):
    rx, ry = rx_at(y)
    return (f'<path d="M{CX - rx:.1f} {y} A{rx:.1f} {ry:.1f} 0 0 0 {CX + rx:.1f} {y}" fill="none" stroke="#0E0C2A" stroke-width="{w + 6}" opacity=".45" transform="translate(0 4)"/>'
            f'<path d="M{CX - rx:.1f} {y} A{rx:.1f} {ry:.1f} 0 0 0 {CX + rx:.1f} {y}" fill="none" stroke="url(#gold)" stroke-width="{w}" opacity="{op}"/>'
            f'<path d="M{CX - rx * .9:.1f} {y - w * .22:.1f} A{rx * .9:.1f} {ry:.1f} 0 0 0 {CX + rx * .2:.1f} {y + ry * .98 - w * .22:.1f}" fill="none" stroke="#FFF6D6" stroke-width="{w * .18:.1f}" opacity=".55"/>')


def bucket():
    o = []
    # うしろの光と、地面の光のたまり
    o.append(f'<ellipse cx="{CX}" cy="{(TY + BY) / 2}" rx="520" ry="470" fill="url(#halo)"/>')
    o.append(f'<ellipse cx="{CX}" cy="{BY + 100}" rx="520" ry="64" fill="url(#pool)"/>')
    o.append(f'<ellipse cx="{CX}" cy="{BY + 98}" rx="300" ry="30" fill="#E2F3FF" opacity=".25" filter="url(#b14)"/>')
    for k, (rx, ry, op) in enumerate([(200, 22, .5), (300, 34, .35), (410, 48, .22)]):
        o.append(f'<ellipse cx="{CX + 20}" cy="{BY + 102}" rx="{rx}" ry="{ry}" fill="none" stroke="#D9EEFF" stroke-width="2.5" opacity="{op}"/>')
    # 水たまりに映るバケツ
    o.append(f'<g opacity=".16" filter="url(#b6)"><path d="{body_path()}" fill="url(#metal)" transform="translate(0 {2 * (BY + RYB) - 24}) scale(1 -1)"/></g>')
    # 影
    o.append(f'<ellipse cx="{CX + 10}" cy="{BY + 12}" rx="{RXB + 40}" ry="{RYB + 10}" fill="#07051A" opacity=".55" filter="url(#b14)"/>')
    # 取っ手（うしろ）
    lx, rx_, hy = CX - RXT + 14, CX + RXT - 14, TY + 30
    o.append(f'<path d="M{lx} {hy} C {lx + 10} {TY - 215} {rx_ - 10} {TY - 215} {rx_} {hy}" fill="none" stroke="#2A1E06" stroke-width="16" opacity=".5" transform="translate(4 6)"/>'
             f'<path d="M{lx} {hy} C {lx + 10} {TY - 215} {rx_ - 10} {TY - 215} {rx_} {hy}" fill="none" stroke="url(#goldV)" stroke-width="13"/>'
             f'<path d="M{lx} {hy} C {lx + 10} {TY - 215} {rx_ - 10} {TY - 215} {rx_} {hy}" fill="none" stroke="#FFF4CC" stroke-width="3" stroke-dasharray="300 2000" stroke-dashoffset="-40" opacity=".75" transform="translate(-2 -3)"/>')
    # 口の中（内側の壁と、奥で光る水）
    o.append(f'<ellipse cx="{CX}" cy="{TY}" rx="{RXT}" ry="{RYT}" fill="url(#inner)"/>')
    o.append(f'<ellipse cx="{CX}" cy="{TY + 12}" rx="{RXT * .8:.0f}" ry="{RYT * .55:.0f}" fill="url(#glowC)" opacity=".9"/>')
    # 口からのぼる光
    o.append(f'<path d="M{CX - 200} {TY} L{CX - 280} {TY - 240} L{CX + 280} {TY - 240} L{CX + 200} {TY}Z" fill="url(#beam)" opacity=".35" filter="url(#b14)"/>')
    # 胴
    bp = body_path()
    o.append(f'<path d="{bp}" fill="url(#metal)"/>')
    o.append(f'<g clip-path="url(#bodyClip)"><rect x="{CX - RXT}" y="{TY - RYT}" width="{2 * RXT}" height="{BY - TY + RYT + RYB}" fill="url(#metalV)"/>'
             f'<rect x="{CX - RXT}" y="{TY - RYT}" width="{2 * RXT}" height="{BY - TY + RYT + RYB}" filter="url(#brushed)" opacity=".07" style="mix-blend-mode:overlay"/>'
             # 右の縁の光（月）
             f'<path d="M{CX + RXT - 14} {TY} L{CX + RXB - 10} {BY}" stroke="#C9B8FF" stroke-width="16" opacity=".45" filter="url(#b6)"/>'
             # 左に映る水の光
             f'<ellipse cx="{CX - RXT + 70}" cy="{TY + 260}" rx="38" ry="230" fill="#A9D8FF" opacity=".18" filter="url(#b14)"/>'
             # 下のほうに映る、こぼれた水の光
             f'<ellipse cx="{CX}" cy="{BY + 10}" rx="{RXB}" ry="70" fill="#9FD3FF" opacity=".25" filter="url(#b14)"/>'
             '</g>')
    # 帯（金）
    for y, w in [(TY + 88, 14), (TY + 280, 9), (BY - 34, 16)]:
        o.append(band(y, w))
    # 小さなリベット
    for y in (TY + 88, BY - 34):
        rx, ry = rx_at(y)
        for a in (-0.82, -0.45, 0, 0.45, 0.82):
            px = CX + rx * a
            py = y + ry * math.sqrt(max(0, 1 - a * a))
            o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="url(#coin)"/>')
    # ふち（金の巻き）
    o.append(f'<path d="M{CX - RXT} {TY} A{RXT} {RYT} 0 0 1 {CX + RXT} {TY}" fill="none" stroke="url(#gold)" stroke-width="15"/>')  # 奥
    o.append(f'<path d="M{CX - RXT} {TY} A{RXT} {RYT} 0 0 0 {CX + RXT} {TY}" fill="none" stroke="#120E30" stroke-width="22" opacity=".5" transform="translate(0 6)"/>'
             f'<path d="M{CX - RXT} {TY} A{RXT} {RYT} 0 0 0 {CX + RXT} {TY}" fill="none" stroke="url(#gold)" stroke-width="19"/>'
             f'<path d="M{CX - RXT + 30} {TY + 18} A{RXT - 10} {RYT - 4} 0 0 0 {CX + 40} {TY + RYT - 2}" fill="none" stroke="#FFF6D6" stroke-width="4" opacity=".75"/>')
    # 取っ手の付け根
    for x in (lx, rx_):
        o.append(f'<circle cx="{x}" cy="{hy}" r="13" fill="url(#coin)" stroke="#6E4A16" stroke-width="2"/>')
    # 胴の飾り（金の細線の星）
    o.append(f'<g opacity=".55">{star4(CX - 60, TY + 190, 16, "#F6DE9A")}{star4(CX + 40, TY + 176, 9, "#F6DE9A")}{star4(CX - 10, TY + 220, 6, "#F6DE9A")}</g>')
    return ''.join(o)


HOLES = [(CX - 108, BY - 150, -1), (CX + 6, BY - 128, 0), (CX + 118, BY - 150, 1)]


def holes_and_leaks():
    o, front = [], []
    for i, (hx, hy, d) in enumerate(HOLES):
        # 穴
        o.append(f'<g filter="url(#rough)"><ellipse cx="{hx}" cy="{hy}" rx="17" ry="12" fill="#0B0820"/>'
                 f'<ellipse cx="{hx}" cy="{hy + 1}" rx="21" ry="15" fill="none" stroke="#3A2A10" stroke-width="3" opacity=".8"/></g>')
        # 水流
        if d < 0:
            p0, p1, p2 = (hx - 6, hy + 2), (hx - 160, hy - 20), (hx - 250, BY + 104)
        elif d > 0:
            p0, p1, p2 = (hx + 6, hy + 2), (hx + 170, hy - 24), (hx + 260, BY + 100)
        else:
            p0, p1, p2 = (hx + 2, hy + 6), (hx + 50, hy + 70), (hx + 70, BY + 112)
        shape = jet(p0, p1, p2, 26, 9)
        front.append(f'<path d="{shape}" fill="#8FCBF8" opacity=".55" filter="url(#b14)"/>'
                     f'<path d="{shape}" fill="url(#water)" opacity=".85"/>'
                     f'<path d="{jet(p0, p1, p2, 7, 2)}" fill="#FFFFFF" opacity=".85" filter="url(#b2)"/>')
        # しぶき
        ex, ey = p2
        for _ in range(9):
            sx, sy = ex + rnd.uniform(-46, 46), ey - rnd.uniform(0, 34)
            r = rnd.uniform(2.5, 6)
            front.append(f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="{r:.1f}" fill="#E6F6FF" opacity="{rnd.uniform(.5, .95):.2f}"/>')
        # 流れの中のきらめき
        for t in (.25, .5, .72):
            x, y = bez(p0, p1, p2, t)
            front.append(f'<g filter="url(#b2)">{star4(x + rnd.uniform(-10, 10), y + rnd.uniform(-10, 10), rnd.uniform(9, 16))}</g>')
    # まん中の穴の、金の目印（傷）
    hx, hy, _ = HOLES[2]
    front.append(f'<circle cx="{hx}" cy="{hy}" r="46" fill="url(#glowG)"/>'
                 f'<circle cx="{hx}" cy="{hy}" r="22" fill="none" stroke="#F7D98C" stroke-width="3"/>')
    return ''.join(o), ''.join(front)


def money():
    o = []
    # 流れ出たお金（コインとお札）
    coins = [(CX - 330, BY + 40, 30, 62, -18), (CX - 250, BY + 112, 26, 74, 8), (CX - 160, BY + 70, 22, 40, 20), (CX - 60, BY + 138, 28, 78, -6),
             (CX + 70, BY + 100, 24, 50, 14), (CX + 200, BY + 130, 30, 76, -10), (CX + 300, BY + 60, 26, 48, 22), (CX + 390, BY + 118, 24, 72, 4),
             (CX + 250, BY - 10, 20, 30, -30), (CX - 300, BY - 30, 18, 20, 30), (CX + 470, BY + 40, 20, 56, -14), (CX - 420, BY + 100, 22, 70, 12)]
    for x, y, r, tilt, rot in coins:
        o.append(f'<circle cx="{x}" cy="{y}" r="{r * 1.9:.0f}" fill="url(#glowG)" opacity=".35"/>' + coin(x, y, r, tilt, rot))
    for x, y, rot, s in [(CX - 430, BY + 40, -24, .9), (CX + 330, BY + 120, 18, .8)]:
        o.append(bill(x, y, rot, s))
    for _ in range(26):
        x, y = CX + rnd.uniform(-520, 540), BY + rnd.uniform(-160, 170)
        o.append(f'<g filter="url(#b2)">{star4(x, y, rnd.uniform(4, 11), rnd.choice(["#FFF3C4", "#FFFFFF", "#FFE08A"]), rnd.uniform(.5, 1))}</g>')
    return ''.join(o)


def watering_can():
    """真鍮のジョウロ。中心(0,0)で描いて、注ぐ角度に回す"""
    g = []
    # 本体
    body = 'M-150 -60 Q-150 -118 -96 -122 L96 -122 Q150 -118 150 -60 L156 82 Q156 112 124 114 L-122 114 Q-154 112 -154 82Z'
    g.append(f'<path d="{body}" fill="#2A1A04" opacity=".5" transform="translate(8 10)" filter="url(#b6)"/>')
    # 注ぎ口（下から右上へ）
    spout = 'M118 70 L330 -128 L346 -110 L140 100Z'
    g.append(f'<path d="{spout}" fill="url(#brassH)"/>'
             f'<path d="M126 74 L332 -120" stroke="#FFF2C4" stroke-width="4" opacity=".7"/>')
    # はす口
    g.append('<g transform="translate(340 -122) rotate(-43)">'
             '<path d="M-14 -16 L40 -46 L40 46 L-14 16Z" fill="url(#brassH)"/>'
             '<ellipse cx="40" cy="0" rx="12" ry="46" fill="url(#brass)" stroke="#6E4A16" stroke-width="3"/>'
             + ''.join(f'<circle cx="{43}" cy="{yy}" r="2.6" fill="#4A300A"/>' for yy in range(-36, 40, 12)) + '</g>')
    g.append(f'<path d="{body}" fill="url(#brass)"/>')
    # 胴の帯と彫り
    g.append('<path d="M-152 -70 L152 -70" stroke="#7A5418" stroke-width="4" opacity=".7"/><path d="M-154 70 L155 70" stroke="#7A5418" stroke-width="4" opacity=".7"/>'
             '<path d="M-152 -64 L152 -64" stroke="#FFF0C2" stroke-width="2" opacity=".6"/>')
    g.append('<path d="M-112 -8 C -90 -40 -60 -40 -44 -14 C -60 12 -90 12 -112 -8Z" fill="none" stroke="#7A5418" stroke-width="2.4" opacity=".6"/>'
             '<path d="M112 -8 C 90 -40 60 -40 44 -14 C 60 12 90 12 112 -8Z" fill="none" stroke="#7A5418" stroke-width="2.4" opacity=".6"/>')
    # 紺のメダリオンと金の星（アオの帽子と同じ）
    g.append('<circle cx="0" cy="0" r="46" fill="#1E2358" stroke="url(#goldV)" stroke-width="7"/>'
             '<circle cx="0" cy="0" r="37" fill="none" stroke="#C9A65B" stroke-width="1.5" opacity=".8"/>'
             '<path d="M0 -24 L6 -7 L24 -7 L10 4 L15 22 L0 11 L-15 22 L-10 4 L-24 -7 L-6 -7Z" fill="url(#goldV)"/>')
    # 上の持ち手と、うしろの持ち手
    g.append('<path d="M-104 -122 C -96 -232 96 -232 104 -122" fill="none" stroke="#2A1A04" stroke-width="22" opacity=".35" transform="translate(4 6)"/>'
             '<path d="M-104 -122 C -96 -232 96 -232 104 -122" fill="none" stroke="url(#goldV)" stroke-width="18"/>'
             '<path d="M-96 -130 C -86 -214 20 -224 60 -206" fill="none" stroke="#FFF4CC" stroke-width="4" opacity=".7"/>'
             '<path d="M-152 -60 C -236 -56 -236 70 -154 74" fill="none" stroke="url(#goldV)" stroke-width="18"/>'
             '<path d="M-156 -52 C -222 -46 -226 30 -196 50" fill="none" stroke="#FFF4CC" stroke-width="3.5" opacity=".6"/>')
    # 光沢
    g.append('<path d="M-118 -100 Q -120 -20 -110 90" stroke="#FFF7D8" stroke-width="12" opacity=".45" filter="url(#b6)" fill="none"/>'
             '<path d="M140 -96 Q 146 0 140 96" stroke="#C9B8FF" stroke-width="10" opacity=".35" filter="url(#b6)" fill="none"/>')
    return ''.join(g)


def pour():
    """ジョウロのはす口から、バケツの口へ"""
    o = []
    sx, sy = 1286, 572  # はす口の位置（回したあと）
    for k, (dy, tx, w0) in enumerate([(-26, CX - 150, 11), (-9, CX - 70, 13), (8, CX + 10, 12), (24, CX + 90, 10)]):
        p0 = (sx, sy + dy)
        p2 = (tx, TY + 6 + abs(k - 1.5) * 4)
        p1 = (p0[0] + (p2[0] - p0[0]) * .55, p0[1] - 34 + k * 6)
        shape = jet(p0, p1, p2, w0, w0 * .55)
        o.append(f'<path d="{shape}" fill="#8FCBF8" opacity=".45" filter="url(#b6)"/>'
                 f'<path d="{shape}" fill="url(#water)" opacity=".7"/>'
                 f'<path d="{jet(p0, p1, p2, 3.2, 1.6)}" fill="#FFFFFF" opacity=".8"/>')
        for t in (.3, .62):
            x, y = bez(p0, p1, p2, t)
            o.append(f'<g filter="url(#b2)">{star4(x, y, rnd.uniform(6, 11), "#FFFFFF", .9)}</g>')
    for _ in range(26):
        t = rnd.uniform(.05, 1)
        x = sx + (CX + 80 - sx) * t + rnd.uniform(-18, 18)
        y = sy - 20 + 120 * t * t + rnd.uniform(-30, 26)
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(1.6, 3.8):.1f}" fill="#EAF7FF" opacity="{rnd.uniform(.5, .95):.2f}"/>')
    o.append(f'<ellipse cx="{CX - 40}" cy="{TY + 4}" rx="170" ry="26" fill="#CFEAFF" opacity=".45" filter="url(#b14)"/>')
    return ''.join(o)


def leader(x1, y1, x2, y2, dashed=False):
    da = ' stroke-dasharray="10 9"' if dashed else ''
    return (f'<path d="M{x1} {y1} L{x2} {y2}" stroke="#E7C77A" stroke-width="3"{da} opacity=".95"/>'
            f'<circle cx="{x2}" cy="{y2}" r="11" fill="#F3D788" stroke="#FFF6D6" stroke-width="2"/>'
            f'<circle cx="{x2}" cy="{y2}" r="26" fill="url(#glowG)" opacity=".7"/>')


CSS = '''
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #111; }
#scene { position: relative; width: 2560px; height: 1440px; overflow: hidden; }
#scene > img.bg { position: absolute; inset: 0; width: 2560px; height: 1440px; }
#scene > svg { position: absolute; inset: 0; }
.mincho { font-family: 'Shippori Mincho B1', serif; font-weight: 800; }
.maru { font-family: 'Zen Maru Gothic', sans-serif; font-weight: 700; }
.head { position: absolute; left: 150px; top: 92px; text-align: left; }
.head .l1 { font-size: 54px; letter-spacing: .08em; color: #FFFFFF; text-shadow: 0 3px 14px rgba(10,6,40,.85); }
.head .l2 { display: inline-block; margin-top: 4px; font-size: 124px; letter-spacing: .04em; line-height: 1.12;
  background: linear-gradient(180deg, #FFF6D6 0%, #F7DC92 28%, #E2B24E 55%, #C08A2E 72%, #F4D486 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent;
  filter: drop-shadow(0 4px 0 rgba(40,20,0,.55)) drop-shadow(0 0 26px rgba(255,214,120,.35)); }
.box { position: absolute; background: rgba(16,14,56,.74); border: 3px solid #D9B86A; border-radius: 30px; padding: 34px 44px;
  box-shadow: 0 18px 40px rgba(5,3,25,.45), inset 0 0 0 1px rgba(255,240,200,.08); }
.box .t { font-size: 78px; line-height: 1.15; color: #FFFFFF; }
.box .t.g { background: linear-gradient(180deg, #FFF3CC 0%, #F2CF77 45%, #C99436 75%, #F3D58A 100%); -webkit-background-clip: text; background-clip: text; color: transparent; }
.box .s { margin-top: 14px; font-size: 40px; line-height: 1.5; color: #EDE8FF; letter-spacing: .02em; }
.box .s b { color: #F6D88A; font-weight: 700; }
.foot { position: absolute; left: 0; right: 0; bottom: 62px; text-align: center; font-size: 64px; color: #FFFFFF; letter-spacing: .05em;
  text-shadow: 0 3px 16px rgba(8,5,30,.95), 0 0 30px rgba(8,5,30,.8); }
.foot b { color: #F6D88A; }
.shade { position: absolute; left: 0; right: 0; bottom: 0; height: 360px; background: linear-gradient(180deg, rgba(10,8,34,0) 0%, rgba(10,8,34,.62) 55%, rgba(10,8,34,.78) 100%); }
'''


def page():
    links = ''.join(f'<link rel="stylesheet" href="../node_modules/{f}">' for f in FONTS)
    hole_svg, leak_svg = holes_and_leaks()
    defs = DEFS.replace('BODY', body_path())
    can = f'<g transform="translate(952 487) rotate(38) scale(.85)">{watering_can()}</g>'
    hx, hy, _ = HOLES[2]
    svg = (f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}">{defs}'
           f'{bucket()}{hole_svg}{money()}{leak_svg}{can}{pour()}'
           f'{leader(520, 880, 905, 600, dashed=True)}{leader(1860, 960, hx + 26, hy + 2)}</svg>')
    html = f'''<!doctype html><html lang="ja"><head><meta charset="utf-8">{links}<style>{CSS}</style></head><body>
<div id="scene"><img class="bg" src="../assets/bg_night_v4.jpg">{svg}
<div class="shade"></div>
<div class="head"><div class="l1 maru">どれだけ注いでも、たまらないのは</div><div class="l2 mincho">底に、穴があるから</div></div>
<div class="box" style="left:150px; top:880px; width:600px"><div class="t mincho">家計簿・節約</div><div class="s maru">＝ 注ぎ方の工夫。<br>やり方は、悪くない</div></div>
<div class="box" style="left:1860px; top:800px; width:620px"><div class="t g mincho">底の穴</div><div class="s maru">子どもの頃の傷＝<br><b>お金のメンタルブロック</b></div></div>
<div class="foot maru">直すのは「注ぎ方」ではなく、<b>底の穴</b>のほうです</div>
</div></body></html>'''
    out = ROOT / 'build' / 'bucket_v4.html'
    out.write_text(html, encoding='utf-8')
    print(out)


if __name__ == '__main__':
    page()
