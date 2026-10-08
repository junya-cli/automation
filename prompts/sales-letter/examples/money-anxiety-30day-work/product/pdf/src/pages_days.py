"""30日ワークの各Dayページ（読む・書くの2ページ）"""
import re
from lib import icon, aoi, talk, lab_row, paras
from parse_days import parse
from figs_days import FIGS
from fields import render_fields

DAYS = parse()

WEEK = {}
for n in range(31):
    WEEK[n] = ('start' if n == 0 else 'see' if n <= 7 else 'split' if n <= 14 else 'loosen' if n <= 21 else 'decide' if n <= 29 else 'gold')
WEEK_LABEL = {'start': 'はじまり', 'see': '1週目｜見る', 'split': '2週目｜分ける', 'loosen': '3週目｜ほどく', 'decide': '4週目｜決める', 'gold': '完成の日'}
WEEK_COLOR = {'start': '#283265', 'see': '#3A74C2', 'split': '#C2862A', 'loosen': '#8064BF', 'decide': '#2A8B7F', 'gold': '#B48C45'}

# 読むページに入りきらない日は、図解を書くページへ
FIG_ON_WRITE = set()


SUB_DOT = {'青': 'var(--c-blue)', '黄': 'var(--c-yellow)', '緑': 'var(--c-green)', '灰': 'var(--c-gray)'}


def md(s):
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    return s


def group_quotes(ps):
    """「〜」だけの段落が続くところは、吹き出しのチップにまとめる"""
    out, buf = [], []
    for x in ps + [None]:
        if x is not None and x.startswith('「') and x.endswith('」') and len(x) < 40:
            buf.append(x)
            continue
        if len(buf) >= 2:
            out.append('<span class="tq">' + ''.join(f'<span>{q}</span>' for q in buf) + '</span>')
        else:
            out.extend(buf)
        buf = []
        if x is not None:
            out.append(x)
    return out


def head_info(n):
    h = DAYS[n]['head']
    title = h.split('　　')[0].strip()
    stars = []
    m = re.search(r'★(.+)$', h)
    if m:
        stars = m.group(1).split('・')
    heavy = '重い日' in h
    return title, stars, heavy


def progress(n):
    out = []
    for i in range(31):
        if i in (1, 8, 15, 22, 30):
            out.append('<span class="sep"></span>')
        c = WEEK_COLOR[WEEK[i]]
        if i < n:
            out.append(f'<span class="dot done" style="background:{c}"></span>')
        elif i == n:
            out.append(f'<span class="dot done cur" style="background:{c}"></span>')
        else:
            out.append('<span class="dot"></span>')
    return f'<div class="progress">{"".join(out)}<span class="lbl">Day{n} / 30</span></div>'


def steps_html(lines):
    nums = [l for l in lines if re.match(r'^\d+\.', l)]
    bullets = [l for l in lines if l.startswith('- ')]
    notes = [l for l in lines if not re.match(r'^\d+\.', l) and not l.startswith('- ') and not l.startswith('　- ')]
    subs = [l for l in lines if l.startswith('　- ')]
    out = ''
    if nums:
        items = []
        for l in lines:
            if re.match(r'^\d+\.', l):
                items.append([re.sub(r'^\d+\.\s*', '', l), []])
            elif l.startswith('　- ') and items:
                items[-1][1].append(l[3:])
        lis = ''
        for t, sub in items:
            sb = ''
            if sub:
                def one(x):
                    dot = SUB_DOT.get(x[:1])
                    dot = f'<i style="background:{dot}"></i>' if dot else '<i></i>'
                    if '：' in x:
                        a, c = x.split('：', 1)
                        return f'<span>{dot}<span><b>{a}</b>：{md(c)}</span></span>'
                    return f'<span>{dot}<span>{md(x)}</span></span>'
                sb = '<div class="subs">' + ''.join(one(x) for x in sub) + '</div>'
            lis += f'<li>{md(t)}{sb}<span class="chk"></span></li>'
        out += f'<ol class="steps">{lis}</ol>'
    if bullets:
        lis = ''
        for b in bullets:
            t = b[2:]
            if '：' in t:
                a, c = t.split('：', 1)
                lis += f'<li><span class="tname">{a}</span>{md(c)}<span class="chk"></span></li>'
            else:
                lis += f'<li>{md(t)}<span class="chk"></span></li>'
        out += f'<ul class="steps typesteps">{lis}</ul>'
    for x in notes:
        out += f'<div class="step-note">{md(x)}</div>'
    return out


def read_page(book, n):
    d = DAYS[n]['sec']
    wk = WEEK[n]
    title, stars, heavy = head_info(n)
    st = ''.join(f'<span>★ {s}</span>' for s in stars)
    st = f'<div class="stars">{st}</div>' if stars else ''
    hv = '<span class="heavy">重い日</span>' if heavy else ''
    head = (f'<div class="dayhead"><div class="daynum"><span class="d">DAY</span><span class="n">{n}</span></div>'
            f'<div class="dayttl"><span class="pill">{WEEK_LABEL[wk]}</span>{hv}<div class="ttl">{title}</div>{st}</div></div>')
    goal_lines = d.get('今日のゴール', [])
    goal = (f'<div class="goal"><div class="lab">{icon("flag", style="width:14px;height:14px")}今日のゴール</div>'
            f'<div class="txt">{md(goal_lines[0])}</div></div>')
    for g in goal_lines[1:]:
        goal += f'<div class="goal-note">{md(g)}</div>'
    pre = ''.join(f'<div class="stopbox" style="margin-bottom:4mm"><div>{icon("feather", style="width:18px;height:18px;color:var(--wk)")}</div><div><p>{md(x.lstrip("※"))}</p></div></div>' for x in d.get('_pre', []))
    t = talk(group_quotes([md(x) for x in d.get('アオの話', [])]))
    fg = '' if n in FIG_ON_WRITE else FIGS[n]()
    why = f'<div class="blk">{lab_row("なぜ？", "lightbulb")}{paras([md(x) for x in d.get("なぜ？", [])])}</div>'
    stp = f'<div class="blk">{lab_row("今日の5分", "timer")}{steps_html(d.get("今日の5分", []))}</div>'
    body = head + progress(n) + goal + pre + t + fg + why + stp
    book.add(body, wk=wk, run=f'30日ワーク　{WEEK_LABEL[wk]}', cls='rp')


def write_page(book, n):
    d = DAYS[n]['sec']
    wk = WEEK[n]
    title, _, _ = head_info(n)
    top = (f'<div class="wtop"><span class="badge">Day{n}</span><span class="t">{title}</span>'
           f'<span class="w">{icon("pencil", style="width:14px;height:14px")}書く</span></div>')
    fg = FIGS[n]() if n in FIG_ON_WRITE else ''
    ex = ''
    if d.get('記入例'):
        ex = f'<div class="example"><span class="lab">記入例</span>{"".join(f"<p>{md(x)}</p>" for x in d["記入例"])}</div>'
    fl = render_fields(n)
    boxes = ''
    for key, ic in (('ここで止まったときは', 'life-buoy'), ('数字が変わらなかったときは', 'compass')):
        if d.get(key):
            items = d[key]
            lis = ''
            for x in items:
                if x.startswith('- '):
                    lis += f'<p>・{md(x[2:])}</p>'
                else:
                    lis += f'<p>{md(x)}</p>'
            boxes += (f'<div class="stopbox">{aoi("s")}<div><div class="t">{icon(ic, style="width:15px;height:15px")}{key}</div>{lis}</div></div>')
    memo = ''
    if d.get('研究メモ'):
        memo = (f'<div class="memo">{icon("book-open-text")}<span class="lab">研究メモ</span>'
                f'<div class="txt">{" ".join(md(x) for x in d["研究メモ"])}</div></div>')
    word = ''
    if d.get('アオのひとこと'):
        word = (f'<div class="word">{aoi("")}<div class="bubble"><div class="who">{icon("sparkles", style="width:13px;height:13px")}アオのひとこと</div>'
                f'{paras([md(x) for x in d["アオのひとこと"]])}</div>'
                f'<div class="done"><b></b>今日のマスを<br>塗りましょう</div></div>')
    notes = f'<div class="notes"><span class="nl">{icon("pen-line")}メモ・気づいたこと</span></div>'
    body = top + fg + ex + fl + boxes + notes + memo + word
    book.add(body, wk=wk, run=f'30日ワーク　{WEEK_LABEL[wk]}', cls='wp')


def day_pages(book, n):
    book.mark(f'day{n}')
    read_page(book, n)
    write_page(book, n)
