# Output Contract

Use this structure for full observations.

```text
# 登録候補｜存在名

## 構想メモ
- カテゴリ：
- モチーフ：
- 現実との接続点：
- 架空の裏事情：
- 反応の方向：
- ビジュアルの核：

## ウラガワ図鑑
### 観測文
### 特徴
### 習性
### 注意点

## ビジュアル設計
- 絵だけで伝えるべき意外性：
- 現実との接続を見せる要素：
- 裏事情の表現方法：
- 視覚的な主役：
- 画面内で起きている行動：
- 誰に刺す魅力：
- 想定ターゲット：
- 少し尖らせるポイント：
- 主役題材としての適性：
- 推奨商品フォーマット：
- 画像戦略タイプ：
- 背景の扱い：
- 描き込み範囲：
- 主役と周辺物のスケール：
- ステッカーにしたときの外形：
- 避ける弱い表現：
- 商品化で映えるポイント：

## 画像生成プロンプト
### 構造化プロンプト
[GOAL]
[CORE SUBJECT]
[HIDDEN-WORLD LOGIC]
[VISUAL HOOK]
[COMPOSITION]
primary format:
secondary crops:
visual strategy:
background:
camera / angle:
spacing:
master canvas:
[PRODUCT USE]
target product:
sticker cutout:
t-shirt / tote placement:
phone-case crop:
acrylic concerns:
[STYLE]
[MUST INCLUDE]
[MUST AVOID]
[NEGATIVE CONSTRAINTS]

## SNS投稿文
### 短文版
### 図鑑版
### 商品紹介版

## SUZURI商品化メモ
- Tシャツ：
- ステッカー：
- スマホケース：
- ワンポイント：
- 総柄：
- 文字の有無：

## 存在台帳登録用
id	title	category	motif	visual_strategy	target_products	status	score	continuity_links	created_at	notes
No.XXX	存在名	カテゴリ	モチーフ	画像戦略	対象商品	draft	0	-	YYYY-MM-DD	-
```

## Prompt Requirements

- Make visible objects, action, hidden-world logic, composition, product use, style, must-include items, and avoid items explicit.
- Prefer `primary format: square`.
- Use `3000 x 3000 transparent PNG` as the default master canvas.
- Choose a visual strategy from `Character Icon`, `World Object`, `Relationship Pair`, `Scene Emblem`, `Pattern Seed`.
- Avoid tiny explanatory text and horizontal-only layouts.
