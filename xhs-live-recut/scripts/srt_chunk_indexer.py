#!/usr/bin/env python3
"""Build a fast mechanical chapter index from an SRT transcript."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


TIME_RE = re.compile(r"(?P<h>\d{1,2}):(?P<m>\d{2}):(?P<s>\d{2})[,.](?P<ms>\d{3})")


@dataclass
class Cue:
    start: float
    end: float
    text: str


def parse_time(value: str) -> float:
    match = TIME_RE.fullmatch(value.strip())
    if not match:
        raise ValueError(f"invalid SRT time: {value}")
    parts = {key: int(val) for key, val in match.groupdict().items()}
    return parts["h"] * 3600 + parts["m"] * 60 + parts["s"] + parts["ms"] / 1000


def parse_srt(path: Path) -> list[Cue]:
    raw = path.read_text(encoding="utf-8-sig").strip()
    blocks = re.split(r"\r?\n\s*\r?\n", raw)
    cues: list[Cue] = []
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        timing_index = next((i for i, line in enumerate(lines) if "-->" in line), None)
        if timing_index is None:
            continue
        left, right = [part.strip() for part in lines[timing_index].split("-->", 1)]
        text = " ".join(lines[timing_index + 1 :]).strip()
        if text:
            cues.append(Cue(parse_time(left), parse_time(right), text))
    return cues


def clock(seconds: float) -> str:
    whole = max(0, int(seconds))
    return f"{whole // 3600:02}:{whole % 3600 // 60:02}:{whole % 60:02}"


def group_cues(cues: list[Cue], seconds: float) -> list[list[Cue]]:
    groups: list[list[Cue]] = []
    current: list[Cue] = []
    window_start = cues[0].start if cues else 0
    for cue in cues:
        if current and cue.start - window_start >= seconds:
            groups.append(current)
            current = []
            window_start = cue.start
        current.append(cue)
    if current:
        groups.append(current)
    return groups


def excerpt(group: list[Cue], max_chars: int) -> str:
    text = re.sub(r"\s+", " ", " ".join(cue.text for cue in group)).strip()
    return text if len(text) <= max_chars else text[: max_chars - 1].rstrip() + "…"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("srt", type=Path)
    parser.add_argument("--minutes", type=float, default=5.0)
    parser.add_argument("--excerpt-chars", type=int, default=180)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.minutes <= 0:
        parser.error("--minutes must be positive")
    groups = group_cues(parse_srt(args.srt), args.minutes * 60)
    lines = ["# Coarse transcript index", "", "Mechanical windows; rename them editorially.", ""]
    for index, group in enumerate(groups, 1):
        lines.extend([
            f"## {index:02}. {clock(group[0].start)}–{clock(group[-1].end)}",
            "",
            excerpt(group, args.excerpt_chars),
            "",
        ])
    output = "\n".join(lines).rstrip() + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
