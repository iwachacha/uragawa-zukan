# Codex Instructions for ウラガワ図鑑

このリポジトリでは「ウラガワ図鑑」の世界観を守りながら、SNS投稿、画像生成プロンプト、SUZURI商品化候補を継続制作する。

## 必ず守る核

- 固定するのは表現パターンではなく「身近な存在の見えていない裏事情を観測する」という態度。
- 裏事情は架空でよいが、形、質感、用途、扱われ方、季節性、名前、印象など現実との接続点を必ず持たせる。
- 「ありえないけど、なんかわかる」を目指す。
- 教訓、社会批評、正解の押しつけに寄せすぎない。
- かわいい、怖い、笑える、エモい、おしゃれ、変など反応の方向を固定しない。
- 商品化候補は、説明文なしでも単体ビジュアルとして欲しくなる形まで整理する。

## 作業開始時

1. `uragawa_zukan.md` と `uragawa_zukan_output_rules.md` を必要範囲で読む。
2. 過去生成物との接続が必要な場合は `data/uragawa_ledger.tsv` と `data/continuity_notes.md` を確認する。
3. 偏りを避けるため、`python scripts/check_motif_balance.py` を実行し、`data/motif_rotation.tsv` と `data/style_memory.tsv` を確認する。
   原則として主役級は `生き物` と `植物・菌類` を多めにする。`道具・日用品` は少なめにし、関係性や周辺現象として使うことを優先する。
   `道具・日用品` が過多と表示された場合、ユーザーが明示しない限り新規主役に道具を選ばない。
4. 女性中心のターゲットを前提に、`docs/audience_and_motif_safety.md` を確認する。不快に思われやすい虫や害虫は主役にしない。
5. 新規制作は `templates/observation.md` の構成を基本にする。ただし、語り口や反応の方向は固定しない。
6. 画像戦略は `docs/visual_strategy.md` から選び、背景なしの存在主役か、背景込みの世界主役かを決める。
7. 画像生成プロンプトは `gpt-image2.0` に渡しやすい、具体的な視覚要素中心の文章にする。

## 出力品質の判断

- モチーフが一目でわかる。
- 裏事情が絵だけでも少し伝わる。
- 現実との接続点が画面内に残っている。
- ただのキャラクター化で終わっていない。
- 見た目の第一印象に、キャラクター性、ストーリー性、シルエット、シュールさ、かわいさ、グラフィック性のうち最低2つの強みがある。
- 誰に刺すのか、何に刺さるのかを明示する。平均点にまとめず、健気さ、不穏さ、労働感、所有欲、変なかっこよさなどのどれかを少し尖らせる。
- 画面内で何かが起きている。置かれているだけの静物画にしない。
- ステッカー、Tシャツ、トート、スマホケースのどれかで成立する余白と外形がある。
- 過去作に似すぎていない。似せる場合は意図した再登場や関係性として扱う。

## ファイル運用

- 正式採用した存在だけ `data/uragawa_ledger.tsv` に1行で追加する。
- 正式採用番号は `python scripts/next_uragawa_number.py` で確認する。
- 台帳の状態は `docs/operating_decisions.md` の採用ステータスに合わせる。
- 関係性、再登場候補、避けたい反復は `data/continuity_notes.md` に短く記録する。
- 反応方向、視覚トリック、色方向の履歴は `data/style_memory.tsv` に残す。
- 台帳登録や画像生成前に、必要なら `templates/concept_review.md` で採点・懸念・次アクションを残す。
- 視覚的な強さに迷う場合は `docs/visual_strength_gate.md` を先に確認する。
- 商品化候補の魅力が弱い場合は `docs/pointed_appeal_gate.md` を確認する。
- 世界観が弱い、現実に寄りすぎている場合は `docs/fantasy_amplitude_policy.md` を確認する。
- 主役題材として扱えるか迷う場合は `docs/motif_suitability_gate.md` を確認する。
- 商品化候補は `docs/product_format_rules.md` に従い、原則 `primary format: square` で設計する。
- SUZURI向けの入稿・商品化判断は `docs/suzuri_product_references.md` を参照し、正式入稿前は公式テンプレートを再確認する。
- 画像生成プロンプトは `docs/structured_image_prompt.md` の構造を優先する。
- モチーフ安全性チェックは `python scripts/check_motif_safety.py <file>` を使う。
- 生成画像を見た後は `templates/image_review.md` でレビューし、必要ならプロンプトを修正する。
- 完成出力は `outputs/` 配下にMarkdownで保存する。ファイル名は `NoXXX-name.md` または `candidate-name.md` を推奨する。
- 構成チェックは `python scripts/validate_uragawa_output.py <file>` を使う。
- 台帳チェックは `python scripts/validate_ledger.py` を使う。
- 履歴チェックは `python scripts/validate_style_memory.py` を使う。
- モチーフ配分チェックは `python scripts/check_motif_balance.py` を使う。

## 避けること

- 毎回「中に何かがいる」にする。
- 毎回「かわいい」「エモい」「怖い」「図鑑形式」に寄せる。
- 画像生成プロンプトを雰囲気語だけで終わらせる。
- SNS文だけで成立していて、ビジュアルでは何も起きていない案を通す。
- 商品化候補に長文説明を前提にした構図を残す。
