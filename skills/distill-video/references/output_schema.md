# Output Schema

Use this schema for final artifacts when the user asks for structured distillation.

````markdown
# <Source-Derived Framework Or Skill Name>

## Source
- URL:
- Title:
- Author/Speaker:
- Duration:
- Extraction:
- Source artifacts:

## Source Type
Audio-first video, visual-rich video, or public image/text post. Explain the reason in one sentence.

For image/text posts, label evidence as post caption, image OCR, or inference.

## Evidence Layers
- Raw audio:
- Audio used for ASR:
- Raw timestamped ASR:
- Source subtitle/caption tracks:
- Sampled frames and frame OCR:
- Reconciled transcript:

Do not overwrite raw evidence with cleaned output.

## Reorganized and Denoised Transcript
Remove filler, duplicated speech, false starts, ad/sponsor noise, and obvious ASR fragments. Preserve claims, examples, caveats, numbers, uncertainty, and timestamps.

## Executive Summary
- 

## Framework
| Step | What | Why It Matters | How To Apply | Evidence |
|---|---|---|---|---|

## Reusable Prompts Or Templates
```text
...
```

## Details Not To Lose
- 

## Caveats
- 

## Timestamp Evidence
- 

## Reusable Skill
Operational checklist or skill-style instructions.
````
