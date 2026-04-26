# Production Workflow

制作の正本は `docs/creative_decision_pipeline.md`。このファイルは実務手順だけを短くまとめる。

## 1. 配分を見る

```powershell
python scripts/check_motif_balance.py
```

未採用案も含めて偏りを見る場合:

```powershell
python scripts/check_motif_balance.py --include-ideas
```

## 2. 案を出す

新規制作では、まず `templates/idea_batch.md` で 20-40 案を出す。

- 主役級は `生き物` と `植物・菌類` を多めにする。
- `道具・日用品` は関係性や舞台装置として使う比率を上げる。
- 不快感が強い虫や害虫は主役にしない。
- ただかわいい案、置いてあるだけの案、横長専用の案はこの段階で落とす。

## 3. 選別を記録する

- 未採用・保留案: `data/idea_bank.tsv`
- ユーザー判断: `data/selection_feedback.tsv`
- 良い/悪い理由タグを残し、次回の案出しに反映する。

## 4. フル出力に昇格する

選ばれた案だけ `templates/observation.md` へ昇格する。

画像生成前に次を決める。

- 誰に刺すか。
- 何が刺さるか。
- 背景なし主役型か、背景込み世界型か。
- 第一候補商品は何か。
- 小さくしたとき何が残るか。

## 5. レビューする

画像生成前:

```powershell
python scripts/validate_uragawa_output.py --strict outputs\candidate-name.md
python scripts/check_motif_safety.py --strict outputs\candidate-name.md
```

必要に応じて `templates/concept_review.md` を作る。

画像生成後:

- `templates/image_review.md` で、見た目、世界観、商品化適性を確認する。
- 弱い場合は、設定ではなく主役の形、行動、関係性、商品配置を修正する。

## 6. 採用して記録する

正式採用したものだけ `data/uragawa_ledger.tsv` に登録する。番号は採用時にだけ確定する。

```powershell
python scripts/next_uragawa_number.py
python scripts/validate_ledger.py
python scripts/validate_style_memory.py
python scripts/validate_idea_workflow.py
```

採用、画像生成、SNS投稿、商品化候補化のたびに `data/style_memory.tsv` へ反応方向と視覚トリックを残す。
