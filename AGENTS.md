# Codex Instructions for ウラガワ図鑑

このリポジトリでは「ウラガワ図鑑」の世界観を守りながら、SNS投稿、画像生成プロンプト、SUZURI商品化候補を継続制作する。

## 最初に読むもの

1. `uragawa_zukan.md`: 変更しない世界観の核。
2. `docs/current_strategy.md`: 現在のターゲット、モチーフ配分、商品化方針。
3. `docs/creative_decision_pipeline.md`: 制作判断の順序。

細部が必要になった場合だけ、個別ゲート文書やテンプレートを読む。

## 制作の基本フロー

1. `python scripts/check_motif_balance.py` を実行し、直近の偏りを確認する。
2. 新規制作では、まず `templates/idea_batch.md` で複数案を出す。
3. ユーザーの選別結果は `data/selection_feedback.tsv`、未採用案は `data/idea_bank.tsv` に残す。
4. 選ばれた案だけ `templates/observation.md` へ昇格する。
5. 画像生成前に `templates/concept_review.md` で必須ゲートとスコアを確認する。
6. 画像生成プロンプトは `docs/structured_image_prompt.md` の構造を使う。
7. 生成画像は `templates/image_review.md` で商品化前提にレビューする。
8. 正式採用したものだけ `data/uragawa_ledger.tsv` に登録する。

## 必ず守る核

- 固定するのは表現パターンではなく「身近な存在の見えていない裏事情を観測する」という態度。
- 裏事情は架空でよいが、形、質感、用途、扱われ方、季節性、名前、印象など現実との接続点を必ず持たせる。
- 「ありえないけど、なんかわかる」を目指す。
- 教訓、社会批評、正解の押しつけに寄せすぎない。
- 商品化候補は、説明文なしでも単体ビジュアルとして欲しくなる形まで整理する。

## 現在の運用優先

- 主役級は `生き物` と `植物・菌類` を多めにする。
- `道具・日用品` は完全禁止ではないが、主役より関係性や舞台装置として使う。
- 女性中心ターゲットを前提に、ゆるかわ、エモ、おしゃれを入口にする。
- ただかわいいだけでは通さない。世界観、意外性、ストーリー性、商品化したくなる外形のいずれかを強める。
- 不快感が強い虫や害虫は主役にしない。詳細は `data/motif_taxonomy.tsv` と `docs/current_strategy.md` に従う。

## 出力品質の判断

- モチーフが一目でわかる。
- 裏事情が絵だけでも少し伝わる。
- 現実との接続点が画面内に残っている。
- 画面内で何かが起きている。
- 見た目の第一印象に、キャラクター性、ストーリー性、シルエット、シュールさ、かわいさ、グラフィック性のうち最低2つの強みがある。
- 誰に刺すのか、何が刺さるのかを明示する。
- ステッカー、Tシャツ、トート、スマホケースのどれかで成立する余白と外形がある。

## 検証

```powershell
python scripts/validate_uragawa_output.py templates\observation.md
python scripts/validate_uragawa_output.py --strict outputs\candidate-name.md
python scripts/check_motif_safety.py --strict outputs\candidate-name.md
python scripts/check_motif_balance.py
python scripts/check_motif_balance.py --include-ideas
python scripts/validate_ledger.py
python scripts/validate_style_memory.py
python scripts/validate_idea_workflow.py
```

採用番号は次で確認する。

```powershell
python scripts/next_uragawa_number.py
```
