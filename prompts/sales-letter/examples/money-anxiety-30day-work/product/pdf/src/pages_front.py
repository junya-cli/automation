"""表紙・前付け・第1〜4章・30日ワークの扉"""
from lib import icon, aoi, talk, fig, flow, cards, vs, bars, stat, lab_row, paras

NOTE_URL = 'https://docs.google.com/document/d/1MtiOOO_1daacIk8Mfc6gGC205H8gvT42gDvBLhSxJ6o/copy'
LINE_URL = 'https://lin.ee/zx8oP4j'


def flower(size, color='#8A86D0', center='#E9D6AE', op=1):
    petals = ''.join(f'<ellipse cx="50" cy="27" rx="15" ry="24" fill="{color}" transform="rotate({a} 50 50)"/>' for a in range(0, 360, 72))
    return (f'<svg viewBox="0 0 100 100" style="width:{size}mm;height:{size}mm;opacity:{op}">{petals}'
            f'<circle cx="50" cy="50" r="11" fill="{center}"/></svg>')


def sparkle(size, color='#D9BE85'):
    return (f'<svg viewBox="0 0 24 24" style="width:{size}mm;height:{size}mm"><path fill="{color}" '
            f'd="M12 0C12.6 6.6 17.4 11.4 24 12C17.4 12.6 12.6 17.4 12 24C11.4 17.4 6.6 12.6 0 12C6.6 11.4 11.4 6.6 12 0Z"/></svg>')


def pos(html, top=None, left=None, right=None, bottom=None, extra=''):
    p = ''.join(f'{k}:{v}mm;' for k, v in (('top', top), ('left', left), ('right', right), ('bottom', bottom)) if v is not None)
    return f'<div style="position:absolute;{p}{extra}">{html}</div>'


# ---------- 小さな部品 ----------
def head(kicker, title, h1=False):
    t = f'<h1 class="title">{title}</h1>' if h1 else f'<h2 class="sec">{title}</h2>'
    return f'<div class="hd"><div class="kicker">{kicker}</div>{t}</div>'


def add(book, body, **kw):
    """前付け・章・付録の本文ページ（余白の自動調整の対象）"""
    kw.setdefault('cls', 'fp')
    book.add(body, **kw)


def memo(text):
    return (f'<div class="memo">{icon("book-open-text")}<span class="lab">研究メモ</span>'
            f'<div class="txt">{text}</div></div>')


def point(text, lab='POINT', style=''):
    st = f' style="{style}"' if style else ''
    return f'<div class="conclusion"{st}><span class="lab">{lab}</span><div class="txt">{text}</div></div>'


def ilist(items, ic='check', style=''):
    lis = ''.join(f'<li><span class="ib">{icon(x[0] if isinstance(x, tuple) else ic)}</span><span>{x[1] if isinstance(x, tuple) else x}</span></li>' for x in items)
    st = f' style="{style}"' if style else ''
    return f'<ul class="ilist"{st}>{lis}</ul>'


def nlist(items, style=''):
    st = f' style="{style}"' if style else ''
    return f'<ol class="nlist"{st}>' + ''.join(f'<li>{x}</li>' for x in items) + '</ol>'


def h3(text, ic=None):
    i = icon(ic, style='width:17px;height:17px;color:var(--wk);margin-right:2mm') if ic else ''
    return f'<h3 class="sub" style="display:flex;align-items:center">{i}{text}</h3>'


def tip(text, flip=False, style=''):
    """図解の外で使うアオのひとこと"""
    return (f'<div class="fig" style="background:transparent;border:0;padding:0;{style}"><div class="tip{" r" if flip else ""}" style="margin-top:0">{aoi("s", flip=flip)}'
            f'<div class="tb">{text}</div></div></div>')


def qr(name):
    return f'<div class="qr"><img src="../assets/{name}.svg" style="width:100%;height:100%;display:block"></div>'


WAVE = ('<svg class="wave" viewBox="0 0 210 16" preserveAspectRatio="none"><path fill="#FFFDF8" '
        'd="M0 9 C 30 0, 60 0, 92 7 S 160 16, 210 4 L210 16 L0 16 Z"/></svg>')

TYPES = [
    # 名前, 口ぐせ, アイコン, 色, 薄い色
    ('ため込みタイプ', '「減ったら終わり」', 'piggy-bank', '#3A74C2', '#E8F0FB'),
    ('人に出しすぎタイプ', '「自分の分は最後でいい」', 'hand-heart', '#C9677A', '#FBECEF'),
    ('がまん爆発タイプ', '「頑張った日だけ使っていい」', 'zap', '#C2862A', '#FBF1DE'),
    ('受け取れないタイプ', '「自分の値段は安くていい」', 'gift', '#8064BF', '#F1ECFA'),
    ('見ないふりタイプ', '「見なければ大丈夫」', 'eye-off', '#2A8B7F', '#E1F3F0'),
]


# ---------- 表紙 ----------
def cover(book):
    deco = (pos(flower(26, '#9C98DC', op=.55), top=196, left=4) + pos(flower(16, '#B6B3E8', op=.6), top=222, left=24) +
            pos(flower(20, '#9C98DC', op=.5), top=204, right=8) + pos(flower(12, '#C9C6EF', op=.7), top=228, right=30) +
            pos(sparkle(6), top=34, left=30) + pos(sparkle(4), top=46, left=22) + pos(sparkle(7), top=30, right=28) +
            pos(sparkle(4), top=44, right=40) + pos(sparkle(5), top=150, left=26) + pos(sparkle(6), top=140, right=24))
    title = (
        '<div style="position:absolute;top:30mm;left:0;right:0;text-align:center">'
        '<div style="display:inline-block;border:1.3px solid var(--gold);color:var(--gold);border-radius:99px;'
        'padding:1mm 6mm;font-family:Zen Maru Gothic;font-weight:700;font-size:10.5pt;letter-spacing:.25em;background:rgba(255,255,255,.7)">アダルトチルドレン必見</div>'
        '<div class="mg" style="font-weight:700;color:var(--navy);margin-top:7mm;line-height:1.3">'
        '<div style="font-size:21pt;letter-spacing:.12em">毒親育ちの</div>'
        '<div style="font-size:35pt;letter-spacing:.06em">お金の不安が</div>'
        '<div style="font-size:35pt;letter-spacing:.06em">なくなる小さな習慣</div></div>'
        f'<div style="display:flex;align-items:center;justify-content:center;gap:4mm;margin:5mm 0 3mm">'
        f'<span style="width:28mm;height:1px;background:var(--gold-l)"></span>{sparkle(4.5, "#C9A867")}<span style="width:28mm;height:1px;background:var(--gold-l)"></span></div>'
        '<div class="mg" style="font-weight:700;color:var(--navy-2);font-size:13.5pt;letter-spacing:.12em">心と財布に余裕が生まれる30日ワーク</div></div>')
    img = ('<div style="position:absolute;top:128mm;left:50%;width:104mm;height:104mm;margin-left:-52mm;border-radius:50%;'
           'background:#fff url(../assets/aoi_circle_600.png) center/cover no-repeat;'
           'box-shadow:0 0 0 2.5px #E8D6AE, 0 0 0 7px #fff, 0 0 0 8.2px #E8D6AE, 0 12px 30px rgba(40,50,101,.16)"></div>')
    pills = ''.join(f'<span style="display:inline-flex;align-items:center;gap:2mm;background:var(--navy);color:#fff;border-radius:99px;'
                    f'padding:1.4mm 5mm;font-family:Zen Maru Gothic;font-weight:700;font-size:10.5pt;letter-spacing:.08em">{icon(ic, style="width:13px;height:13px")}{t}</span>'
                    for ic, t in (('timer', '1日5分'), ('pencil', '書き込み式'), ('calendar-days', '30日')))
    bottom = (f'<div style="position:absolute;top:243mm;left:0;right:0;text-align:center"><div style="display:flex;gap:3mm;justify-content:center">{pills}</div>'
              '<div class="mg" style="margin-top:7mm;color:var(--navy);font-weight:700;font-size:13pt;letter-spacing:.4em">アオ</div></div>')
    book.add('<div class="frame"></div>' + deco + title + img + bottom, cls='cover', raw=True)


# ---------- 目次 ----------
def toc(book):
    items = [
        ('01', 'このワークで伝えたいこと', '', 'intro'),
        ('02', 'はじめに：このワークの使い方', 'アオの紹介／進め方／用意するもの／3つの約束', 'hajime'),
        ('03', '第1章　お金の不安の正体', '', 'ch1'),
        ('04', '第2章　お金のクセ・セルフチェック', 'セルフチェック20問／5つのタイプ', 'ch2'),
        ('05', '第3章　使ってないのにお金がない本当の理由', '4つの「もれ口」', 'ch3'),
        ('06', '第4章　心と財布に余裕をつくる3つの小さな習慣', '見る／分ける／ひと呼吸', 'ch4'),
        ('07', '30日ワーク　Day0〜Day30', 'Day0 スタートの日／1週目 見る／2週目 分ける／3週目 ほどく／4週目 決める／Day30 完成の日', 'work'),
        ('08', '付録', '心と財布の余裕プラン／進捗表とスキップ券／記録表／よくある質問', 'appendix'),
        ('09', 'このワークのあとに', 'ひとりで続ける方へ／個別セッションのご案内', 'after'),
    ]
    lis = ''.join(f'<li><span class="no">{n}</span><span class="tt">{t}{f"<small>{s}</small>" if s else ""}</span><span class="pg">{{{{PG:{k}}}}}</span></li>' for n, t, s, k in items)
    wk = [('Day0', 'スタートの日', '#283265', 'day0'), ('1週目', '見る', '#3A74C2', 'wk1'), ('2週目', '分ける', '#C2862A', 'wk8'),
          ('3週目', 'ほどく', '#8064BF', 'wk15'), ('4週目', '決める', '#2A8B7F', 'wk22'), ('Day30', '完成の日', '#B48C45', 'day30')]
    chips = ''.join(f'<div style="border-radius:3mm;background:#fff;border:1.3px solid {c};padding:1.6mm 2mm;text-align:center">'
                    f'<div class="mg" style="font-weight:700;color:{c};font-size:8pt;letter-spacing:.08em">{a}</div>'
                    f'<div class="mg" style="font-weight:700;color:var(--navy);font-size:10pt">{b}</div>'
                    f'<div style="font-size:7.6pt;color:var(--mute)">p.{{{{PG:{k}}}}}</div></div>' for a, b, c, k in wk)
    body = (head('CONTENTS', '目次', h1=True) +
            f'<ul class="toc">{lis}</ul>'
            f'<div class="mt4" style="display:grid;grid-template-columns:repeat(6,1fr);gap:2mm">{chips}</div>' +
            talk(['はじめての日は、「このワークで伝えたいこと」から第2章までを読めば大丈夫です。そのあとは、1日2ページずつ進みます。'], who='アオより', ic='sparkles') )
    body = body.replace('<div class="talk">', '<div class="talk" style="margin-top:7mm">')
    add(book, body, run='目次')


# ---------- このワークで伝えたいこと ----------
def message(book):
    book.mark('intro')
    habits = cards([
        {'icon': 'eye', 'k': '習慣 1', 'h': '見る', 's': '週に1回、5分だけお金を見る'},
        {'icon': 'layers', 'k': '習慣 2', 'h': '分ける', 's': '給料日に、使う前に先に分ける'},
        {'icon': 'wind', 'k': '習慣 3', 'h': 'ひと呼吸', 's': '「もし〜になったら、〜する」と1文だけ決めておく'},
    ], cols=3)
    flowfig = flow([
        {'icon': 'house', 'h': '子どもの頃の家', 's': '見て覚えた'},
        {'icon': 'cloud-rain', 'h': '「足りない」という受け止め方', 's': ''},
        {'icon': 'sprout', 'h': '30日・3つの小さな習慣で', 's': '少しずつゆるめる', 'hi': True},
    ])
    left = [('user-round', '自分のお金のクセ（5つのタイプのうち、強く出ている2つ）'),
            ('droplets', 'お金の<b>「もれ口」</b>（気づかないうちにお金が出ていくところ）と、見えていなかった出費の金額'),
            ('scroll-text', '「心と財布の余裕プラン」1枚')]
    body = (head('MESSAGE', 'このワークで伝えたいこと', h1=True) +
            point('お金の不安は、持っているお金の額よりも、<br>「足りない」という<span class="hl">受け止め方</span>から生まれます。<br>'
                  '<span style="font-size:10.6pt;font-weight:500;color:var(--ink)">その受け止め方は、子どもの頃に家で見て覚えたもの。だから、30日・3つの小さな習慣で、少しずつゆるめていけます。</span>',
                  style='margin-top:6mm') +
            fig('お金の不安は、こうして生まれ、こうしてゆるむ', flowfig, tag='全体図') +
            h3('身につけるのは、この3つの小さな習慣だけ', 'sparkles') + habits +
            h3('30日後に、手元に残るもの', 'gift') + ilist(left))
    add(book, body, run='このワークで伝えたいこと')


# ---------- はじめに ----------
def hajime_aoi(book):
    book.mark('hajime')
    portrait = ('<div style="width:58mm;height:58mm;border-radius:50%;flex:none;background:#fff url(../assets/aoi_circle_600.png) center/cover no-repeat;'
                'box-shadow:0 0 0 2px var(--gold-l), 0 0 0 5px #fff, 0 0 0 6px var(--gold-l), 0 8px 18px rgba(40,50,101,.14)"></div>')
    intro = ('<div style="flex:1">'
             '<div class="mg" style="font-weight:700;color:var(--gold);letter-spacing:.3em;font-size:9pt">GUIDE</div>'
             '<div class="mg" style="font-weight:700;color:var(--navy);font-size:22pt;letter-spacing:.2em;line-height:1.3">アオ</div>'
             '<div class="small" style="margin-bottom:2mm">この30日の案内役</div>'
             '<p class="lead">はじめまして、アオです。この30日、僕がとなりで案内します。</p></div>')
    story = paras(['僕は子どもの頃、いわゆる「いい子」でした。大人になってから、ストレスでめまいがして倒れたことがあります。そのあと「アダルトチルドレン」という言葉に出会い、ずっと抱えてきたしんどさに、やっと名前がついた夜がありました。'])
    st = ('<div class="box tint" style="display:flex;align-items:center;gap:6mm;margin:4mm 0 5mm">' +
          stat('250', '人', 'いまは1対1のセッションで、<br>これまで250人の方と向き合ってきました。') + '</div>')
    sample = ('<div class="box" style="margin-top:2mm"><h4>' + icon('message-circle') + '毎日のページの最初に、「アオの話」があります</h4>'
              '<p class="small" style="margin-bottom:2.4mm">その日のテーマについて、僕が少しだけ話します。たとえば、こんなふうに。</p>' +
              talk(['「足りない」と感じるとき、何がどれくらい足りないのか、すぐに答えられますか。答えられなくても大丈夫です。'], size='s') + '</div>')
    body = (head('はじめに：このワークの使い方', 'このワークは、アオが案内します') +
            f'<div style="display:flex;gap:8mm;align-items:center;margin:5mm 0 6mm">{portrait}{intro}</div>' + story + st + sample)
    add(book, body, run='はじめに')


def hajime_plan(book):
    rows = [('Day0', 'スタートの日', 'セルフチェックで、今の自分を知る', '#283265'),
            ('Day1〜7', '見る', 'お金の流れと、気づかないうちにお金が出ていく「もれ口」を見る', '#3A74C2'),
            ('Day8〜14', '分ける', 'お金を「安心ボックス」「特別費」「使っていいお金」の3つに分ける', '#C2862A'),
            ('Day15〜21', 'ほどく', '家で覚えたお金の口ぐせに気づいて、少しずつゆるめる', '#8064BF'),
            ('Day22〜29', '決める', 'お金を見る日、断る一言、「もしもの一文」を決める', '#2A8B7F'),
            ('Day30', '完成', 'あなただけの「余裕プラン」ができる', '#B48C45')]
    tl = '<div class="tl">' + ''.join(
        f'<div class="tr" style="--c:{c}"><div class="td">{d}</div><div class="tdot"><i></i></div>'
        f'<div class="tc"><span class="tt">{t}</span><span class="tx">{x}</span></div></div>' for d, t, x, c in rows) + '</div>'
    steps = nlist(['最初の日だけ、第1章と第2章を読みます（約15分）。セルフチェックの20問に答えたら、それでDay0は完了です。',
                   '第3章と第4章は、Day1〜7のあいだに少しずつ読みます。',
                   'Day1からは、1日2ページずつ進めます（1日5分）。'])
    body = (head('はじめに：このワークの使い方', '1日5分、4週間で進みます') +
            fig('30日の地図', tl, tip='1週ごとに、ページの色が変わります。今どこにいるか、色で分かります。', tag='図解') +
            f'<div class="box tint"><h4>{icon("footprints")}進め方</h4>{steps}</div>')
    add(book, body, run='はじめに')


def hajime_prepare(book):
    pens = ''.join(f'<span class="dotc" style="background:var(--c-{c});margin-right:1mm"></span>' for c in ('blue', 'yellow', 'green', 'gray'))
    c4 = cards([
        {'icon': 'file-text', 'k': '1', 'h': 'このPDF', 's': '印刷するか、スマホ用の書き込みノートで'},
        {'icon': 'pen-tool', 'k': '2', 'h': 'ペン', 's': f'4色あると、色分けメモが楽です<br>{pens}'},
        {'icon': 'landmark', 'k': '3', 'h': 'お金の記録', 's': '銀行アプリ・通帳・カードの明細'},
        {'icon': 'receipt', 'k': '4', 'h': 'レシート', 's': '最近のものを1枚'},
    ], cols=2)

    def qbox(name, ttl, ic, txt, url):
        return (f'<div class="box" style="display:flex;gap:5mm;align-items:center">{qr(name)}<div>'
                f'<h4>{icon(ic)}{ttl}</h4><p class="small" style="margin:0 0 1.4mm">{txt}</p>'
                f'<div style="font-size:7pt;color:var(--mute);word-break:break-all;line-height:1.4">{url}</div></div></div>')
    body = (head('はじめに：このワークの使い方', '始める前に、4つだけ用意します') +
            fig('用意するもの', c4, tip='全部そろっていなくても大丈夫。今あるもので始めましょう。') +
            h3('スマホで書きたい方・困ったときの窓口', 'smartphone') +
            '<div style="display:flex;flex-direction:column;gap:3.4mm">' +
            qbox('qr_note', '書き込みノート（スマホ用）', 'notebook-pen',
                 'Day0〜30の書く欄が、1つのGoogleドキュメントにまとまっています。QRを開くと、自分用のコピーが作れます。', NOTE_URL) +
            qbox('qr_line', '購入者限定LINE', 'message-circle-heart',
                 'よくある質問の追加、ワークで手が止まったときのヒント、Day30のあとのご案内をお届けします。', LINE_URL) +
            '</div>')
    add(book, body, run='はじめに')


def hajime_twopages(book):
    def mp(title, blocks, color):
        bl = ''.join(f'<div class="mb" style="background:{bg};height:{h}mm">{t}</div>' for t, bg, h in blocks)
        return (f'<div class="mini-page"><div class="mh">{title}</div>{bl}</div>')
    read = mp('1ページ目｜読む', [('DAY　今日のタイトル', '#E8F0FB', 8), ('今日のゴール', '#E8F0FB', 6), ('アオの話', '#FFFFFF;border:1px solid #E8F0FB', 9),
                                ('図解', '#F5F3EE', 14), ('なぜ？', '#FFFFFF;border:1px dashed #E6E1D4', 6), ('今日の5分 □', '#FFFFFF;border:1px dashed #E6E1D4', 9)], '')
    write = mp('2ページ目｜書く', [('記入例', '#FFFCF5;border:1px dashed #E8D6AE', 8), ('書く欄', '#FFFFFF;border:1px solid #E6E1D4', 20),
                                 ('メモ・気づいたこと', '#FFFFFF;border:1px solid #E6E1D4', 11), ('研究メモ', '#FAF6EC', 5), ('アオのひとこと　□', '#F8F1E2', 7)], '')
    spread = (f'<div class="mini-spread">{read}<div style="display:flex;align-items:center;color:var(--wk)">{icon("arrow-right", style="width:7mm;height:7mm")}</div>{write}</div>'
              '<div class="center mt3 mg" style="font-weight:700;color:var(--navy);font-size:11pt">読む5分のあとに、書く。1日はこの2ページだけです。</div>')
    legend = ('<div class="legend">'
              f'<div class="lg"><div class="sw"><span class="chip" style="background:var(--gold-xl);color:var(--gold)">★ タイプ名</span></div><div class="lt"><b>★がついている日</b>特定のタイプに特によく効く日です。自分のタイプでなければ、読むだけでもかまいません。</div></div>'
              f'<div class="lg"><div class="sw"><span class="chip" style="background:var(--cream);color:var(--gold)">{icon("book-open-text", style="width:12px;height:12px")}研究メモ</span></div><div class="lt"><b>研究メモ</b>その日の内容の根拠になった研究の紹介です。読み飛ばしてかまいません。</div></div>'
              f'<div class="lg"><div class="sw"><span class="chip" style="background:#FDECEE;color:#B04A5A">重い日</span></div><div class="lt"><b>重い日</b>親の話など、少し深いところに触れる日です。つらければ飛ばしてかまいません。</div></div>'
              f'<div class="lg"><div class="sw"><span class="chip" style="background:var(--lav-l);color:#5E4596">{icon("life-buoy", style="width:12px;height:12px")}止まったら</span></div><div class="lt"><b>つまずきポイント</b>手が止まりやすい日には、止まる理由と、ひとりでできることを用意しています。</div></div>'
              '</div>')
    body = (head('はじめに：このワークの使い方', '1日は2ページ、5分で終わります') +
            fig('1日の2ページ', spread, tag='図解') +
            h3('ページの中の目じるし', 'map-pin') + legend +
            tip('右上の□は、やったらチェック。終わったら、付録2の進捗表のマスを塗りましょう。', style='margin-top:5mm'))
    add(book, body, run='はじめに')


def hajime_rest(book):
    sq = ''.join(f'<span style="width:7mm;height:7mm;border-radius:1.6mm;border:1.3px solid {"var(--navy)" if i < 2 else "var(--line)"};'
                 f'background:{"var(--navy)" if i < 2 else "#fff"};display:inline-block"></span>' for i in range(32))
    grid = f'<div style="display:grid;grid-template-columns:repeat(16,7mm);gap:1.6mm;justify-content:center">{sq}</div>'
    tk = ''.join(f'<div class="ticket" style="padding:1.6mm 1mm"><div class="tk">SKIP</div><div class="tn" style="font-size:8.6pt">スキップ券</div></div>' for _ in range(8))
    tk = f'<div style="display:grid;grid-template-columns:repeat(8,1fr);gap:1.6mm">{tk}</div>'
    days7 = [0, 5, 9, 12, 19, 29, 30]
    colors = {0: '#283265', 5: '#3A74C2', 9: '#C2862A', 12: '#C2862A', 19: '#8064BF', 29: '#2A8B7F', 30: '#B48C45'}
    course = ''.join(f'<div style="text-align:center;flex:1"><div style="width:11mm;height:11mm;border-radius:50%;background:{colors[d]};color:#fff;'
                     f'display:flex;align-items:center;justify-content:center;margin:0 auto;font-family:Zen Maru Gothic;font-weight:700;font-size:10pt">{d}</div>'
                     f'<div style="font-size:7.6pt;color:var(--sub);margin-top:1mm">Day{d}</div></div>' for d in days7)
    course = (f'<div style="position:relative;display:flex;gap:1mm"><div style="position:absolute;left:8%;right:8%;top:5.5mm;height:1.4px;background:var(--line)"></div>{course}</div>')
    body = (head('はじめに：このワークの使い方', '休んでも大丈夫。次の日に戻ればOKです') +
            fig('進捗表は32マス', grid + '<div class="center small mt2">「買った」＋Day0〜Day30。Day0が終わったら、最初の2マスを塗ります。</div>', tag='図解') +
            fig('スキップ券は8枚', tk + '<div class="center small mt2">書けない日は、×ではなく「スキップ」と書きます。</div>', tag='図解') +
            fig('時間がない人は、7日だけでも一周できます', course,
                tip='Day0・5・9・12・19・29・30の7日だけでも、ひと回りできるように作っています。', tag='7日コース') +
            memo('1日休んでも、習慣づくりへの影響はほとんどなかった、という研究があります（Lally ほか, 2010）。'))
    add(book, body, run='はじめに')


def hajime_promise(book):
    pr = [('heart', 'あなたを責めません', 'お金のクセは、性格ではなく、家で見て覚えたものだからです。'),
          ('hand', '親を許さなくていい', '親と向き合う必要も、許す必要もありません。'),
          ('skip-forward', 'つらいページは飛ばしていい', 'Day16のような重い日は、飛ばしても一周できます。')]
    rows = ''.join(f'<div style="display:flex;gap:5mm;align-items:center;background:#fff;border:1.4px solid var(--gold-l);border-radius:4mm;padding:4.4mm 5mm;margin-bottom:3.4mm">'
                   f'<div style="width:14mm;height:14mm;border-radius:50%;background:var(--gold-xl);color:var(--gold);display:flex;align-items:center;justify-content:center;flex:none">{icon(ic, style="width:7mm;height:7mm")}</div>'
                   f'<div><div class="mg" style="font-size:8.4pt;font-weight:700;color:var(--gold);letter-spacing:.14em">約束 {i + 1}</div>'
                   f'<div class="mg" style="font-weight:700;color:var(--navy);font-size:14pt;line-height:1.4">{t}</div><div style="font-size:9.8pt;color:var(--sub)">{s}</div></div></div>'
                   for i, (ic, t, s) in enumerate(pr))
    body = (head('はじめに：このワークの使い方', 'このワークは、あなたを責めません') +
            talk(['ここだけは、先に約束させてください。'], who='アオより', ic='sparkles') + rows +
            '<div class="box cream mt4"><p style="margin:0;font-size:9.6pt">アダルトチルドレン（AC）は、病名や診断名ではありません。いまの生きづらさが、子どもの頃の親との関係から来ていると、自分で気づいた人が使う言葉です（信田さよ子, 2016）。このワークも、治療ではありません。</p></div>')
    add(book, body, run='はじめに')


def hajime_stuck(book):
    book.mark('tsumazuki')
    flags = [(13, 'つまずき①'), (20, 'つまずき②'), (28, 'つまずき③')]
    pct = lambda d: 3 + d / 30 * 94
    fl = ''.join(f'<div class="fl" style="left:{pct(d):.1f}%"><div class="fb">{t}</div><div class="pole"></div><div class="pt"></div></div>' for d, t in flags)
    lb = ''.join(f'<div class="lb" style="left:{pct(d):.1f}%">Day{d}</div>' for d in (0, 7))
    lb += f'<div class="lb" style="left:{pct(30):.1f}%;color:var(--gold)">完成</div>'
    lb += ''.join(f'<div class="lb" style="left:{pct(d):.1f}%;color:#5E4596">Day{d}</div>' for d, _ in flags)
    road = f'<div class="road"><div class="ln"></div>{fl}{lb}</div>'
    items = ['<b>つまずき①</b>　使っていいお金を決めたのに、何に使いたいのか分からない（Day13）',
             '<b>つまずき②</b>　頭では分かったのに、気持ちが変わらない（Day20）',
             '<b>つまずき③</b>　決めたのに、できない日がある（Day28）']
    body = (head('はじめに：このワークの使い方', '途中で手が止まりやすい日が、3つあります') +
            '<p>30日のうち、多くの人が手を止めやすい日が3日あります。このワークでは<b>「つまずきポイント」</b>と呼んでいます。</p>' +
            fig('30日の中の、3つのつまずきポイント', road + '<div class="wk-loosen">' + nlist(items, style='margin-top:2mm') + '</div>',
                tip='止まるのは、手を抜かずに進んできたからです。その日のページに、止まる理由と、ひとりでできることを用意しています。', tag='図解') +
            '<div class="stopbox"><div>' + icon('life-buoy', style='width:22px;height:22px;color:#5E4596') + '</div><div>'
            '<div class="t">3日以上、止まったままのときは</div>'
            '<p>巻末の「このワークのあとに」（p.{{PG:after}}）も読んでみてください。</p></div></div>')
    add(book, body, run='はじめに')


def hajime_can(book):
    can = ilist(['お金の流れが見えるようになる', '自分のお金のクセ（タイプ）が分かる', 'お金を分ける仕組みができる', '困る場面で使う「一言」が決まる'], ic='check')
    hard = ilist(['子どもの頃の経験が、今の生きづらさにどうつながっているかを、深く整理すること',
                  '頭では分かっているのに動かない気持ちを、ひとりで動かすこと',
                  'お金以外の場面（人間関係や仕事）にも出ている同じクセに、取り組むこと'], ic='circle-help')
    berg = ('<div class="berg"><svg viewBox="0 0 176 92" preserveAspectRatio="none">'
            '<polygon points="110,27.6 116,20 121,15 126,8 131,11 136,14 142,21 150,27.6" fill="#FFFFFF" stroke="#9AA6D6" stroke-width=".5"/>'
            '<polygon points="102,27.6 158,27.6 166,38 163,52 169,64 156,78 134,87 114,83 101,72 96,56 99,41" fill="rgba(255,255,255,.55)" stroke="#8E9AD0" stroke-width=".5"/>'
            '<polyline points="126,27.6 122,45 131,62 124,80" fill="none" stroke="#B9C2E6" stroke-width=".4"/><polyline points="142,27.6 148,48 140,70" fill="none" stroke="#B9C2E6" stroke-width=".4"/>'
            '<line x1="0" y1="27.6" x2="176" y2="27.6" stroke="#7F8EC9" stroke-width=".5" stroke-dasharray="2 1.4"/></svg>'
            '<div class="lab" style="left:6mm;top:5mm;width:90mm"><b style="color:var(--navy)">水面の上：このワークで扱うところ</b>お金の流れ・あなたのタイプ・分ける仕組み・困る場面の一言</div>'
            '<div class="wl" style="top:22.5mm;left:6mm">水面</div>'
            '<div class="lab" style="left:6mm;top:36mm;width:84mm"><b style="color:#3D4A8A">水面の下：ひとりでは見えにくいところ</b>子どもの頃の家で覚えた「自分の扱い方」、頭では分かっているのに動かない気持ち、お金以外の場面に出ている同じクセ</div>'
            '<div class="mg" style="position:absolute;left:112mm;top:52mm;width:46mm;text-align:center;font-weight:700;color:#3D4A8A;font-size:10pt;line-height:1.5">根っこは、<br>ここにあることも</div>'
            f'<div style="position:absolute;left:6mm;bottom:5mm">{aoi("s")}</div></div>')
    body = (head('はじめに：このワークの使い方', 'このワークでできること、ひとりでは難しいこと') +
            '<p>始める前に、正直にお伝えしておきます。</p>' +
            f'<div class="grid2" style="margin-bottom:4mm"><div class="box tint"><h4>{icon("circle-check")}このワークでできること</h4>{can}</div>'
            f'<div class="box" style="background:var(--lav-l);border-color:transparent"><h4 style="color:#5E4596">{icon("circle-help", style="width:16px;height:16px;color:#8064BF")}このワークだけでは難しいこと</h4><div class="wk-loosen">{hard}</div></div></div>' +
            fig('お金のクセは、氷山の「見えている部分」', berg, tag='図解') +
            '<p>このワークは、まず「お金」という、目に見えて数字で確かめられるところから始めます。</p>'
            '<p>30日やってみて、それでも残るものがあれば、それはあなたの努力が足りないのではありません。<b>根っこが、ひとりでは見えにくい場所にある</b>というサインです。'
            'そのときのために、巻末に個別セッションのご案内（p.{{PG:session}}）を用意しています。</p>')
    add(book, body, run='はじめに')


# ---------- 章扉 ----------
def chapter_open(book, key, no, title, conclusion, intro, list_title, items, wk, run, extra=''):
    book.mark(key)
    bg = f'<div class="chop-bg"><div class="no">{no:02d}</div>{WAVE}</div>'
    hd = (f'<div class="chop-head"><div class="ck">CHAPTER {no}</div><div class="ct">{title}</div><div class="bar"></div>'
          f'<div class="chop-aoi"></div></div>')
    body = (hd + point(conclusion, lab='この章の結論', style='margin-top:4mm') + paras(intro) +
            (f'<div class="box tint mt3"><h4>{icon("list-checks")}{list_title}</h4>{nlist(items)}</div>' if items else '') + extra)
    add(book, body, wk=wk, run=run, bg=bg)


# ---------- 第1章 ----------
def ch1(book):
    run = '第1章　お金の不安の正体'
    chapter_open(book, 'ch1', 1, 'お金の不安の正体',
                 'お金の不安の正体は、持っているお金の額ではなく、<br>「足りない」という<span class="hl">受け止め方</span>です。',
                 ['給料日の夜なのに、残高のアプリを開けない。大きな買い物はしていないのに、なぜかいつも足りない気がする。そんな夜に覚えがあるなら、この章を読んでみてください。'],
                 'この章でわかること',
                 ['お金の不安は、2つの部分でできている', '不安の大きさは、お金の額では決まらない',
                  '「足りない」という感じ方は、家で見て覚えたもの。それが消えないのには、2つの理由がある'], 'start', run)

    # 2つの部分 ＋ 額では決まらない
    two = ('<div style="display:flex;align-items:stretch;gap:0">' +
           '<div class="card" style="flex:1;text-align:center;padding:4mm"><div class="ci" style="margin:0 auto 1.6mm">' + icon('wallet') + '</div>'
           '<div class="k">1</div><div class="h" style="font-size:11.4pt">今月のやりくりのしんどさ</div>'
           '<div class="mg" style="font-weight:700;color:var(--wk);margin-top:1.6mm">「今月、足りるかな」</div></div>'
           '<div style="width:12mm;display:flex;align-items:center;justify-content:center;font-family:Zen Maru Gothic;font-weight:700;color:var(--wk);font-size:20pt">＋</div>'
           '<div class="card" style="flex:1;text-align:center;padding:4mm"><div class="ci" style="margin:0 auto 1.6mm">' + icon('compass') + '</div>'
           '<div class="k">2</div><div class="h" style="font-size:11.4pt">この先の安心のなさ</div>'
           '<div class="mg" style="font-weight:700;color:var(--wk);margin-top:1.6mm">「この先、大丈夫かな」</div></div></div>')
    st2 = ('<div class="grid2">' +
           '<div class="box tint">' + stat('74.5', '%', '資産が<b>100万ドル以上</b>ある人のうち、「完全に幸せになるには、今の2倍以上必要」と答えた人') + '</div>'
           '<div class="box tint">' + stat('約7', '割', '資産が<b>1,000万ドル以上</b>ある人でも、「2倍以上必要」と答えた人') + '</div></div>')
    body = (head('第1章', 'お金の不安は、2つの部分でできています') +
            fig('お金の不安＝2つが混ざったもの', two, tip='混ざったままだと、どこから手をつければいいのか分からない。だから、2つを分けて扱います。') +
            '<p>お金の不安は、この2つが混ざってできています。このワークでは、2つを分けて扱います。</p>' +
            memo('お金の不安が「今月のやりくり」と「この先の安心」の2つでできていることは、研究で確かめられています（Netemeyer ほか, 2018）。') +
            '<div class="sep2"></div>' +
            head('第1章', '不安の大きさは、お金の額では決まりません') + st2 +
            '<p class="mt3">どれだけ持っていても、「足りない」という感じ方は消えません。お金の不安の正体は、額ではなく、<b>「足りない」という受け止め方</b>です。</p>' +
            memo('すでに十分幸せだと答えた人などを除いた887人の調査です（Donnelly ほか, 2018）。生活の満足と結びついていたのは、年収より「口座に今いくらあるか」だった、という研究もあります（Ruberton ほか, 2016）。'))
    add(book, body, run=run)

    # 家で見て覚えた ＋ マシュマロ
    homes = cards([{'icon': 'message-square-warning', 'h': '「うちはお金がない」が口ぐせの家'},
                   {'icon': 'cloud', 'h': 'お金の話になると、空気が重くなる家'},
                   {'icon': 'shuffle', 'h': '親の機嫌しだいで、お金がもらえたり、もらえなかったりする家'}], cols=3)
    mm = bars([{'l': '破られた', 'v': 3, 'max': 12, 'd': '3分', 'gray': True}, {'l': '守ってもらえた', 'v': 12, 'max': 12, 'd': '12分'}], cls='wide')
    body = (head('第1章', '「足りない」という感じ方は、家で見て覚えたものです') +
            '<div class="box tint" style="margin-bottom:3mm">' + stat('15.2', '%', '家で親から、お金の使い方を<b>教わる機会があった人</b>は、これだけしかいません。') + '</div>' +
            '<p>教わってはいないのに、見て覚えてはいる。たとえば、こんな家です。</p>' + homes +
            memo('子どもはお金について、「教わったこと」より、親が「やって見せたこと」から学ぶとされています。7歳ごろまでに、お金の使い方につながる考え方の多くが育つ、という報告もあります（Whitebread & Bingham, 2013）。15.2%は、金融経済教育推進機構（J-FLEC）「金融リテラシー調査」2025年。').replace('class="memo"', 'class="memo" style="margin-top:3mm"') +
            '<div class="sep2"></div>' +
            head('第1章', '子どもの頃に身についたルールには、ちゃんと理由がありました') +
            fig('「待てたら、もう1つあげる」と言われた子どもが、待てた時間（平均）', mm + '<div class="small center mt2">大人に約束を「破られた」子どもと、「守ってもらえた」子ども</div>',
                tip='待てるかどうかは、性格より「ここは約束が守られる場所か」で変わりました。') +
            '<p>約束が守られない場所では、「今もらえるものを、今もらう」のは、かしこい判断です。お金のクセも同じで、当時のあなたを守っていたルールが、今も動き続けているだけなのかもしれません。</p>' +
            memo('3〜5歳の子どもに「待てたら、もう1つあげる」と伝えた実験です。その前に大人が約束を破ったかどうかで、待てる時間が変わりました（Kidd ほか, 2013）。'))
    add(book, body, run=run)

    # 理由① ＋ 理由②
    loop = ('<div class="loop">' + flow([{'icon': 'cloud-rain', 'h': '不安'}, {'icon': 'eye-off', 'h': '見ない'},
                                         {'icon': 'circle-help', 'h': '分からない'}, {'icon': 'cloud-lightning', 'h': 'もっと不安', 'hi': True}]) +
            '<div class="back"><span>くり返し</span></div></div>')
    line = ('<div style="position:relative;height:30mm;margin:2mm 2mm 0">'
            '<div style="position:absolute;left:0;right:0;top:9mm;height:7mm;border-radius:99px;background:linear-gradient(90deg,#F2EFE7 0 58%, var(--wk-t) 58%)"></div>'
            '<div style="position:absolute;left:58%;top:2mm;bottom:6mm;border-left:2px dashed var(--wk)"></div>'
            '<div class="mg" style="position:absolute;left:58%;top:-1mm;transform:translateX(-50%);background:var(--wk);color:#fff;font-weight:700;font-size:8.6pt;border-radius:99px;padding:0 3mm;white-space:nowrap">安心ライン</div>'
            '<div style="position:absolute;left:0;width:56%;top:18mm;text-align:center;font-size:9pt;color:var(--sub)">安心ラインがないと……<br><b style="color:#77768A">いつまでも「足りない」</b></div>'
            '<div style="position:absolute;left:60%;right:0;top:18mm;text-align:center;font-size:9pt;color:var(--sub)">安心ラインを越えたら……<br><b>「大丈夫」と言える</b></div></div>')
    body = (head('第1章', '「足りない」が消えない理由①　お金の流れを見ていない') +
            '<div class="box tint" style="margin-bottom:3mm">' + stat('27.8', '%', '1か月にいくら使っているか<b>把握していない人</b>') + '</div>' +
            '<p>見ないのは、だらしないからではありません。<b>不安だから、見られない</b>のです。</p>' +
            fig('このくり返しの中にいると……', loop, tip='「足りない」は一度も確かめられないまま、ずっと正しいことになってしまいます。') +
            memo('借金や赤字があると、人は口座を見る回数が減る、という研究があります（Olafsson & Pagel, 2017）。27.8%は、J-FLEC「金融リテラシー調査」2025年。'))
    add(book, body, run=run)
    body = (head('第1章', '「足りない」が消えない理由②　この先に要るお金が分からない') +
            '<div class="box tint" style="margin-bottom:3mm">' + stat('30.0', '%', '急な出費に備えた生活費を<b>確保していない人</b>') + '</div>' +
            '<p>何にいくら要るのかが分からないと、「ここまであれば大丈夫」という金額が決められません。このワークでは、この金額を<b>「安心ライン」</b>と呼びます。</p>' +
            fig('安心ラインを決めると、不安に終わりが来る', line) +
            '<p>大事なのは、大きな額を貯めることではなく、手元に少しでも貯えがあることです。</p>' +
            memo('安心感と強く結びついていたのは、手元にある少しの貯えでした（米国消費者金融保護局, 2017）。30.0%は、J-FLEC「金融リテラシー調査」2025年。'))
    add(book, body, run=run)

    # 本当に足りない／足りない気がする
    tree = ('<div class="center"><span class="mg" style="display:inline-block;background:var(--navy);color:#fff;border-radius:3mm;padding:2mm 6mm;font-weight:700;font-size:11pt">お金の不安</span></div>'
            '<div class="center" style="color:var(--wk)">' + icon('arrow-down', style='width:6mm;height:6mm') + '</div>'
            '<div class="center"><span class="mg" style="display:inline-flex;align-items:center;gap:2mm;background:var(--wk-t);color:var(--wk-d);border-radius:3mm;padding:2mm 6mm;font-weight:700;font-size:11pt">' + icon('eye', style='width:15px;height:15px') + 'まず「見る」（1週目）</span></div>'
            '<svg viewBox="0 0 160 12" style="width:100%;height:10mm;display:block" preserveAspectRatio="none"><path d="M80 0 V5 M40 5 H120 M40 5 V12 M120 5 V12" stroke="#9AA0C3" stroke-width=".8" fill="none"/></svg>'
            '<div class="grid2">'
            '<div class="box" style="border-color:#D5D2DC"><h4 style="color:#55546A">' + icon('scale', style='width:16px;height:16px;color:#77768A') + '本当に足りない不安</h4>'
            '<p class="small" style="margin:0 0 2mm">数字で見ても、本当に足りない</p>'
            '<div style="background:#F3F2F0;border-radius:2.4mm;padding:2mm 3mm;font-weight:700;color:var(--navy);font-size:9.6pt">→ 仕組みで、実際にお金を足していく</div></div>'
            '<div class="box" style="border-color:var(--wk)"><h4>' + icon('cloud-fog') + '足りない気がする不安</h4>'
            '<p class="small" style="margin:0 0 2mm">数字では足りているのに、「足りない」と感じる</p>'
            '<div style="background:var(--wk-t);border-radius:2.4mm;padding:2mm 3mm;font-weight:700;color:var(--navy);font-size:9.6pt">→ 安心ラインを決めて、お金の口ぐせを書き直す</div></div></div>')
    body = (head('第1章', '不安には、「本当に足りない不安」と「足りない気がする不安」があります') +
            fig('どちらの不安かは、見てみるまで分からない', tree,
                tip='だからこのワークは、最初の1週間を「見る」ことに使います。') +
            '<p>どちらなのかは、見てみるまで分かりません。だからこのワークは、最初の1週間を「見る」ことに使います。</p>' +
            memo('「人の行動の95%は無意識」とよく言われますが、この数字を測った研究はありません。測られているのは、「毎日の行動の約4割は、ほぼ毎日同じ場所でくり返す習慣」ということです（Wood ほか, 2002）。'))
    add(book, body, run=run)


# ---------- 第2章 ----------
QUESTIONS = ['用もないのに、残高を何度も確かめてしまう', '人のためのお金はすぐ出せるのに、自分のためだと迷う', '頑張った日や疲れた日に、まとめて買ってしまう',
             '給料や値段の話を、自分から切り出せない', '明細やカードの利用額を見るのが怖くて、後回しにしている', 'いくら貯まっても「まだ足りない」と感じる',
             '家族や近い人に頼まれると、理由を聞く前に出してしまう', 'しばらく我慢したあと、反動で一気に使うことがある', '見積もりや希望の金額を、出す直前に下げてしまう',
             '月末にお金が足りなくなる理由が、自分でもよく分からない', '「何かあったときのため」と思うと、必要なものでも買えない', '会計のとき、つい多めに払ってしまう',
             '「これだけ頑張ったんだから」と自分に言い聞かせて使う', '「私なんかが、これをもらっていいのかな」と思う', '予算を決めても、気づくと続いていない',
             '貯金を崩すくらいなら、我慢するほうを選ぶ', '自分の分は、いつもいちばん最後に回している', '買ったあとで「なんで買ったんだろう」と落ち込む',
             '褒め言葉やお礼を、すぐに打ち消してしまう', '自分がいくら持っているか、だいたいでも言えない']

TYPE_PAGES = [
    {'point': '貯める力は本物です。安心ライン（ここまであれば大丈夫、という金額）を決めれば、その力が安心に変わります。',
     'scene': '残高を何度も確かめる。必要なものでも買えない。いくら貯まっても足りない気がする。',
     'why': 'お金が減ることが、「危ないこと」と結びついています。研究で「お金に用心深い型」と呼ばれるクセに近いものです。',
     'trap': '目標額を上げ続けること。安心ラインがないかぎり、「足りない」は終わりません。',
     'todo': ['安心ラインを、金額で決める', 'お金を見る日を決めて、それ以外の日は見ない', '「使っていいお金」を、貯金とは別に分ける'],
     'if': ('用もなく残高を開きたくなったら', '「見るのは日曜」と声に出して、アプリを閉じる'),
     'memo': 'Klontz ほか, 2011。', 'days': 'Day2・8・22'},
    {'point': '人の困りごとに気づける力は本物です。人に出すお金の「枠」と「上限」を先に決めれば、自分の分を守れます。',
     'scene': '人のためにはすぐ出せるのに、自分には使えない。頼まれると断れない。会計で多めに払ってしまう。',
     'why': '家の空気を守るために、自分を後回しにしてきたのかもしれません。人に合わせる性格の人ほど、貯金が少なく、借金や支払いの遅れが多い、という研究があります。',
     'trap': '「人のために使うと幸せになれる」と信じて、もっと出すこと。気持ちが満たされるのは、自分で選んで助けたときです。',
     'todo': ['人に出すお金の「枠」と「上限」を、先に決める', '出すのは、自分で選んだときだけにする', '頼まれたときの、断る一言を用意する'],
     'if': ('お金のことを頼まれたら', '「一晩考えるね」と言ってから決める'),
     'memo': 'Matz & Gladstone, 2020／Weinstein & Ryan, 2010。', 'days': 'Day6・12・23・25'},
    {'point': '自分をいたわる力があります。ごほうびを「頑張ったかどうか」から切り離せば、その力が味方になります。',
     'scene': '我慢が続いたあと、まとめて使う。お金が入った月に消える。買ったあとで落ち込む。',
     'why': 'お金を使うのに、「頑張った」という許可が必要になっています。人は、頑張りが大きいほど、ぜいたくなごほうびを選びやすくなります。',
     'trap': '「頑張ったかどうか」を、使っていい条件にし続けること。0か100かの使い方から抜けられなくなります。',
     'todo': ['頑張りとは関係なく、「予定に入れた小さな楽しみ」を週1回入れる', '落ち込んだ日は、買い物アプリで「選ぶ」ところまでにして閉じる', '使いすぎやすい場面だけ、支払いにひと手間を足す'],
     'if': ('疲れた夜に買いたくなったら', 'カートに入れて閉じ、明日の朝もう一度見る'),
     'memo': 'Kivetz & Simonson, 2002。', 'days': 'Day6・12・26・27'},
    {'point': '相手の立場に立てる力があります。自分に言い聞かせるより、自分が大事にしていることから動くと変わります。',
     'scene': '値段や給料の話ができない。見積もりを出す直前に下げる。褒め言葉やお礼を受け取れない。',
     'why': '「自分はそれに値しない」と感じると、人は自分へのぜいたくを控えるようになります。',
     'trap': '「私はお金を受け取っていい」と、鏡の前で言い聞かせること。自分への評価が低いときは、かえって気分が悪くなることがあります。',
     'todo': ['言い聞かせるかわりに、「大事にしていること」を書く', 'それに沿った、小さなお金の使い道を1つ試す', '値段や希望を、「すみません」を付けずに言い切る一文をつくる'],
     'if': ('値段を聞かれたら', '「すみません」を付けずに、金額だけを言う'),
     'memo': 'Cavanaugh, 2014／Wood ほか, 2009。', 'days': 'Day12・24・25'},
    {'point': '自分を守る力があります。守り方を「見ない」から「少しだけ見る」に変えていきます。',
     'scene': '明細を開かない。予算を決めても続かない。使っていないはずなのに、お金がない。',
     'why': '見ないことで、不安から自分を守っています。不安があると、人は口座を見なくなります。',
     'trap': '「今日から家計簿を毎日つける」と、いきなり全部を見ようとすること。不安が大きすぎて、また見なくなります。',
     'todo': ['お金を見る日を、週に1回だけ決める', '給料日に先に取り分けるお金を、自動にする', '記録は、1日1行だけにする'],
     'if': ('日曜の夜になったら', 'お茶をいれてから、5分だけ残高を見る'),
     'memo': 'Olafsson & Pagel, 2017／Klontz ほか, 2012。', 'days': 'Day2・8・22・27'},
]


def type_style(t):
    return f'--wk:{t[3]};--wk-t:{t[4]};--wk-d:{t[3]};--tc:{t[3]};--tt:{t[4]}'


def ch2(book):
    run = '第2章　お金のクセ・セルフチェック'
    chapter_open(book, 'ch2', 2, 'お金のクセ・<br>セルフチェック',
                 'お金のクセは、5つのタイプに分かれます。点数が高い2つ（<span class="hl">あなたの2タイプ</span>）が分かると、30日で特にやることが決まります。',
                 ['まずは、今の自分のクセを知るところから。20問、気楽に答えてみてください。',
                  '<span class="small">このチェックは、「お金についての思い込みには、いくつかの型がある」という研究（Klontz ほか, 2011）を参考に、アオが作ったものです。医学的・心理学的な診断ではありません。今のあなたの「傾向」を知るためのものです。</span>'],
                 'この章でやること',
                 ['セルフチェック20問に答える（これがDay0）', '点数を足して、あなたの2タイプを見つける', '自分のタイプのページを読む'], 'loosen', run)

    # セルフチェック
    book.mark('selfcheck')
    rows = ''.join(f'<tr><td class="n">{i + 1}</td><td>{q}</td><td class="o">' + ''.join(f'<span>{v}</span>' for v in range(4)) + '</td></tr>'
                   for i, q in enumerate(QUESTIONS))
    body = (head('第2章｜Day0でやること', '最近1か月のあなたに、0〜3で答えてください') +
            '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.6mm"><span class="small">考えこまず、パッと浮かんだ数字に丸をつけてください。</span>'
            '<div class="scale" style="margin:0"><span>0 当てはまらない</span><span>1 少し</span><span>2 かなり</span><span>3 とても当てはまる</span></div></div>' +
            f'<table class="qlist">{rows}</table>' +
            '<div class="small mt2" style="display:flex;align-items:center;gap:2mm">' + icon('smartphone', style='width:14px;height:14px;color:var(--wk)') +
            '書き込みノートにも、同じ20問と合計の表があります。</div>')
    add(book, body, wk='loosen', run=run)

    # 集計
    tr = ''.join(f'<tr><td class="k" style="--wk:{t[3]}"><span style="display:inline-flex;align-items:center;gap:2mm;color:{t[3]}">{icon(t[2], style="width:16px;height:16px")}<span style="color:var(--navy)">{t[0]}</span></span></td>'
                 f'<td><span class="chip" style="background:{t[4]};color:{t[3]}">{nums}</span></td><td style="width:34mm"><span style="display:inline-block;width:20mm;border-bottom:1.2px dotted #C9C3B3;height:6mm"></span> 点</td></tr>'
                 for t, nums in zip(TYPES, ['1・6・11・16', '2・7・12・17', '3・8・13・18', '4・9・14・19', '5・10・15・20']))
    tbl = f'<table class="tbl"><tr><th>タイプ</th><th>足す番号</th><th>合計（0〜12点）</th></tr>{tr}</table>'
    ex = bars([{'l': 'ため込み', 'v': 9, 'max': 12, 'd': '9点', 'st': 'background:#3A74C2'},
               {'l': '人に出しすぎ', 'v': 7, 'max': 12, 'd': '7点', 'st': 'background:#C9677A'},
               {'l': '見ないふり', 'v': 5, 'max': 12, 'd': '5点', 'gray': True},
               {'l': '受け取れない', 'v': 4, 'max': 12, 'd': '4点', 'gray': True},
               {'l': 'がまん爆発', 'v': 3, 'max': 12, 'd': '3点', 'gray': True}], cls='wide')
    fill = ('<div class="box" style="display:flex;align-items:center;gap:3mm;border:1.6px solid var(--wk);margin-top:4mm">'
            '<span class="mg" style="font-weight:700;color:var(--wk);white-space:nowrap">わたしの2タイプ</span>'
            '<span style="flex:1;border-bottom:1.2px dotted #C9C3B3;height:8mm"></span><span>／</span><span style="flex:1;border-bottom:1.2px dotted #C9C3B3;height:8mm"></span></div>')
    body = (head('第2章', '点数を足して、あなたの2タイプを見つけます') + tbl + fill +
            '<p class="mt3">点数が高い2つが、<b>あなたの2タイプ</b>です。同点なら両方を読んでください。全部が4点未満なら、いちばん高いタイプを1つ読めば十分です。タイプは、混ざっていて当たり前です。</p>' +
            fig('例）ある人の合計点', ex,
                tip='この人の2タイプは、「ため込みタイプ」と「人に出しすぎタイプ」です。', tag='例'))
    add(book, body, wk='loosen', run=run)

    # 相談 ＋ 不安メーター
    meter = ('<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:3mm">' +
             ''.join(f'<div style="text-align:center;background:{bg};border-radius:3.5mm;padding:3mm 2mm"><div class="mg" style="font-weight:700;color:{c};font-size:14pt">{d}</div>'
                     f'<div class="small">{s}</div><div class="mg" style="font-weight:700;color:var(--navy);font-size:10pt">{t}</div></div>'
                     for d, s, t, c, bg in [('Day0', 'はじめ', '今の自分を知る', '#283265', '#ECEEF6'), ('Day15', 'まんなか', '測り直す', '#8064BF', '#F1ECFA'),
                                            ('Day30', '完成の日', '30日前と比べる', '#B48C45', '#F8F1E2')]) + '</div>')
    qs = nlist(['今月のお金のことを考えると、不安はどれくらいですか？（0〜10）', 'これから1〜3年のお金のことを考えると、不安はどれくらいですか？（0〜10）',
                '1か月にいくら使っているか、だいたい分かりますか？（はい／いいえ）', '急な出費に備えたお金（生活費の1か月分くらい）はありますか？（はい／いいえ／分からない）'])
    body = (head('第2章', '1つでも当てはまったら、ワークより先に相談してください') +
            '<div class="warn"><h4>' + icon('triangle-alert', style='width:18px;height:18px') + 'こんなときは、先に相談を</h4>' +
            '<ul class="ilist" style="--wk:#C25B6A;--wk-t:#FBE3E6">' + ''.join(f'<li><span class="ib">{icon("circle-alert")}</span><span>{x}</span></li>' for x in
                                                                        ['買い物をやめたいのにやめられず、隠したり、うそをついたりしている', '借金やリボ払いの返済のために、別の借り入れをしている',
                                                                         '眠れない・食べられないなどの不調が、2週間以上続いている']) + '</ul>'
            '<p style="margin:2mm 0 0;font-size:9.8pt">当てはまるときは、ひとりで抱えずに、医療機関や専門の窓口に相談してください。このワークは、そのあとからでも始められます。</p>'
            '<p class="small" style="margin:1mm 0 0">※巻末の個別セッションも、医療や専門の窓口の代わりにはなりません。</p></div>' +
            '<div class="sep2"></div>' +
            head('第2章', 'お金の不安メーターで、30日の変化を確かめます') +
            '<p>Day0・Day15・Day30に、同じ4つの質問に答えます。</p>' +
            fig('3回、同じ質問に答える', meter + '<div class="mt3">' + qs + '</div>', tip='答えは、付録3の記録表（p.{{PG:record}}）に書きます。'))
    add(book, body, wk='loosen', run=run)

    # 5タイプ一覧
    book.mark('types')
    tr = ''.join(f'<tr><td class="k"><span style="display:inline-flex;align-items:center;gap:2mm"><span style="width:8mm;height:8mm;border-radius:50%;background:{t[4]};color:{t[3]};display:inline-flex;align-items:center;justify-content:center">{icon(t[2], style="width:4.6mm;height:4.6mm")}</span>{t[0]}</span></td>'
                 f'<td class="mg" style="font-weight:700;color:{t[3]}">{t[1]}</td><td>{s}</td><td style="width:14mm;font-size:8pt;color:var(--mute)">p.{{{{PG:type{i}}}}}</td></tr>'
                 for i, (t, s) in enumerate(zip(TYPES, ['残高を何度も確かめる', '人には出せるのに、自分には使えない', '我慢のあとに、まとめて使う', '値段や給料の話ができない', '明細を開かない'])))
    hand = ('<div style="display:flex;justify-content:center;gap:4mm;margin-top:2mm">' +
            ''.join(f'<div style="text-align:center;width:31mm"><div style="width:18mm;height:18mm;border-radius:50%;background:{t[4]};color:{t[3]};display:flex;align-items:center;justify-content:center;margin:0 auto">{icon(t[2], style="width:9mm;height:9mm")}</div>'
                    f'<div class="mg" style="font-weight:700;color:var(--navy);font-size:8.6pt;margin-top:1.4mm;white-space:nowrap">{t[0]}</div></div>' for t in TYPES) + '</div>')
    body = (head('第2章', 'お金のクセは、5つのタイプに分かれます') +
            fig('5つのタイプ', hand, tag='一覧') +
            f'<table class="tbl" style="--wk:var(--navy)"><tr><th>タイプ</th><th>心の中の口ぐせ</th><th>よく出る場面</th><th></th></tr>{tr}</table>' +
            tip('次のページから、タイプごとに読んでいきます。あなたの2タイプのページを読めば十分です。', style='margin-top:6mm'))
    add(book, body, wk='loosen', run=run)

    for i, (t, d) in enumerate(zip(TYPES, TYPE_PAGES)):
        book.mark(f'type{i}')
        hero = (f'<div class="type-hero"><div class="ti">{icon(t[2])}</div><div><div class="kicker" style="color:{t[3]}">TYPE {i + 1}</div>'
                f'<div class="tn">{t[0]}</div><div class="tq">{t[1]}</div></div>'
                f'<div style="margin-left:auto;text-align:center">{aoi("", extra="width:22mm;height:22mm")}</div></div>')
        kv = ('<div class="kv">' +
              f'<div class="k">{icon("map-pin", style="width:15px;height:15px")}よく出る場面</div><div class="v">{d["scene"]}</div>'
              f'<div class="k">{icon("lightbulb", style="width:15px;height:15px")}なぜ</div><div class="v">{d["why"]}</div>'
              f'<div class="k">{icon("triangle-alert", style="width:15px;height:15px")}やりがちな<br>落とし穴</div><div class="v">{d["trap"]}</div></div>')
        todo = '<ol class="steps">' + ''.join(f'<li>{x}<span class="chk"></span></li>' for x in d['todo']) + '</ol>'
        ift = (f'<div class="ifthen"><div class="if"><div class="k">もし</div><div class="v">{d["if"][0]}</div></div>'
               f'<div class="ar">{icon("arrow-right", sw=2.5, style="width:5mm;height:5mm")}</div>'
               f'<div class="th"><div class="k">する</div><div class="v">{d["if"][1]}</div></div></div>')
        body = (hero + point(d['point'], style='margin-top:5mm') + kv +
                f'<div class="blk mt4">{lab_row("30日でやること3つ", "list-checks")}{todo}</div>' +
                f'<div class="blk">{lab_row("もしもの一文の例", "wind")}{ift}</div>' +
                f'<div class="small" style="display:flex;align-items:center;gap:2mm;margin-bottom:3mm">{icon("star", style="width:13px;height:13px;color:var(--gold)")}このタイプに★がついている日：{d["days"]}</div>' +
                memo(d['memo']))
        add(book, f'<div style="{type_style(t)}">{body}</div>', wk='loosen', run=run)


# ---------- 第3章 ----------
def ch3(book):
    run = '第3章　使ってないのにお金がない本当の理由'
    chapter_open(book, 'ch3', 3, '使ってないのに<br>お金がない<br>本当の理由',
                 '「使ってないのにない」の正体は、だらしなさではありません。気づかないうちにお金が出ていく、<span class="hl">4つの「もれ口」</span>です。',
                 ['大きな買い物はしていない。家賃も食費も、だいたい同じ。なのに、気づくと貯金が減っている。「やっぱり自分はだらしないんだ」と思った夜はありませんか。',
                  'この章では、自分を責める前に、お金のもれ口を探します。'], 'この章でわかること',
                 ['お金が気づかないうちに出ていく、4つの「もれ口」', 'あなたのタイプに出やすいもれ口', '家計簿や節約が続かなかった、本当の理由'], 'split', run)
    # もれ口の全体図
    leaks = [('もれ口1', 'calculator', '少なめに見積もるクセ', '来月の出費を、実際より少なく見積もる', 'Day4'),
             ('もれ口2', 'calendar-heart', '年に数回の出費（特別費）', '「今回だけ」の出費を、実際の約半分に見積もる', 'Day3・11'),
             ('もれ口3', 'repeat', '勝手に出ていくお金', 'サブスク・自動の支払い・キャッシュレス', 'Day5'),
             ('もれ口4', 'heart-crack', '気持ちで出ていくお金', '気分・人のため・受け取らない', 'Day6')]
    grid = ('<div style="position:relative"><div class="cards c2" style="gap:16mm 30mm">' +
            ''.join(f'<div class="card" style="padding:4.4mm 4mm 4mm;min-height:40mm;display:flex;flex-direction:column"><div class="row"><div class="ci">{icon(ic)}</div><div><div class="k">{k}</div><div class="h" style="font-size:11.4pt">{h}</div></div></div>'
                    f'<div class="s" style="flex:1;font-size:9.4pt">{s}</div><div><span class="chip" style="background:#fff">{icon("calendar-days", style="width:12px;height:12px")}{d}で確かめる</span></div></div>'
                    for k, ic, h, s, d in leaks) + '</div>'
            '<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:27mm;height:27mm;border-radius:50%;background:#fff;'
            'box-shadow:0 0 0 2px var(--wk), 0 4px 12px rgba(40,50,101,.12);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">'
            f'{icon("wallet", style="width:9mm;height:9mm;color:var(--wk)")}<div class="mg" style="font-weight:700;color:var(--navy);font-size:8.4pt;line-height:1.35;margin-top:1mm">あなたの<br>お財布</div></div></div>')
    body = (head('第3章', 'お金には、気づかないうちに出ていく「もれ口」が4つあります') +
            fig('「使ってないのにない」の正体＝4つのもれ口', grid, tip='次のページから、1つずつ見ていきます。Day3〜7で、自分のもれ口を実際に探します。') +
            '<p>「使ってないのにない」の正体は、この4つです。</p>')
    add(book, body, wk='split', run=run)

    taisaku = lambda t: f'<div class="box tint" style="display:flex;gap:3mm;align-items:flex-start;padding:3mm 4mm"><span class="chip" style="background:var(--wk);color:#fff;flex:none">対策</span><span>{t}</span></div>'
    b1 = bars([{'l': '予想', 'v': 82, 'd': '82', 'gray': True}, {'l': '実際', 'v': 100, 'd': '100'}])
    b2 = bars([{'l': '予想', 'v': 56, 'd': '56', 'gray': True}, {'l': '実際', 'v': 100, 'd': '100'}])
    body = (head('第3章｜もれ口1', '人は、来月の出費を少なめに見積もります') +
            fig('来月の出費：予想と実際', b1 + '<div class="center small mt2">実際より <b style="font-size:12pt;color:var(--wk)">15〜20%</b> 少なく見積もる</div>') +
            '<p>思い出しやすい「いつもの出費」をもとに考えてしまうからです。しかも、「貯めたい」気持ちが強い人ほど、見積もりが甘くなります。</p>' +
            taisaku('「今回はいつもと違う出費が出そうな理由」を考えてから予想する（Day4）。') +
            memo('10の研究・6,044人を調べた研究です（Howard ほか, 2022）。貯めたい気持ちが強い人ほど出費を少なく見積もり、実際の出費は減らなかった、という研究もあります（Peetz & Buehler, 2009）。').replace('class="memo"', 'class="memo" style="margin-top:3mm"') +
            '<div class="sep2"></div>' +
            head('第3章｜もれ口2', '年に数回の出費は、約半分に見積もられます') +
            fig('冠婚葬祭・プレゼント・修理などの「今回だけ」の出費', b2 + '<div class="center small mt2">予想は、実際の <b style="font-size:12pt;color:var(--wk)">約半分</b></div>') +
            '<p>どれも「今回だけ」と思うからです。でも1年で見ると、「今回だけ」は毎月のように起きています。このワークでは、こうした年に数回の出費を<b>「特別費」</b>と呼びます。</p>' +
            taisaku('去年の特別費を書き出して、毎月の予定に変える（Day3・Day11）。') +
            memo('Sussman & Alter, 2012。').replace('class="memo"', 'class="memo" style="margin-top:3mm"'))
    add(book, body, wk='split', run=run)

    c3 = cards([{'icon': 'repeat', 'h': 'サブスク', 's': '毎月決まった額を払うサービス。やめたいのに続きやすい'},
                {'icon': 'credit-card', 'h': 'キャッシュレス', 's': 'カードやスマホでの支払い。現金より、少しだけ多く使いやすい'},
                {'icon': 'rotate-cw', 'h': 'リボ払い', 's': '毎月の支払いを一定にする払い方。残りに手数料がかかり続ける'}], cols=3)
    c4 = cards([{'icon': 'cloud-rain', 'h': '気分で出ていくお金', 's': '悲しいときは、高く払いやすく、目先のものを選びやすい'},
                {'icon': 'hand-heart', 'h': '人のために出ていくお金', 's': '断れない、多めに払う、頼まれたら出す'},
                {'icon': 'hand-coins', 'h': '受け取らないことで減るお金', 's': '値段を下げる、遠慮する。入ってくるはずのお金が減る'}], cols=3)
    body = (head('第3章｜もれ口3', '勝手に出ていくお金は、気づかないうちに続きます') +
            fig('勝手に出ていく3つのお金', c3 +
                '<div class="box tint mt3" style="padding:3mm 4mm">' + stat('47.2', '%', 'リボ払いと分割払いの手数料のちがいを問う問題に、<b>正しく答えられた人</b>') + '</div>') +
            taisaku('自動の支払いを書き出して、1つだけ「止める／続ける」を決める（Day5）。') +
            memo('キャッシュレスの影響は小さいので、全部やめる必要はありません（Schomburgk ほか, 2024）。47.2%は、J-FLEC「金融リテラシー調査」2025年。').replace('class="memo"', 'class="memo" style="margin-top:3mm"') +
            '<div class="sep2"></div>' +
            head('第3章｜もれ口4', 'お金は、気持ちでも出ていきます') +
            fig('気持ちで出ていく3つのお金', c4, tip='どれも、あなたのタイプと深くつながっています。次のページで確かめましょう。') +
            memo('Cryder ほか, 2008／Lerner ほか, 2013。'))
    add(book, body, wk='split', run=run)

    # タイプ×もれ口
    M = [[1, 1, 0, 0], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [1, 0, 1, 0]]
    notes = {(0, 0): '我慢するほど見積もりが甘く', (0, 1): '特別費の不意打ち', (1, 3): '人のために', (2, 3): '気分で', (3, 3): '受け取らないことで',
             (4, 2): '勝手に出ていく', (4, 0): '少なめに見積もる'}
    th = ''.join(f'<th>もれ口{j + 1}<small>{s}</small></th>' for j, s in enumerate(['少なめに見積もる', '特別費', '勝手に出ていく', '気持ちで出ていく']))
    tr = ''
    for i, t in enumerate(TYPES):
        tds = ''
        for j in range(4):
            if M[i][j]:
                tds += f'<td><span class="on" style="background:{t[3]}">{icon("check", sw=3, style="width:4mm;height:4mm")}</span><span class="nt">{notes.get((i, j), "")}</span></td>'
            else:
                tds += '<td><span class="off"></span></td>'
        tr += f'<tr><td class="tn"><span style="display:inline-flex;align-items:center;gap:2mm"><span style="color:{t[3]}">{icon(t[2], style="width:16px;height:16px")}</span>{t[0]}</span></td>{tds}</tr>'
    body = (head('第3章', 'あなたのタイプには、出やすいもれ口があります') +
            fig('タイプ × もれ口', f'<table class="mx"><tr><th></th>{th}</tr>{tr}</table>', tag='早見表',
                tip='あなたの2タイプの行を見て、気をつけるもれ口に印をつけてください。') +
            '<div class="box cream"><h4>' + icon('pencil') + 'わたしが気をつけるもれ口</h4>'
            '<div class="circle-opts" style="margin-top:2mm"><span>もれ口1</span><span>もれ口2</span><span>もれ口3</span><span>もれ口4</span></div></div>')
    add(book, body, wk='split', run=run)

    # 続かなかったのは意志のせいではない
    rs = cards([{'icon': 'weight', 'h': 'やり方が重すぎた', 's': '細かい家計簿より、簡単なルールの方が効く'},
                {'icon': 'book-x', 'h': '知識だけでは変わりにくい', 's': '知っているのにできないのは、怠けているからではない'},
                {'icon': 'eye-off', 'h': '見るのが怖かった', 's': '不安だと、人は見られない'},
                {'icon': 'arrow-left-right', 'h': 'やり方が、心のルールと逆だった', 's': '「使っちゃダメ」と覚えた人が、もっと我慢しようとしていた'}], cols=2)
    venn = ('<div style="position:relative;height:50mm;width:120mm;margin:0 auto">'
            '<div style="position:absolute;left:14mm;top:2mm;width:58mm;height:46mm;border-radius:50%;background:rgba(138,134,208,.18);border:1.5px solid #8A86D0"></div>'
            '<div style="position:absolute;right:14mm;top:2mm;width:58mm;height:46mm;border-radius:50%;background:rgba(194,134,42,.15);border:1.5px solid #C2862A"></div>'
            f'<div style="position:absolute;left:18mm;top:15mm;width:28mm;text-align:center">{icon("heart", style="width:7mm;height:7mm;color:#8064BF")}<div class="mg" style="font-weight:700;color:#5E4596">心（クセ）</div></div>'
            f'<div style="position:absolute;right:18mm;top:15mm;width:28mm;text-align:center">{icon("wallet", style="width:7mm;height:7mm;color:#C2862A")}<div class="mg" style="font-weight:700;color:#94641A">財布（仕組み）</div></div>'
            '<div class="mg" style="position:absolute;left:50%;top:19mm;transform:translateX(-50%);font-weight:700;color:var(--navy);font-size:9pt;text-align:center;line-height:1.35">この<br>ワーク</div></div>')
    body = (head('第3章', '家計簿や節約が続かなかったのは、意志のせいではありません') +
            fig('続かなかった4つの理由', rs) +
            fig('だから、心と財布を同時に扱う', venn, tip='このワークは、心（クセ）と財布（仕組み）を、同時に扱います。') +
            memo('小さな事業をしている人たちの研究では、お金の管理が苦手な人ほど、細かい帳簿より簡単なルールが効きました（Drexler ほか, 2014）。お金の教育で説明できる行動の違いは0.1%でした（Fernandes ほか, 2014。もう少し効果があるという新しい分析もあります）。'))
    add(book, body, wk='split', run=run)


# ---------- 第4章 ----------
def ch4(book):
    run = '第4章　心と財布に余裕をつくる3つの小さな習慣'
    chapter_open(book, 'ch4', 4, '心と財布に<br>余裕をつくる<br>3つの小さな習慣',
                 '身につけるのは、「見る」「分ける」「ひと呼吸」の<span class="hl">3つだけ</span>です。',
                 ['たくさんの方法を並べるより、3つに絞った方が続けられます。毎日のクセにも、疲れた夜のまとめ買いにも、この3つが効きます。',
                  'そして、不安が出てきたときは、<b>3つのステップ</b>で解きます。①感情に名前をつける、②なぜその感情が生じたのか考える、③別の解釈を考えてみる。①は習慣1の「見る」で毎週、②と③は3週目の「ほどく」（Day16〜19）で練習します。'], '', [], 'decide', run,
                 extra=cards([{'icon': 'eye', 'k': '習慣 1', 'h': '見る', 's': '週に1回、5分だけ'},
                              {'icon': 'layers', 'k': '習慣 2', 'h': '分ける', 's': '給料日に、先に分ける'},
                              {'icon': 'wind', 'k': '習慣 3', 'h': 'ひと呼吸', 's': '「もしもの一文」を1つ'}], cols=3, style='margin-top:5mm'))

    f1 = flow([{'icon': 'tag', 'num': 'STEP 1', 'h': '今の気持ちに名前をつける', 's': '「不安」「焦り」など1つ'},
               {'icon': 'landmark', 'num': 'STEP 2', 'h': '残高を見る'},
               {'icon': 'droplets', 'num': 'STEP 3', 'h': '今週のお金のもれ口を見る', 'hi': True}])
    scene = ('<div class="box tint" style="display:flex;align-items:center;gap:5mm;margin-bottom:4mm">'
             f'<div style="width:20mm;height:20mm;border-radius:50%;background:#fff;color:var(--wk);display:flex;align-items:center;justify-content:center;flex:none">{icon("coffee", style="width:10mm;height:10mm")}</div>'
             '<div><div class="mg" style="font-weight:700;color:var(--navy);font-size:13pt">日曜の夜、お茶をいれて5分だけ。</div><div class="small">この順番で見ます。</div></div></div>')
    tw = cards([{'icon': 'eye-off', 'color': '#2A8B7F', 'k': '見ないふりタイプには', 'h': '「少しだけ見る練習」に'},
                {'icon': 'piggy-bank', 'color': '#3A74C2', 'k': 'ため込みタイプには', 'h': '「見る日以外は見なくていい練習」に'}], cols=2)
    body = (head('第4章｜習慣1　見る', '週に1回、5分だけお金を見ます') + scene +
            fig('見る順番', f1, tip='気持ちに名前をつけてから見ると、数字に飲み込まれにくくなります。') + tw +
            memo('気持ちに名前をつけているあいだは、脳の"警報係"の反応が弱まった、という研究があります（Lieberman ほか, 2007）。').replace('class="memo"', 'class="memo" style="margin-top:4mm"'))
    add(book, body, wk='decide', run=run)

    boxes = ('<div style="display:flex;flex-direction:column;align-items:center">'
             '<div class="mg" style="display:inline-flex;align-items:center;gap:2mm;background:var(--navy);color:#fff;border-radius:3mm;padding:2mm 7mm;font-weight:700;font-size:11.4pt">'
             + icon('banknote', style='width:16px;height:16px') + '給料が入ったら、使う前に</div>'
             '<svg viewBox="0 0 160 14" style="width:100%;height:11mm;display:block" preserveAspectRatio="none"><path d="M80 0 V6 M26 6 H134 M26 6 V14 M80 6 V14 M134 6 V14" stroke="#2A8B7F" stroke-width=".8" fill="none"/></svg></div>' +
             '<div class="grid3">' + ''.join(
                 f'<div style="background:var(--wk-t);border-radius:4mm;padding:5mm 4mm 4.4mm;text-align:center">'
                 f'<div style="width:17mm;height:17mm;border-radius:50%;background:#fff;color:var(--wk);display:flex;align-items:center;justify-content:center;margin:0 auto 2mm">{icon(ic, style="width:9mm;height:9mm")}</div>'
                 f'<div class="mg" style="font-weight:700;color:var(--wk);font-size:8.6pt;letter-spacing:.12em">BOX {k}</div>'
                 f'<div class="mg" style="font-weight:700;color:var(--navy);font-size:13pt">{h}</div>'
                 f'<div style="font-size:9pt;color:var(--sub);line-height:1.6;margin-top:1.6mm;text-align:left">{t}</div>'
                 f'<div style="margin-top:2.4mm"><span class="chip" style="background:#fff">{icon("calendar-days", style="width:12px;height:12px")}{d}</span></div></div>'
                 for ic, k, h, t, d in [('shield-check', '1', '安心ボックス', '急な出費に備えるお金。名前と写真をつけて、1万円くらいから始める', 'Day8・9'),
                                        ('calendar-heart', '2', '特別費', '去年の年に数回の出費の合計を12で割った額を、毎月とっておく', 'Day11'),
                                        ('heart', '3', '使っていいお金', '罪悪感なしで、自分のために使うためのお金', 'Day12')]) + '</div>')
    body = (head('第4章｜習慣2　分ける', '給料日に、使う前に先に3つに分けます') +
            '<p>給料が入ったら、使う前に、先に取り分けます（これを<b>「先取り」</b>と言います）。分ける先は3つです。</p>' +
            fig('先取りで、3つに分ける', boxes, tip='「使っていいお金」は、自分を甘やかすためのお金ではありません。罪悪感なしで「自分のために使う」練習をするための箱です。') +
            memo('お金は、目的を決めて分けた方が多く貯まります（Soman & Cheema, 2011）。'))
    add(book, body, wk='decide', run=run)

    kw = cards([{'icon': 'minimize-2', 'h': '小さく', 's': '続けられる額から'}, {'icon': 'refresh-cw', 'h': '自動で', 's': '給料日に勝手に分かれる'},
                {'icon': 'tag', 'h': '名前をつけて', 's': '目的が見えると崩しにくい'}], cols=3)
    b = bars([{'l': '申し込む方式', 'v': 37, 'd': '37%', 'gray': True}, {'l': '自動で加入', 'v': 86, 'd': '86%'}], cls='wide')
    body = (head('第4章｜習慣2　分ける', '分けたお金は、「小さく・自動で・名前をつけて」続けます') +
            fig('続けるための3つのコツ', kw) +
            '<div class="grid2" style="margin-bottom:4mm">' +
            fig('積み立ての加入率', b, tag='研究') +
            fig('「目標の名前」入りのお知らせ', '<div class="center">' + stat('2', '倍', '名前のないお知らせより、<br>よく効きました', style='justify-content:center') + '</div>', tag='研究') +
            '</div>' +
            '<p>先取りが続かなかったのは、額が大きすぎたか、急な出費のたびに崩してしまったからかもしれません。だから、小さな額を、自動で、名前をつけて分けます。</p>' +
            memo('37%→86%は、ある会社の積み立て制度の例です（Madrian & Shea, 2001）。名前入りのお知らせ（Karlan ほか, 2016）。'))
    add(book, body, wk='decide', run=run)

    ift = ('<div class="ifthen"><div class="if"><div class="k">もし（場面）</div><div class="v">疲れた夜に、買いたくなったら</div></div>'
           f'<div class="ar">{icon("arrow-right", sw=2.5, style="width:5mm;height:5mm")}</div>'
           '<div class="th"><div class="k">する（行動）</div><div class="v">カートに入れて閉じ、明日の朝もう一度見る</div></div></div>')
    other = cards([{'icon': 'shopping-cart', 'h': '選んで閉じる', 's': '落ち込んだ日は、選ぶところまでにしてアプリを閉じる'},
                   {'icon': 'hand', 'h': '支払いにひと手間', 's': '使いすぎやすい場面だけ、カード情報を保存しない・金額を1行書く'}], cols=2)
    body = (head('第4章｜習慣3　ひと呼吸', '「もしもの一文」を1つだけ決めます') +
            '<p>買う前・払う前に、ひと呼吸。そのために、<b>「もし〇〇になったら、△△する」</b>という1文を先に決めておきます。このワークでは、これを<b>「もしもの一文」</b>と呼びます。</p>' +
            fig('もしもの一文', ift, tip='数は1つで十分です。書いたら、声に出して1回くり返します。') +
            h3('ほかにも、ひと呼吸を置く方法があります', 'wind') + other +
            memo('この一文で行動に移しやすくなることは、642件の実験をまとめた研究で確かめられています（Sheeran ほか, 2025）。選ぶだけで悲しい気持ちが軽くなった（Rick ほか, 2014。怒っているときは効きませんでした）。金額を書き写すと、次の買い物にブレーキがかかった（Soman, 2001）。').replace('class="memo"', 'class="memo" style="margin-top:4mm"'))
    add(book, body, wk='decide', run=run)

    steps = [('見つける', '子どもの頃に聞いたお金の言葉を書く', 'Day16', 'search'),
             ('知る', 'そのルールが守ってくれていたものを書く', 'Day18', 'shield'),
             ('言い換える', '当てはまる例と当てはまらない例から、やさしい言い方に直す', 'Day19', 'refresh-cw'),
             ('書く', '誇りに思えたこと・大事にしている価値を1つ書く', 'Day20', 'pencil'),
             ('使ってみる', 'その価値に沿った、小さな使い道を1つ試す', 'Day20', 'sprout')]
    stair = ('<div style="display:flex;align-items:flex-end;gap:2mm;height:78mm">' +
             ''.join(f'<div style="flex:1;height:{38 + i * 10}mm;background:{"var(--wk)" if i == 4 else "var(--wk-t)"};border-radius:3mm 3mm 0 0;padding:2.6mm 2mm;display:flex;flex-direction:column;align-items:center;text-align:center">'
                     f'<div style="width:9mm;height:9mm;border-radius:50%;background:#fff;color:var(--wk);display:flex;align-items:center;justify-content:center">{icon(ic, style="width:5mm;height:5mm")}</div>'
                     f'<div class="mg" style="font-weight:700;font-size:8pt;color:{"#fff" if i == 4 else "var(--wk)"};margin-top:1mm">{i + 1}・{d}</div>'
                     f'<div class="mg" style="font-weight:700;font-size:11pt;color:{"#fff" if i == 4 else "var(--navy)"}">{n}</div>'
                     f'<div style="font-size:7.8pt;line-height:1.45;color:{"rgba(255,255,255,.9)" if i == 4 else "var(--sub)"};margin-top:1mm">{s}</div></div>'
                     for i, (n, s, d, ic) in enumerate(steps)) + '</div>')
    body = (head('第4章', 'お金の口ぐせは、5つの手順でゆるめます') +
            '<p>よく「メンタルブロック」と呼ばれるものを、このワークでは<b>「お金の口ぐせ」</b>と呼びます。家で聞いたり見たりして覚えた、お金についての言葉や考えのことです。3週目の「ほどく」では、これを次の5つの手順で少しずつゆるめます。</p>' +
            fig('口ぐせをゆるめる5段階', stair, tip='「私はお金を受け取っていい」と言い聞かせることはしません。自分への評価が低いときには、かえって逆効果になることがあるからです。', style='--wk:#8064BF;--wk-t:#F1ECFA;--wk-d:#5E4596') +
            memo('Wood ほか, 2009／Hall ほか, 2014。'))
    add(book, body, wk='decide', run=run)


# ---------- 30日ワークの扉・週の扉 ----------
WEEK_INFO = {
    1: ('see', 'WEEK 1', '見る', 'Day1〜7', 'お金の流れと、気づかないうちにお金が出ていく「もれ口」を見る1週間です。',
        '責めるために見るのではありません。確かめるために、少しだけ見ます。', range(1, 8)),
    8: ('split', 'WEEK 2', '分ける', 'Day8〜14', 'お金を「安心ボックス」「特別費」「使っていいお金」の3つに分ける1週間です。',
        '小さく・自動で・名前をつけて。Day10は、30日の中でいちばん大事な日です。', range(8, 15)),
    15: ('loosen', 'WEEK 3', 'ほどく', 'Day15〜21', '家で覚えたお金の口ぐせに気づいて、少しずつゆるめる1週間です。',
         '親の話が出てきますが、親を責めるためではありません。つらい日は、飛ばしてかまいません。', range(15, 22)),
    22: ('decide', 'WEEK 4', '決める', 'Day22〜29', 'お金を見る日、断る一言、「もしもの一文」を決める1週間です。',
         '一言カードは、困る場面で読み返すためのものです。完璧でなくて大丈夫です。', range(22, 30)),
}
WEEK_DIVIDERS = set(WEEK_INFO)


def week_divider(book, n):
    from pages_days import DAYS, head_info
    wk, en, jp, rng, desc, msg, days = WEEK_INFO[n]
    book.mark(f'wk{n}')
    rows = ''
    for d in days:
        t, stars, heavy = head_info(d)
        tags = ''
        if stars:
            tags += f'<span class="tg">★ {"・".join(s.replace("タイプ", "") for s in stars)}</span>'
        if heavy:
            tags += '<span class="tg r">重い日</span>'
        if d in (13, 20, 28):
            tags += '<span class="tg" style="background:var(--lav-l);color:#5E4596">つまずきポイント</span>'
        rows += f'<div class="dy"><span class="dn">Day{d}</span><span class="dt">{t}</span>{tags}<span class="pg">p.{{{{PG:day{d}}}}}</span></div>'
    rings = (pos('', top=-40, right=-50, extra='width:150mm;height:150mm;border-radius:50%;border:1.5px solid rgba(255,255,255,.16)') +
             pos('', top=-20, right=-30, extra='width:110mm;height:110mm;border-radius:50%;border:1.5px solid rgba(255,255,255,.14)') +
             pos('', bottom=-60, left=-50, extra='width:130mm;height:130mm;border-radius:50%;background:rgba(255,255,255,.06)'))
    body = (f'<div class="wkd"><div class="ck">{en}　｜　{rng}</div><div class="ct">{jp}</div><div class="cd">{desc}</div>'
            f'<div class="days">{rows}</div>' + talk([msg], who='', size='l') + '</div>')
    add(book, body, wk=wk, run='30日ワーク', cls='divider', bg=rings)


def work_opening(book):
    stages = [('Day0', 'スタート', '#283265'), ('1週目', '見る', '#3A74C2'), ('2週目', '分ける', '#C2862A'),
              ('3週目', 'ほどく', '#8064BF'), ('4週目', '決める', '#2A8B7F'), ('Day30', '完成', '#B48C45')]
    mp = ('<div style="display:flex;align-items:center;gap:1mm">' +
          ''.join((f'<div style="color:var(--line)">{icon("chevron-right", sw=3, style="width:5mm;height:5mm")}</div>' if i else '') +
                  f'<div style="flex:1;text-align:center"><div style="width:20mm;height:20mm;border-radius:50%;background:{c};color:#fff;margin:0 auto;display:flex;flex-direction:column;align-items:center;justify-content:center">'
                  f'<div style="font-size:7.4pt;opacity:.9">{a}</div><div class="mg" style="font-weight:700;font-size:12pt;line-height:1.2">{b}</div></div></div>'
                  for i, (a, b, c) in enumerate(stages)) + '</div>')
    today = ('<div class="grid2">'
             f'<div class="box tint"><h4>{icon("book-open")}1ページ目｜読む</h4><p class="small" style="margin:0">今日のゴール／アオの話／図解／なぜ？／今日の5分</p></div>'
             f'<div class="box tint"><h4>{icon("pencil")}2ページ目｜書く</h4><p class="small" style="margin:0">記入例／書く欄／メモ／研究メモ／アオのひとこと</p></div></div>')
    body = (f'<div style="text-align:center;padding-top:16mm"><div class="kicker" style="letter-spacing:.4em">30 DAYS WORK</div>'
            '<div class="mg" style="font-weight:700;color:var(--navy);font-size:34pt;letter-spacing:.1em;margin-top:3mm">30日ワーク</div>'
            '<div class="mg" style="font-weight:700;color:var(--sub);font-size:12pt;margin-top:2mm">1日5分。Day0から、1ページずつ進みます。</div></div>'
            '<div style="width:62mm;height:62mm;border-radius:50%;margin:10mm auto 10mm;background:#fff url(../assets/aoi_circle_600.png) center/cover no-repeat;'
            'box-shadow:0 0 0 2px var(--gold-l), 0 0 0 6px #fff, 0 0 0 7px var(--gold-l), 0 10px 24px rgba(40,50,101,.14)"></div>' +
            fig('30日の進み方', mp, tag='地図') + today +
            tip('迷ったら、今日のゴールだけ読めば大丈夫。1行書けたら、その日は終わりです。', style='margin-top:6mm'))
    add(book, body, run='30日ワーク')


def build(book):
    cover(book)
    toc(book)
    message(book)
    hajime_aoi(book)
    hajime_plan(book)
    hajime_prepare(book)
    hajime_twopages(book)
    hajime_rest(book)
    hajime_promise(book)
    hajime_stuck(book)
    hajime_can(book)
    ch1(book)
    ch2(book)
    ch3(book)
    ch4(book)
