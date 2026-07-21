#!/usr/bin/env python3
"""Convert UTF-8 SRT with inline ASS color tags into native ASS."""

import argparse
import re
from pathlib import Path


def ass_time(value: str) -> str:
    h, m, rest = value.replace(",", ".").split(":")
    sec, ms = rest.split(".")
    return f"{int(h)}:{int(m):02d}:{int(sec):02d}.{int(ms[:2]):02d}"


def convert(src: Path, dst: Path, font: str, size: int, outline: int, margin_v: int) -> None:
    srt = src.read_text(encoding="utf-8")
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font},{size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,{outline},0,2,45,45,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for block in re.split(r"\r?\n\r?\n", srt.strip()):
        lines = block.splitlines()
        if len(lines) < 3 or " --> " not in lines[1]:
            continue
        start, end = lines[1].split(" --> ")
        text = r"\N".join(lines[2:])
        events.append(f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Default,,0,0,0,,{text}")
    dst.write_text(header + "\n".join(events) + "\n", encoding="utf-8")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("input", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--font", default="Microsoft YaHei")
    p.add_argument("--size", type=int, default=80)
    p.add_argument("--outline", type=int, default=7)
    p.add_argument("--margin-v", type=int, default=500)
    a = p.parse_args()
    convert(a.input, a.output, a.font, a.size, a.outline, a.margin_v)


if __name__ == "__main__":
    main()
