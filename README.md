# uragawa-zukan

「ウラガワ図鑑」の制作基盤です。世界観の核を固定しながら、SNS投稿、画像生成プロンプト、SUZURI商品化候補を継続制作します。

## 入口

- [uragawa_zukan.md](uragawa_zukan.md): 世界観の核
- [docs/current_strategy.md](docs/current_strategy.md): 現在の運用方針
- [docs/creative_decision_pipeline.md](docs/creative_decision_pipeline.md): 制作判断の順序
- [AGENTS.md](AGENTS.md): Codex向け作業指示

## よく使うテンプレート

- [templates/idea_batch.md](templates/idea_batch.md): 複数案の軽量出し
- [templates/observation.md](templates/observation.md): 採用候補のフル出力
- [templates/concept_review.md](templates/concept_review.md): 画像生成前の採用判断
- [templates/image_review.md](templates/image_review.md): 生成画像レビュー

## データ

- [data/idea_bank.tsv](data/idea_bank.tsv): 未採用案・保留案
- [data/selection_feedback.tsv](data/selection_feedback.tsv): ユーザー選別結果
- [data/uragawa_ledger.tsv](data/uragawa_ledger.tsv): 正式採用した存在
- [data/style_memory.tsv](data/style_memory.tsv): 公開・生成済みの反応方向と視覚トリック
- [data/motif_taxonomy.tsv](data/motif_taxonomy.tsv): モチーフ分類、安全性、配分
- [data/continuity_notes.md](data/continuity_notes.md): 関係性や再登場候補

## 主要ドキュメント

- [docs/visual_language.md](docs/visual_language.md): 見た目の基準
- [docs/product_qa.md](docs/product_qa.md): SUZURI商品化前提の確認
- [docs/structured_image_prompt.md](docs/structured_image_prompt.md): gpt-image2.0向け構造化プロンプト
- [docs/suzuri_product_references.md](docs/suzuri_product_references.md): SUZURI公式仕様と参考
- [docs/quality_rubric.md](docs/quality_rubric.md): 必須ゲートと採点基準

## 検証

```powershell
python scripts/validate_uragawa_output.py --self-test
python scripts/validate_uragawa_output.py templates\observation.md
python scripts/validate_uragawa_output.py --strict tests\fixtures\valid_observation.md
python scripts/validate_ledger.py
python scripts/validate_style_memory.py
python scripts/validate_idea_workflow.py
python scripts/check_motif_balance.py
python scripts/check_motif_balance.py --include-ideas
python scripts/check_motif_safety.py --strict tests\fixtures\valid_observation.md
python scripts/next_uragawa_number.py
```

失敗することを確認するfixture:

```powershell
python scripts/validate_uragawa_output.py --strict tests\fixtures\blocked_motif_observation.md
python scripts/validate_uragawa_output.py --strict tests\fixtures\invalid_horizontal_observation.md
python scripts/check_motif_safety.py --strict tests\fixtures\blocked_motif_observation.md
```
