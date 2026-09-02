#!/usr/bin/env python3
"""Minimal video distillation helper.

This script does the mechanical part of the MVP stack:
1. Fetch a video page or accept a direct media URL.
2. Extract/download the first mp4/m3u8 media candidate.
3. Extract audio with ffmpeg.
4. Transcribe with faster-whisper when available.
5. Emit a distillation prompt for a downstream LLM/Codex pass.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.request import Request, urlopen


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
)


def fetch_text(url: str) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def extract_media_urls(html: str) -> list[str]:
    pattern = re.compile(r"https?://[^\"'\\<> ]+\.(?:mp4|m3u8)[^\"'\\<> ]*")
    seen: set[str] = set()
    urls: list[str] = []
    for raw in pattern.findall(html):
        url = raw.replace("\\u002F", "/").replace("&amp;", "&")
        if url not in seen:
            seen.add(url)
            urls.append(url)
    return urls


def download(url: str, target: Path, referer: str | None = None) -> None:
    headers = {"User-Agent": USER_AGENT}
    if referer:
        headers["Referer"] = referer
    req = Request(url, headers=headers)
    with urlopen(req, timeout=60) as resp, target.open("wb") as f:
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def ytdlp_command() -> list[str] | None:
    """Return an available yt-dlp command without installing globally."""
    if shutil.which("yt-dlp"):
        return ["yt-dlp"]
    if shutil.which("uvx"):
        return ["uvx", "--from", "yt-dlp", "yt-dlp"]
    return None


def probe_with_ytdlp(url: str) -> dict:
    command = ytdlp_command()
    if command is None:
        raise SystemExit("yt-dlp is unavailable. Install yt-dlp or uv/uvx, then retry.")
    try:
        result = subprocess.run(
            [*command, "--no-playlist", "--simulate", "--dump-single-json", url],
            check=True,
            text=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as exc:
        detail_lines = [line.strip() for line in (exc.stderr or "").splitlines() if line.strip()]
        detail = detail_lines[-1] if detail_lines else "no extractor details"
        raise SystemExit(
            "yt-dlp could not resolve this source. If the page requires login, use the approved "
            f"browser session and export its visible media asset. Extractor detail: {detail}"
        ) from exc
    return json.loads(result.stdout)


def download_with_ytdlp(url: str, out_dir: Path, subtitle_languages: str) -> tuple[Path, dict, list[Path]]:
    command = ytdlp_command()
    if command is None:
        raise SystemExit("yt-dlp is unavailable. Install yt-dlp or uv/uvx, then retry.")
    metadata = probe_with_ytdlp(url)
    output_template = str(out_dir / "video.%(ext)s")
    try:
        result = subprocess.run(
            [
                *command,
                "--no-playlist",
                "--merge-output-format",
                "mp4",
                "--output",
                output_template,
                "--print",
                "after_move:filepath",
                url,
            ],
            check=True,
            text=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as exc:
        detail_lines = [line.strip() for line in (exc.stderr or "").splitlines() if line.strip()]
        detail = detail_lines[-1] if detail_lines else "no extractor details"
        raise SystemExit(f"yt-dlp could not download the media. Extractor detail: {detail}") from exc
    output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if not output_lines:
        raise SystemExit("yt-dlp completed without reporting a downloaded media path.")
    media_path = Path(output_lines[-1]).expanduser().resolve()
    if not media_path.is_file():
        raise SystemExit(f"yt-dlp reported a missing media file: {media_path}")
    subtitle_result = subprocess.run(
        [
            *command,
            "--no-playlist",
            "--skip-download",
            "--write-subs",
            "--write-auto-subs",
            "--sub-langs",
            subtitle_languages,
            "--output",
            output_template,
            url,
        ],
        check=False,
        text=True,
        capture_output=True,
    )
    if subtitle_result.returncode != 0:
        detail_lines = [line.strip() for line in subtitle_result.stderr.splitlines() if line.strip()]
        metadata["subtitle_download_error"] = detail_lines[-1] if detail_lines else "unknown subtitle error"
    subtitle_paths = sorted(
        path
        for path in out_dir.glob("video.*")
        if path.suffix.lower() in {".vtt", ".srt", ".ass", ".ttml"}
    )
    return media_path, metadata, subtitle_paths


def normalize_language(language: str | None) -> str | None:
    if language is None or language.lower() in {"auto", "detect"}:
        return None
    return language


def transcribe(audio_path: Path, out_json: Path, out_txt: Path, model_name: str, language: str | None = None) -> None:
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise SystemExit("Install faster-whisper to transcribe: pip install faster-whisper") from exc

    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segments, info = model.transcribe(str(audio_path), language=language, vad_filter=True, beam_size=5)
    rows = [
        {"start": round(seg.start, 2), "end": round(seg.end, 2), "text": seg.text.strip()}
        for seg in segments
    ]
    out_json.write_text(
        json.dumps({"language": info.language, "duration": info.duration, "segments": rows}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    out_txt.write_text(
        "\n".join(f"[{row['start']:06.2f}-{row['end']:06.2f}] {row['text']}" for row in rows),
        encoding="utf-8",
    )


def write_prompt(out_path: Path, transcript_path: Path) -> None:
    out_path.write_text(
        "\n".join(
            [
                "# Distillation Prompt",
                "",
                "Use the transcript and sampled frames to produce a reusable skill/knowledge artifact.",
                "",
                "Requirements:",
                "- Do not omit details mentioned in the video.",
                "- Correct obvious ASR errors by context, but keep timestamp evidence.",
                "- Extract: purpose, prerequisites, steps, prompts, checkpoints, outputs, failure modes.",
                "- Preserve the original framework order.",
                "- Cross-check audio ASR against source subtitles and timestamped frame/OCR evidence.",
                "- Preserve the raw transcript; write reorganized/denoised prose as a separate artifact.",
                "- Remove filler, repetition, false starts, and transcription noise without deleting caveats or changing claims.",
                "- Mark unresolved conflicts between audio, subtitles, and visible text instead of guessing.",
                "- Produce a concise but operational skill that someone can apply to a new topic.",
                "",
                f"Transcript: `{transcript_path}`",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Video page URL or direct video URL")
    parser.add_argument("--media-url", help="Direct mp4/m3u8 URL override")
    parser.add_argument("--out-dir", default="artifacts/mvp_run")
    parser.add_argument("--model", default="small")
    parser.add_argument(
        "--probe-only",
        action="store_true",
        help="Resolve the source and print JSON metadata without downloading or transcribing.",
    )
    parser.add_argument(
        "--download-only",
        action="store_true",
        help="Download the media but skip audio extraction and transcription.",
    )
    parser.add_argument(
        "--subtitle-languages",
        default="en,zh-Hans,zh-Hant,zh-CN,zh-TW",
        help="yt-dlp subtitle selector. Defaults to common English and Chinese tracks; use all,-live_chat for every track.",
    )
    parser.add_argument(
        "--denoise-audio",
        action="store_true",
        help="Create a speech-focused denoised WAV before transcription while preserving the raw WAV.",
    )
    parser.add_argument(
        "--language",
        default="auto",
        help="Transcription language code such as en or zh. Use auto/detect to let Whisper detect it.",
    )
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    media_url = args.media_url
    media_path: Path | None = None
    extraction_method = "direct-media-url"
    metadata: dict = {}

    if not media_url:
        try:
            html = fetch_text(args.url)
        except Exception as fetch_error:
            html = ""
            metadata["html_fetch_error"] = f"{type(fetch_error).__name__}: {fetch_error}"
        if html:
            (out_dir / "page.html").write_text(html, encoding="utf-8")
            candidates = extract_media_urls(html)
            (out_dir / "media_candidates.json").write_text(
                json.dumps(candidates, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            if candidates:
                media_url = candidates[0]
                extraction_method = "embedded-html-media"

        if media_url is None:
            metadata.update(probe_with_ytdlp(args.url))
            extraction_method = "yt-dlp"

    if args.probe_only:
        print(
            json.dumps(
                {
                    "source_url": args.url,
                    "extraction_method": extraction_method,
                    "media_url": media_url,
                    "title": metadata.get("title"),
                    "uploader": metadata.get("uploader"),
                    "duration": metadata.get("duration"),
                    "id": metadata.get("id"),
                },
                ensure_ascii=False,
            )
        )
        return 0

    if extraction_method == "yt-dlp":
        media_path, metadata, subtitle_paths = download_with_ytdlp(
            args.url, out_dir, args.subtitle_languages
        )
    else:
        media_path = out_dir / "video.mp4"
        subtitle_paths = []
        assert media_url is not None
        download(media_url, media_path, args.url)

    (out_dir / "source.json").write_text(
        json.dumps(
            {
                "source_url": args.url,
                "extraction_method": extraction_method,
                "media_url": media_url,
                "subtitle_paths": [str(path) for path in subtitle_paths],
                "metadata": metadata,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    if args.download_only:
        print(
            json.dumps(
                {
                    "source_url": args.url,
                    "extraction_method": extraction_method,
                    "video": str(media_path),
                },
                ensure_ascii=False,
            )
        )
        return 0

    raw_wav_path = out_dir / "audio_raw.wav"
    run(["ffmpeg", "-y", "-i", str(media_path), "-vn", "-ac", "1", "-ar", "16000", str(raw_wav_path)])
    wav_path = raw_wav_path
    if args.denoise_audio:
        wav_path = out_dir / "audio_denoised.wav"
        run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(raw_wav_path),
                "-af",
                "highpass=f=80,lowpass=f=12000,afftdn=nf=-25,dynaudnorm=f=150:g=15",
                str(wav_path),
            ]
        )

    transcript_json = out_dir / "transcript.json"
    transcript_txt = out_dir / "transcript.txt"
    transcribe(wav_path, transcript_json, transcript_txt, args.model, normalize_language(args.language))
    write_prompt(out_dir / "distillation_prompt.md", transcript_txt)

    print(
        json.dumps(
            {
                "source_url": args.url,
                "extraction_method": extraction_method,
                "media_url": media_url,
                "video": str(media_path),
                "audio_raw": str(raw_wav_path),
                "audio_used_for_asr": str(wav_path),
                "subtitle_paths": [str(path) for path in subtitle_paths],
                "transcript": str(transcript_txt),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
