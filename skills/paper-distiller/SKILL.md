---
name: paper-distiller
description: Explain or distill a research paper from a PDF, arXiv/DOI link, title, abstract, or screenshot. Use for paper-specific summaries, method explanations, deep reads, and teaching artifacts; match the requested depth and format.
---

# Paper Distiller

Explain the paper's problem, mechanism, evidence, and limits at the depth the user requested. A question about one equation can receive one focused explanation; it does not require a full teaching package.

## Workflow

1. Identify the paper and available source layers using [input-handling.md](references/input-handling.md). Prefer the actual paper and official supplementary material. Verify a title or screenshot against a primary source before attributing claims.
2. Read the sections needed to answer. For an overview, start with the abstract, motivation, main method, results, and limitations. For a technical deep read, inspect the relevant equations, evaluation setup, ablations, and appendix. Report unavailable source material rather than inventing it.
3. Explain the motivation before new abstractions. Use a concrete example when it clarifies a procedure. Distinguish the paper's claims, its measured evidence, background knowledge, and your inference; cite sections, figures, tables, or source URLs near substantive claims.
4. Match the user's language, length, audience, and output format. For an unspecified summary, provide the main idea, supporting result, and most consequential limitation, then expand only where needed.
5. For a requested full teaching artifact, select relevant sections from [distillation-template.md](references/distillation-template.md). The template is a menu, not a requirement to produce every retelling variant.
6. Use a diagram or interactive illustration when it materially improves understanding. For a requested HTML teaching page, see [visualize-contract.md](references/visualize-contract.md). For PPTX, Google Slides, a document, or a chat answer, use that format and the appropriate available authoring tools. HTML is optional.
7. Verify the delivered explanation against the source; for an artifact, also inspect its rendering and report its actual path or link.

## Quality checks

- Name the baseline and metric before interpreting a reported improvement.
- Explain notation before using it; mark where an analogy stops applying.
- Separate what was tested from a proposed application or unproven generalization.
- Do not present OCR, an abstract-only reading, or a secondary summary as a complete reading of the paper.
- Do not add a second language, multiple scripts, or fast/deep interface modes unless useful to the requested deliverable.
