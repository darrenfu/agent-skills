---
name: video-use
description: Edit video files by trimming, selecting takes, grading, adding subtitles, or composing animations and montages. Use when the user requests a video edit; select tools and verification according to the footage and requested result.
---

# Video Use

Edit footage to the requested duration, content, style, and delivery format. Preserve source media. Use the simplest pipeline that can deliver and verify the actual edit.

## Choose the workflow

- **Known trim, crop, resize, or format conversion:** inspect the relevant source with `ffprobe`, apply the requested operation with an appropriate media tool, then verify the output. No transcript, animation engine, strategy approval, or provider API key is needed unless the task itself needs one.
- **Speech editing or take selection:** inspect audio and visuals, use available accurate transcripts, and obtain word alignment only when cuts require it. Preserve requested source layers and speech meaning. Phrase subtitles can be adequate for reading; they do not establish precise word boundaries.
- **Montage, music, or visual editing:** reason from shots, motion, music, and the user's brief. Speech-first editing is not a universal workflow.
- **Animation or substantial narrative work:** plan enough to keep the sequence coherent, then implement within the user's authorization. Use [editing-techniques.md](references/editing-techniques.md) for optional craft examples.

Use decisions and authorization already established in the conversation. A request to perform an edit authorizes its reversible local execution. Do not require a second strategy, palette, preview, or final-render approval for unchanged scope. Ask only for a missing material choice, or before an action outside that scope. A request for a plan or preview alone does not authorize publication.

## Workspace and setup

Use the user's chosen output directory; otherwise use `<videos_dir>/edit/`. Do not overwrite source media or write session outputs inside the installed skill. For a continuing project, read an existing `edit/project.md` and continue the requested work; do not ask again whether to continue. Record useful decisions for substantial projects without creating a ledger for a trivial trim.

Resolve helpers relative to this SKILL.md. Check only dependencies required by the selected workflow. See [install.md](install.md) for setup details. Install optional engines in a project-local environment when authorized and allowed by host policy.

The bundled transcription helper uses ElevenLabs Scribe and expects its JSON schema. Use it only when that provider is appropriate and configured. Never ask the user to paste an API key into chat; use the host's approved secret configuration. A missing provider key does not block a task that can use another available transcript/alignment method or needs no transcription.

Cache transcripts with source identity, provider/model, settings, and correction history. Reuse valid results; re-transcribe or realign when source, settings, accuracy, or required fidelity changes. Do not silently rewrite raw source evidence.

## Bundled helpers

| Helper | Use |
|---|---|
| `helpers/transcribe.py <video>` | Scribe transcription; inspect options for speaker count and cache behavior |
| `helpers/transcribe_batch.py <videos_dir>` | Batch transcription when several sources need it |
| `helpers/pack_transcripts.py --edit-dir <dir>` | Pack cached transcripts for take selection |
| `helpers/timeline_view.py <video> <start> <end>` | Inspect relevant frames and waveform near a decision or suspected defect |
| `helpers/render.py <edl.json> -o <out>` | Bundled EDL rendering; supports `--preview` and `--build-subtitles` |
| `helpers/grade.py <in> -o <out>` | Grade with a preset or explicit filter |

Inspect a helper's schema and options before using it with a different provider or pipeline. Helper-specific assumptions are not universal ffmpeg limitations. Use a direct command or another suitable renderer when it is simpler.

## Production checks

- Preserve intended speech and visual continuity. For speech-sensitive cuts, inspect word boundaries and allow suitable padding; do not assume a transcript timestamp is exact.
- Avoid audible discontinuities; add short fades or crossfades where appropriate rather than applying a fixed fade to every boundary regardless of material.
- Match overlay timestamps to their intended output windows. The bundled renderer uses shifted PTS; verify any alternative pipeline's equivalent behavior.
- Remap captions after edits: `output_time = source_time - segment_start + segment_output_offset`. Keep captions legible above overlays, normally compositing them last when using the bundled pipeline.
- Select codec, dimensions, frame rate, audio, and color handling for the requested delivery. Stream copy is suitable only when stream compatibility and cut precision permit it. Filtered rendering may need encoding; avoid redundant passes rather than banning combined filtergraphs.
- Routine edits run in one session. Follow current project delegation and writer rules; animation count alone does not require subagents. Tool names such as `Agent` are not assumed to exist.

## EDL example for the bundled renderer

```json
{
  "version": 1,
  "sources": {"take1": "/abs/path/take1.mp4"},
  "ranges": [
    {"source": "take1", "start": 2.0, "end": 6.5,
     "beat": "explanation", "quote": "source speech", "reason": "requested passage"}
  ],
  "grade": "none",
  "total_duration_s": 4.5
}
```

Optional `overlays` entries use `file`, `start_in_output`, and `duration`; optional `subtitles` names an output-timeline subtitle file. Read the renderer before adding settings not shown here. For Manim, read the nested [manim-video skill](skills/manim-video/SKILL.md); other engines are optional.

## Verify and deliver

Inspect the rendered output, not only source footage. For a simple trim, verify duration, streams, and both cut boundaries. For multiple cuts or overlays, inspect affected transitions, synchronization, caption placement, and representative start/middle/end segments. Recheck failed or changed portions after fixes; do not repeat unchanged expensive renders to report status.

Report the actual file, meaningful edits, checks performed, and unresolved defects. Do not claim complete playback or listening if only frames and metadata were inspected. If the user asked for a finished local edit, deliver the final render after relevant checks; sharing or publishing it externally remains a separate authorized action.
