"""ページ部品（アイコン・アオ・図解パーツ・ページ枠）"""
import pathlib, re
from html import escape

ROOT = pathlib.Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / 'node_modules' / 'lucide-static' / 'icons'
_icon_cache = {}


def icon(name, cls='ic', sw=2, style=''):
    if name not in _icon_cache:
        svg = (ICON_DIR / f'{name}.svg').read_text(encoding='utf-8')
        svg = re.sub(r'<!--.*?-->', '', svg, flags=re.S)
        head, rest = svg.split('>', 1)
        head = re.sub(r'\s(class|width|height)="[^"]*"', '', head)
        svg = head + '>' + rest
        svg = re.sub(r'\s+', ' ', svg).strip()
        _icon_cache[name] = svg
    svg = _icon_cache[name].replace('stroke-width="2"', f'stroke-width="{sw}"')
    st = f' style="{style}"' if style else ''
    return f'<span class="{cls}"{st}>{svg}</span>'


def aoi(size='', flip=False, extra=''):
    img = 'aoi_face_flip.png' if flip else 'aoi_face.png'
    return f'<div class="aoi {size}" style="background-image:url(../assets/{img});{extra}"></div>'


def paras(items):
    return ''.join(f'<p>{t}</p>' for t in items)


def talk(items, who='アオの話', rev=False, size='', ic='message-circle'):
    lab = f'<div class="who">{icon(ic, style="width:13px;height:13px")}{who}</div>' if who else ''
    return (f'<div class="talk{" rev" if rev else ""}">{aoi(size, flip=rev)}'
            f'<div class="bubble">{lab}{paras(items)}</div></div>')


def fig(title, inner, tip=None, rtip=False, tag='図解', style=''):
    t = ''
    if tip:
        t = (f'<div class="tip{" r" if rtip else ""}">{aoi("s", flip=rtip)}'
             f'<div class="tb">{tip}</div></div>')
    st = f' style="{style}"' if style else ''
    return (f'<div class="fig"{st}><div class="fh"><span class="tag">{tag}</span>'
            f'<span class="ft">{title}</span></div>{inner}{t}</div>')


def flow(steps, arrow='chevron-right'):
    out = []
    for i, s in enumerate(steps):
        if i:
            out.append(f'<div class="ar">{icon(arrow, sw=2.5)}</div>')
        num = f'<div class="num">{s["num"]}</div>' if s.get('num') else ''
        ico = f'<div class="ico">{icon(s["icon"])}</div>' if s.get('icon') else ''
        sub = f'<div class="s">{s["s"]}</div>' if s.get('s') else ''
        out.append(f'<div class="st{" hi" if s.get("hi") else ""}">{ico}{num}<div class="h">{s["h"]}</div>{sub}</div>')
    return f'<div class="flow">{"".join(out)}</div>'


def cards(items, cols=2, style=''):
    out = []
    for c in items:
        cc = f'--cc:{c["color"]};' if c.get('color') else ''
        bg = f'background:{c["bg"]};' if c.get('bg') else ''
        k = f'<div class="k">{c["k"]}</div>' if c.get('k') else ''
        ci = f'<div class="ci">{icon(c["icon"])}</div>' if c.get('icon') else ''
        s = f'<div class="s">{c["s"]}</div>' if c.get('s') else ''
        out.append(f'<div class="card{" sel" if c.get("sel") else ""}" style="{cc}{bg}">'
                   f'<div class="row">{ci}<div>{k}<div class="h">{c["h"]}</div></div></div>{s}</div>')
    st = f' style="{style}"' if style else ''
    return f'<div class="cards c{cols}"{st}>{"".join(out)}</div>'


def vs(a, b, mid='arrow-right'):
    def pn(cls, d):
        s = f'<div class="s">{d["s"]}</div>' if d.get('s') else ''
        ic = icon(d['icon'], style='width:13px;height:13px') if d.get('icon') else ''
        return f'<div class="pn {cls}"><div class="pl">{ic}{d["l"]}</div><div class="q">{d["q"]}</div>{s}</div>'
    return f'<div class="vs">{pn("a", a)}<div class="mid">{icon(mid, sw=2.5, style="width:6mm;height:6mm")}</div>{pn("b", b)}</div>'


def bars(rows, cls=''):
    out = []
    for r in rows:
        w = max(2, min(100, r['v'] / r.get('max', 100) * 100))
        out.append(f'<div class="bar{" g" if r.get("gray") else ""}"><div class="bl">{r["l"]}</div>'
                   f'<div class="bt"><div class="bf" style="width:{w:.1f}%;{r.get("st","")}"></div></div>'
                   f'<div class="bv">{r.get("d", r["v"])}</div></div>')
    return f'<div class="bars {cls}">{"".join(out)}</div>'


def stat(big, unit, label, style=''):
    return (f'<div class="stat" style="{style}"><div class="big">{big}<small>{unit}</small></div>'
            f'<div class="lbl">{label}</div></div>')


def lab_row(text, ic):
    return f'<div class="lab-row">{icon(ic)}<span>{text}</span></div>'


def deco_stars():
    s = icon('sparkle', sw=1.6)
    return (f'<div class="deco-star" style="top:9mm;right:12mm;width:5mm;height:5mm">{s}</div>'
            f'<div class="deco-star" style="top:14mm;right:8mm;width:3mm;height:3mm">{s}</div>')


class Book:
    """ページを順に積み、最後にページ番号と目次の参照を埋める"""

    def __init__(self):
        self.pages = []
        self.marks = {}

    def mark(self, key):
        self.marks[key] = len(self.pages) + 1

    def add(self, body, wk='start', run='', cls='', folio=True, raw=False, stars=False, bg=''):
        n = len(self.pages) + 1
        if raw:
            self.pages.append(f'<section class="page {cls} wk-{wk}">{body}</section>')
            return
        r = (f'<div class="run"><span class="run-l"><i></i>{run}</span>'
             f'<span>毒親育ちのお金の不安がなくなる小さな習慣</span></div>') if run else ''
        f = f'<div class="folio">{n}</div>' if folio else ''
        d = deco_stars() if stars else ''
        self.pages.append(f'<section class="page {cls} wk-{wk}">{bg}{d}{r}<div class="body">{body}</div>{f}</section>')

    def html(self):
        doc = '\n'.join(self.pages)
        for k, v in self.marks.items():
            doc = doc.replace('{{PG:%s}}' % k, str(v))
        return doc
