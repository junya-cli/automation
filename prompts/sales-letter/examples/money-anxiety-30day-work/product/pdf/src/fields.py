"""Day0〜30 の書き込み欄"""
from lib import icon


def B(w):
    return ('blank', w)


def L(label, n=1, numbered=False, h=9):
    return {'k': 'L', 'label': label, 'n': n, 'num': numbered, 'h': h}


def I(label, parts):
    return {'k': 'I', 'label': label, 'parts': parts}


def T(headers, rows, widths=None):
    return {'k': 'T', 'headers': headers, 'rows': rows, 'widths': widths}


def C(label, opts):
    return {'k': 'C', 'label': label, 'opts': opts}


def K(title, tpl, n=2):
    return {'k': 'K', 'title': title, 'tpl': tpl, 'n': n}


def G(items):
    return {'k': 'G', 'items': items}


def N(text):
    return {'k': 'N', 'text': text}


FIELDS = {
    0: [I('あなたの2タイプ', [B(58), '／', B(58)]),
        I('不安メーター', ['今月', B(16), '／10　　この先', B(16), '／10']),
        L('レシートを見たときの気持ち'), L('毎日やる時間と場所')],
    1: [L('今の「足りない」（1行で）'), I('その強さ', [B(18), '点（0〜10）']),
        T(['使ったもの', '金額', '色（青・黄・緑・灰）'], 6, ['46%', '22%', '32%'])],
    2: [L('見る前の気持ち', 2), L('見たあとの気持ち', 2)],
    3: [{'k': 'M'}, I('合計', [B(45), '円　→ Day11で使います'])],
    4: [I('最初の予想', [B(40), '円']), L('いつもと違う出費が出そうな理由', 3, True), I('書き直した予想', [B(40), '円'])],
    5: [T(['何の支払い', '月額', '最後に使った日', '決めたこと'], 7, ['34%', '18%', '24%', '24%'])],
    6: [C('一番多い色に丸', ['青', '黄', '緑', '灰']), L('その色が多くなる場面', 2)],
    7: [C('もれ口トップ1に丸', ['もれ口1', 'もれ口2', 'もれ口3', 'もれ口4']),
        I('私の「足りない」の正体は、', [B(104), 'だった']), I('今月の不安', [B(16), '／10'])],
    8: [L('場所'), L('名前'), I('目標額', [B(40), '円']), L('写真')],
    9: [I('毎月', [B(16), '日に', B(34), '円を自動で']), L('移す先'), L('お知らせの名前'),
        N('設定できたら、ここにチェック □')],
    10: [I('使ったもの', [B(70), '金額', B(30), '円']), L('使う前の気持ち', 2), L('使ったあとの気持ち', 2)],
    11: [I('Day3の合計', [B(34), '円 ÷ 12 ＝ 毎月', B(30), '円']), L('置き場所')],
    12: [I('毎月の使っていいお金', [B(40), '円']),
         I('予定に入れた小さな楽しみ', ['毎週', B(14), '曜日／', B(72)])],
    13: [L('子どもの頃、本当は欲しかったもの・やりたかったこと', 3, True), L('最近、少しでも心が動いたこと', 3, True),
         L('試せそうなもの（丸をつけた1つ）')],
    14: [I('安心ボックスの目標', [B(40), '円']), I('毎月の特別費', [B(40), '円']), I('毎月の使っていいお金', [B(40), '円']),
         N('3つを書いたら、「この3つがそろっていれば、今月は大丈夫」と声に出して読みます')],
    15: [N('付録の記録表に、今日の点数を書きます'), L('変わったこと', 2), L('変わっていないこと', 2)],
    16: [L('聞いた言葉', 3, True), L('覚えている場面', 3)],
    17: [{'k': 'LINK', 'rows': 3}],
    18: [K('1文で書く', '「　　　　　　　　」のおかげで、子どもの私は、　　　　　　　　　　でいられた', 3)],
    19: [L('口ぐせ'), L('当てはまる例'), L('当てはまらない例'), L('言い換え', 2)],
    20: [L('誇りに思えたこと'), L('大事にしている価値'), I('使い道', [B(76), '金額', B(24), '円'])],
    21: [L('書き直したお金の口ぐせ', 2), L('書いた場所')],
    22: [K('一言カード', '「◯曜日の◯時、◯◯で、5分だけお金を見る」', 2)],
    23: [K('一言カード', '「頼まれたら『◯◯』と言う。出すのは月◯円まで」', 2)],
    24: [K('一言カード', '値段や希望を、「すみません」を付けずに言い切る1文', 2)],
    25: [K('一言カード', '褒め言葉・お礼・ごちそうを受け取るときの一言', 2)],
    26: [K('一言カード', '「疲れた夜は、◯◯まで。買うかどうかは◯◯に決める」', 2)],
    27: [K('一言カード', '使いすぎやすい場面と、足すひと手間', 2)],
    28: [L('できなかった場面'), G([L('場所'), L('時間'), L('気持ち'), L('誰と')]), L('変えられること', 2)],
    29: [{'k': 'IF'}],
    30: [C('いちばん止まったつまずきポイントに丸', ['① 何に使いたいか分からない（Day13）', '② 分かっても気持ちが変わらない（Day20）', '③ 決めたのにできない（Day28）']),
         L('30日後の私へ', 4)],
}


def render_field(f, idx):
    k = f['k']
    if k == 'L':
        if f['num']:
            lines = ''.join(f'<div class="ln" style="display:flex;align-items:flex-end;padding-bottom:1mm"><span class="mg" style="color:var(--wk);font-weight:700;width:7mm">{"①②③④⑤"[i]}</span></div>' for i in range(f['n']))
        else:
            lines = '<div class="ln"></div>' * f['n']
        return f'<div class="field"><div class="fl">{f["label"]}</div>{lines}</div>'
    if k == 'I':
        parts = []
        for p in f['parts']:
            if isinstance(p, tuple):
                parts.append(f'<span class="blank" style="width:{p[1]}mm"></span>')
            else:
                parts.append(f'<span>{p}</span>')
        return f'<div class="field"><div class="inline"><span class="fl" style="margin:0 2mm 0 0">{f["label"]}</span>{"".join(parts)}</div></div>'
    if k == 'T':
        w = f['widths'] or [''] * len(f['headers'])
        th = ''.join(f'<th style="width:{x}">{h}</th>' for h, x in zip(f['headers'], w))
        tr = ''.join('<tr>' + '<td></td>' * len(f['headers']) + '</tr>' for _ in range(f['rows']))
        return f'<div class="field"><table class="wtable"><tr>{th}</tr>{tr}</table></div>'
    if k == 'C':
        ops = ''.join(f'<span>{o}</span>' for o in f['opts'])
        return f'<div class="field"><div class="fl">{f["label"]}</div><div class="circle-opts">{ops}</div></div>'
    if k == 'K':
        lines = '<div class="ln"></div>' * f['n']
        return (f'<div class="field"><div class="card-fill"><div class="ttl">{icon("id-card", style="width:14px;height:14px")}{f["title"]}</div>'
                f'<div class="tpl">{f["tpl"]}</div>{lines}</div></div>')
    if k == 'G':
        inner = ''.join(render_field(x, 0) for x in f['items'])
        return f'<div style="display:grid;grid-template-columns:1fr 1fr;column-gap:6mm">{inner}</div>'
    if k == 'N':
        return f'<div class="field small" style="display:flex;gap:2mm;align-items:center">{icon("info", style="width:14px;height:14px;color:var(--wk)")}{f["text"]}</div>'
    if k == 'M':
        def half(ms):
            rows = ''.join(f'<tr><td class="m">{m}月</td><td></td><td></td></tr>' for m in ms)
            return f'<table class="wtable"><tr><th style="width:15mm">月</th><th>何に</th><th style="width:26mm">いくら</th></tr>{rows}</table>'
        return f'<div class="field" style="display:grid;grid-template-columns:1fr 1fr;gap:4mm">{half(range(1, 7))}{half(range(7, 13))}</div>'
    if k == 'LINK':
        rows = ''.join('<div style="display:flex;align-items:center;gap:3mm;margin-bottom:3mm">'
                       '<div class="box" style="flex:1;height:13mm;border:1.2px solid var(--line);border-radius:3mm;background:#fff"></div>'
                       '<div style="width:22mm;border-top:2px dashed var(--line)"></div>'
                       '<div class="box" style="flex:1;height:13mm;border:1.2px solid var(--line);border-radius:3mm;background:#fff"></div></div>'
                       for _ in range(f['rows']))
        head = ('<div style="display:flex;gap:3mm;font-family:Zen Maru Gothic;font-weight:700;color:var(--navy);font-size:10pt;margin-bottom:1.4mm">'
                '<div style="flex:1">家で聞いた言葉・場面</div><div style="width:22mm"></div><div style="flex:1">今のクセ（あなたの2タイプ）</div></div>')
        return f'<div class="field">{head}{rows}<div class="small">つながっていると思うものを、線で結びましょう。</div></div>'
    if k == 'IF':
        return ('<div class="field"><div class="card-fill"><div class="ttl">' + icon('id-card', style='width:14px;height:14px') + 'もしもの一文</div>'
                '<div style="display:flex;align-items:flex-end;gap:2mm;margin-top:3mm"><span class="mg" style="font-weight:700;color:var(--wk);font-size:12pt">もし</span>'
                '<span class="blank" style="flex:1;border-bottom:1.2px dotted #C9C3B3;height:9mm"></span><span class="mg" style="font-weight:700;color:var(--wk);font-size:12pt">になったら、</span></div>'
                '<div style="display:flex;align-items:flex-end;gap:2mm;margin-top:2mm"><span class="blank" style="flex:1;border-bottom:1.2px dotted #C9C3B3;height:9mm"></span>'
                '<span class="mg" style="font-weight:700;color:var(--wk);font-size:12pt">する</span></div></div></div>')
    raise ValueError(k)


def render_fields(n):
    return '<div class="fields">' + ''.join(render_field(f, i) for i, f in enumerate(FIELDS[n])) + '</div>'
