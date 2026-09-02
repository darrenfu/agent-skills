#!/usr/bin/env python3
"""Extract slide crops and OCR text from presentation-style videos.

The script is intentionally dependency-light: it shells out to ffmpeg,
ImageMagick, and Tesseract because those are already common in local Codex
video workflows.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FrameInfo:
    index: int
    timestamp: float
    full_path: Path
    ocr_crop_path: Path
    group_signature: bytes
    text: str = ""


@dataclass
class SlideInfo:
    index: int
    start: float
    end: float
    representative: FrameInfo
    members: list[FrameInfo]
    slide_path: Path
    text_path: Path


def run(cmd: list[str], *, capture: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        check=True,
        text=False if capture else True,
        capture_output=capture,
    )


def require_tools() -> None:
    missing = [tool for tool in ("ffmpeg", "ffprobe", "magick", "tesseract") if not shutil.which(tool)]
    if missing:
        raise SystemExit(f"Missing required tools: {', '.join(missing)}")


def video_duration(video_path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(video_path),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    return float(result.stdout.strip())


def fmt_ts(seconds: float) -> str:
    seconds = max(0, int(round(seconds)))
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}-{m:02d}-{s:02d}"


def normalize_text(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def clean_ocr_text(text: str) -> str:
    lines: list[str] = []
    for raw in text.splitlines():
        line = re.sub(r"\s+", " ", raw).strip()
        if not line:
            continue
        if "video.mp4" in line.lower():
            continue
        lines.append(line)
    return "\n".join(lines)


def text_score(text: str) -> int:
    cleaned = clean_ocr_text(text)
    normalized = normalize_text(cleaned)
    line_bonus = min(80, len(cleaned.splitlines()) * 8)
    return len(normalized) + line_bonus


def mean_abs_diff(a: bytes, b: bytes) -> float:
    if len(a) != len(b):
        raise ValueError("Signature lengths do not match")
    if not a:
        return 0.0
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


def extract_full_frames(video_path: Path, full_dir: Path, fps: float, force: bool) -> list[Path]:
    full_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(full_dir.glob("frame_*.jpg"))
    if existing and not force:
        return existing

    if force and full_dir.exists():
        shutil.rmtree(full_dir)
        full_dir.mkdir(parents=True, exist_ok=True)

    vf = ",".join(
        [
            f"fps={fps}",
            "scale=w='min(1568,iw)':h='min(1568,ih)':force_original_aspect_ratio=decrease",
            "format=gray",
            "eq=contrast=1.3:brightness=0.05",
            "unsharp=5:5:0.7:5:5:0.0",
        ]
    )
    run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-i",
            str(video_path),
            "-vf",
            vf,
            "-q:v",
            "1",
            str(full_dir / "frame_%05d.jpg"),
        ]
    )
    return sorted(full_dir.glob("frame_*.jpg"))


def crop_frame(src: Path, dst: Path, crop: str) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    run(["magick", str(src), "-crop", crop, "+repage", str(dst)])


def signature(src: Path, crop: str) -> bytes:
    result = run(
        [
            "magick",
            str(src),
            "-crop",
            crop,
            "+repage",
            "-resize",
            "64x36!",
            "-colorspace",
            "Gray",
            "-depth",
            "8",
            "gray:-",
        ],
        capture=True,
    )
    return result.stdout


def ocr_image(path: Path, languages: str) -> str:
    attempts: list[str] = []
    for psm in ("3", "11", "6"):
        result = subprocess.run(
            ["tesseract", str(path), "stdout", "--psm", psm, "-l", languages],
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=12,
        )
        if result.returncode == 0:
            cleaned = clean_ocr_text(result.stdout)
            attempts.append(cleaned)
            if text_score(cleaned) >= 50:
                break
    if not attempts:
        return ""
    return max(attempts, key=text_score, default="")


def build_frames(
    full_frames: list[Path],
    out_dir: Path,
    fps: float,
    ocr_crop: str,
    group_crop: str,
    force: bool,
) -> list[FrameInfo]:
    crop_dir = out_dir / "work" / "ocr_crops"
    crop_dir.mkdir(parents=True, exist_ok=True)
    frames: list[FrameInfo] = []
    for pos, full_path in enumerate(full_frames, start=1):
        crop_path = crop_dir / full_path.name
        if force or not crop_path.exists():
            crop_frame(full_path, crop_path, ocr_crop)
        frames.append(
            FrameInfo(
                index=pos,
                timestamp=(pos - 1) / fps,
                full_path=full_path,
                ocr_crop_path=crop_path,
                group_signature=signature(full_path, group_crop),
            )
        )
    return frames


def group_frames(frames: list[FrameInfo], change_threshold: float, min_group_seconds: float, fps: float) -> list[list[FrameInfo]]:
    groups: list[list[FrameInfo]] = []
    current: list[FrameInfo] = []
    min_group_frames = max(1, int(round(min_group_seconds * fps)))

    previous: FrameInfo | None = None
    for frame in frames:
        if previous is not None:
            diff = mean_abs_diff(previous.group_signature, frame.group_signature)
            if diff >= change_threshold and len(current) >= min_group_frames:
                groups.append(current)
                current = []
        current.append(frame)
        previous = frame
    if current:
        groups.append(current)
    return groups


def ocr_group(group: list[FrameInfo], ocr_step: int, ocr_languages: str) -> FrameInfo:
    candidate_indexes = set(range(0, len(group), max(1, ocr_step)))
    candidate_indexes.update({0, len(group) // 2, len(group) - 1})
    best = group[0]
    best_score = -1
    for idx in sorted(candidate_indexes):
        frame = group[idx]
        if not frame.text:
            frame.text = ocr_image(frame.ocr_crop_path, ocr_languages)
        score = text_score(frame.text)
        if score > best_score:
            best = frame
            best_score = score
    return best


def write_contact_sheet(slide_paths: list[Path], target: Path) -> None:
    if not slide_paths:
        return
    cmd = [
        "montage",
        *[str(path) for path in slide_paths],
        "-thumbnail",
        "320x220",
        "-tile",
        "4x",
        "-geometry",
        "+10+34",
        "-pointsize",
        "16",
        "-label",
        "%f",
        str(target),
    ]
    run(cmd)


def write_outputs(
    groups: list[list[FrameInfo]],
    out_dir: Path,
    fps: float,
    ocr_step: int,
    args: argparse.Namespace,
) -> list[SlideInfo]:
    slides_dir = out_dir / "slides"
    text_dir = out_dir / "ocr"
    slides_dir.mkdir(parents=True, exist_ok=True)
    text_dir.mkdir(parents=True, exist_ok=True)

    slides: list[SlideInfo] = []
    for slide_index, group in enumerate(groups, start=1):
        representative = ocr_group(group, ocr_step, args.ocr_languages)
        stem = f"slide_{slide_index:03d}_{fmt_ts(representative.timestamp)}"
        slide_path = slides_dir / f"{stem}.jpg"
        text_path = text_dir / f"{stem}.txt"
        shutil.copy2(representative.ocr_crop_path, slide_path)
        text_path.write_text(representative.text.strip() + "\n", encoding="utf-8")
        slides.append(
            SlideInfo(
                index=slide_index,
                start=group[0].timestamp,
                end=group[-1].timestamp + (1.0 / fps),
                representative=representative,
                members=group,
                slide_path=slide_path,
                text_path=text_path,
            )
        )

    write_contact_sheet([slide.slide_path for slide in slides], out_dir / "slides_contact.jpg")
    write_markdown(slides, out_dir, args)
    write_manifest(slides, out_dir, args)
    return slides


def write_frame_ocr(frames: list[FrameInfo], out_dir: Path, languages: str) -> Path:
    """OCR every sampled frame and preserve a timestamped JSONL evidence stream."""
    target = out_dir / "frame_ocr.jsonl"
    with target.open("w", encoding="utf-8") as handle:
        for frame in frames:
            if not frame.text:
                frame.text = ocr_image(frame.ocr_crop_path, languages)
            handle.write(
                json.dumps(
                    {
                        "frame_index": frame.index,
                        "timestamp": round(frame.timestamp, 3),
                        "image": str(frame.full_path),
                        "ocr_crop": str(frame.ocr_crop_path),
                        "text": frame.text,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
    return target


def write_markdown(slides: list[SlideInfo], out_dir: Path, args: argparse.Namespace) -> None:
    lines = [
        "# Slide OCR Benchmark",
        "",
        f"- Source video: `{args.video}`",
        f"- FPS sampled: `{args.fps}`",
        f"- OCR crop: `{args.ocr_crop}`",
        f"- Group crop: `{args.group_crop}`",
        f"- Visual change threshold: `{args.change_threshold}`",
        f"- Kept group range: `{args.keep_group_range or 'all'}`",
        f"- Dropped output indexes: `{args.drop_output_indexes or 'none'}`",
        f"- Slides detected: `{len(slides)}`",
        "",
    ]
    for slide in slides:
        rel_img = slide.slide_path.relative_to(out_dir)
        text = slide.representative.text.strip() or "[OCR empty]"
        lines.extend(
            [
                f"## Slide {slide.index:03d}  `{fmt_ts(slide.start)}` - `{fmt_ts(slide.end)}`",
                "",
                f"Image: `{rel_img}`",
                "",
                "```text",
                text,
                "```",
                "",
            ]
        )
    (out_dir / "slides_ocr.md").write_text("\n".join(lines), encoding="utf-8")


def write_manifest(slides: list[SlideInfo], out_dir: Path, args: argparse.Namespace) -> None:
    payload = {
        "video": args.video,
        "fps": args.fps,
        "ocr_crop": args.ocr_crop,
        "group_crop": args.group_crop,
        "change_threshold": args.change_threshold,
        "ocr_step": args.ocr_step,
        "keep_group_range": args.keep_group_range,
        "drop_output_indexes": args.drop_output_indexes,
        "slides": [
            {
                "index": slide.index,
                "start": round(slide.start, 3),
                "end": round(slide.end, 3),
                "representative_frame": slide.representative.index,
                "representative_timestamp": round(slide.representative.timestamp, 3),
                "member_count": len(slide.members),
                "slide_path": str(slide.slide_path),
                "text_path": str(slide.text_path),
                "ocr_score": text_score(slide.representative.text),
            }
            for slide in slides
        ],
    }
    (out_dir / "manifest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_report(slides: list[SlideInfo], frame_count: int, duration: float, out_dir: Path, args: argparse.Namespace) -> None:
    empty = [slide for slide in slides if not slide.representative.text.strip()]
    short = [slide for slide in slides if 0 < text_score(slide.representative.text) < 25]
    lines = [
        "# Benchmark Report",
        "",
        "## Method",
        "",
        "- Extracted OCR-enhanced frames with ffmpeg at fixed FPS.",
        "- Cropped the projected slide area with ImageMagick.",
        "- Grouped consecutive frames by mean absolute difference on a subtitle-light crop.",
        "- Ran Tesseract across candidate frames in each group and selected the highest-scoring text result.",
        "",
        "## Settings",
        "",
        f"- Duration: `{duration:.2f}s`",
        f"- Frames extracted: `{frame_count}`",
        f"- Slides detected: `{len(slides)}`",
        f"- FPS: `{args.fps}`",
        f"- OCR crop: `{args.ocr_crop}`",
        f"- Group crop: `{args.group_crop}`",
        f"- Change threshold: `{args.change_threshold}`",
        f"- OCR step: `{args.ocr_step}`",
        f"- OCR languages: `{args.ocr_languages}`",
        f"- Per-frame OCR: `{args.ocr_all_frames}`",
        f"- Kept group range: `{args.keep_group_range or 'all'}`",
        f"- Dropped output indexes: `{args.drop_output_indexes or 'none'}`",
        "",
        "## Verification Targets",
        "",
        "- The contact sheet should cover each visually distinct slide without obvious missing pages or duplicate over-splitting.",
        "- OCR text should be dense enough to identify slide titles, numbered steps, prompts, tables, or diagrams that carry the teaching content.",
        "- Review `slides_contact.jpg` for missed pages or duplicate over-splitting.",
        "- Review `slides_ocr.md` for OCR-empty or short OCR slides.",
        "",
        "## OCR Risk",
        "",
        f"- Empty OCR slides: `{len(empty)}`",
        f"- Very short OCR slides: `{len(short)}`",
    ]
    if empty:
        lines.append(f"- Empty indexes: `{', '.join(str(slide.index) for slide in empty)}`")
    if short:
        lines.append(f"- Short indexes: `{', '.join(str(slide.index) for slide in short)}`")
    (out_dir / "benchmark_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def keep_group_range(groups: list[list[FrameInfo]], value: str | None) -> list[list[FrameInfo]]:
    if not value:
        return groups
    match = re.fullmatch(r"(\d+):(\d+)", value.strip())
    if not match:
        raise SystemExit("--keep-group-range must use 1-based inclusive form like 60:99")
    start, end = (int(match.group(1)), int(match.group(2)))
    if start < 1 or end < start:
        raise SystemExit("--keep-group-range must have 1 <= start <= end")
    return groups[start - 1 : end]


def drop_output_indexes(groups: list[list[FrameInfo]], value: str | None) -> list[list[FrameInfo]]:
    if not value:
        return groups
    try:
        drops = {int(part.strip()) for part in value.split(",") if part.strip()}
    except ValueError as exc:
        raise SystemExit("--drop-output-indexes must be a comma-separated list such as 4,10,17") from exc
    if any(index < 1 for index in drops):
        raise SystemExit("--drop-output-indexes values must be 1-based positive integers")
    return [group for index, group in enumerate(groups, start=1) if index not in drops]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build slide crops and OCR from a presentation video.")
    parser.add_argument("video", help="Path to the video file")
    parser.add_argument("--out-dir", default="artifacts/slide_ocr_benchmark")
    parser.add_argument("--fps", type=float, default=1.0)
    parser.add_argument("--ocr-crop", default="980x600+300+35")
    parser.add_argument("--group-crop", default="980x500+300+35")
    parser.add_argument("--change-threshold", type=float, default=9.0)
    parser.add_argument("--min-group-seconds", type=float, default=1.0)
    parser.add_argument("--ocr-step", type=int, default=5, help="OCR every Nth frame inside each visual group.")
    parser.add_argument(
        "--ocr-languages",
        default="eng",
        help="Tesseract language expression, for example eng, chi_sim, or eng+chi_sim.",
    )
    parser.add_argument(
        "--ocr-all-frames",
        action="store_true",
        help="OCR every sampled frame and write frame_ocr.jsonl with timestamps.",
    )
    parser.add_argument(
        "--keep-group-range",
        help="Keep only a 1-based inclusive range of visual groups after detection, e.g. 60:99.",
    )
    parser.add_argument(
        "--drop-output-indexes",
        help="Drop 1-based indexes after --keep-group-range filtering, e.g. 4,10,17,18.",
    )
    parser.add_argument("--force", action="store_true", help="Regenerate extracted frames and crops.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    require_tools()

    video_path = Path(args.video)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    duration = video_duration(video_path)
    full_dir = out_dir / "work" / "full_frames"
    full_frames = extract_full_frames(video_path, full_dir, args.fps, args.force)
    frames = build_frames(full_frames, out_dir, args.fps, args.ocr_crop, args.group_crop, args.force)
    frame_ocr_path = None
    if args.ocr_all_frames:
        frame_ocr_path = write_frame_ocr(frames, out_dir, args.ocr_languages)
    groups = group_frames(frames, args.change_threshold, args.min_group_seconds, args.fps)
    groups = keep_group_range(groups, args.keep_group_range)
    groups = drop_output_indexes(groups, args.drop_output_indexes)
    slides = write_outputs(groups, out_dir, args.fps, args.ocr_step, args)
    write_report(slides, len(full_frames), duration, out_dir, args)

    print(
        json.dumps(
            {
                "out_dir": str(out_dir),
                "frames": len(full_frames),
                "slides": len(slides),
                "slides_ocr": str(out_dir / "slides_ocr.md"),
                "contact_sheet": str(out_dir / "slides_contact.jpg"),
                "report": str(out_dir / "benchmark_report.md"),
                "frame_ocr": str(frame_ocr_path) if frame_ocr_path else None,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
