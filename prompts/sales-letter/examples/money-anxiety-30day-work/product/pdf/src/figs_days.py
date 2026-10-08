"""Day0〜30 の図解（すべてアオのポイントつき）"""
from lib import fig, flow, cards, vs, bars, stat, icon

BLUE, YEL, GRN, GRY = '#3F7BD0', '#E3AE22', '#3E9E62', '#9097A0'


def colorchip(c, t):
    return f'<span class="chip" style="background:{c};color:#fff">{t}</span>'


def d0():
    return fig('今日やるのは、「知る」ことだけ', flow([
        {'icon': 'clipboard-check', 'num': 'STEP 1', 'h': 'セルフチェック', 's': '20問に答えて<br>あなたの2タイプを知る'},
        {'icon': 'gauge', 'num': 'STEP 2', 'h': '不安メーター', 's': '「今月」と「この先」<br>を0〜10で'},
        {'icon': 'receipt', 'num': 'STEP 3', 'h': 'レシート1枚', 's': '見たときの気持ちに<br>名前をつける'},
        {'icon': 'square-check-big', 'num': 'STEP 4', 'h': '2マス塗る', 's': '進捗表の<br>「買った」「Day0」', 'hi': True},
    ]), tip='今日は、直そうとしなくて大丈夫。いまの自分を「知る」だけです。')


def d1():
    cs = cards([
        {'icon': 'heart', 'color': BLUE, 'k': '青', 'h': '満たされた', 's': '使ってよかった', 'bg': '#EAF1FB'},
        {'icon': 'cloud-lightning', 'color': YEL, 'k': '黄', 'h': '気分', 's': '疲れ・イライラ・さみしさ', 'bg': '#FCF4DC'},
        {'icon': 'hand-heart', 'color': GRN, 'k': '緑', 'h': '人のため', 's': '家族・友人・職場のため', 'bg': '#E6F4EB'},
        {'icon': 'repeat', 'color': GRY, 'k': '灰', 'h': '勝手に', 's': 'サブスク・自動・なんとなく', 'bg': '#EFF0F2'},
    ], cols=4)
    ex = (f'<div class="row2 mt3" style="justify-content:center;gap:6mm;font-size:9.6pt">'
          f'<span>ランチ 900円 {colorchip(YEL, "黄")}</span><span>母へ 20,000円 {colorchip(GRN, "緑")}</span>'
          f'<span>動画サービス 990円 {colorchip(GRY, "灰")}</span></div>')
    return fig('色分けメモ：使ったお金に、4色のどれかで印をつける', cs + ex,
               tip='迷ったら、いちばん近い色でOK。正しさより、続けることが大事です。')


def d2():
    f = flow([
        {'icon': 'tag', 'num': 'まず', 'h': '気持ちに名前', 's': '「不安」「焦り」など<br>1つだけ'},
        {'icon': 'smartphone', 'num': 'つぎに', 'h': '残高だけ見る', 's': '金額は<br>書かなくていい'},
        {'icon': 'tag', 'num': 'さいごに', 'h': '見たあとの気持ち', 's': 'もう一度、<br>名前をつける', 'hi': True},
    ], arrow='arrow-right')
    return fig('見る前に、気持ちに名前をつける', f,
               tip='開けた。それだけで、昨日より一歩進んでいます。')


def d3():
    months = {3: ('友人の結婚式', '30,000円'), 8: ('帰省', '25,000円'), 11: ('パソコン修理', '18,000円'), 12: ('プレゼント', '10,000円')}
    cells = []
    for m in range(1, 13):
        if m in months:
            e, y = months[m]
            cells.append(f'<div class="c on"><div class="m">{m}月</div><div class="e">{e}</div><div class="y">{y}</div></div>')
        else:
            cells.append(f'<div class="c"><div class="m">{m}月</div></div>')
    cal = f'<div class="cal m12">{"".join(cells)}</div>'
    tot = ('<div class="row2 mt3"><div class="grow">' + bars([
        {'l': '予想', 'v': 56, 'd': '56', 'gray': True},
        {'l': '実際', 'v': 100, 'd': '100'},
    ]) + '</div><div class="eq"><div class="t res"><div class="v">83,000円</div><div class="k">去年の合計（記入例）</div></div></div></div>')
    return fig('「今回だけ」は、1年で見ると毎月のようにやってくる', cal + tot,
               tip='人は「今回だけ」の出費を、実際の約半分に見積もります。思い出せない月は空欄でOK。')


def d4():
    b = bars([{'l': '予想', 'v': 82, 'd': '82', 'gray': True}, {'l': '実際', 'v': 100, 'd': '100'}])
    f = flow([
        {'icon': 'calculator', 'h': '最初の予想', 's': '15万円'},
        {'icon': 'help-circle', 'h': 'いつもと違う理由を3つ', 's': '友人の誕生日／冬のコート／歯医者'},
        {'icon': 'pen-line', 'h': '書き直した予想', 's': '18万円', 'hi': True},
    ])
    return fig('来月の出費は、15〜20%少なめにズレる', b + '<div class="mt3"></div>' + f,
               tip='予想が外れるのは、あなたのせいではありません。人の頭のクセです。')


def d5():
    rows = [('動画サービス', '990円', '2か月前', False), ('写真のアプリ', '400円', '毎日', True)]
    items = ''.join(
        f'<div class="row2" style="background:#fff;border:1.2px solid var(--line);border-radius:3mm;padding:2.2mm 3.4mm;margin-bottom:2mm">'
        f'{icon("repeat", style="width:5mm;height:5mm;color:var(--c-gray)")}<div class="grow"><b>{n}</b>　<span class="small">月額 {p}／最後に使った日：{d}</span></div>'
        f'<span class="chip" style="{"" if on else "background:#F3F2F0;color:#77768A"}">{"続ける" if on else "止める"}</span>'
        f'<span style="width:11mm;height:6mm;border-radius:99px;background:{"var(--wk)" if on else "#D6D3DD"};position:relative;display:inline-block">'
        f'<i style="position:absolute;top:.8mm;{"right" if on else "left"}:.8mm;width:4.4mm;height:4.4mm;border-radius:50%;background:#fff"></i></span></div>'
        for n, p, d, on in rows)
    eq = ('<div class="eq mt2"><div class="t"><div class="v">990円</div><div class="k">月額</div></div><div class="op">×</div>'
          '<div class="t"><div class="v">12か月</div><div class="k"></div></div><div class="op">＝</div>'
          '<div class="t res"><div class="v">11,880円</div><div class="k">1年で取り戻せる額</div></div></div>')
    return fig('自動で出ていくお金を書き出して、1つだけ決める', items + eq,
               tip='1つ止められたら、それはもう「財布の最初の一勝」です。今日は1つで十分。')


def d6():
    seg = [(BLUE, 1, '青'), (YEL, 4, '黄'), (GRN, 2, '緑'), (GRY, 1, '灰')]
    tot = sum(s[1] for s in seg)
    bar = ''.join(f'<div style="flex:{n};background:{c};color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:9pt">{t} {n}</div>' for c, n, t in seg)
    b = f'<div style="display:flex;height:9mm;border-radius:99px;overflow:hidden">{bar}</div>'
    sc = vs({'l': 'いちばん多い色', 'icon': 'palette', 'q': '黄（気分）'},
            {'l': 'その色が多くなる場面', 'icon': 'map-pin', 'q': '残業した日の帰り道、コンビニで'})
    return fig('6日分の色分けメモ。いちばん多いのは何色？', b + '<p class="small center mt2">（記入例：6日間で使ったお金8件の色の数）</p>' + sc,
               tip='色が偏っていても大丈夫。偏りが分かれば、手の打ちようがあります。')


def d7():
    cs = cards([
        {'icon': 'calculator', 'k': 'もれ口1', 'h': '少なめに見積もるクセ'},
        {'icon': 'calendar-days', 'k': 'もれ口2', 'h': '年に数回の出費（特別費）', 'sel': True},
        {'icon': 'repeat', 'k': 'もれ口3', 'h': '勝手に出ていくお金'},
        {'icon': 'heart-crack', 'k': 'もれ口4', 'h': '気持ちで出ていくお金'},
    ], cols=4)
    s = ('<div class="card-fill mt3"><div class="ttl">' + icon('quote', style='width:13px;height:13px') +
         '1行にまとめる</div><div class="mg" style="font-weight:700;color:var(--navy);font-size:11pt;margin-top:1mm">'
         '私の「足りない」の正体は、<span class="ul-wk">毎月は来ないと思っていた特別な出費</span>だった</div></div>')
    return fig('4つのもれ口から、自分の「トップ1」を選ぶ', cs + s,
               tip='「なんとなく足りない」が「ここから出ていた」に変わるだけで、不安の形は変わります。')


def d8():
    box = ('<div class="row2" style="align-items:stretch;gap:5mm">'
           '<div style="width:46mm;flex:none;background:var(--wk-t);border-radius:4mm;padding:4mm;text-align:center;position:relative">'
           f'<div style="width:22mm;height:22mm;margin:0 auto;border-radius:50%;background:#fff;color:var(--wk);display:flex;align-items:center;justify-content:center">{icon("package", style="width:12mm;height:12mm")}</div>'
           '<div class="mg" style="font-weight:700;color:var(--navy);font-size:12pt;margin-top:2mm">わたしの非常口</div>'
           '<div class="small">ネット銀行の口座</div></div>'
           '<div class="grow">' +
           cards([
               {'icon': 'map-pin', 'k': '1　場所', 'h': '使っていない口座・封筒など'},
               {'icon': 'tag', 'k': '2　名前', 'h': '「わたしの非常口」'},
               {'icon': 'target', 'k': '3　目標額', 'h': '最初は1万円くらい'},
               {'icon': 'image', 'k': '4　写真', 'h': '目標を思い出せる1枚'},
           ], cols=2) +
           '<div class="mt2">' + bars([{'l': '目標', 'v': 30, 'd': '1万円', 'max': 100}]) + '</div></div></div>')
    return fig('安心ボックス：名前と写真をつけた、あなた専用の「非常口」', box,
               tip='額の大きさより、「ある」ことが大事です。')


def d9():
    f = flow([
        {'icon': 'landmark', 'num': '25日', 'h': '給料が入る', 's': '（給料日）'},
        {'icon': 'refresh-cw', 'num': '26日', 'h': '自動で3,000円', 's': '定額自動振込・積立など'},
        {'icon': 'package', 'num': '毎月', 'h': '安心ボックスへ', 's': '「わたしの非常口」', 'hi': True},
    ])
    n = ('<div class="row2 mt3"><div class="notice grow"><div class="ap">' + icon('bell') + '</div><div>'
         '<div class="nt">お知らせ（イメージ）</div><div class="nm">「わたしの非常口」に3,000円が移りました</div></div></div>'
         '<div class="grow">' + bars([{'l': '自分で申込', 'v': 37, 'd': '37%', 'gray': True}, {'l': '自動で加入', 'v': 86, 'd': '86%'}]) + '</div></div>')
    return fig('1回の設定で、毎月がんばらなくても続く', f + n,
               tip='決めるのは、今日の1回だけ。これからのあなたを、毎月助けてくれる設定です。')


def d10():
    v = vs({'l': '使う前', 'icon': 'cloud', 'q': '「こんなの、私が買っていいのかな」', 's': 'たとえば：罪悪感・こわい・もったいない'},
           {'l': '使ったあと', 'icon': 'sun', 'q': '「着てみたら、うれしかった」', 's': 'たとえば：安心・うれしい・意外と平気'})
    return fig('使う前の気持ちと、使ったあとの気持ちをくらべる', v,
               tip='レジで胸がぎゅっとしても大丈夫。気持ちは「使う前」と「使ったあと」で変わることがあります。')


def d11():
    env = ''.join(f'<span style="display:inline-flex;flex-direction:column;align-items:center;width:11mm">'
                  '<svg viewBox="0 0 24 16" style="width:8.4mm;height:5.6mm"><rect x="1" y="1" width="22" height="14" rx="2" fill="#fff" stroke="#C2862A" stroke-width="1.3"/>'
                  '<path d="M1.8 2.2 L12 9.4 L22.2 2.2" fill="none" stroke="#C2862A" stroke-width="1.3" stroke-linejoin="round"/></svg>'
                  f'<span style="font-size:6.8pt;color:var(--sub);margin-top:.6mm">{m}月</span></span>'
                  for m in range(1, 13))
    eq = ('<div class="eq"><div class="t"><div class="v">83,000円</div><div class="k">Day3の合計</div></div><div class="op">÷</div>'
          '<div class="t"><div class="v">12</div><div class="k">か月</div></div><div class="op">＝</div>'
          '<div class="t res"><div class="v">約7,000円</div><div class="k">毎月の特別費</div></div></div>')
    return fig('特別費は「来るか来ないか」ではなく「いつ来るか」', eq + f'<div class="center mt3" style="display:flex;justify-content:center;gap:1mm;flex-wrap:wrap">{env}</div>',
               tip='全額が無理なら、半分からでかまいません。これで来年の「今回だけ」に先回りできます。')


def d12():
    v = vs({'l': 'ごほうび型', 'icon': 'x', 'q': '頑張った日だけ使っていい', 's': '0か100かになり、罪悪感が残る'},
           {'l': '予定型', 'icon': 'check', 'q': '毎週土曜の朝は、パン屋さん（800円）', 's': '頑張りと関係なく、予定に入れる'})
    days = ['月', '火', '水', '木', '金', '土', '日']
    cal = ''.join(f'<div class="c{" on" if d == "土" else ""}"><div class="m">{d}</div>'
                  f'{"<div class=e>パン屋で朝ごはん</div><div class=y>800円</div>" if d == "土" else ""}</div>' for d in days)
    return fig('「ごほうび」ではなく、「予定」に入れる', v + f'<div class="cal w7 mt3">{cal}</div>',
               tip='「使っていい」と決めたお金は、わがままのお金ではありません。')


def d13():
    def bub(t, c='#fff'):
        return f'<span style="background:{c};border:1.3px solid var(--wk-t);border-radius:99px;padding:1mm 3.4mm;font-size:9pt;font-weight:700;color:var(--navy)">{t}</span>'
    col = lambda h, xs: (f'<div class="grow" style="background:var(--wk-t);border-radius:3.5mm;padding:2.6mm 3mm">'
                         f'<div class="mg" style="font-weight:700;color:var(--wk);font-size:9pt;margin-bottom:1.6mm">{h}</div>'
                         f'<div style="display:flex;flex-direction:column;gap:1.4mm;align-items:flex-start">{"".join(bub(x) for x in xs)}</div></div>')
    inner = ('<div class="row2" style="align-items:stretch">' +
             col('子どもの頃、本当は欲しかったもの', ['ピアノを習いたかった', '自分の部屋が欲しかった', '友だちと同じ文房具']) +
             col('最近、少し心が動いたこと', ['雑貨屋さんのマグカップ', 'カフェのピアノの音', '友人の旅行の写真']) +
             f'<div style="display:flex;align-items:center;color:var(--wk)">{icon("arrow-right", sw=2.5, style="width:6mm;height:6mm")}</div>'
             '<div style="width:36mm;flex:none;border:2px solid var(--wk);border-radius:4mm;background:#fff;padding:3mm;display:flex;flex-direction:column;justify-content:center;text-align:center">'
             f'<div style="color:var(--wk)">{icon("circle-check", style="width:8mm;height:8mm")}</div>'
             '<div class="mg" style="font-weight:700;color:var(--navy);font-size:10.4pt;line-height:1.5">カフェでピアノの<br>生演奏を聴く</div>'
             '<div class="small">試せそうなものに丸</div></div></div>')
    return fig('6つの候補から、1つだけ選ぶ', inner,
               tip='分からないのは、ずっと人を優先してきた証拠です。今日は候補が1つ見つかれば十分。')


def d14():
    blocks = [('安心ボックス', '1万円', 'package', 34), ('特別費', '月7,000円', 'mail', 26), ('使っていいお金', '月8,000円', 'coffee', 30)]
    stack = ''.join(f'<div style="height:{h}%;background:var(--wk-t);border:1.3px solid var(--wk);border-radius:2.4mm;display:flex;align-items:center;gap:2mm;padding:0 3mm;margin-top:1.4mm">'
                    f'{icon(ic, style="width:5mm;height:5mm;color:var(--wk)")}<b style="font-size:9.6pt">{n}</b><span class="grow"></span>'
                    f'<span class="mg" style="font-weight:700;color:var(--wk);font-size:10.6pt">{v}</span></div>' for n, v, ic, h in blocks)
    inner = ('<div class="row2" style="align-items:stretch;gap:6mm"><div style="width:84mm;flex:none;height:44mm;display:flex;flex-direction:column;justify-content:flex-end;position:relative;padding-top:6mm">'
             '<div style="position:absolute;top:0;left:-2mm;right:-2mm;border-top:2.4px dashed var(--gold)"></div>'
             '<div class="mg" style="position:absolute;top:-4.6mm;right:0;background:var(--gold);color:#fff;font-weight:700;font-size:8.4pt;padding:0 2.6mm;border-radius:99px">安心ライン</div>'
             + stack + '</div><div class="grow" style="display:flex;flex-direction:column;justify-content:center">'
             '<div class="mg" style="font-weight:700;color:var(--navy);font-size:12.4pt;line-height:1.6">「この3つがそろっていれば、<br>今月は大丈夫」</div>'
             '<p class="small mt2">声に出して、1回読みます。あとで何度変えてもかまいません。</p></div></div>')
    return fig('安心ライン＝3つの数字', inner, tip='仮のラインでいいんです。ラインがあること自体が大事です。')


def d15():
    b = bars([
        {'l': '今月 Day0', 'v': 7, 'max': 10, 'd': '7', 'gray': True},
        {'l': '今月 Day15', 'v': 5, 'max': 10, 'd': '5'},
        {'l': 'この先 Day0', 'v': 8, 'max': 10, 'd': '8', 'gray': True},
        {'l': 'この先 Day15', 'v': 8, 'max': 10, 'd': '8'},
    ])
    c = cards([
        {'icon': 'calendar-days', 'k': '「今月」が下がらない', 'h': '2週目の「分ける」を続ける', 's': 'まだ流れが見えきっていないか、本当に足りない不安かも'},
        {'icon': 'sprout', 'k': '「この先」だけ下がらない', 'h': '3週目の「ほどく」へ', 's': '家で覚えたお金のルールが関係していることが多い'},
    ], cols=2)
    return fig('Day0とくらべて、次にやることを決める', '<p class="small">（例）</p>' + b + '<div class="mt3"></div>' + c,
               tip='数字が変わらなくても、失敗ではありません。揺り戻しも、よくあることです。')


def d16():
    c = cards([{'icon': 'message-square-quote', 'k': '見つけるもの 1', 'h': '聞いた言葉', 's': '例：「大学に行かせるお金なんかないぞ」'},
               {'icon': 'house', 'k': '見つけるもの 2', 'h': '覚えている場面', 's': '例：お金のことで、両親がよく揉めていた'}], cols=2)
    chips = ('<div class="row2 mt2" style="justify-content:center;gap:5mm">' +
             '<span class="chip">' + icon('search', style='width:12px;height:12px') + '見つけるだけ</span>' +
             '<span class="chip">' + icon('feather', style='width:12px;height:12px') + '1つでもいい（多くても3つ）</span>' +
             '<span class="chip">' + icon('skip-forward', style='width:12px;height:12px') + 'つらければ飛ばしてOK</span></div>')
    return fig('家で聞いた言葉と場面を、そっと「見つける」', c + chips,
               tip='親を責めなくても、許さなくてもかまいません。見つけただけで、今日は十分です。')


def d17():
    L = ['「贅沢は敵だ」', 'お金の話をしない家']
    R = ['ため込みタイプ<br><small>「減ったら終わり」</small>', '受け取れないタイプ<br><small>「値段を言えない」</small>']
    row = lambda a, b: ('<div class="row2" style="gap:0;margin-bottom:2.4mm">'
                        f'<div style="width:62mm;flex:none;background:#fff;border:1.3px solid var(--wk-t);border-radius:3mm;padding:2mm 3mm;font-weight:700;color:var(--navy);font-size:9.6pt">{a}</div>'
                        '<div class="grow" style="height:0;border-top:2px dashed var(--wk);position:relative;margin:0 2mm">'
                        '<i style="position:absolute;left:-2mm;top:-2.2mm;width:3.6mm;height:3.6mm;border-radius:50%;background:var(--wk)"></i>'
                        '<i style="position:absolute;right:-2mm;top:-2.2mm;width:3.6mm;height:3.6mm;border-radius:50%;background:var(--wk)"></i></div>'
                        f'<div style="width:62mm;flex:none;background:var(--wk-t);border-radius:3mm;padding:2mm 3mm;font-weight:700;color:var(--navy);font-size:9.6pt;line-height:1.4">{b}</div></div>')
    head = ('<div class="row2" style="gap:0;margin-bottom:1.6mm;font-size:8.4pt;font-weight:700;color:var(--wk)">'
            '<div style="width:62mm">家で聞いた言葉・場面</div><div class="grow"></div><div style="width:62mm">今のクセ（あなたの2タイプ）</div></div>')
    return fig('言葉と今のクセを、線で結ぶ', head + row(L[0], R[0]) + row(L[1], R[1]),
               tip='線が1本でも引けたら、それは大きな発見です。「性格」が「覚えたルール」に見えてきます。')


def d18():
    f = flow([
        {'icon': 'quote', 'num': 'ルール', 'h': '「贅沢は敵だ」'},
        {'icon': 'shield', 'num': 'そのおかげで', 'h': '子どもの私は', 's': '父に怒られずにいられた', 'hi': True},
        {'icon': 'hand', 'num': 'いまは', 'h': '使うかどうかを<br>自分で選べる'},
    ], arrow='arrow-right')
    return fig('そのルールは、小さかったあなたを守っていた', f,
               tip='そのルールに「ありがとう」と言ってもいいし、言わなくてもいい。')


def d19():
    inner = ('<div class="row2" style="align-items:stretch;gap:3mm">'
             '<div style="width:44mm;flex:none;background:#F3F2F0;border-radius:3.5mm;padding:3mm;display:flex;flex-direction:column;justify-content:center">'
             '<div class="small" style="font-weight:700">口ぐせ</div><div class="mg" style="font-weight:700;color:#77768A;font-size:10.4pt;line-height:1.5">「お金は、頑張った人だけが使っていい」</div></div>'
             f'<div style="display:flex;align-items:center;color:var(--wk)">{icon("chevron-right", sw=2.5, style="width:5mm;height:5mm")}</div>'
             '<div class="grow" style="display:flex;flex-direction:column;gap:2mm">'
             '<div style="background:#fff;border:1.3px solid var(--line);border-radius:3mm;padding:1.8mm 3mm;font-size:9pt"><b style="color:var(--sub)">当てはまる例</b>　残業した日のごほうびは、気持ちが楽</div>'
             '<div style="background:#fff;border:1.3px solid var(--wk);border-radius:3mm;padding:1.8mm 3mm;font-size:9pt"><b style="color:var(--wk)">当てはまらない例</b>　友人には、頑張っていない日でも「休んでね」と言える</div></div>'
             f'<div style="display:flex;align-items:center;color:var(--wk)">{icon("chevron-right", sw=2.5, style="width:5mm;height:5mm")}</div>'
             '<div style="width:48mm;flex:none;background:var(--wk);border-radius:3.5mm;padding:3mm;display:flex;flex-direction:column;justify-content:center">'
             '<div style="font-size:8pt;font-weight:700;color:rgba(255,255,255,.85)">言い換え</div><div class="mg" style="font-weight:700;color:#fff;font-size:10pt;line-height:1.5">「お金は、頑張ったかどうかと関係なく、暮らしのために使っていい」</div></div></div>')
    return fig('口ぐせは、消さずに「言い換える」', inner,
               tip='「いつも本当にそう？」と、当てはまらない例を探すのがコツ。言い換えは1つで十分です。')


def d20():
    f = flow([
        {'icon': 'award', 'num': '1', 'h': '誇りに思えたこと', 's': '「丁寧な仕事をありがとう」と言われた'},
        {'icon': 'gem', 'num': '2', 'h': '大事にしている価値', 's': '丁寧さ'},
        {'icon': 'pen-line', 'num': '3', 'h': '500円以内で試す', 's': '仕事で使うペンを、少しいいものに（480円）', 'hi': True},
    ])
    v = vs({'l': 'やらないこと', 'icon': 'x', 'q': '「私はお金を受け取っていい」と言い聞かせる'},
           {'l': 'やること', 'icon': 'check', 'q': '大事にしていることから、小さく動く'})
    return fig('言い聞かせるより、大事にしていることから動く', f + '<div class="mt3"></div>' + v,
               tip='分かったのに変わらない。それは、ちゃんと向き合っている人だけがぶつかるつまずきです。')


def d21():
    inner = ('<div class="row2" style="gap:7mm;justify-content:center">'
             '<div class="phone"><div class="scr"><div class="tm">9:41</div>'
             '<div class="msg">お金がない家で育った。<br>でも今の私には、<br>非常口がある</div></div></div>'
             '<div style="max-width:88mm">' + cards([
                 {'icon': 'notebook-pen', 'h': '手帳'},
                 {'icon': 'smartphone', 'h': 'スマホの待ち受け'},
                 {'icon': 'sticky-note', 'h': 'メモアプリ'},
                 {'icon': 'door-open', 'h': '毎日目に入る場所'},
             ], cols=2) + '<p class="small mt2">Day19の言い換えを読み返して、1文に決めます。これが余裕プランの「書き直したお金の口ぐせ」になります。</p></div></div>')
    return fig('書き直した口ぐせを1文にして、目に入る場所へ', inner, tip='3週間、よく続けました。あと1週間です。')


def d22():
    days = ['月', '火', '水', '木', '金', '土', '日']
    cal = ''.join(f'<div class="c{" on" if d == "日" else ""}"><div class="m">{d}</div>'
                  f'{"<div class=e>夜9時<br>ソファで5分</div>" if d == "日" else ""}</div>' for d in days)
    f = flow([
        {'icon': 'tag', 'num': '1', 'h': '気持ちに名前'},
        {'icon': 'wallet', 'num': '2', 'h': '残高を見る'},
        {'icon': 'search', 'num': '3', 'h': '今週のもれ口', 'hi': True},
    ])
    return fig('週に1回、5分だけ。見る日と順番を決める', f'<div class="cal w7">{cal}</div><div class="mt3"></div>' + f,
               tip='見る日が決まると、見ない日を安心して過ごせます。給料日のあとの曜日がおすすめ。')


def d23():
    f = flow([
        {'icon': 'phone-incoming', 'h': '頼まれる', 's': '「ちょっとお金のことで…」'},
        {'icon': 'moon', 'h': '「一晩考えるね」', 's': 'すぐに答えない', 'hi': True},
        {'icon': 'sun', 'h': '翌朝、自分で選ぶ', 's': '上限は月1万円まで'},
    ])
    v = vs({'l': '仕方なく出す', 'icon': 'x', 'q': 'その場で「いいよ」', 's': '助けても、気持ちが満たされにくい'},
           {'l': '選んで出す', 'icon': 'check', 'q': '一晩おいて、自分で決める', 's': '助ける側も、助けられる側も楽になる'})
    return fig('すぐに答えない。一晩おいて「選んで出す」', f + '<div class="mt3"></div>' + v,
               tip='すぐに答えないことも、相手を大事にする方法の1つです。')


def d24():
    v = vs({'l': 'いつもの言い方', 'icon': 'x', 'q': '<span class="strike">すみません、</span>お見積もりは5万円<span class="strike">なんですが…</span>'},
           {'l': '言い切る一文', 'icon': 'check', 'q': '「お見積もりは5万円です」'})
    v2 = vs({'l': '会社員の場合', 'icon': 'briefcase', 'q': '「この役割を引き受けるなら、手当について相談させてください」'},
            {'l': '個人事業主の場合', 'icon': 'store', 'q': '「お見積もりは5万円です」'}, mid='minus')
    return fig('「すみません」を外して、言い切る', v + '<div class="mt3"></div>' + v2,
               tip='言い切る練習は、紙の上からで大丈夫です。')


def d25():
    v = vs({'l': '打ち消す', 'icon': 'x', 'q': '「いえいえ、全然です」'},
           {'l': '受け取る', 'icon': 'check', 'q': '「ありがとうございます、うれしいです」'})
    v2 = vs({'l': 'ごちそうになったら', 'icon': 'x', 'q': '「すみません、悪いです…」'},
            {'l': '受け取る', 'icon': 'check', 'q': '「ごちそうさまです。すごくおいしかったです」'})
    return fig('お金の前に、言葉を受け取る練習から', v + '<div class="mt3"></div>' + v2,
               tip='受け取ることも、相手への返事の1つです。')


def d26():
    f = flow([
        {'icon': 'moon', 'h': '疲れた夜', 's': '買い物アプリを開く'},
        {'icon': 'shopping-cart', 'h': 'カートに入れる', 's': '「選ぶ」ところまで'},
        {'icon': 'x-circle', 'h': '閉じる', 's': 'リマインダーを入れて', 'hi': True},
        {'icon': 'sun', 'h': '翌朝、見直す', 's': '買うかどうかは朝に決める'},
    ])
    return fig('落ち込んだ日は、「選んで、閉じる」', f + '<p class="small mt2">※選ぶだけで悲しい気持ちは軽くなりますが、怒っているときには効きにくいことが分かっています。</p>',
               tip='我慢ではなく、「あとで決める」です。')


def d27():
    cs = cards([
        {'icon': 'credit-card', 'k': 'ひと手間 1', 'h': 'カード情報を保存しない', 's': '通販サイトで、毎回入力する'},
        {'icon': 'layout-grid', 'k': 'ひと手間 2', 'h': 'アプリを2ページ目に移す', 's': '開くまでに、ひと呼吸できる'},
        {'icon': 'pen-line', 'k': 'ひと手間 3', 'h': '金額を手で1行書く', 's': '書き写すと、次の買い物にブレーキ'},
    ], cols=3)
    return fig('使いすぎやすい場面にだけ、ひと手間を1つ足す', cs,
               tip='手間は、未来の自分からの「ちょっと待って」です。全部の支払いに足さなくて大丈夫。')


def d28():
    q = lambda ic, k, v: (f'<div style="background:var(--wk-t);border-radius:3mm;padding:2mm 3mm">'
                          f'<div style="display:flex;gap:4px;align-items:center;font-weight:700;color:var(--wk);font-size:8.6pt">{icon(ic, style="width:13px;height:13px")}{k}</div>'
                          f'<div style="font-size:9.2pt;font-weight:700;color:var(--navy)">{v}</div></div>')
    inner = ('<div style="display:grid;grid-template-columns:1fr 46mm 1fr;gap:2.6mm;align-items:center">'
             + q('map-pin', '場所', '会社の帰り道') +
             '<div style="grid-row:span 2;background:#fff;border:2px solid var(--wk);border-radius:4mm;padding:3mm;text-align:center">'
             '<div class="small" style="font-weight:700;color:var(--wk)">できなかった場面</div>'
             '<div class="mg" style="font-weight:700;color:var(--navy);font-size:10pt;line-height:1.5">母の電話に、その場で「いいよ」と答えた</div></div>'
             + q('clock', '時間', '夜7時') + q('cloud', '気持ち', '疲れていて、早く切りたかった') + q('user', '誰と', '一人') + '</div>'
             '<div class="card-fill mt3"><div class="ttl">' + icon('lightbulb', style='width:13px;height:13px') + '変えられること'
             '</div><div class="mg" style="font-weight:700;color:var(--navy);font-size:10.6pt">帰り道の電話には出ず、家に着いてからかけ直す</div></div>')
    return fig('できなかった場面を、4つに分けて見直す', inner,
               tip='できなかった日を書けたなら、それは失敗ではなく、次への材料です。')


def d29():
    card = ('<div class="row2" style="gap:3mm;align-items:stretch">'
            '<div class="grow" style="background:var(--wk-t);border-radius:4mm;padding:3.4mm 4mm">'
            '<div class="mg" style="font-weight:700;color:var(--wk);font-size:12pt">もし</div>'
            '<div class="mg" style="font-weight:700;color:var(--navy);font-size:12pt">母から電話がきたら、</div></div>'
            f'<div style="display:flex;align-items:center;color:var(--wk)">{icon("arrow-right", sw=2.5, style="width:7mm;height:7mm")}</div>'
            '<div class="grow" style="background:var(--wk);border-radius:4mm;padding:3.4mm 4mm">'
            '<div class="mg" style="font-weight:700;color:rgba(255,255,255,.85);font-size:12pt">する</div>'
            '<div class="mg" style="font-weight:700;color:#fff;font-size:12pt">『一晩考えるね』と言ってから切る</div></div></div>')
    return fig('いちばん手強い場面のための「もしもの一文」', card + '<p class="small mt2 center">書いたら、声に出して1回くり返します。642件の実験をまとめた研究で、行動に移しやすくなることが確かめられています。</p>',
               tip='1つだけ。それでいちばんよく効きます。')


def d30():
    f = flow([
        {'icon': 'line-chart', 'num': '1', 'h': '並べる', 's': 'Day0・15・30の記録表'},
        {'icon': 'file-check', 'num': '2', 'h': '余裕プランを完成', 's': '付録の1枚を埋める'},
        {'icon': 'list-checks', 'num': '3', 'h': 'ふり返りチェック', 's': 'A・B・Cから1つ選ぶ', 'hi': True},
        {'icon': 'mail-open', 'num': '4', 'h': '30日後の自分へ', 's': '3行の手紙'},
    ])
    return fig('完成の日にやること', f)


FIGS = {i: globals()[f'd{i}'] for i in range(31)}
