# ローンチ配信（30日ワーク 第1期「一緒に始める30日」）

配信台本のページ（吹き出しごとにコピーできる）：https://claude.ai/artifact/AHwnc9JGKcjhXHgPpwdT3C

| ファイル | 中身 |
|---|---|
| `research.md` | 調べた型（プロダクト・ローンチ・フォーミュラ、ソープオペラ・シーケンス、日本のLINEローンチ）、日程の数字、LINE実務、法律と倫理の注意。出典つき |
| `launch_plan.md` | オファー（第1期）、日程表、準備リスト、測るもの、守ること |
| `line_messages.md` | LINE配信の全文（ローンチ12通＋あいさつ＋第1期の伴走6通） |
| `x_posts.md` | X投稿9本 |
| `okane-no-kuse-shindan.pdf` | LINE登録特典「お金のクセ診断」（5ページ） |
| `messages.py` | 文面の元。直したら `python3 launch/make_launch.py` で md と台本ページを作り直す |

診断PDFは、ワークブックのページから作っています：
`cd product/pdf && python3 src/build.py && node src/make_shindan.mjs ../../launch/okane-no-kuse-shindan.pdf`
