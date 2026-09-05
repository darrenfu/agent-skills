# Design principles for HTML visualizations

Design for the content and audience. These are defaults to weigh against the user's requested format, existing design system, accessibility needs, and offline constraints.

- Make the main relationship or result easy to see. Use interaction when it helps exploration, not as decoration.
- Reuse established fonts, colors, and layouts when they aid familiarity. System fonts, flat backgrounds, and repeated templates are valid choices. Custom typography or a visual metaphor should earn its space.
- Use color consistently and provide adequate contrast. Do not rely on color alone to convey categories or status.
- Keep paragraphs readable, labels legible, and dense tables usable at narrow widths. Adapt language-specific typography.
- Motion is optional. When used, keep it purposeful and honor reduced-motion preferences.
- For a requested dark-only page, provide an accessible dark design. If using the bundled theme toggle, implement distinct light and dark variables according to its integration contract.
- Use semantic HTML, visible focus, keyboard-operable controls, and meaningful text alternatives.
- Preserve evidence, caveats, source links, and numerical accuracy. A visual must not imply unsupported precision or causality.
- Add a footer, author identity, or generated-by attribution only when requested or required by an applicable license. Do not infer a private user's name for publication.

For a substantial page, decide purpose, audience, information hierarchy, visual encoding, and interaction before implementation. A small chart does not require a six-part creative brief. Inspect the result rather than judging it by novelty or an arbitrary aesthetic score.
