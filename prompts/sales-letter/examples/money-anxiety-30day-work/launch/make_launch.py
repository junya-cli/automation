"""ローンチ配信の md と台本ページを作る: python3 launch/make_launch.py

LINE公式の決まり（吹き出し3つまで・1つ500字まで）と、Xの文字数（280＝日本語140字）を、作るたびに確かめる。
"""
import json, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from messages import LINE, X, IMAGES, type_cards, auto  # noqa: E402

PHASES = ['はじめ', '教育', '予告', '販売', '締め切り', 'お礼', '第1期']
TIER_NOTE = {'必須': '必須（節約版でも送る）', 'できれば': 'できれば（通数が足りないときは送らない）', '自動': '自動（通数に数えない）'}


def x_len(text):
    """Xの重みつき文字数（上限280）。日本語は2、英数字・改行は1、URLは23"""
    n = 0
    for ch in re.sub(r'【(LINE|note)のURL】', '\0', text):
        cp = ord(ch)
        if ch == '\0':
            n += 23
        elif cp <= 4351 or 8192 <= cp <= 8205 or 8208 <= cp <= 8223 or 8242 <= cp <= 8247:
            n += 1
        else:
            n += 2
    return n


def check():
    errs = []
    for m in LINE + auto():
        bs = m['bubbles']
        if len(bs) > 3:
            errs.append(f"{m['id']}: 吹き出しが{len(bs)}つ（3つまで）")
        for i, b in enumerate(bs):
            if isinstance(b, str) and len(b) > 500:
                errs.append(f"{m['id']} 吹き出し{i + 1}: {len(b)}字（500字まで）")
            if isinstance(b, dict) and b['img'] not in IMAGES:
                errs.append(f"{m['id']} 吹き出し{i + 1}: 画像 {b['img']} が IMAGES にない")
        if isinstance(bs[0], dict):
            errs.append(f"{m['id']}: 1つ目が画像（通知に文字が出ない）")
    for c in type_cards():
        if len(c['text']) > 500:
            errs.append(f"{c['key']}: {len(c['text'])}字（500字まで）")
    for d, k, t, img in X:
        if x_len(t) > 280:
            errs.append(f'X {d} {k}: {x_len(t)}（280まで）')
        if img and img not in IMAGES:
            errs.append(f'X {d} {k}: 画像 {img} が IMAGES にない')
    for p in set(IMAGES.values()):
        if not (HERE.parent / p).exists():
            errs.append(f'画像ファイルがない: {p}')
    if errs:
        print('\n'.join(errs))
        sys.exit(1)


def bubble_md(i, b):
    if isinstance(b, str):
        return [f'**吹き出し{i + 1}**（{len(b)}字）', '', '```', b, '```', '']
    if b.get('rich'):
        return [f'**吹き出し{i + 1}：リッチメッセージ**', '',
                f"- 画像：`{IMAGES[b['img']]}`（1040×1040）",
                f"- タイトル（通知とトーク一覧に出る文字）：{b['alt']}",
                f"- タップしたときに開くURL：{b['link']}", '']
    return [f'**吹き出し{i + 1}：画像**', '', f"- 画像：`{IMAGES[b['img']]}`", '']


def msg_md(m, head):
    out = ['---', '', f"## {m['id']}　{m['title']}", '']
    out += [f"- **{k}**：{v}" for k, v in head]
    out.append(f"- **ねらい**：{m['purpose']}")
    if m['memo']:
        out.append(f"- **メモ**：{m['memo']}")
    out.append('')
    for i, b in enumerate(m['bubbles']):
        out += bubble_md(i, b)
    return out


def md():
    out = ['# LINE配信の全文（ローンチ）', '',
           '2026年の日程：教育 10/11・12・14、予告 10/15、発売 10/16 20:00、第1期の締め切り 10/21 23:59、第1期スタート 10/22。【】は差し替える所。',
           '',
           '- 一斉配信は、吹き出し3つまでで1通。**画像・リッチメッセージも吹き出し1つに数えます**（ここの配信は、すべて3つ以内）',
           '- テキストの吹き出しは、1つ500字まで',
           '- 1行目は、通知とトーク一覧に出る文。あいさつより先に、中身を書いています',
           '- **区分**：必須＝節約版でも送る／できれば＝通数が足りないときは送らない／自動＝あいさつ・応答メッセージ（通数に数えない）。くわしくは `launch_plan.md` の「0. 配信の前に」',
           '- 文面を直すときは `messages.py` を直して `python3 launch/make_launch.py` で作り直してください。', '',
           '| ID | いつ | どこ | 区分 | タイトル |', '|---|---|---|---|---|']
    for m in LINE:
        out.append(f"| {m['id']} | {m['when']} | {m['where']} | {m['tier']} | {m['title']} |")
    for a in auto():
        out.append(f"| {a['id']} | {a['when']} | 応答メッセージ（キーワード「{a['key']}」） | 自動 | {a['title']} |")
    out.append('')
    for m in LINE:
        out += msg_md(m, [('いつ', m['when']), ('どこ', m['where']), ('区分', TIER_NOTE[m['tier']])])
    out += ['---', '', '# 自動応答（応答メッセージ）', '',
            'LINE公式の「応答メッセージ」で、キーワードを完全一致で登録します。通数に数えません。第1期特典のタイプ別メッセージは `type_cards.md`。', '']
    for a in auto():
        out += msg_md(a, [('キーワード', f"「{a['key']}」"), ('設定する期間', a['when'])])
    (HERE / 'line_messages.md').write_text('\n'.join(out), encoding='utf-8')

    xo = ['# X（旧Twitter）の投稿', '',
          '2026年の日程。【】は差し替える所。数字はXの文字数（280まで＝日本語140字。URLは23で数えています）。',
          '発売までは「LINEの診断」へ、発売からは「note」へつなぎます。1日2本の日は、朝と夜に分けて投稿してください。', '']
    for d, k, t, img in X:
        xo += ['---', '', f'## {d}　{k}（{x_len(t)}/280）', '']
        if img:
            xo += [f'画像：`{IMAGES[img]}`', '']
        xo += ['```', t, '```', '']
    (HERE / 'x_posts.md').write_text('\n'.join(xo), encoding='utf-8')

    co = ['# 第1期特典：あなたのタイプ専用メッセージ（15通り）', '',
          'LINE公式の「応答メッセージ」に、キーワードごとに登録します（キーワードは完全一致。逆順と全角数字も、同じ文面で登録）。',
          '第1期の人は、A3・C0の案内に従って「タイプ25」のように送ってきます。自動応答が合わなかったときは、ここからコピーして手で返信してください。', '',
          '| キーワード | 内容 |', '|---|---|']
    cards = type_cards()
    for c in cards:
        co.append(f"| {'、'.join(c['keys'])} | {c['title']} |")
    co.append('')
    for c in cards:
        co += ['---', '', f"## {c['title']}", '', f"キーワード：{'、'.join(c['keys'])}", '', '```', c['text'], '```', '']
    (HERE / 'type_cards.md').write_text('\n'.join(co), encoding='utf-8')


def page():
    data = {'line': LINE, 'auto': auto(), 'x': [{'when': d, 'kind': k, 'text': t, 'image': img, 'len': x_len(t)} for d, k, t, img in X],
            'phases': PHASES, 'cards': type_cards()}
    tpl = (HERE / 'script_template.html').read_text(encoding='utf-8')
    (HERE / 'script.html').write_text(tpl.replace('/*__DATA__*/null', json.dumps(data, ensure_ascii=False)), encoding='utf-8')


if __name__ == '__main__':
    check()
    md()
    page()
    sends = [m for m in LINE if m['tier'] != '自動' and m['phase'] != '第1期']
    print('ok', len(LINE), 'LINE（一斉配信', len(sends), '回・うち必須', sum(m['tier'] == '必須' for m in sends), '回）/',
          len(auto()), '自動応答 /', len(X), 'X')
