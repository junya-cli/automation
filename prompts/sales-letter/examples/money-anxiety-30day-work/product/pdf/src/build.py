"""PDF用HTMLを組み立てる: python3 src/build.py [--test]"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import Book, ROOT
import pages_days

FONTS = ['@fontsource/noto-sans-jp/400.css', '@fontsource/noto-sans-jp/500.css', '@fontsource/noto-sans-jp/700.css',
         '@fontsource/zen-maru-gothic/500.css', '@fontsource/zen-maru-gothic/700.css']


def head():
    links = ''.join(f'<link rel="stylesheet" href="../node_modules/{f}">' for f in FONTS)
    return (f'<!doctype html><html lang="ja"><head><meta charset="utf-8">'
            f'<title>毒親育ちのお金の不安がなくなる小さな習慣</title>{links}'
            f'<link rel="stylesheet" href="../src/style.css"></head><body>')


def main():
    test = '--test' in sys.argv
    book = Book()
    if test:
        import pages_front
        pages_front.cover(book)
        for n in (1, 10, 16, 22):
            pages_days.day_pages(book, n)
    else:
        import pages_front, pages_back
        pages_front.build(book)
        book.mark('work')
        pages_front.work_opening(book)
        for n in range(31):
            if n in pages_front.WEEK_DIVIDERS:
                pages_front.week_divider(book, n)
            pages_days.day_pages(book, n)
        pages_back.build(book)
    out = ROOT / 'build'
    out.mkdir(exist_ok=True)
    (out / 'book.html').write_text(head() + book.html() + '</body></html>', encoding='utf-8')
    print('pages:', len(book.pages))


if __name__ == '__main__':
    main()
