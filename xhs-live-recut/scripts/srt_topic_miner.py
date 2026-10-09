#!/usr/bin/env python3
"""Roughly mine Chinese livestream SRT files for remake candidate windows.

This is an editorial helper, not an automatic final selector.
It groups subtitle cues into time windows and scores them with simple heuristics.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


KEYWORDS = [
    "ai",
    "AI",
    "课堂",
    "学生",
    "老师",
    "教师",
    "互动",
    "网页",
    "提示词",
    "学情",
    "分析",
    "数据",
    "收集",
    "表单",
    "QuickForm",
    "deepseek",
    "DeepSeek",
    "案例",
    "演示",
    "生成",
    "反馈",
    "正确率",
    "易错",
    "建议",
]

HOOK_MARKERS = [
    "不是",
    "其实",
    "关键",
    "问题",
    "一定要",
    "不要",
    "为什么",
    "怎么",
    "最",
    "核心",
    "第一步",
    "注意",
]


@dataclass
class Cue:
    start: float
    end: float
    text: str


def parse_time(value: str) -> float:
    match = re.match(r"(\d+):(\d+):(\d+),(\d+)", value.strip())
    if not match:
        raise ValueError(f"Bad SRT timestamp: {value}")
    hh, mm, ss, ms = map(int, match.groups())
    return hh * 3600 + mm * 60 + ss + ms / 1000


def fmt_time(seconds: float) -> str:
    seconds = max(0, int(round(seconds)))
    hh = seconds // 3600
    mm = (seconds % 3600) // 60
    ss = seconds % 60
    return f"{hh:02d}:{mm:02d}:{ss:02d}"


def clean_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def read_srt(path: Path) -> list[Cue]:
    content = path.read_text(encoding="utf-8-sig", errors="ignore")
    blocks = re.split(r"\n\s*\n", content.strip())
    cues: list[Cue] = []
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if len(lines) < 2:
            continue
        timing_index = next((i for i, line in enumerate(lines) if "-->" in line), -1)
        if timing_index < 0:
            continue
        start_raw, end_raw = [part.strip() for part in lines[timing_index].split("-->", 1)]
        text = clean_text(" ".join(lines[timing_index + 1 :]))
        if text:
            cues.append(Cue(parse_time(start_raw), parse_time(end_raw), text))
    return cues


def score_text(text: str) -> int:
    score = 0
    for keyword in KEYWORDS:
        if keyword in text:
            score += 2
    for marker in HOOK_MARKERS:
        if marker in text:
            score += 1
    if "？" in text or "?" in text:
        score += 2
    if 60 <= len(text) <= 260:
        score += 2
    if len(text) > 420:
        score -= 2
    return score


def build_windows(cues: list[Cue], window_seconds: int, step_seconds: int) -> list[dict]:
    if not cues:
        return []
    start = cues[0].start
    end = cues[-1].end
    rows = []
    cursor = start
    while cursor < end:
        win_end = cursor + window_seconds
        selected = [cue for cue in cues if cue.start < win_end and cue.end >= cursor]
        text = clean_text(" ".join(cue.text for cue in selected))
        if text:
            rows.append(
                {
                    "start": fmt_time(cursor),
                    "end": fmt_time(win_end),
                    "score": score_text(text),
                    "text_preview": text[:240],
                }
            )
        cursor += step_seconds
    rows.sort(key=lambda row: row["score"], reverse=True)
    return rows


def suppress_overlaps(rows: list[dict], max_overlap: float) -> list[dict]:
    selected: list[dict] = []
    for row in rows:
        row_start = parse_time(row["start"] + ",000")
        row_end = parse_time(row["end"] + ",000")
        row_duration = max(1.0, row_end - row_start)
        overlaps_too_much = False
        for kept in selected:
            kept_start = parse_time(kept["start"] + ",000")
            kept_end = parse_time(kept["end"] + ",000")
            intersection = max(0.0, min(row_end, kept_end) - max(row_start, kept_start))
            if intersection / row_duration > max_overlap:
                overlaps_too_much = True
                break
        if not overlaps_too_much:
            selected.append(row)
    return selected


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Mine SRT candidate windows for XHS livestream recuts.")
    parser.add_argument("srt", type=Path)
    parser.add_argument("--window", type=int, default=120, help="Window length in seconds")
    parser.add_argument("--step", type=int, default=60, help="Step size in seconds")
    parser.add_argument("--top", type=int, default=20, help="Number of rows to output")
    parser.add_argument(
        "--max-overlap",
        type=float,
        default=0.5,
        help="Suppress lower-scoring windows whose overlap ratio exceeds this value",
    )
    parser.add_argument("--format", choices=["json", "csv"], default="json")
    args = parser.parse_args()

    cues = read_srt(args.srt)
    rows = suppress_overlaps(
        build_windows(cues, args.window, args.step), args.max_overlap
    )[: args.top]

    if args.format == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=["start", "end", "score", "text_preview"])
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
