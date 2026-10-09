#!/usr/bin/env python3
"""Make restrained 3:4 covers from source frames, with mobile previews.

Usage: python make_portrait_cover.py manifest.json [--overwrite]

The manifest has a ``covers`` array. Each cover supplies ``source``, ``output``,
``number``, one or two ``title_lines``, an explicit ``title_font_size``, and a
source-pixel ``crop``. Optional ``redact`` rectangles are applied before crop.
The default composition is one headline plus one evidence panel; adapt or use a
custom composition when the actual source cannot fit legibly.
"""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

from make_screen_cover import checked_rect, load_frame, resolve


SIZE = (1080, 1440)
DEFAULT_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")
DEFAULT_REGULAR = Path(r"C:\Windows\Fonts\msyh.ttc")
RESAMPLE = Image.Resampling.LANCZOS


def color(value, label):
    if not isinstance(value, str) or len(value) != 7 or value[0] != "#":
        raise ValueError(f"{label} must be #RRGGBB")
    try:
        tuple(int(value[i:i + 2], 16) for i in (1, 3, 5))
    except ValueError as exc:
        raise ValueError(f"{label} must be #RRGGBB") from exc
    return value


def output_paths(base, item):
    out = resolve(base, item["output"])
    if out.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
        raise ValueError("output must be .png or .jpg")
    preview = out.with_name(out.stem + "-mobile.png")
    return out, preview


def checked_cover_rect(raw, label):
    rect = checked_rect(raw, SIZE, label)
    if rect[0] < 55 or rect[2] > SIZE[0] - 55:
        raise ValueError(f"{label} must keep a 55px horizontal safety margin")
    return rect


def build_cover(item, common, base, bold_path, regular_path, overwrite):
    src_path = resolve(base, item["source"])
    if not src_path.is_file():
        raise FileNotFoundError(src_path)
    out, preview = output_paths(base, item)
    if not overwrite and (out.exists() or preview.exists()):
        raise FileExistsError(f"Refusing to overwrite {out} or {preview}")

    title = item["title_lines"]
    if not isinstance(title, list) or not (1 <= len(title) <= 2) or not all(
        isinstance(line, str) and line.strip() for line in title
    ):
        raise ValueError("title_lines must have one or two nonempty strings")
    font_size = int(item["title_font_size"])
    if not 60 <= font_size <= 160:
        raise ValueError("title_font_size must be 60..160 px")
    if "label_font_size" not in item and "label_font_size" not in common:
        raise ValueError("Set an explicit label_font_size in the cover or manifest")
    label_size = int(item.get("label_font_size", common.get("label_font_size")))
    if not 18 <= label_size <= 42:
        raise ValueError("label_font_size must be 18..42 px")

    palette = {**common.get("palette", {}), **item.get("palette", {})}
    bg = color(palette.get("background", "#F5F5F1"), "background")
    fg = color(palette.get("foreground", "#191D1E"), "foreground")
    accent = color(palette.get("accent", "#8F4537"), "accent")
    rule = color(palette.get("rule", "#B4B7B1"), "rule")
    panel_bg = color(palette.get("panel_background", "#FFFFFF"), "panel_background")

    frame = load_frame(src_path, float(item.get("at", 0)))
    if "crop" not in item:
        raise ValueError("Set an explicit source-pixel crop; exclude desktop chrome")
    crop = checked_rect(item["crop"], frame.size, "crop")
    for index, raw in enumerate(item.get("redact", [])):
        rect = checked_rect(raw, frame.size, f"redact[{index}]")
        ImageDraw.Draw(frame).rectangle(rect, fill="#E8E8E6")
    evidence = frame.crop(crop)

    canvas = Image.new("RGB", SIZE, bg)
    draw = ImageDraw.Draw(canvas)
    marker = str(item.get("series_label", common.get("series_label", "录播教学 / 精剪")))
    marker_font = ImageFont.truetype(str(regular_path), label_size)
    if draw.textbbox((0, 0), marker, font=marker_font)[2] > 775:
        raise ValueError("series_label is too wide")
    draw.text((74, 83), marker, font=marker_font, fill=fg)
    number = str(item["number"])
    number_font = ImageFont.truetype(str(bold_path), 48)
    if draw.textbbox((0, 0), number, font=number_font)[2] > 90:
        raise ValueError("number is too wide")
    draw.text((928, 79), number, font=number_font, fill=accent)
    draw.line((72, 158, 1008, 158), fill=rule, width=2)

    title_font = ImageFont.truetype(str(bold_path), font_size)
    title_ys = item.get("title_ys", [273, 450])
    if not isinstance(title_ys, list) or len(title_ys) < len(title):
        raise ValueError("title_ys must give a y position for every title line")
    bottom = 0
    for line, raw_y in zip(title, title_ys):
        y = int(raw_y)
        bounds = draw.textbbox((72, y), line, font=title_font)
        if bounds[2] > 1008 or bounds[0] < 72 or bounds[1] < 205:
            raise ValueError(f"Title leaves its safe area: {line!r}")
        if bounds[1] < bottom + 15:
            raise ValueError("Title lines overlap or are too close")
        draw.text((72, y), line, font=title_font, fill=fg)
        bottom = bounds[3]
    rule_y = int(item.get("accent_rule_y", 678))
    if rule_y < bottom + 30:
        raise ValueError("Accent rule crowds the title")
    draw.line((73, rule_y, 213, rule_y), fill=accent, width=10)

    panel = checked_cover_rect(item.get("evidence_box", [76, 840, 1004, 1100]), "evidence_box")
    if panel[1] < rule_y + 90 or panel[3] > 1300:
        raise ValueError("Evidence panel needs breathing room above and below")
    draw.rounded_rectangle(panel, radius=22, fill=panel_bg, outline=rule, width=3)
    inset = (panel[0] + 4, panel[1] + 4, panel[2] - 4, panel[3] - 4)
    target = (inset[2] - inset[0], inset[3] - inset[1])
    fitted = ImageOps.contain(evidence, target, RESAMPLE)
    visual = Image.new("RGB", target, panel_bg)
    visual.paste(fitted, ((target[0] - fitted.width) // 2,
                          (target[1] - fitted.height) // 2))
    mask = Image.new("L", target, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, *target), radius=18, fill=255)
    canvas.paste(visual, inset[:2], mask)

    out.parent.mkdir(parents=True, exist_ok=True)
    if out.suffix.lower() in {".jpg", ".jpeg"}:
        canvas.save(out, quality=94, subsampling=0)
    else:
        canvas.save(out)
    canvas.resize((270, 360), RESAMPLE).save(preview)
    return out, preview


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--bold-font", type=Path, default=DEFAULT_BOLD)
    parser.add_argument("--regular-font", type=Path, default=DEFAULT_REGULAR)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    for p in (args.bold_font, args.regular_font):
        if not p.is_file():
            raise FileNotFoundError(p)
    manifest = args.manifest.resolve()
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    items = payload.get("covers")
    if not isinstance(items, list) or not items:
        raise ValueError("Manifest needs a nonempty covers array")
    destinations = []
    for item in items:
        destinations.extend(output_paths(manifest.parent, item))
    if len(set(destinations)) != len(destinations):
        raise ValueError("Manifest has duplicate output paths")
    if not args.overwrite:
        existing = [p for p in destinations if p.exists()]
        if existing:
            raise FileExistsError(f"Refusing to overwrite existing output: {existing[0]}")
    for item in items:
        out, preview = build_cover(item, payload, manifest.parent,
                                   args.bold_font, args.regular_font, args.overwrite)
        print(out)
        print(preview)


if __name__ == "__main__":
    main()
