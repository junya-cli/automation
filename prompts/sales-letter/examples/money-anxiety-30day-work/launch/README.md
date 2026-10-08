# ローンチ配信（30日ワーク 第1期「一緒に始める30日」）

配信台本のページ（吹き出し・画像・自動応答をコピーできる）：https://claude.ai/artifact/AHwnc9JGKcjhXHgPpwdT3C

**最初に `launch_plan.md` の「正直に」と「0. 配信の前に」を読んでください。** LINEの通数の上限によっては、全部の配信を送れません。

| ファイル | 中身 |
|---|---|
| `launch_plan.md` | 売れない原因の洗い出しと直したこと、通数の計算と節約版、オファー（第1期）、日程表、LINEの設定、準備リスト、途中で直すための数字、守ること |
| `research.md` | 調べた型（プロダクト・ローンチ・フォーミュラ、ソープオペラ・シーケンス、日本のLINEローンチ）、日程の数字、LINE実務（料金・吹き出し・オーディエンス）、法律と倫理の注意。出典つき |
| `line_messages.md` | LINE配信の全文（ローンチ12回＋あいさつ2種＋第1期の伴走6回）と、自動応答4つ（診断・まとめ・第1期×2） |
| `type_cards.md` | 第1期特典：タイプ専用メッセージ15通り（自動応答） |
| `x_posts.md` | X投稿20本（文字数つき） |
| `images/` | リッチメッセージ画像2枚（1040×1040）と、Day1のページの画像 |
| `okane-no-kuse-shindan.pdf` | LINE登録特典「お金のクセ診断」（5ページ） |
| `messages.py` | 文面の元。直したら `python3 launch/make_launch.py` で md と台本ページを作り直す（吹き出しの数・文字数・Xの文字数も確かめる） |

画像は、ワークブックのデザイン部品から作っています：

```bash
cd product/pdf
python3 src/build.py                                   # build/book.html
node src/make_shindan.mjs ../../launch/okane-no-kuse-shindan.pdf
python3 src/launch_images.py && node src/shoot.mjs build/launch_figs.html ../../launch/images rich1:1:rich_hatsubai.png rich2:1:rich_shimekiri.png
node src/shoot_day.mjs 1 ../../launch/images/day1.png
```
