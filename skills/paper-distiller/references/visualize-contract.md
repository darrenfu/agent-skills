# Visualize Contract

Use this when rendering a paper distillation with the `visualize` skill.

## Required Page Features

The HTML must include:

- Fast-read / deep-read mode switch.
- Source card with title, authors, date, source URL/path, and caveats.
- One-sentence thesis.
- Motivation funnel: old bottleneck -> why naive fixes fail -> key observation -> paper's lever.
- Algorithm or pipeline flow diagram.
- Worked toy example.
- Concept ladder cards: plain language, analogy, analogy boundary, technical explanation.
- Evidence ledger with paper section/figure/table/equation references.
- Experiments section: baselines, metrics, headline results, and what the results do not prove.
- Limitations and follow-up questions.
- Retelling scripts: 60 seconds, 3 minutes, nontechnical, ML-engineer.

## Interaction

- Provide toggles or tabs for `速读 Fast Read` and `精读 Deep Read`.
- Keep the fast-read view concise enough for screenshots.
- Keep the deep-read view navigable with anchors or section jumps.
- Use visible evidence labels such as `Paper says`, `Evidence`, and `Inference`.

## Visual Metaphors

Choose a metaphor that matches the paper, not a generic dashboard:

- Systems/inference paper: dispatch board, control room, scheduling console.
- Architecture paper: blueprint, circuit bench, model lab.
- Theory paper: proof map, terrain map, theorem ladder.
- Dataset/evaluation paper: evidence room, benchmark arena.
- Human/behavior paper: field notebook, causal map.

## Instruction to Pass to Visualize

```text
Use $visualize to create a self-contained HTML page from this paper distillation.
Output type: interactive single-page explainer.
Audience: the user first, then a general audience retelling.
Must include fast-read and deep-read modes, motivation funnel, algorithm flow, worked toy example, evidence ledger, limitations, and retelling scripts.
Use bilingual Chinese/English headings when the distillation is bilingual.
Save to: <output-directory>
```
