# ウラガワ図鑑｜毎回の出力ルール

この文書は、フル観測出力の最低ルールを定める。制作判断の順序は `docs/creative_decision_pipeline.md`、現在の運用方針は `docs/current_strategy.md` を優先する。

## 基本方針

- 身近な存在の、見えていない裏事情を観測する。
- 現実の形、性質、用途、扱われ方、季節性、印象などと薄く接続させる。
- 裏事情は自由に作ってよいが、絵の中に接続点を残す。
- かわいい、怖い、笑える、エモいなど反応の方向は固定しない。
- ただかわいいだけで終わらせない。
- 商品化を見据え、文字なしでも単体ビジュアルとして成立させる。

## 標準フロー

1. `templates/idea_batch.md` で複数案を出す。
2. ユーザー選別後、選ばれた案だけ `templates/observation.md` に昇格する。
3. `templates/concept_review.md` で必須ゲートとスコアを確認する。
4. `docs/structured_image_prompt.md` に沿って gpt-image2.0 用プロンプトを作る。
5. 生成画像は `templates/image_review.md` で商品化前提に見直す。
6. 正式採用したものだけ `data/uragawa_ledger.tsv` に登録する。

## フル出力の必須構成

`templates/observation.md` を使う。

- 構想メモ
- ウラガワ図鑑本文
- ビジュアル設計
- 画像生成プロンプト
- SNS投稿文
- SUZURI商品化メモ
- 存在台帳登録用

## ビジュアル設計で必ず決めること

- 絵だけで伝えるべき意外性
- 現実との接続を見せる要素
- 裏事情の表現方法
- 視覚的な主役
- 画面内で起きている行動
- 誰に刺す魅力
- 想定ターゲット
- 少し尖らせるポイント
- 画像戦略タイプ
- 背景の扱い
- 主役と周辺物のスケール
- ステッカーにしたときの外形
- 避ける弱い表現
- 商品化で映えるポイント

## 画像生成プロンプト

必ず `docs/structured_image_prompt.md` の構造を使う。

- `[GOAL]`
- `[CORE SUBJECT]`
- `[HIDDEN-WORLD LOGIC]`
- `[VISUAL HOOK]`
- `[COMPOSITION]`
- `[PRODUCT USE]`
- `[STYLE]`
- `[MUST INCLUDE]`
- `[MUST AVOID]`
- `[NEGATIVE CONSTRAINTS]`

原則は `primary format: square`。横長専用にしない。

## 台帳

正式採用する存在だけ `data/uragawa_ledger.tsv` に登録する。試作段階は `No.XXX`、正式採用時に `scripts/next_uragawa_number.py` で番号を確定する。

台帳の列:

```tsv
id	title	category	motif	visual_strategy	target_products	status	score	continuity_links	created_at	notes
```

## チェック

```powershell
python scripts/validate_uragawa_output.py --strict outputs\candidate-name.md
python scripts/check_motif_safety.py --strict outputs\candidate-name.md
python scripts/validate_ledger.py
python scripts/validate_style_memory.py
```
