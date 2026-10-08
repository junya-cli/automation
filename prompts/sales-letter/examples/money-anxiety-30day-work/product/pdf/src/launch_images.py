"""LINEのリッチメッセージ画像（1040×1040）のHTMLを作る: python3 src/launch_images.py
書き出し: node src/shoot.mjs build/launch_figs.html ../../launch/images rich1:1:rich_hatsubai.png rich2:1:rich_shimekiri.png
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import icon, ROOT
from build import FONTS
from pages_front import flower, sparkle

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #ddd; font-family: 'Noto Sans JP', sans-serif; color: #34344A; }
.mg { font-family: 'Zen Maru Gothic', 'Noto Sans JP', sans-serif; font-weight: 700; }
.ic { display: inline-block; flex: none; }
.ic svg { width: 100%; height: 100%; display: block; }
.rich { width: 1040px; height: 1040px; margin: 20px; position: relative; overflow: hidden;
  background: radial-gradient(circle at 50% 38%, #FFFFFF 0, #FFFDF8 40%, #F4EDDD 100%); }
.rich .frame { position: absolute; inset: 26px; border: 2px solid #E8D6AE; border-radius: 30px; }
.rich .frame::after { content: ""; position: absolute; inset: 8px; border: 1px solid #EFE3C6; border-radius: 23px; }
.deco { position: absolute; }
.tag { display: inline-flex; align-items: center; gap: 12px; background: #283265; color: #fff; border-radius: 99px; padding: 10px 34px; font-size: 32px; letter-spacing: .14em; }
.tag .ic { width: 30px; height: 30px; color: #E8D6AE; }
.center { position: absolute; left: 0; right: 0; text-align: center; }
.t1 { font-size: 46px; letter-spacing: .14em; color: #283265; }
.t2 { font-size: 80px; letter-spacing: .04em; color: #283265; line-height: 1.22; }
.sub { font-size: 31px; color: #3B4682; letter-spacing: .08em; }
.pills { display: flex; justify-content: center; gap: 16px; }
.pill { display: inline-flex; align-items: center; gap: 10px; background: #fff; color: #283265; border: 2px solid #E8D6AE; border-radius: 99px; padding: 8px 26px; font-size: 28px; letter-spacing: .06em; }
.pill .ic { width: 28px; height: 28px; color: #A9813A; }
.aoi { position: absolute; border-radius: 50%; background: #fff url(../assets/aoi_circle_600.png) center/cover no-repeat;
  box-shadow: 0 0 0 4px #E8D6AE, 0 0 0 12px #fff, 0 0 0 14px #E8D6AE, 0 14px 30px rgba(40,50,101,.16); }
.offer { position: absolute; background: #283265; color: #fff; border-radius: 28px; padding: 28px 34px; box-shadow: 0 14px 30px rgba(40,50,101,.18); }
.offer .k { font-size: 24px; letter-spacing: .18em; color: #E8D6AE; }
.offer .h { font-size: 38px; letter-spacing: .04em; margin-top: 4px; }
.offer .d { font-size: 27px; margin-top: 6px; color: #F4EDDD; }
.cta { display: inline-flex; align-items: center; gap: 12px; background: #A9813A; color: #fff; border-radius: 99px; padding: 14px 40px; font-size: 36px; letter-spacing: .1em;
  box-shadow: 0 6px 0 #8A6A2E, 0 14px 24px rgba(40,50,101,.18); }
.cta .ic { width: 36px; height: 36px; }
.big { font-size: 150px; line-height: 1.05; color: #C25B6A; letter-spacing: .02em; }
.big small { font-size: 72px; color: #283265; margin-right: 18px; letter-spacing: .08em; }
.say { position: absolute; display: flex; align-items: center; justify-content: center; gap: 22px; }
.say .face { width: 130px; height: 130px; border-radius: 50%; background: #fff url(../assets/aoi_face.png) center/cover; box-shadow: 0 0 0 4px #E8D6AE; flex: none; }
.say .bb { position: relative; background: #EEEDF9; border-radius: 26px; padding: 22px 30px; font-size: 32px; color: #5E4596; line-height: 1.5; }
.say .bb::before { content: ""; position: absolute; left: -16px; top: 50%; margin-top: -14px; border: 14px solid transparent; border-right: 18px solid #EEEDF9; border-left: 0; }
.note { font-size: 25px; color: #6A6A7E; }
"""


def head():
    links = ''.join(f'<link rel="stylesheet" href="../node_modules/{f}">' for f in FONTS)
    return f'<!doctype html><html lang="ja"><head><meta charset="utf-8">{links}<style>{CSS}</style></head><body>'


def deco(items):
    return ''.join(f'<div class="deco" style="{pos}">{svg.replace("mm;", "px;").replace("mm\"", "px\"")}</div>' for svg, pos in items)


def cta():
    return f'<span class="cta mg">タップして読む{icon("chevron-right", sw=3)}</span>'


def rich_open():
    pills = ''.join(f'<span class="pill mg">{icon(ic)}{t}</span>' for ic, t in (('timer', '1日5分'), ('pencil', '書き込み式'), ('calendar-days', '30日')))
    d = deco([(flower(70, '#9C98DC', op=.45), 'left:60px;top:300px'), (flower(46, '#B6B3E8', op=.5), 'left:58px;top:420px'),
              (flower(64, '#9C98DC', op=.42), 'right:58px;top:250px'), (sparkle(20), 'right:120px;top:120px'),
              (sparkle(12), 'right:160px;top:170px'), (sparkle(16), 'left:110px;top:120px')])
    return (f'<div class="rich" id="rich1"><div class="frame"></div>{d}'
            f'<div class="center" style="top:78px"><span class="tag mg">{icon("sparkles")}発売しました</span></div>'
            '<div class="center" style="top:178px"><div class="mg t1">毒親育ちの</div><div class="mg t2">お金の不安が</div><div class="mg t2">なくなる小さな習慣</div></div>'
            '<div class="center" style="top:470px"><div class="mg sub">心と財布に余裕が生まれる30日ワーク</div></div>'
            f'<div class="center" style="top:540px"><div class="pills">{pills}</div></div>'
            '<div class="aoi" style="left:78px;top:668px;width:270px;height:270px"></div>'
            '<div class="offer" style="left:392px;right:70px;top:650px">'
            '<div class="k mg">第1期「一緒に始める30日」</div><div class="h mg">10月21日（水）23:59まで</div>'
            '<div class="d">10月22日に、全員でDay0を始めます</div></div>'
            f'<div style="position:absolute;left:392px;right:70px;top:872px;text-align:center">{cta()}</div></div>')


def rich_close():
    d = deco([(flower(66, '#9C98DC', op=.42), 'left:64px;top:96px'), (flower(44, '#B6B3E8', op=.5), 'left:132px;top:160px'),
              (flower(60, '#9C98DC', op=.4), 'right:62px;top:120px'), (sparkle(18), 'right:150px;top:84px'),
              (sparkle(12), 'left:200px;top:96px')])
    return (f'<div class="rich" id="rich2"><div class="frame"></div>{d}'
            f'<div class="center" style="top:90px"><span class="tag mg">{icon("calendar-days")}第1期「一緒に始める30日」</span></div>'
            '<div class="center" style="top:205px"><div class="mg t1" style="letter-spacing:.2em">締め切りは</div></div>'
            '<div class="center" style="top:270px"><div class="mg big"><small>今夜</small>23:59</div></div>'
            '<div class="center" style="top:452px"><div class="mg sub" style="font-size:34px;color:#283265">10月21日（水）</div></div>'
            '<div class="center" style="top:520px"><div class="mg sub">10月22日（木）に、全員でDay0を始めます</div>'
            '<div class="note" style="margin-top:12px">締め切りのあとも、価格は同じです（第1期の特典だけが、つかなくなります）</div></div>'
            '<div class="say" style="left:96px;right:96px;top:680px"><div class="face"></div>'
            '<div class="bb mg">始めるかどうかは、<br>あなたが決めてください。</div></div>'
            f'<div class="center" style="top:868px">{cta()}</div></div>')


def main():
    out = ROOT / 'build' / 'launch_figs.html'
    out.write_text(head() + rich_open() + rich_close() + '</body></html>', encoding='utf-8')
    print(out)


if __name__ == '__main__':
    main()
