---
name: uragawa-zukan
description: Create and refine ウラガワ図鑑 content, including new observations, hidden-world concepts, gpt-image2.0 visual prompts, SNS copy, SUZURI merchandise notes, continuity links, and ledger-ready entries. Use when Codex is asked to produce, evaluate, adapt, or merchandise Uragawa Zukan ideas while preserving the fixed worldview and allowing flexible creative variation.
---

# ウラガワ図鑑

## Core

Create observations of the unseen back side of familiar things. Keep the worldview fixed, but do not fix the format, emotion, motif type, or visual trick.

The invariant is:

```text
身近な存在 × 現実との接続点 × 架空の裏事情 × 反応の方向 × 視覚化
```

Aim for "ありえないけど、なんかわかる". Avoid turning the work into only a cute mascot, a single joke, a moral lesson, or a repeated template.

## Workflow

1. Read `references/worldview-core.md` for the non-negotiable worldview.
2. If producing a full output, follow `references/output-contract.md`.
3. Check past continuity in the project files when available:
   - `data/uragawa_ledger.tsv`
   - `data/continuity_notes.md`
   - `data/style_memory.tsv`
   - `data/motif_rotation.tsv`
   - run `scripts/check_motif_balance.py`
4. Generate several directions before choosing one. Vary motif class, emotional direction, and visual mechanism.
   Prefer living beings and plants/fungi as main characters. Use tools and daily objects less often, usually as relationship or supporting motifs.
5. Write the visual design before the image prompt.
6. For gpt-image2.0 prompts, describe visible objects, action, hidden story visualization, expression, colors, line quality, background, and merchandise-friendly silhouette.
7. Validate full Markdown outputs with `scripts/validate_uragawa_output.py` when working in this repository.
8. Before image generation or ledger registration, use `templates/concept_review.md` when the candidate needs an explicit go/no-go record.
9. Validate ledger and history changes with `scripts/validate_ledger.py` and `scripts/validate_style_memory.py`; get adopted numbers with `scripts/next_uragawa_number.py`.

## Creative Guardrails

- Preserve: unseen hidden circumstances, thin real-world connection, observational tone, visual merchandise potential.
- Vary: motif, reaction, tone, format, visual trick, composition, product layout.
- Prefer a specific visual mechanism over a vague mood.
- Require at least two first-glance strengths: character, story/action, silhouette, surrealness, cuteness, or graphic appeal.
- State who the concept is for and what will hit them. Push one appeal slightly: devotion, unease, labor, ownership desire, odd coolness, or scary-cuteness.
- Reject still-life concepts where objects are merely placed and the hidden story lives only in text or tiny details.
- Let captions enrich the world, but make the image work without long text.
- Use relationships between beings sparingly and keep them local to the observation unless the user asks for continuity.

## Output Modes

Use the mode that matches the request.

- **New observation**: produce the full template from `references/output-contract.md`.
- **Idea batch**: produce compact candidates with motif, connection point, hidden story, visual core, and product potential.
- **Relationship observation**: read ledger/continuity first, then connect two or more beings without over-systematizing the world.
- **Merch refinement**: reduce explanatory text, strengthen silhouette, simplify colors, and produce product-specific prompts.
- **Image review**: use `templates/image_review.md` after generation, then revise the prompt or concept.
- **Concept review**: use `templates/concept_review.md` before image generation, SNS testing, or adoption.
- **Review/validation**: use `references/quality-rubric.md` and list concrete fixes.

## Must Check Before Finalizing

- The motif is recognizable at a glance.
- The hidden side can be partly understood visually.
- A real-world property remains visible in the image.
- The concept is not only cute.
- The visual has a clear protagonist and action.
- The image can become a sticker or one-point product without relying on text.
- It does not repeat the same hidden-story format as recent outputs unless intentional.

## References

- `references/worldview-core.md`: fixed worldview and anti-patterns.
- `references/output-contract.md`: full output structure and prompt requirements.
- `references/quality-rubric.md`: scoring rubric for concept and merchandise strength.
- Project docs to consult when available: `docs/audience_and_motif_safety.md`, `docs/visual_strategy.md`, `docs/suzuri_product_references.md`, `docs/visual_strength_gate.md`, `docs/pointed_appeal_gate.md`, `docs/fantasy_amplitude_policy.md`, `docs/motif_suitability_gate.md`, `docs/product_format_rules.md`, `docs/structured_image_prompt.md`.
