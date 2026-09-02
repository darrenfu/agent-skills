---
name: distill-video
description: Use when the user provides a video, video page, or public Xiaohongshu post and wants resilient source extraction plus structured knowledge distillation. Covers direct media, YouTube, authenticated Stockbee pages through visible Chrome login, Xiaohongshu video, and public Xiaohongshu image/text posts.
---

# Distill Video

## Overview

Convert a video or public social post into structured knowledge by reconciling three independent evidence streams: frames/OCR, source subtitles, and audio transcription. Start audio-first for interview, lecture, podcast, and talking-head videos; add dense frame/OCR extraction when visuals contain unique instructional content. Preserve raw evidence, then create a separate reorganized and denoised artifact. For Xiaohongshu image/text posts, preserve the caption, every downloaded image, image OCR, and the distinction between those evidence layers.

## Improved User Goal Prompt

Before running, normalize the user's request to this goal:

```text
Distill this video into high-signal, reusable knowledge.
Auto-detect whether the video is audio-first or visual-rich.
If it is an interview, lecture, podcast, or talking-head video, prioritize audio transcription and speaker logic; only sample frames to confirm there is no important visual-only content.
Extract the thesis, framework, steps, examples, caveats, prompt templates, decision rules, and timestamped evidence.
Return a clear structured artifact and, when useful, a reusable skill/checklist that can be applied to new situations.
Do not omit details that materially affect the framework.
```

## Workflow

1. **Get media**
   - Create a stable artifact folder first, such as `artifacts/<platform-or-domain>_<short-id>`, so every retry preserves page HTML, media candidates, downloaded video, transcript, and notes.
   - Run `scripts/video_mvp.py` as the first pass for direct video files and pages with visible mp4/m3u8 URLs.
   - If the first pass fails, classify the failure before asking the user:
     - Network/DNS/sandbox error: retry with available network permissions or a browser-backed path. Do not treat this as content unavailable.
     - HTTP 403/404 on a social short link: treat it as a route failure, not a final deletion signal.
     - "No mp4/m3u8 media URL found": inspect saved HTML or page state for embedded JSON before giving up.
   - Search saved HTML for `mp4`, `m3u8`, `masterUrl`, `default_screencast_stream`, `subtitles`, `noteDetailMap`, `__INITIAL_STATE__`, `title`, `desc`, and author fields. If an embedded media URL is found, rerun `video_mvp.py` with `--media-url`.
   - If the page is gated or media is loaded only after client-side rendering, use the platform-specific approved fetch path. For a page that needs the user's logged-in Chrome state, read [references/source_routes.md](references/source_routes.md) before interacting with it. Only ask the user for a downloadable media URL after the generic, embedded-JSON, platform, and approved browser paths fail.
   - Keep the original URL, final page URL if resolved, page/title/author metadata, resolved media URL, transcript, and artifacts in the working directory.

2. **Use platform fallbacks without overfitting**
   - Read [references/source_routes.md](references/source_routes.md) for YouTube, Xiaohongshu video, public Xiaohongshu image/text posts, and Stockbee login routing.
   - For Xiaohongshu/Rednote URLs (`xhslink.com`, `xiaohongshu.com`, `xhscdn.com`), do not conclude from bare `curl`/urllib 404 alone. Public short links can be browser-resolvable while direct HTTP looks dead.
   - Try the normal `video_mvp.py` path first for video; Xiaohongshu SSR pages often include `noteDetailMap` and a usable `masterUrl`.
   - For a public Xiaohongshu image/text post, use the anonymous share-detail path first and download all images. Do not require login unless the public page itself returns a login or risk-control gate.
   - For other platforms, use the same pattern: direct helper first, embedded JSON/media URL second, `yt-dlp` or an approved platform fetcher third, approved browser session fourth, user handoff last.

3. **Classify video type**
   - Audio-first: interview, lecture, podcast, talking head, narrated essay, panel discussion, static B-roll.
   - Visual-rich: screen recording, slides, whiteboard, code walkthrough, physical demo, charts, UI workflow, product review where visuals change the meaning.
   - For audio-first videos, do not over-invest in OCR. Generate a contact sheet or a few sampled frames only to verify that visuals are not carrying missing steps.
   - For slide/PPT videos, produce a per-slide artifact set rather than only a contact sheet. Use `scripts/slide_ocr_benchmark.py` to extract dense OCR-enhanced frames, crop the projected slide area, group near-duplicate frames, and write slide crops plus OCR markdown.
   - Public image/text post: preserve post metadata and caption, download every image, OCR images only when they carry independent text, and label caption-derived versus image-derived claims.

4. **Build synchronized visual and subtitle evidence**
   - Preserve source subtitle/caption files when available. Do not assume auto-captions are more accurate than audio ASR.
   - For ordinary video, sample frames densely enough to catch scene, text, UI, or subtitle changes. For requests that require frame-level evidence, use `--ocr-all-frames` with an appropriate FPS and OCR crop; this means every sampled frame, not necessarily every encoded frame.
   - For burned-in subtitles, crop the subtitle band and OCR it with the correct Tesseract languages. Deduplicate consecutive repeats but retain timestamps.
   - For slides, diagrams, or screen recordings, retain representative full frames as the visual source of truth.
   - Read [references/multimodal_reconciliation.md](references/multimodal_reconciliation.md) before producing a combined transcript or claim timeline.

5. **Transcribe and clean**
   - Extract and preserve mono 16 kHz raw audio with `ffmpeg`.
   - If background noise materially harms recognition, use `--denoise-audio` to create a separate speech-focused WAV. Never overwrite raw audio, and compare a sample of raw versus denoised ASR because filtering can remove quiet speech.
   - Transcribe with `faster-whisper`; default to language auto-detection unless the language is known.
   - Correct obvious ASR errors by context, but record uncertainty when a term is ambiguous.
   - Preserve timestamp evidence for the main claims and framework steps.
   - Keep the raw timestamped ASR as an immutable evidence layer. Write reorganized/denoised prose separately: remove filler, duplicated sentences, false starts, sponsor/ad noise, and obvious ASR fragments while preserving claims, examples, caveats, numbers, and speaker intent.

6. **Reconcile, reorganize, and distill**
   - Align frames/OCR, source subtitles, and audio ASR by timestamp.
   - Resolve obvious proper-name and terminology errors using visible text or stronger source evidence. If sources conflict and the answer is not clear, preserve the disagreement rather than guessing.
   - Reorganize by argument or procedure instead of transcript order when that improves clarity, but attach timestamps back to each material claim.
   - Identify the central thesis.
   - Extract the named or implied framework in order.
   - Capture exact prompts, formulas, steps, and examples.
   - Separate actionable advice from commentary.
   - Note caveats, prerequisites, and failure modes.
   - Convert the framework into a reusable skill/checklist when the content is procedural.

7. **Output structure**
   - `Source`: URL/title/author if available, duration, extraction method.
   - `Video Type`: audio-first or visual-rich, with reason.
   - `Executive Summary`: 3-6 bullets.
   - `Framework`: ordered steps with what/why/how.
   - `Reusable Prompts or Templates`: copy-ready text.
   - `Examples and Details`: details that should not be lost.
   - `Caveats`: where the advice fails or needs context.
   - `Timestamp Evidence`: key timestamps.
   - `Reusable Skill`: a compact operational version when applicable.

## Source acceptance criteria

A platform route is only considered successful when the requested source is saved and inspectable:

- Video: a playable local media file or a verified browser-exported video asset, plus audio/transcript when spoken content matters.
- YouTube: resolved metadata from `yt-dlp` and either captions/transcript or downloaded media.
- Stockbee: the intended page is visibly authenticated in Chrome and the page exposes or exports the expected video asset. A login-page redirect is not success.
- Xiaohongshu video: resolved note metadata and a playable media file; a short-link redirect alone is not success.
- Xiaohongshu image/text post: structured note text plus all public images saved locally; OCR is an additional evidence layer, not a substitute for the original images.
- Multimodal video: raw audio, raw timestamped ASR, available source subtitles, sampled frames or frame OCR, and a separate reconciled/denoised narrative. Do not overwrite one evidence layer with another.

## Script

Run from a working directory. Replace `<skill-dir>` with this skill folder, for example `skills/video/distill-video` inside this repository:

```bash
python3 <skill-dir>/scripts/video_mvp.py \
  "<video-url>" \
  --out-dir artifacts/video_distill_run \
  --model small \
  --language auto
```

For noisy speech, preserve raw audio and transcribe a filtered copy:

```bash
python3 <skill-dir>/scripts/video_mvp.py \
  "<video-url>" \
  --out-dir artifacts/video_distill_run \
  --model small \
  --language auto \
  --denoise-audio
```

To validate a route without downloading or transcribing:

```bash
python3 <skill-dir>/scripts/video_mvp.py \
  "<video-url>" \
  --out-dir artifacts/video_probe \
  --probe-only
```

YouTube and other extractor-supported sites automatically fall back to `yt-dlp`. If `yt-dlp` is not installed, the helper uses `uvx --from yt-dlp yt-dlp` when `uvx` is available.

If a direct media URL is already known:

```bash
python3 <skill-dir>/scripts/video_mvp.py \
  "<source-page-url>" \
  --media-url "<direct-mp4-or-m3u8-url>" \
  --out-dir artifacts/video_distill_run \
  --model small \
  --language auto
```

If the spoken language is known, pass a language code such as `--language en` or `--language zh`.

For presentation videos where the slide text matters, run the slide benchmark after downloading the video:

```bash
python3 <skill-dir>/scripts/slide_ocr_benchmark.py \
  artifacts/video_distill_run/video.mp4 \
  --out-dir artifacts/video_distill_run/slide_pages \
  --fps 1 \
  --change-threshold 8
```

For timestamped OCR on every sampled frame, including burned-in subtitles, set a suitable crop and language pack:

```bash
python3 <skill-dir>/scripts/slide_ocr_benchmark.py \
  artifacts/video_distill_run/video.mp4 \
  --out-dir artifacts/video_distill_run/frame_timeline \
  --fps 2 \
  --ocr-crop "<subtitle-or-full-frame-crop>" \
  --group-crop "<content-change-crop>" \
  --ocr-languages eng+chi_sim \
  --ocr-all-frames
```

If the first pass contains non-slide stage/camera frames or repeated animation states, inspect `slides_contact.jpg`, then rerun with explicit curation:

```bash
python3 <skill-dir>/scripts/slide_ocr_benchmark.py \
  artifacts/video_distill_run/video.mp4 \
  --out-dir artifacts/video_distill_run/slide_pages_visible \
  --fps 1 \
  --change-threshold 8 \
  --keep-group-range 65:106 \
  --drop-output-indexes 4,10,17,18
```

Notes:
- Keep generated frame/crop files under the repo artifact directory before OCR; local Tesseract may fail to read images from `/tmp` on some macOS setups.
- Treat OCR as an index and quote source. The slide crop images are the source of truth when OCR text is garbled.
- Record visible page ranges when the video starts mid-deck or cuts away before some pages are shown.
- Stop platform exploration once you have a valid media file and transcript unless the user's question depends on page text, author metadata, comments, or linked resources.

## Common Mistakes

- Do not summarize before transcription is checked.
- Do not collapse raw ASR, source subtitles, and OCR into one silent rewrite. Preserve each source, then produce a separately labeled reconciled version.
- Do not remove repetition that changes emphasis, exceptions, numbers, or decision rules during semantic denoising.
- Do not treat a social short-link 404, DNS failure, QR-code lookup failure, or missing mp4 regex hit as final. These are signals to switch extraction routes.
- Do not inspect Chrome cookies, saved-password stores, profiles, or local storage. Use only visible browser state and visible autofill UI. Stop after the first rejected credential or unexpected authentication error; hand MFA and CAPTCHA to the user.
- Do not force a transcription language unless the spoken language is known; short-video titles and page language can differ from the actual audio.
- Do not force visual extraction for interview-style videos.
- Do not rely on sparse frame samples for slide decks; dense sampling plus visual grouping is needed to avoid missing short-lived pages.
- Do not treat a transcript as perfect; fix obvious ASR errors like names, product terms, and framework labels.
- Do not return only a narrative summary when the user asks for a skill; produce an operational artifact.
- Do not omit timestamp evidence for the main framework steps.
- Do not let optional comment loading block the core task after media and transcript are already recovered.
