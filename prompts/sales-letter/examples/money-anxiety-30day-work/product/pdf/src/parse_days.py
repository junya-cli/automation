"""workbook_v2.md から Day0〜30 の本文を読み取る"""
import re, json, pathlib
MD = pathlib.Path(__file__).resolve().parents[2] / 'workbook_v2.md'
LABELS = ['今日のゴール','アオの話','なぜ？','今日の5分','今日の5分（タイプ別）','今日の5分**（今日は15分くらいかかってもかまいません）','記入例','記入例（アオの場合）','記入例（手紙）','書く欄','研究メモ','アオのひとこと','ここで止まったときは','数字が変わらなかったときは','一言カード','いちばん止まったつまずきポイント（1つに丸）']

def parse():
    text = MD.read_text(encoding='utf-8')
    body = text.split('## 30日ワーク',1)[1].split('<!-- 新規（旧p.108',1)[0]
    parts = re.split(r'\n### (Day\d+)｜', body)[1:]
    days = {}
    for i in range(0, len(parts), 2):
        key, chunk = parts[i], parts[i+1]
        n = int(key[3:])
        head, rest = chunk.split('\n',1)
        d = {'n': n, 'head': head.strip(), 'sec': {}}
        rest = re.sub(r'<!--.*?-->', '', rest)
        cur = '_pre'; d['sec'][cur] = []
        for line in rest.split('\n'):
            s = line.strip()
            if not s or s == '---': continue
            if re.match(r'^(\u3000|\s{2,})-\s', line):
                s = '\u3000- ' + re.sub(r'^[\u3000\s]*-\s*', '', line)
            m = re.match(r'^\*\*(.+?)\*\*\s*(.*)$', s)
            if m and (m.group(1) in LABELS or m.group(1).startswith('今日の5分')):
                lab = m.group(1)
                if lab.startswith('今日の5分'): lab = '今日の5分'
                if lab.startswith('記入例'): lab = '記入例'
                cur = lab; d['sec'].setdefault(cur, [])
                if m.group(2): d['sec'][cur].append(m.group(2))
                continue
            d['sec'][cur].append(s)
        days[n] = d
    return days

if __name__ == '__main__':
    days = parse()
    print(len(days))
    for n in (0, 10, 13, 22, 30):
        print(json.dumps(days[n], ensure_ascii=False, indent=1)[:1500]); print('=====')
