"""note用の画像（見出し画像・5タイプ・3つの習慣）のHTMLを作る: python3 src/note_images.py"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import icon, ROOT
from build import FONTS
from pages_front import flower, sparkle, TYPES

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #ddd; font-family: 'Noto Sans JP', sans-serif; color: #34344A; }
.mg { font-family: 'Zen Maru Gothic', 'Noto Sans JP', sans-serif; font-weight: 700; }
.ic { display: inline-block; flex: none; }
.ic svg { width: 100%; height: 100%; display: block; }
.shot { margin: 20px; position: relative; overflow: hidden; }

/* 見出し画像 1280x670 */
#eyecatch { width: 1280px; height: 670px; background: radial-gradient(circle at 70% 50%, #FFFFFF 0, #FFFDF8 35%, #F4EDDD 100%); }
#eyecatch .frame { position: absolute; inset: 22px; border: 2px solid #E8D6AE; border-radius: 26px; }
#eyecatch .frame::after { content: ""; position: absolute; inset: 7px; border: 1px solid #EFE3C6; border-radius: 20px; }
#eyecatch .left { position: absolute; left: 88px; top: 104px; width: 690px; }
#eyecatch .tag { display: inline-block; border: 2px solid #B48C45; color: #B48C45; border-radius: 99px; padding: 6px 26px; font-size: 22px; letter-spacing: .22em; background: rgba(255,255,255,.75); }
#eyecatch .t1 { font-size: 42px; letter-spacing: .12em; color: #283265; margin-top: 22px; line-height: 1.3; }
#eyecatch .t2 { font-size: 64px; letter-spacing: .04em; color: #283265; line-height: 1.24; white-space: nowrap; }
#eyecatch .rule { display: flex; align-items: center; gap: 16px; margin: 18px 0 12px; }
#eyecatch .rule span { width: 150px; height: 2px; background: #E8D6AE; }
#eyecatch .sub { font-size: 28px; color: #3B4682; letter-spacing: .08em; }
#eyecatch .pills { display: flex; gap: 14px; margin-top: 24px; }
#eyecatch .pill { display: inline-flex; align-items: center; gap: 10px; background: #283265; color: #fff; border-radius: 99px; padding: 10px 26px; font-size: 24px; letter-spacing: .06em; }
#eyecatch .pill .ic { width: 24px; height: 24px; }
#eyecatch .aoi { position: absolute; right: 92px; top: 125px; width: 420px; height: 420px; border-radius: 50%;
  background: #fff url(../assets/aoi_circle_600.png) center/cover no-repeat;
  box-shadow: 0 0 0 4px #E8D6AE, 0 0 0 13px #fff, 0 0 0 15px #E8D6AE, 0 18px 40px rgba(40,50,101,.16); }
#eyecatch .name { position: absolute; right: 92px; width: 420px; bottom: 52px; text-align: center; font-size: 26px; letter-spacing: .5em; color: #283265; }

/* 本文用の図（幅640px・2倍で書き出し） */
.card { width: 640px; background: #FBF8F1; padding: 34px 30px 30px; }
.card .ttl { font-size: 32px; color: #283265; text-align: center; letter-spacing: .04em; }
.card .lead { font-size: 18px; color: #6A6A7E; text-align: center; margin: 8px 0 22px; }
.row { display: flex; align-items: center; gap: 18px; background: #fff; border-radius: 20px; padding: 16px 20px; margin-bottom: 12px; box-shadow: 0 2px 8px rgba(40,50,101,.06); }
.row .n { width: 34px; height: 34px; border-radius: 50%; color: #fff; font-size: 18px; display: flex; align-items: center; justify-content: center; flex: none; }
.row .ci { width: 66px; height: 66px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex: none; }
.row .ci .ic { width: 36px; height: 36px; }
.row .nm { font-size: 26px; color: #283265; line-height: 1.3; }
.row .q { font-size: 20px; line-height: 1.4; margin-top: 2px; }
.foot { display: flex; align-items: center; gap: 14px; margin-top: 18px; }
.foot .face { width: 64px; height: 64px; border-radius: 50%; background: #fff url(../assets/aoi_face.png) center/cover; box-shadow: 0 0 0 3px #E8D6AE; flex: none; }
.foot .bb { background: #EEEDF9; border-radius: 16px; padding: 12px 18px; font-size: 19px; color: #5E4596; line-height: 1.5; }
.no { display: flex; gap: 10px; margin-top: 16px; }
.no span { flex: 1; text-align: center; background: #fff; border: 2px dashed #E2A1A9; color: #B04A5A; border-radius: 14px; padding: 10px 6px; font-size: 19px; line-height: 1.35; }
.no span b { display: block; font-size: 15px; letter-spacing: .1em; }
"""


def head():
    links = ''.join(f'<link rel="stylesheet" href="../node_modules/{f}">' for f in FONTS)
    return f'<!doctype html><html lang="ja"><head><meta charset="utf-8">{links}<style>{CSS}</style></head><body>'


def eyecatch():
    pos = lambda h, s: f'<div style="position:absolute;{s}">{h}</div>'
    deco = (pos(flower(70, '#9C98DC', op=.5), 'left:640px;bottom:40px') + pos(flower(46, '#B6B3E8', op=.55), 'left:720px;bottom:110px') +
            pos(flower(60, '#9C98DC', op=.45), 'right:40px;bottom:30px') + pos(sparkle(18), 'left:780px;top:70px') +
            pos(sparkle(11), 'left:745px;top:110px') + pos(sparkle(15), 'right:60px;top:90px') + pos(sparkle(10), 'left:60px;bottom:70px'))
    deco = deco.replace('mm;', 'px;')
    pills = ''.join(f'<span class="pill mg">{icon(ic)}{t}</span>' for ic, t in (('timer', '1日5分'), ('pencil', '書き込み式'), ('calendar-days', '30日')))
    return (f'<div class="shot" id="eyecatch"><div class="frame"></div>{deco}<div class="left">'
            '<span class="tag mg">アダルトチルドレン必見</span>'
            '<div class="mg t1">毒親育ちの</div><div class="mg t2">お金の不安が</div><div class="mg t2">なくなる小さな習慣</div>'
            f'<div class="rule"><span></span>{sparkle(6, "#C9A867").replace("mm", "px").replace("width:6px;height:6px", "width:22px;height:22px")}<span></span></div>'
            f'<div class="mg sub">心と財布に余裕が生まれる30日ワーク</div><div class="pills">{pills}</div></div>'
            '<div class="aoi"></div><div class="mg name">アオ</div></div>')


def types():
    rows = ''.join(f'<div class="row"><span class="n mg" style="background:{t[3]}">{i + 1}</span>'
                   f'<span class="ci" style="background:{t[4]};color:{t[3]}">{icon(t[2])}</span>'
                   f'<div><div class="mg nm">{t[0]}</div><div class="mg q" style="color:{t[3]}">{t[1]}</div></div></div>'
                   for i, t in enumerate(TYPES))
    return (f'<div class="shot card" id="types"><div class="mg ttl">お金のクセ、5つのタイプ</div>'
            f'<div class="lead">5問の答えと、同じ番号です</div>{rows}'
            '<div class="foot"><div class="face"></div><div class="bb mg">2つ以上あてはまって、あたりまえ。<br>どのタイプかで、30日でやることが変わります。</div></div></div>')


def habits():
    hs = [('eye', '見る', '週に1回、5分だけ、お金を見る', '#3A74C2', '#E8F0FB'),
          ('layers', '分ける', '給料日に、使う前に、先に分けておく', '#C2862A', '#FBF1DE'),
          ('wind', 'ひと呼吸', '「もし〇〇になったら、△△する」<br>と、1文だけ決めておく', '#2A8B7F', '#E1F3F0')]
    rows = ''.join(f'<div class="row" style="padding:20px 22px"><span class="n mg" style="background:{c};width:40px;height:40px;font-size:22px">{i + 1}</span>'
                   f'<span class="ci" style="background:{bg};color:{c};width:76px;height:76px">{icon(ic, style="width:42px;height:42px")}</span>'
                   f'<div><div class="mg nm" style="font-size:30px;color:{c}">{h}</div><div class="q" style="font-size:20px;color:#34344A">{s}</div></div></div>'
                   for i, (ic, h, s, c, bg) in enumerate(hs))
    no = ''.join(f'<span class="mg"><b>しない</b>{x}</span>' for x in ('細かい家計簿', '我慢の節約', '親を許すこと'))
    return (f'<div class="shot card" id="habits"><div class="mg ttl">やることは、3つだけ</div>'
            f'<div class="lead">1日5分・30日</div>{rows}<div class="no">{no}</div></div>')


def main():
    out = ROOT / 'build' / 'note_figs.html'
    out.write_text(head() + eyecatch() + types() + habits() + '</body></html>', encoding='utf-8')
    print(out)


if __name__ == '__main__':
    main()
