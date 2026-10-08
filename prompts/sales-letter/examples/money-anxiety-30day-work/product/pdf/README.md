# PDF版ワークブックの作り方

`../workbook_v2.md` の原稿から、A4・118ページのPDF（`../okane-no-fuan-30days-workbook.pdf`）を作ります。

## 作り直す手順

```bash
npm install                      # フォント・アイコン・QR・Chromium操作
node src/make_qr.mjs             # QRコード（書き込みノート／購入者限定LINE）
python3 src/build.py             # build/book.html を組み立てる
node src/render.mjs --pdf build/book.pdf --shots all   # はみ出しチェック＋ページ画像＋PDF
python3 src/finalize.py build/book.pdf ../okane-no-fuan-30days-workbook.pdf
```

- `render.mjs` は Chromium のパス（`/opt/pw-browsers/...`）を直接指定しています。環境に合わせて書き換えてください。
- `python3 src/sheet.py 1-8` で、ページ画像を8枚ずつ並べた確認用シートを作れます。

## ファイル

| ファイル | 中身 |
|---|---|
| `src/style.css` | 配色・文字・部品のデザイン |
| `src/lib.py` | アイコン、アオ、図解パーツ、ページ枠 |
| `src/pages_front.py` | 表紙・目次・はじめに・第1〜4章・週の扉 |
| `src/parse_days.py` | 原稿から Day0〜30 の本文を読み取る |
| `src/figs_days.py` | Day0〜30 の図解（すべてアオのひとこと付き） |
| `src/fields.py` | Day0〜30 の書き込み欄 |
| `src/pages_days.py` | 1日2ページ（読む／書く）の組み立て |
| `src/pages_back.py` | ふり返りチェック・付録・セッション案内・おわりに |
| `assets/` | アオの画像（`aoi_src.webp` から切り抜き）とQRコード |

本文を直すときは `../workbook_v2.md` を直してから作り直してください（Dayページは原稿から自動で流し込みます）。前付け・章・付録の文章は `pages_front.py` / `pages_back.py` に入っています。
