"""ローンチ配信の md と台本ページを作る: python3 launch/make_launch.py"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from messages import LINE, X  # noqa: E402

PHASES = ['はじめ', '教育', '予告', '販売', '締め切り', 'お礼', '第1期']


def md():
    out = ['# LINE配信の全文（ローンチ）', '',
           '日付は例（給料日が25日、第1期のスタートが15日、31日まである月）。【】は差し替える所。',
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

    xo = ['# X（旧Twitter）の投稿', '', '日付は例。【】は差し替える所。すべて140字（日本語）以内です。', '']
    for d, k, t, img in X:
        xo += ['---', '', f'## {d}　{k}', '']
        if img:
            xo += [f'画像：`note/images/{img}`', '']
        xo += ['```', t, '```', '']
    (HERE / 'x_posts.md').write_text('\n'.join(xo), encoding='utf-8')


def page():
    data = {'line': LINE, 'x': [{'when': d, 'kind': k, 'text': t, 'image': img} for d, k, t, img in X], 'phases': PHASES}
    tpl = (HERE / 'script_template.html').read_text(encoding='utf-8')
    (HERE / 'script.html').write_text(tpl.replace('/*__DATA__*/null', json.dumps(data, ensure_ascii=False)), encoding='utf-8')


if __name__ == '__main__':
    md()
    page()
    print('ok', len(LINE), 'LINE /', len(X), 'X')
