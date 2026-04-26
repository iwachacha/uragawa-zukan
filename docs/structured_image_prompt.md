# Structured Image Prompt

gpt-image2.0 向けプロンプトは、人間向けの企画説明ではなく、画像生成AIが優先順位を誤らない視覚仕様として書く。

## Canonical Structure

```text
[GOAL]
product-ready illustration for {target products}. The most important appeal is {刺さる魅力}. The image must communicate the hidden-world idea without relying on text.

[CORE SUBJECT]
main subject:
supporting subjects:
recognizable real-world features:
relative scale:

[HIDDEN-WORLD LOGIC]
real-world connection:
fictional hidden circumstance:
why it feels strangely understandable:

[VISUAL HOOK]
first-glance surprise:
visible action:
silhouette:
accent detail:

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
line:
color:
texture:
expression:
finish:

[MUST INCLUDE]
-
-
-

[MUST AVOID]
-
-
-

[NEGATIVE CONSTRAINTS]
no tiny explanatory text, no horizontal-only composition, no realistic unpleasant insect details, no weak still life, no white subject disappearing on white background
```

## Required Decisions

- `primary format` は原則 `square`。
- `master canvas` は商品展開用の基準として `3000 x 3000 transparent PNG` を基本にする。
- `target product` は `Sticker`, `T-Shirt`, `Tote`, `Smartphone Case`, `Acrylic Key Chain`, `Acrylic Stand` から具体的に選ぶ。
- `visual strategy` は `Character Icon`, `World Object`, `Relationship Pair`, `Scene Emblem`, `Pattern Seed` から選ぶ。
- 横長構図は `secondary crops` に置く。`primary format: horizontal` は明確な商品理由がある場合だけ。

## Writing Rules

- 1セクションは1-3文、または短い箇条書きにする。
- 抽象語だけで終わらせない。「かわいい」ではなく、何がどうかわいいかを書く。
- 裏事情は `[HIDDEN-WORLD LOGIC]`、見た目は `[VISUAL HOOK]` に分ける。
- 文字や説明を入れる場合も、画像そのものが文字なしで成立するようにする。
- 背景なし単体なのか、背景込みで世界を見せるのかを明示する。
- 主役と周辺物のスケールを書く。現実接続を壊すほど大きさを誇張しない。
- 不快な虫、害虫、リアルな脚、群がり、複眼、卵、寄生感は明確に避ける。

## Bad Example

```text
かわいくて不思議なカタツムリが雨を運んでいるイラスト。
```

## Better Example

```text
[GOAL]
product-ready square sticker illustration for Sticker, T-Shirt, and Tote. The appeal is a quiet rain-keeper snail that feels gentle and a little magical, not just cute.

[CORE SUBJECT]
main subject: a small round snail with a translucent shell shaped like a tiny rain jar.
supporting subjects: two dewdrops, a short wet leaf, a faint puddle ring.
recognizable real-world features: snail body, spiral shell, wet leaf, rain droplets.
relative scale: snail remains realistically small compared with the leaf.

[HIDDEN-WORLD LOGIC]
real-world connection: snails appear after rain and carry spiral shells.
fictional hidden circumstance: the shell stores leftover rain and releases it drop by drop on dry mornings.
why it feels strangely understandable: the wet body, slow movement, and shell all feel connected to rain.

[VISUAL HOOK]
first-glance surprise: the shell is visibly half-filled with blue rainwater and a tiny cloudy reflection.
visible action: the snail carefully pours one drop onto the leaf with a serious face.
silhouette: round shell, soft body, single large droplet.
accent detail: pale blue water inside the shell.
```
