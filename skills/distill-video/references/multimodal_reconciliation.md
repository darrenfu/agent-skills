# Multimodal Reconciliation

Use this procedure when a video has more than one useful evidence stream.

## Preserve evidence first

Keep these artifacts separate:

- Original video
- Raw extracted audio
- Optional denoised audio
- Raw timestamped ASR
- Source subtitles or auto-captions
- Sampled frames
- Timestamped frame/OCR output
- Reconciled and reorganized transcript

Never replace the raw transcript with a cleaned rewrite.

## Align the streams

Build timestamp windows around each spoken claim or procedural step. Within each window, compare:

1. Audio ASR for what was spoken
2. Source subtitle track for alternate wording and timing
3. Visible frame text/OCR for names, numbers, commands, UI labels, charts, or formulas
4. Adjacent context for incomplete sentences and pronoun references

Prefer direct audio for spoken meaning, visible source text for exact spellings and displayed values, and human-authored subtitles when audio is unclear. Treat auto-captions and OCR as fallible. When the streams disagree without a clear winner, record the conflict.

## Reorganize

Transform transcript order into a useful structure while retaining timestamp links:

- Thesis or intended outcome
- Concepts and prerequisites
- Ordered procedure or argument
- Examples and demonstrations
- Exceptions, caveats, and failure modes
- Reusable prompts, formulas, commands, or decision rules

Move repeated explanations together. Do not merge separate claims merely because they sound similar.

## Semantic denoising

Remove only material that does not change meaning:

- Filler words and verbal tics
- Exact repetition and abandoned false starts
- Obvious ASR fragments
- Sponsor reads, housekeeping, and unrelated banter
- OCR duplicates across consecutive frames

Preserve emphasis when repetition is meaningful, all numbers and qualifiers, uncertainty, examples, warnings, and contradictions. Mark repaired names or terms when the correction is not obvious.

## Audio denoising

Use audio filtering only when noise measurably degrades ASR. Preserve raw audio and compare short transcript samples before and after filtering. If filtering removes quiet speech, revert to raw audio or use a milder filter. Audio cleanup is an ASR aid, not a replacement for evidence reconciliation.
