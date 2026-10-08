"""Day30のあと：ふり返りチェック・付録・このワークのあとに・おわりに"""
from lib import icon, aoi, talk, fig, flow, cards, paras, lab_row
from pages_front import add, head, memo, point, ilist, nlist, h3, tip, qr, pos, flower, sparkle, TYPES, LINE_URL

TODO = '<span class="todo">要確認</span>'


# ---------- Day30のあと ----------
def furikaeri(book):
    book.mark('furikaeri')

    def abc(letter, color, tint, title, inner, go):
        return (f'<div class="abc" style="border-color:{color};background:{tint}"><div class="ah"><span class="al" style="background:{color}">{letter}</span>'
                f'<span class="at">{title}</span></div>{inner}<div class="go" style="color:{color}">{icon("arrow-right", sw=2.5, style="width:15px;height:15px")}{go}</div></div>')
    a = abc('A', '#2A8B7F', '#F1F9F7', '不安が下がり、余裕プランが回り始めた',
            '<ul><li>不安メーターが、Day0より下がった</li><li>お金を見る日、先取り、一言カードのどれかが続いている</li></ul>',
            'このワークを、ひとりで続けましょう。「ひとりで続ける方へ」（p.{{PG:alone}}）に、次の30日の進め方を書いています。')
    b = abc('B', '#8064BF', '#F7F4FC', 'お金の流れは見えたのに、気持ちが変わらない',
            '<div style="font-size:9.4pt;margin-bottom:1mm">次のうち、<b>2つ以上</b>当てはまる</div><ul class="cb" style="color:#8064BF">' +
            ''.join(f'<li><span style="color:var(--ink)">{x}</span></li>' for x in [
                '頭では分かったのに、気持ちがついてこない（つまずき②で止まった）', '自分が何をしたいのか、まだよく分からない（つまずき①で止まった）',
                '決めたのに、同じ相手・同じ場面で、同じことをくり返している（つまずき③で止まった）', 'お金の話になると、今も親の顔や声が浮かぶ',
                '「この先」の不安の点数が、Day0からほとんど変わらない', 'お金以外の場面（人間関係・仕事）でも、人に合わせすぎて疲れてしまう']) + '</ul>',
            '次のページを読んでください。')
    c = abc('C', '#C25B6A', '#FDF3F4', '心や体のつらさが強い',
            '<ul><li>眠れない・食べられないなどの不調が、2週間以上続いている</li><li>買い物をやめたいのにやめられず、隠したり、うそをついたりしている</li><li>返済のために、別の借り入れをしている</li></ul>',
            'ワークを続けるより先に、医療機関や専門の窓口に相談してください。ひとりで抱えないでください。')
    body = (head('Day30｜完成の日', '30日のふり返りチェック：次の30日を、どう進めますか') +
            '<p>記録表と余裕プランを見ながら、いちばん近いものを1つ選んでください。</p>' + a + b + c)
    add(book, body, wk='gold', run='30日ワーク　完成の日')


def kawaranakatta(book):
    book.mark('kawaranakatta')
    lines = ''.join(f'<p style="margin:0 0 .2em">{x}</p>' for x in ['お金の流れは、見えるようになった。', '分ける仕組みも、一言カードもできた。',
                                                                     'それでも気持ちが動かないなら、根っこはもう、お金の使い方にはありません。'])
    rules = ''.join(f'<div style="flex:1;background:#fff;border:1.3px solid var(--lav);border-radius:3mm;padding:2.4mm 3mm;text-align:center" class="mg"><b style="color:#5E4596;font-size:9.8pt">{x}</b></div>'
                    for x in ['自分の分は、いつも最後でいい', '自分には、それを受け取る価値がない', '自分が何をしたいかより、相手の機嫌が先'])
    body = (head('Day30のあとに', '30日やっても、変わらなかったあなたへ') +
            talk(['Bに当てはまったなら、最初に伝えさせてください。'], who='アオより', ic='sparkles') +
            point('それは、あなたのやり方が悪かったからでも、<br>努力が足りなかったからでもありません。', lab='まず、これだけは') +
            '<p>30日、手を抜かずに進んできた人ほど、ここにたどり着きます。</p>' +
            f'<div style="border-left:3px solid var(--gold-l);padding:1mm 0 1mm 5mm;margin:3mm 0 4mm;font-family:Zen Maru Gothic;font-weight:700;color:var(--navy);font-size:11.4pt;line-height:1.9">{lines}</div>' +
            '<div class="box" style="background:var(--lav-l);border-color:transparent;text-align:center;padding:5mm">'
            '<div class="small">根っこは、ここにあります</div>'
            '<div class="mg" style="font-weight:700;color:#5E4596;font-size:16pt;margin:1mm 0 3mm">子どもの頃の家で覚えた「自分の扱い方」</div>'
            f'<div style="display:flex;gap:2.4mm">{rules}</div></div>' +
            '<p class="mt3">お金のクセは、この「自分の扱い方」が、いちばん目に見える形で出てきたものです。だから、お金のワークだけでは、根っこまでは届かないことがあります。</p>')
    add(book, body, wk='loosen', run='このワークのあとに')

    rec = flow([{'icon': 'user-round', 'h': 'あなたの2タイプ', 's': 'Day0'}, {'icon': 'scroll-text', 'h': '余裕プラン', 's': 'Day30'},
                {'icon': 'message-square-quote', 'h': '家で聞いたお金の言葉', 's': 'Day16'}], arrow='plus')
    eyes = ('<div class="grid2">'
            '<div class="box" style="text-align:center"><div style="color:#9A98A8">' + icon('user', style='width:10mm;height:10mm') + '</div>'
            '<div class="mg" style="font-weight:700;color:#77768A;margin-top:1mm">ひとりで30日</div><div class="small">自分の思い込みには、<br>自分ではなかなか気づけない</div></div>'
            '<div class="box tint" style="text-align:center"><div style="color:var(--wk)">' + icon('users', style='width:10mm;height:10mm') + '</div>'
            '<div class="mg" style="font-weight:700;color:var(--navy);margin-top:1mm">ほかの人と一緒に</div><div class="small">ひとりで見えなかったものが、<br>思いがけず見えることがある</div></div></div>')
    body = (head('Day30のあとに', 'ひとりで見えなかったものは、一緒に見ると見えることがあります') +
            '<p>人は自分の思い込みに、自分ではなかなか気づけません（Day20の研究メモ）。ひとりで30日向き合っても見えなかったものが、ほかの人と一緒に見ると、思いがけず見えることがあります。</p>' +
            fig('ひとりで見る／一緒に見る', eyes) +
            '<p class="mg" style="font-weight:700;color:var(--navy);font-size:12pt">僕が1対1のセッションをしているのは、そのためです。</p>' +
            fig('ゼロからではなく、この30日の続きから', rec + '<div class="center mt3 mg" style="font-weight:700;color:var(--navy)">このワークで書いてきたものは、そのままセッションで使えます。</div>',
                tip='詳しくは、巻末の「個別セッションのご案内」（p.{{PG:session}}）を読んでください。', tag='図解', style='--wk:#8064BF;--wk-t:#F1ECFA;--wk-d:#5E4596'))
    add(book, body, wk='loosen', run='このワークのあとに')


# ---------- 付録 ----------
def plan(book):
    book.mark('appendix')
    book.mark('plan')
    rows = [('わたしの2タイプ', '', 'Day0'), ('お金のもれ口トップ1', '', 'Day7'), ('お金を見る日', '毎週　　曜日　　時、　　　　で', 'Day22'),
            ('安心ボックス', '名前　　　　／目標　　　円／毎月　　　円を自動で', 'Day8・9'), ('特別費', '毎月　　　円／置き場所', 'Day11'),
            ('使っていいお金', '毎月　　　円／予定に入れた楽しみ', 'Day12'), ('人に出す枠と上限', '月　　　円まで／頼まれたら「　　　　」と言う', 'Day23'),
            ('書き直したお金の口ぐせ', '', 'Day21'), ('もしもの一文', 'もし　　　　になったら、　　　　する', 'Day29'),
            ('疲れているサイン', 'お金を使う前の、わたしの前ぶれ：', 'Day28'), ('次の30日でやること', '', 'Day30')]
    tr = ''.join(f'<tr><td class="no">{i + 1}</td><td class="it">{a}</td><td class="tp">{b}</td><td class="dy">{c}</td></tr>' for i, (a, b, c) in enumerate(rows))
    body = (head('付録1', '心と財布の余裕プラン', h1=True).replace('h1 class="title"', 'h1 class="title" style="margin-bottom:1mm"') +
            '<p class="small" style="margin-bottom:3mm">Day30に完成させる、あなただけの1枚です。分かるところから埋めていってかまいません。</p>' +
            f'<table class="plan"><tr><th style="width:9mm">#</th><th>項目</th><th>わたしの場合</th><th style="width:20mm;text-align:center;white-space:nowrap">書いた日</th></tr>{tr}</table>')
    add(book, body, wk='gold', run='付録')


def progress(book):
    book.mark('progress')
    cells = ['買った'] + [f'Day{i}' for i in range(31)]
    col = lambda i: '#283265' if i <= 0 else '#3A74C2' if i <= 7 else '#C2862A' if i <= 14 else '#8064BF' if i <= 21 else '#2A8B7F' if i <= 29 else '#B48C45'
    out = ''
    for k, c in enumerate(cells):
        n = k - 1
        stp = {13: 'つまずき①', 20: 'つまずき②', 28: 'つまずき③'}.get(n, '')
        w = f'<div class="pw">{stp}</div>' if stp else ''
        out += f'<div class="pc" style="--pc:{col(n) if n >= 0 else "#B48C45"}"><div class="pd">{c}</div>{w}</div>'
    tk = ''.join(f'<div class="ticket"><div class="tk">SKIP TICKET</div><div class="tn">スキップ券</div><div class="td">使った日：Day＿＿</div></div>' for _ in range(8))
    body = (head('付録2', '進捗表とスキップ券', h1=True) +
            '<p>1日やったら、1マス塗ります。「買った」と「Day0」の2マスは、Day0が終わったら塗ってください。</p>' +
            fig('進捗表（32マス）', f'<div class="ptable">{out}</div>', tag='塗る') +
            fig('スキップ券（8枚）', f'<div class="tickets">{tk}</div>',
                tip='書けない日は、1枚使って、その日のマスに「スキップ」と書いてください。翌日に戻ってくれば大丈夫です。', tag='使う'))
    add(book, body, wk='gold', run='付録')


def record(book):
    book.mark('record')
    tr = ''.join(f'<tr><td class="k"><span style="color:{t[3]};margin-right:1.6mm">{icon(t[2], style="width:14px;height:14px")}</span>{t[0]}</td><td class="v"></td><td class="v"></td><td class="v"></td></tr>' for t in TYPES)
    t1 = f'<table class="rec" style="--wk:var(--navy)"><tr><th style="text-align:left">タイプ（各0〜12点）</th><th>Day0</th><th>Day15</th><th>Day30</th></tr>{tr}</table>'
    qs = ['今月のお金の不安（0〜10）', 'これから1〜3年のお金の不安（0〜10）', '1か月にいくら使っているか、だいたい分かる（はい／いいえ）',
          '急な出費に備えたお金（生活費の1か月分くらい）がある（はい／いいえ／分からない）']
    tr2 = ''.join(f'<tr><td class="k" style="font-size:8.8pt;padding:1.4mm 3mm">{q}</td><td class="v"></td><td class="v"></td><td class="v"></td></tr>' for q in qs)
    t2 = f'<table class="rec" style="--wk:var(--navy)"><tr><th style="text-align:left">お金の不安メーター</th><th>Day0</th><th>Day15</th><th>Day30</th></tr>{tr2}</table>'
    # グラフ
    W, H, L, B, T, R = 176, 64, 14, 10, 6, 10
    g = ''
    for v in range(0, 11, 2):
        y = T + (H - T - B) * (1 - v / 10)
        g += f'<line x1="{L}" y1="{y:.1f}" x2="{W - R}" y2="{y:.1f}" stroke="#ECE7DA" stroke-width=".3"/><text x="{L - 3}" y="{y + 1.2:.1f}" font-size="3.2" fill="#9A98A8" text-anchor="end">{v}</text>'
    xs = [L + 14, (L + W - R) / 2, W - R - 14]
    for x, lab in zip(xs, ['Day0', 'Day15', 'Day30']):
        g += f'<line x1="{x:.1f}" y1="{T}" x2="{x:.1f}" y2="{H - B}" stroke="#E0DACB" stroke-width=".3" stroke-dasharray="1 1"/><text x="{x:.1f}" y="{H - 3}" font-size="3.4" fill="#283265" text-anchor="middle" font-weight="700">{lab}</text>'
    chart = (f'<div class="chart"><svg viewBox="0 0 {W} {H}" style="width:100%;height:100%;display:block">{g}</svg></div>'
             '<div style="display:flex;gap:6mm;justify-content:center;margin-top:2mm;font-size:8.6pt">'
             '<span><span class="dotc" style="background:#3A74C2"></span> 今月の不安（●でつなぐ）</span><span><span style="display:inline-block;width:0;height:0;border-left:1.8mm solid transparent;border-right:1.8mm solid transparent;border-bottom:3.2mm solid #B48C45;vertical-align:-1px"></span> この先の不安（▲でつなぐ）</span></div>')
    body = (head('付録3', '記録表（Day0・Day15・Day30）', h1=True) + t1 + '<div style="height:4mm"></div>' + t2 +
            fig('不安メーターの変化をグラフに', chart, tag='書く', style='margin-top:4mm'))
    add(book, body, wk='gold', run='付録')


FAQ = [('書く時間がない日は？', '1行だけでかまいません。それも無理な日は、スキップ券を使ってください。'),
       ('家計簿アプリを使ってもいいですか？', 'もちろん使えます。ただ、見るのは週に1回、5分だけにしてください。'),
       ('実家に仕送りをしています。減らさないといけませんか？', '減らすかどうかは、あなたが決めることです。このワークでするのは、出す枠と上限を「自分で選んで」決めることです。'),
       ('パートナーと家計が一緒です。', 'まずは、自分の分のお金から始めてください。'),
       ('借金があります。', '返済のために別の借り入れをしているときは、ワークより先に、専門の窓口に相談してください。'),
       ('親のことを思い出すのがつらいです。', 'Day16は飛ばしてかまいません。親を許す必要も、親と向き合う必要もありません。'),
       ('30日で終わりませんでした。', '何日かかってもかまいません。戻ってきた日が、続きの日です。'),
       ('先取りの自動設定のやり方が分かりません。', '使っている銀行のアプリやサイトで、「定額自動振込」「自動入金」「積立」などの言葉を探してみてください。銀行によって名前が違います。'),
       ('30日やっても、変わりませんでした。', 'Day30の「30日のふり返りチェック」（p.{{PG:furikaeri}}）に答えてみてください。Bに当てはまるなら、それはあなたの努力不足ではなく、根っこがひとりでは見えにくい場所にあるサインです。巻末の個別セッションのご案内（p.{{PG:session}}）を読んでみてください。'),
       ('個別セッションは、ワークを最後まで終えていないと受けられませんか？', '途中でも受けられます。ワークの記録があると、その続きから始められます。' + TODO)]


def faq(book):
    book.mark('faq')
    qa = ''.join(f'<div class="faq"><div class="q"><span class="qq">Q</span><span>{q}</span></div><div class="a"><span class="aa">A</span><span>{a}</span></div></div>' for q, a in FAQ)
    body = (head('付録4', 'よくある質問', h1=True) + qa +
            '<div class="small mt3" style="display:flex;align-items:center;gap:2mm">' + icon('message-circle-heart', style='width:15px;height:15px;color:var(--gold)') +
            'いただいた質問と答えは、購入者限定のLINEでお届けします。</div>')
    add(book, body, wk='gold', run='付録')


# ---------- このワークのあとに ----------
def alone(book):
    book.mark('after')
    book.mark('alone')
    rh = [('calendar-check', '週に1回', 'お金を見る日', 'そのまま続けます（5分）'),
          ('gauge', '月に1回', '不安メーター', '4つの質問に答えて、記録表に書き足します'),
          ('scroll-text', '3か月に1回', '余裕プランを見直す', '暮らしが変われば、書き直していいものです'),
          ('wind', '場面が変わったら', 'もしもの一文', '手強い場面が変わったら、1つだけ書き直します')]
    tl = '<div class="tl">' + ''.join(
        f'<div class="tr" style="--c:#2A8B7F;grid-template-columns:31mm 8mm 1fr"><div class="td" style="white-space:nowrap">{a}</div><div class="tdot"><i></i></div>'
        f'<div class="tc"><span class="tt" style="display:flex;align-items:center;gap:1.6mm;width:46mm;white-space:nowrap">{icon(ic, style="width:15px;height:15px")}{b}</span><span class="tx">{c}</span></div></div>' for ic, a, b, c in rh) + '</div>'
    body = (f'<div style="text-align:center;padding-top:6mm"><div class="kicker" style="letter-spacing:.4em">AFTER 30 DAYS</div>'
            '<div class="mg" style="font-weight:700;color:var(--navy);font-size:26pt;letter-spacing:.08em;margin:2mm 0 8mm">このワークのあとに</div></div>' +
            head('このワークのあとに', 'ひとりで続ける方へ') +
            '<p>30日は、新しい習慣のいちばん大変な最初の上り坂です。ここからは、少しずつ力を抜いていきましょう。</p>' +
            fig('次の30日のリズム', tl, tip='迷ったときは、このワークのどのページからでも、またやり直してください。', style='--wk:#2A8B7F;--wk-t:#E1F3F0;--wk-d:#1C665D') +
            '<div class="stopbox" style="margin-top:2mm"><div>' + icon('compass', style='width:22px;height:22px;color:#5E4596') + '</div><div>'
            '<div class="t">ひとりで続けても、同じところで止まるときは</div>'
            '<p>Day30の「30日のふり返りチェック」（p.{{PG:furikaeri}}）をもう一度見てみてください。Bに当てはまるなら、次のページの個別セッションのご案内も読んでみてください。</p></div></div>')
    add(book, body, wk='decide', run='このワークのあとに')


def session(book):
    book.mark('session')
    hero = ('<div class="offer" style="display:flex;gap:6mm;align-items:center">'
            '<div style="flex:1"><div class="on">INDIVIDUAL SESSION</div><div class="ot">アダルトチルドレン克服セッション<span style="font-size:11pt;margin-left:2mm;color:var(--gold-l)">（1対1）</span></div>'
            '<p style="margin:0">このワークで見えてきた「お金のクセ」の、その奥にある根っこを、僕と一緒に見ていくセッションです。</p></div>'
            '<div style="width:36mm;height:36mm;border-radius:50%;flex:none;background:#fff url(../assets/aoi_circle_600.png) center/cover no-repeat;box-shadow:0 0 0 2px var(--gold-l),0 0 0 5px rgba(255,255,255,.25)"></div>'
            + pos(sparkle(5, '#E8D6AE'), top=6, right=48) + pos(sparkle(3, '#E8D6AE'), top=14, right=44) + '</div>')
    who = ilist(['30日のふり返りチェックで、Bに当てはまった', '頭では分かっているのに、気持ちがついてこない', '親の言葉や顔が、今もお金の場面で浮かぶ',
                 'お金だけでなく、人間関係や仕事でも、同じクセがくり返し出てくる'], ic='check')
    do = flow([{'num': 'STEP 1', 'icon': 'notebook-pen', 'h': 'ワークの記録を一緒に見る', 's': 'あなたの2タイプ・余裕プラン・家で聞いたお金の言葉'},
               {'num': 'STEP 2', 'icon': 'search', 'h': '「根っこのルール」を言葉にする', 's': 'ひとりでは見えにくいところ'},
               {'num': 'STEP 3', 'icon': 'git-merge', 'h': 'お金以外の場面も整理する', 's': '同じクセが出ているところ'},
               {'num': 'STEP 4', 'icon': 'flag', 'h': '次の1か月でやることを1つ決める', 'hi': True}])
    dont = cards([{'icon': 'hand', 'h': '親と向き合うことや、許すことを求めません'}, {'icon': 'heart', 'h': 'あなたを責めません'},
                  {'icon': 'stethoscope', 'h': '病気の診断や治療はしません', 's': '必要なときは、医療機関をおすすめします'}], cols=3)
    body = (head('このワークのあとに', '個別セッションのご案内') + hero +
            '<div class="grid2 mt4" style="grid-template-columns:1.5fr .62fr">'
            f'<div class="box tint"><h4>{icon("user-round-check")}こんな方に</h4>{who}</div>'
            '<div class="box" style="display:flex;flex-direction:column;justify-content:center;text-align:center">'
            '<div class="small">これまで</div><div class="mg" style="font-weight:700;color:var(--wk);font-size:30pt;line-height:1.1">250<small style="font-size:12pt">人</small></div>'
            '<div class="small">1対1のセッションで<br>向き合ってきた方の数</div></div></div>' +
            fig('セッションでやること ' + TODO, do, tag='流れ', style='margin-top:4mm') +
            h3('セッションでやらないこと', 'shield-check') + dont)
    add(book, body, wk='decide', run='このワークのあとに')

    info = ('<table class="tbl" style="--wk:var(--navy)">'
            f'<tr><td class="k" style="width:28mm">形式</td><td>{TODO}　オンライン／時間／回数</td></tr>'
            f'<tr><td class="k">料金</td><td>{TODO}</td></tr>'
            '<tr><td class="k">申し込み</td><td>購入者限定LINEで<b>「セッション」</b>と送ってください。詳しいご案内と、申し込みフォームをお送りします。</td></tr></table>')
    line = (f'<div class="box" style="display:flex;gap:6mm;align-items:center;border:1.8px solid #06C755;margin-top:4mm">{qr("qr_line")}'
            '<div><div class="mg" style="font-weight:700;color:var(--navy);font-size:13pt">LINEで「セッション」と送るだけ</div>'
            '<div class="small" style="margin:1mm 0 2mm">QRを読み取って、購入者限定LINEを開いてください。</div>'
            '<div style="display:inline-flex;align-items:center;gap:2mm;background:#06C755;color:#fff;border-radius:99px;padding:1mm 5mm;font-weight:700;font-size:10pt">'
            + icon('send', style='width:14px;height:14px') + '「セッション」と送る</div>'
            f'<div style="font-size:7.4pt;color:var(--mute);margin-top:1.6mm">{LINE_URL}</div></div></div>')
    bring = ilist([('table', '付録3の記録表（Day0・Day15・Day30）'), ('scroll-text', '付録1の余裕プラン'),
                   ('book-open', '書ける範囲で、Day16〜19のページ（見せたくないところは、見せなくてかまいません）')])
    body = (head('このワークのあとに', '申し込み方法と、用意してほしいもの') + info + line +
            h3('セッションの前に用意してほしいもの', 'clipboard-list') + bring +
            '<div class="warn mt4"><h4>' + icon('triangle-alert', style='width:18px;height:18px') + 'セッションより先に、相談してほしいとき</h4>'
            '<p style="margin:0;font-size:9.6pt">次のような状態のときは、セッションより先に、医療機関や専門の窓口に相談してください。眠れない・食べられないなどの不調が2週間以上続いている／買い物をやめられず隠してしまう／返済のために別の借り入れをしている。</p></div>' +
            tip('このワークで書いてきたものを持って、続きから始めましょう。', style='margin-top:6mm'))
    add(book, body, wk='decide', run='このワークのあとに')


def owari(book):
    book.mark('owari')
    deco = (pos(flower(22, '#9C98DC', op=.35), bottom=16, left=10) + pos(flower(13, '#B6B3E8', op=.45), bottom=36, left=28) +
            pos(flower(17, '#9C98DC', op=.35), bottom=20, right=14) + pos(sparkle(5), top=40, right=26) + pos(sparkle(3.5), top=50, right=36))
    body = (f'<div style="text-align:center;padding-top:10mm"><div class="kicker" style="letter-spacing:.4em;color:var(--gold)">EPILOGUE</div>'
            '<div class="mg" style="font-weight:700;color:var(--navy);font-size:26pt;letter-spacing:.12em;margin-top:2mm">おわりに</div>'
            '<div style="width:44mm;height:44mm;border-radius:50%;margin:8mm auto 9mm;background:#fff url(../assets/aoi_circle_600.png) center/cover no-repeat;'
            'box-shadow:0 0 0 2px var(--gold-l), 0 0 0 5px #fff, 0 0 0 6px var(--gold-l)"></div></div>'
            '<div style="max-width:142mm;margin:0 auto;font-size:11pt;line-height:2.05">' +
            paras(['30日間、このワークにつき合ってくださって、ありがとうございました。',
                   'お金の不安は、あなたの性格のせいではありませんでした。家で見て覚えたルールと、気づかないうちにお金が出ていくもれ口と、まだ決まっていなかった安心ラインが、重なっていただけです。',
                   'この30日でつくった余裕プランは、完成品ではありません。暮らしが変われば、書き直していいものです。迷ったときは、このワークのどのページからでも、またやり直してください。',
                   'そして、もしひとりでは届かない場所に気づいたなら、そのときは、一緒に見ていきましょう。']) +
            '<div class="mg" style="text-align:right;font-weight:700;color:var(--navy);font-size:14pt;letter-spacing:.3em;margin-top:6mm">アオ</div></div>')
    add(book, body, wk='gold', run='おわりに', bg=deco)


def back_cover(book):
    inner = ('<div style="position:absolute;inset:0;background:linear-gradient(160deg,#2E3A73,#232B5A)"></div>'
             + pos(sparkle(6, '#E8D6AE'), top=40, left=34) + pos(sparkle(4, '#E8D6AE'), top=52, left=26) + pos(sparkle(5, '#E8D6AE'), top=210, right=34)
             + '<div style="position:absolute;top:96mm;left:0;right:0;text-align:center;color:#fff">'
             '<div style="width:40mm;height:40mm;border-radius:50%;margin:0 auto 9mm;background:#fff url(../assets/aoi_circle_600.png) center/cover no-repeat;box-shadow:0 0 0 2px #E8D6AE,0 0 0 6px rgba(255,255,255,.12)"></div>'
             '<div class="mg" style="font-weight:700;font-size:15pt;letter-spacing:.08em">毒親育ちのお金の不安がなくなる小さな習慣</div>'
             '<div class="mg" style="font-weight:700;font-size:10.5pt;color:#E8D6AE;letter-spacing:.14em;margin-top:2mm">心と財布に余裕が生まれる30日ワーク</div>'
             '<div class="mg" style="margin-top:14mm;font-weight:700;letter-spacing:.4em;font-size:11pt">アオ</div></div>')
    book.add(inner, cls='cover', raw=True)


def build(book):
    furikaeri(book)
    kawaranakatta(book)
    plan(book)
    progress(book)
    record(book)
    faq(book)
    alone(book)
    session(book)
    owari(book)
    back_cover(book)
