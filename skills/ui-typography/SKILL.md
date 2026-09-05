---
name: ui-typography
description: Review or refine UI typography, readable text hierarchy, spacing, punctuation, and font choices when the task concerns typography or visual design. Apply changes to the affected interface and follow its language, brand, and code conventions.
---

# UI Typography

Refine typography when it is part of the requested UI work. Preserve existing brand conventions and text semantics; a functional code change does not justify rewriting unrelated visible copy.

## Attribution

Inspired by Matthew Butterick's *Practical Typography* (https://practicaltypography.com). Treat stylistic advice as context-sensitive guidance, not universal correctness rules.

## Apply to the affected surface

- Establish a clear heading and body hierarchy using the existing design system. Prefer readable sizes, line lengths, line spacing, and restrained emphasis; inspect them in the actual layout.
- Choose fonts for legibility, language coverage, load constraints, and brand consistency. System fonts and monospace data views are legitimate choices. Limit unnecessary families rather than enforcing a universal font count.
- For prose, use punctuation appropriate to its language and editorial style. Preserve straight quotes and exact characters in code, identifiers, commands, data, and verbatim quotations. Do not run a global smart-quote replacement.
- Distinguish hyphens, ranges, minus signs, and quotation marks according to meaning. Preserve mathematical symbols, measurement notation, and locale-specific conventions.
- Avoid artificial tracking in scripts where it harms reading; all-cap labels and Latin letter-spacing advice are not universal rules for CJK text.
- Use emphasis, capitals, emoji, and punctuation according to the product's voice. Do not remove meaning to satisfy a stylistic ban. Keep links identifiable and focus visible.
- Inspect truncation, wrapping, zoom, fallback fonts, localization, and responsive layouts where the change can affect them.

## Resources

Read [css-templates.md](css-templates.md) for CSS examples and [html-entities.md](html-entities.md) for character encodings as needed. Adapt examples to the actual stack; reference templates are not a requirement to replace the project's baseline styles.

Preserve valid HTML/JSX/string syntax. Use literal characters or correctly encoded characters for the relevant context, and verify the rendered result rather than applying markup rules inside program strings.

For an audit, report concrete readability or consistency problems with the affected component and a proposed fix. For an authorized refinement, implement it and check the affected views. Avoid a whole-document typography audit for a small UI correction.
