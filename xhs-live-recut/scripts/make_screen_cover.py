#!/usr/bin/env python3
"""Build source-faithful 16:9 covers for screen-recorded lessons.

Usage: python make_screen_cover.py manifest.json [--overwrite]
The manifest contains a ``covers`` array. Each item needs ``source``, ``output``,
``number``, and exactly two ``title_lines``. Optional ``crop`` and ``redact``
rectangles use [left, top, right, bottom] in original-frame pixels.
"""

import argparse
import io
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


W, H = 1920, 1080
FONT_PATH = Path(r"C:\Windows\Fonts\msyhbd.ttc")
BG = "#F5F1E9"
INK = "#202321"
MUTED = "#686B65"
DEFAULT_ACCENT = "#8F282B"
RESAMPLE = Image.Resampling.LANCZOS


def resolve(base: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else base / path


def load_frame(path: Path, at: float) -> Image.Image:
    if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".bmp"}:
        return Image.open(path).convert("RGB")
    command = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", str(at),
        "-i", str(path), "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-",
    ]
    result = subprocess.run(command, capture_output=True, check=True)
    return Image.open(io.BytesIO(result.stdout)).convert("RGB")


def checked_rect(value, size, label: str):
    if not isinstance(value, list) or len(value) != 4:
        raise ValueError(f"{label} must be [left, top, right, bottom]")
    rect = tuple(int(n) for n in value)
    l, t, r, b = rect
    if not (0 <= l < r <= size[0] and 0 <= t < b <= size[1]):
        raise ValueError(f"{label} {rect} is outside source frame {size}")
    return rect


def fit_font(draw: ImageDraw.ImageDraw, text: str, max_width: int, start: int,
             min_size: int, font_path: Path) -> ImageFont.FreeTypeFont:
    for size in range(start, min_size - 1, -2):
        font = ImageFont.truetype(str(font_path), size)
        if draw.textbbox((0, 0), text, font=font)[2] <= max_width:
            return font
    raise ValueError(f"Title is too long for the cover: {text!r}")


def build_cover(item: dict, base: Path, font_path: Path, overwrite: bool) -> Path:
    source = resolve(base, item["source"])
    output = resolve(base, item["output"])
    if not source.is_file():
        raise FileNotFoundError(source)
    if output.exists() and not overwrite:
        raise FileExistsError(f"Refusing to overwrite {output}; pass --overwrite")
    title = item["title_lines"]
    if not isinstance(title, list) or len(title) != 2 or not all(title):
        raise ValueError("title_lines must contain exactly two nonempty lines")
    frame = load_frame(source, float(item.get("at", 0)))
    if item.get("crop") is None:
        raise ValueError("Set an explicit source-pixel crop; do not publish raw screen chrome")
    crop = checked_rect(item["crop"], frame.size, "crop")

    # Opaque masks are applied before scaling, so sensitive pixels cannot leak.
    frame_draw = ImageDraw.Draw(frame)
    for index, raw in enumerate(item.get("redact", [])):
        rect = checked_rect(raw, frame.size, f"redact[{index}]")
        frame_draw.rectangle(rect, fill="#E8E8E6")
    frame = frame.crop(crop)

    accent = item.get("accent", DEFAULT_ACCENT)
    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 20, H), fill=accent)
    draw.rounded_rectangle((112, 118, 366, 178), radius=30, fill=accent)
    small = ImageFont.truetype(str(font_path), 29)
    badge = str(item.get("badge", "录播教学 · 精剪"))
    if draw.textbbox((0, 0), badge, font=small)[2] > 210:
        raise ValueError(f"badge is too long: {badge!r}")
    draw.text((143, 128), badge, font=small, fill="white")

    number = str(item["number"])
    number_font = ImageFont.truetype(str(font_path), 58)
    draw.text((114, 235), number, font=number_font, fill=accent)
    draw.line((114, 325, 238, 325), fill=accent, width=7)

    x = 112
    max_title_width = 690
    line_1 = fit_font(draw, title[0], max_title_width, 94, 60, font_path)
    line_2 = fit_font(draw, title[1], max_title_width, 102, 60, font_path)
    draw.text((x, 394), title[0], font=line_1, fill=INK, stroke_width=0)
    draw.text((x, 542), title[1], font=line_2, fill=accent, stroke_width=0)

    detail = str(item.get("detail", "原画面 · 原声讲解"))
    detail_font = ImageFont.truetype(str(font_path), 35)
    if draw.textbbox((0, 0), detail, font=detail_font)[2] > max_title_width:
        raise ValueError(f"detail is too long: {detail!r}")
    draw.text((x, 746), detail, font=detail_font, fill=MUTED)
    draw.line((112, 852, 742, 852), fill="#D3CDC3", width=2)
    footer_font = ImageFont.truetype(str(font_path), 27)
    draw.text((112, 885), str(item.get("footer", "录播教学 / 原声讲解")),
              font=footer_font, fill=MUTED)

    panel = (843, 172, 1848, 889)
    draw.rounded_rectangle((panel[0] + 14, panel[1] + 20,
                            panel[2] + 14, panel[3] + 20),
                           radius=24, fill="#DDD6CB")
    draw.rounded_rectangle(panel, radius=24, fill="white", outline="#DED8CE", width=3)
    inset = (panel[0] + 20, panel[1] + 20, panel[2] - 20, panel[3] - 20)
    target_size = (inset[2] - inset[0], inset[3] - inset[1])
    visual = ImageOps.fit(frame, target_size, RESAMPLE, centering=(0.5, 0.5))
    rounded = Image.new("L", target_size, 0)
    ImageDraw.Draw(rounded).rounded_rectangle((0, 0, *target_size), radius=12, fill=255)
    canvas.paste(visual, inset[:2], rounded)

    draw.rounded_rectangle((843, 923, 1037, 978), radius=25, fill=INK)
    draw.text((870, 933), "原画面截帧", font=small, fill="white")
    total = str(item.get("total", ""))
    draw.text((1664, 927), f"{number} / {total}" if total else number,
              font=small, fill=MUTED)

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.suffix.lower() in {".jpg", ".jpeg"}:
        canvas.save(output, quality=94, subsampling=0)
    elif output.suffix.lower() == ".png":
        canvas.save(output)
    else:
        raise ValueError("output must be .jpg or .png")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="UTF-8 JSON manifest with a covers array")
    parser.add_argument("--font", type=Path, default=FONT_PATH)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    manifest = args.manifest.resolve()
    if not args.font.is_file():
        raise FileNotFoundError(f"Font not found: {args.font}")
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    entries = payload["covers"]
    if not entries:
        raise ValueError("Manifest covers array is empty")
    for item in entries:
        settings = {
            "badge": payload.get("badge", "录播教学 · 精剪"),
            "footer": payload.get("footer", "录播教学 / 原声讲解"),
            "total": payload.get("total", ""),
            **item,
        }
        print(build_cover(settings, manifest.parent, args.font, args.overwrite))


if __name__ == "__main__":
    main()
