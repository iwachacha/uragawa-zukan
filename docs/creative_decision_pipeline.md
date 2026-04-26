# Creative Decision Pipeline

ウラガワ図鑑の制作は、発想を狭めず、判断は機械的に迷わない順番で進める。

## 1. Context Check

制作前に最低限だけ確認する。

```powershell
python scripts/check_motif_balance.py
```

- 世界観の核: `uragawa_zukan.md`
- 現在の運用方針: `docs/current_strategy.md`
- 過去採用: `data/uragawa_ledger.tsv`
- 関係性・再登場: `data/continuity_notes.md`
- 反応方向と視覚トリック: `data/style_memory.tsv`

## 2. Idea Batch

新規制作では、いきなり完成形を作らない。まず `templates/idea_batch.md` で 20-40 案を軽量に出す。

各案は次を必ず持つ。

- モチーフカテゴリ
- 現実との接続点
- 架空の裏事情
- メインビジュアル
- 刺さる層
- 商品化戦略
- リスク

採用前の候補は `data/idea_bank.tsv` に残す。ユーザー判断は `data/selection_feedback.tsv` に残し、採用・保留・却下の理由を次回の案出しに反映する。

## 3. Motif Gate

`data/motif_taxonomy.tsv` を基準にする。

- 優先: `生き物`, `植物・菌類`
- 中程度: `食べ物`, `自然・場所`
- 控えめ: `道具・日用品`, `質感・概念`, `その他`

不快感が出やすい虫や害虫は主役から外す。条件付き許可のモチーフでも、かわいさ・おしゃれさ・図案化しやすさが明確でない場合は差し戻す。

## 4. Concept Gate

候補を絞るときは、平均点にまとめない。次のどれかを少し尖らせる。

- 健気さ
- 不穏さ
- 労働感
- 所有欲
- 変なかっこよさ
- 怖かわいさ
- 静かなエモさ
- 図案としての気持ちよさ

ただし、教訓や社会批評を直接言い切らない。

## 5. Visual Gate

絵だけで最低限伝わる状態にする。

- 一目で元モチーフがわかる。
- 裏事情が画面内の行動、形、断面、影、反射、関係性として見える。
- 現実との接続点が画面に残る。
- 置いてあるだけの静物画にしない。
- 小さく表示しても主役の外形と行動が読める。

視覚的に弱い場合は、`docs/visual_language.md` と `docs/visual_strength_gate.md` に戻す。

## 6. Product Gate

画像生成前に商品戦略を決める。

- `Character Icon`: ステッカー、Tシャツ、トート、スマホケース向き。
- `World Object`: 主役の体内、殻、葉、花、断面に小さな世界を入れる。
- `Relationship Pair`: ペア、セット、シリーズ向き。単体化案も考える。
- `Scene Emblem`: 背景込みの世界。スマホケース、アクリル、ポスター寄り。
- `Pattern Seed`: 総柄や小物向き。単体アイコンも同時に作る。

詳細は `docs/product_qa.md` と `docs/suzuri_product_references.md` を確認する。

## 7. Prompt Gate

画像生成プロンプトは `docs/structured_image_prompt.md` の構造を使う。人間向け説明文ではなく、AIが優先順位を誤らない視覚指定にする。

必ず指定する。

- `core subject`
- `hidden-world logic`
- `visual hook`
- `composition`
- `product use`
- `must include`
- `must avoid`
- `negative constraints`

原則は `primary format: square`。横長専用は、商品戦略上の理由がある場合だけにする。

## 8. Review and Record

画像生成前は `templates/concept_review.md`、画像生成後は `templates/image_review.md` を使う。

採用・生成・商品化の段階に応じて記録する。

- 未採用案: `data/idea_bank.tsv`
- ユーザー選別結果: `data/selection_feedback.tsv`
- 正式採用: `data/uragawa_ledger.tsv`
- 反応方向・視覚トリック履歴: `data/style_memory.tsv`
- 関係性・再登場候補: `data/continuity_notes.md`

