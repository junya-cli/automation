"""ローンチ配信の md と台本ページを作る: python3 launch/make_launch.py"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from messages import LINE, X, type_cards  # noqa: E402

PHASES = ['はじめ', '教育', '予告', '販売', '締め切り', 'お礼', '第1期']


def md():
    out = ['# LINE配信の全文（ローンチ）', '',
           '2026年の日程：教育 10/10・12・14、予告 10/15、発売 10/16 20:00、第1期の締め切り 10/21 23:59、第1期スタート 10/22。【】は差し替える所。',
           '吹き出しは1通につき3つまで。画像は `note/images/` のものを使います。',
           '文面を直すときは `messages.py` を直して `python3 launch/make_launch.py` で作り直してください。', '']
    out.append('| ID | いつ | どこ | タイトル |')
    out.append('|---|---|---|---|')
    for m in LINE:
        out.append(f"| {m['id']} | {m['when']} | {m['where']} | {m['title']} |")
    out.append('')
    for m in LINE:
        out += ['---', '', f"## {m['id']}　{m['title']}", '',
                f"- **いつ**：{m['when']}", f"- **どこ**：{m['where']}", f"- **ねらい**：{m['purpose']}"]
        if m['image']:
            out.append(f"- **画像**：`note/images/{m['image']}`")
        if m['memo']:
            out.append(f"- **メモ**：{m['memo']}")
        out.append('')
        for i, b in enumerate(m['bubbles']):
            out += [f'**吹き出し{i + 1}**', '', '```', b, '```', '']
    (HERE / 'line_messages.md').write_text('\n'.join(out), encoding='utf-8')

    xo = ['# X（旧Twitter）の投稿', '', '2026年の日程。【】は差し替える所。すべて140字（日本語）以内です。', '']
    for d, k, t, img in X:
        xo += ['---', '', f'## {d}　{k}', '']
        if img:
            xo += [f'画像：`note/images/{img}`', '']
        xo += ['```', t, '```', '']
    (HERE / 'x_posts.md').write_text('\n'.join(xo), encoding='utf-8')

    co = ['# 第1期特典：あなたのタイプ専用メッセージ（15通り）', '',
          'LINE公式の「応答メッセージ」に、キーワードごとに登録します（キーワードは完全一致。逆順も同じ文面で登録）。',
          '第1期の人は、C0の案内に従って「タイプ25」のように送ってきます。自動応答が合わなかったときは、ここからコピーして手で返信してください。', '',
          '| キーワード | 内容 |', '|---|---|']
    cards = type_cards()
    for c in cards:
        co.append(f"| {'、'.join(c['keys'])} | {c['title']} |")
    co.append('')
    for c in cards:
        co += ['---', '', f"## {c['title']}", '', f"キーワード：{'、'.join(c['keys'])}", '', '```', c['text'], '```', '']
    (HERE / 'type_cards.md').write_text('\n'.join(co), encoding='utf-8')


def page():
    data = {'line': LINE, 'x': [{'when': d, 'kind': k, 'text': t, 'image': img} for d, k, t, img in X], 'phases': PHASES, 'cards': type_cards()}
    tpl = (HERE / 'script_template.html').read_text(encoding='utf-8')
    (HERE / 'script.html').write_text(tpl.replace('/*__DATA__*/null', json.dumps(data, ensure_ascii=False)), encoding='utf-8')


if __name__ == '__main__':
    md()
    page()
    print('ok', len(LINE), 'LINE /', len(X), 'X')
