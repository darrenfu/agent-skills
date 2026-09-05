# Input Handling

Use this reference to identify and normalize the paper source before distillation.

## Supported Inputs / 支持的输入

- **PDF file / PDF 文件**: local `.pdf` path or attachment.
- **Paper link / 论文链接**: arXiv, alphaXiv, OpenReview, DOI, conference page, project page, GitHub release, lab blog with PDF.
- **Screenshot / 截图**: title page, abstract, figure, table, video frame, or social media screenshot.
- **Title only / 只有标题**: exact or approximate paper title.
- **Abstract or pasted text / 摘要或粘贴正文**: enough content to start; still search for full source if the user asks for full-paper distillation.
- **Mixed input / 混合输入**: screenshot plus title, link plus comments, PDF plus user focus.

## Acquisition Rules

1. Prefer primary paper sources: arXiv PDF, conference proceedings, OpenReview, official project page, lab/company page, DOI landing page.
2. For alphaXiv links, check the canonical page, `citation_pdf_url`, and visible metadata. If PDF download fails, retry with a browser user-agent and `Accept: application/pdf`.
3. For screenshots, visually inspect or OCR the image. Extract title, authors, venue/date, visible section labels, and any spoken caption. Then search the exact title.
4. For title-only inputs, search the exact title in quotes first, then without quotes. Confirm the title, authors, and date before reading.
5. If multiple versions exist, prefer the newest official version unless the user points to a specific version. Record the exact source used.
6. If the full paper cannot be retrieved, still produce a "limited-source distillation" and clearly mark which sections are based only on abstract/screenshot/metadata.

## Extraction Rules

- For PDFs, use available PDF tools such as `pdftotext`, `pdfinfo`, Python PDF libraries, or browser extraction.
- Preserve page/section references for claims that will be cited.
- Read figure captions and tables; many paper claims live there rather than in prose.
- If extraction mangles formulas, inspect the PDF page visually or cite the formula location without pretending exact notation is certain.

## Metadata to Capture

Record these fields when available:

- title
- authors
- year/date
- venue/source
- URL/PDF path
- task/domain
- target audience requested by the user
- mode: fast-read, deep-read, or both
- source limitations
