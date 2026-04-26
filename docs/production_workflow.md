# ウラガワ図鑑 Production Workflow

## 1. 種を集める

身近なモチーフを広く出す。動物、植物、食べ物、日用品、自然現象、場所、質感、概念まで含めてよい。
ただし、主役級は生き物・植物・菌類を多めにする。

新規制作前に偏りを確認する。

```powershell
python scripts/check_motif_balance.py
```

各モチーフに対して、現実との接続点を最低3つ出す。

- 形、色、質感
- 用途、置かれ方、扱われ方
- 季節、音、匂い、温度
- 名前、既存イメージ、似ているもの

## 2. 裏事情を作る

基本式:

```text
モチーフ × 現実との接続点 × 架空の裏事情 × 反応の方向 × ビジュアル化
```

裏事情は自由に作る。ただし、現実との接続が画面内に残るものを優先する。

## 3. ビジュアルに変換する

画像生成前に、以下を短く決める。

- 絵だけで伝えるべき意外性
- 現実との接続を見せる要素
- 裏事情の表現方法
- 視覚的な主役
- 画面内で起きている行動
- ステッカーにしたときの外形
- 避ける弱い表現
- 商品化で映えるポイント

設定が面白くても、絵にすると普通のかわいい絵になる案は再設計する。
特に、置かれているだけの静物画になりそうな案は `docs/visual_strength_gate.md` に照らして差し戻す。
商品化候補では、誰に何が刺さるかを `docs/pointed_appeal_gate.md` に照らして確認する。
主役題材に向くかは `docs/motif_suitability_gate.md`、商品フォーマットは `docs/product_format_rules.md` で確認する。

## 4. 出力する

`templates/observation.md` を使って、次を揃える。

- 構想メモ
- ウラガワ図鑑本文
- ビジュアル設計
- gpt-image2.0向け画像生成プロンプト
- SNS投稿文
- SUZURI商品化メモ
- 台帳登録用1行

画像生成プロンプトは `docs/structured_image_prompt.md` の `[GOAL]` から `[AVOID]` までの構造を使う。
画像戦略は `docs/visual_strategy.md` から選ぶ。ターゲットと避けるモチーフは `docs/audience_and_motif_safety.md` を確認する。

## 5. 検証する

構成チェック:

```powershell
python scripts/validate_uragawa_output.py outputs\candidate-name.md
python scripts/validate_ledger.py
python scripts/validate_style_memory.py
```

品質チェック:

- ただのキャラ化になっていないか。
- 現実との接続点が見えるか。
- 絵だけで「普通と違う」が伝わるか。
- 商品にしたとき文字なしで成立するか。
- 過去作と同じ型に寄りすぎていないか。

台帳に入れる前、または画像生成へ進める前に、必要なら `templates/concept_review.md` で点数、懸念、次アクションを残す。

## 6. 台帳に残す

正式採用したものだけ `data/uragawa_ledger.tsv` に追加する。

関係性や再登場候補は `data/continuity_notes.md` に残す。世界全体を厳密な体系にしすぎず、再利用できる軽い索引として扱う。

番号は採用時にだけ確定する。次の番号は以下で確認する。

```powershell
python scripts/next_uragawa_number.py
```

反応方向や視覚トリックが偏らないように、採用・投稿・画像生成のたびに `data/style_memory.tsv` へ軽く記録する。

## 7. 商品化候補を再編集する

SNSで反応がよい案は、投稿そのものを商品化しない。以下を見直す。

- 文字を減らす、またはなくす。
- シルエットを強める。
- 余白を増やす。
- 色数を整理する。
- モチーフを単体化する、またはペア構図にする。
- 小さく印刷しても裏事情の核が残るようにする。
