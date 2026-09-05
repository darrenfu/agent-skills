---
name: stop-slop
description: Edit or review prose for repetitive AI-style phrasing, filler, and unnatural rhythm when the user requests clearer, more natural writing or a slop check. Preserve meaning, voice, and uncertainty.
metadata:
  trigger: Writing prose, editing drafts, reviewing content for AI patterns
  author: Hardik Pandya (https://hvpandya.com)
---

# Stop Slop

Edit prose for clarity and a natural voice while preserving the author's meaning, uncertainty, register, and intended emphasis.

## Workflow

1. Identify the requested edit: light cleanup, substantive rewrite, or style review. Preserve the existing voice unless the user asks to change it.
2. Remove empty introductions, repeated conclusions, vague praise, and formulaic transitions when they add no meaning. Use [phrases](references/phrases.md), [structures](references/structures.md), and [examples](references/examples.md) as diagnostic examples, not literal blacklists.
3. Prefer concrete wording and active voice when the actor matters. Passive voice, nonhuman subjects, adverbs, hedges, and emphasis are appropriate when they preserve technical accuracy or the intended tone.
4. Vary repetitive sentence patterns where it improves reading. Do not enforce quotas for sentence length, list size, punctuation, or rhetorical devices.
5. Preserve quotations, code, identifiers, numerical claims, attribution, and meaningful qualifiers. Do not strengthen an uncertain claim just to make it sound decisive.
6. Read the result once for meaning, fluency, and requested length. Return the edited text; add an explanation only when requested or needed to flag a substantive ambiguity.

## Review criteria

Could a reader identify the main point sooner? Does each retained detail help? Did the edit change a fact, level of certainty, or voice? Fix observed problems rather than iterating toward an arbitrary self-score.

## License

MIT
