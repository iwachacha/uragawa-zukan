---
name: uragawa-zukan
description: Create, evaluate, refine, and merchandise ウラガワ図鑑 content. Use when Codex needs to generate idea batches, hidden-world observations, gpt-image2.0 prompts, SNS copy, SUZURI product notes, image reviews, continuity links, motif-balance checks, or ledger-ready entries while preserving the fixed Uragawa Zukan worldview and current audience/product strategy.
---

# ウラガワ図鑑

## Core

Create observations of the unseen back side of familiar things.

Invariant:

```text
身近な存在 × 現実との接続点 × 架空の裏事情 × 反応の方向 × 視覚化
```

Preserve the worldview. Do not freeze motif type, emotion, output format, visual trick, or product layout.

## Project Workflow

When working inside the project repository:

1. Read `uragawa_zukan.md` for the fixed worldview.
2. Read `docs/current_strategy.md` for current audience, motif, fantasy, and product defaults.
3. Follow `docs/creative_decision_pipeline.md` for the decision order.
4. Run or consult `scripts/check_motif_balance.py` before new ideation.
5. Use `templates/idea_batch.md` before producing full observations unless the user already selected a concept.
6. Promote selected ideas to `templates/observation.md`.
7. Use `docs/structured_image_prompt.md` for gpt-image2.0 prompts.
8. Validate filled outputs with `scripts/validate_uragawa_output.py --strict`.

## Output Modes

- **Idea batch**: produce 20-40 compact candidates with category, motif, reality connection, hidden circumstance, visual hook, target audience, product strategy, and risk.
- **Full observation**: follow `templates/observation.md`.
- **Concept review**: use `templates/concept_review.md` and `docs/quality_rubric.md`.
- **Image prompt**: write structured AI-facing visual instructions, not prose-only explanations.
- **Image review**: use `templates/image_review.md`, focusing on first-glance appeal, worldview clarity, and product viability.
- **Merch refinement**: simplify silhouette, reduce text dependency, choose product crops, and preserve the strongest visual hook.
- **Continuity work**: read `data/uragawa_ledger.tsv`, `data/style_memory.tsv`, and `data/continuity_notes.md` before linking past beings.

## Guardrails

- Prefer `生き物` and `植物・菌類` as main subjects unless the user asks otherwise or balance data says otherwise.
- Use `道具・日用品` sparingly, often as supporting objects, settings, or relationship anchors.
- Avoid unpleasant insect or pest motifs as protagonists; use `data/motif_taxonomy.tsv` and `scripts/check_motif_safety.py`.
- Make the image work without long captions.
- Require a visible action, transformation, relationship, shadow, reflection, cutaway, interior world, or other visual mechanism.
- Do not pass concepts that are only cute, only a pun, only a moral lesson, or only a static object.
- Design for SUZURI from the start: square master by default, clear silhouette, no tiny explanatory text, no horizontal-only composition.

## Validation

Use these when available:

```powershell
python scripts/check_motif_balance.py
python scripts/check_motif_balance.py --include-ideas
python scripts/validate_uragawa_output.py --strict outputs\candidate-name.md
python scripts/check_motif_safety.py --strict outputs\candidate-name.md
python scripts/validate_ledger.py
python scripts/validate_style_memory.py
```

## Bundled References

- `references/worldview-core.md`: portable worldview summary.
- `references/output-contract.md`: portable full-output contract.
- `references/quality-rubric.md`: portable review rubric.
