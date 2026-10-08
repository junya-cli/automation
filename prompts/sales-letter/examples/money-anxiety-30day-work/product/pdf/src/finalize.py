"""書き出したPDFに文書情報を入れて、配布用ファイルとして保存する: python3 src/finalize.py build/book.pdf ../out.pdf"""
import sys
from pypdf import PdfReader, PdfWriter
src, dst = sys.argv[1], sys.argv[2]
w = PdfWriter(clone_from=PdfReader(src))
w.add_metadata({'/Title': '毒親育ちのお金の不安がなくなる小さな習慣 〜心と財布に余裕が生まれる30日ワーク〜',
                '/Author': 'アオ', '/Subject': '1日5分・書き込み式の30日ワーク'})
w.page_mode = '/UseNone'
w.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)
with open(dst, 'wb') as f:
    w.write(f)
print(dst)
