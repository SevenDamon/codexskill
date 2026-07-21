#!/usr/bin/env python3
"""Create a two-line Chinese talking-head cover from a source frame."""

import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("frame", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("line1")
    p.add_argument("line2")
    p.add_argument("--font", default=r"C:\Windows\Fonts\msyhbd.ttc")
    p.add_argument("--accent", default="#FFC400")
    a = p.parse_args()

    img = Image.open(a.frame).convert("RGBA")
    w, h = img.size
    top, bottom = int(h * 0.54), int(h * 0.82)
    shade = Image.new("RGBA", img.size, (0, 0, 0, 0))
    px = shade.load()
    for y in range(top, bottom):
        alpha = int(25 + 120 * min(1.0, (y - top) / max(1, h * 0.12)))
        for x in range(w):
            px[x, y] = (0, 0, 0, alpha)
    img = Image.alpha_composite(img, shade)
    draw = ImageDraw.Draw(img)

    def centered(text: str, y: int, size: int, color: str) -> None:
        font = ImageFont.truetype(a.font, size)
        box = draw.textbbox((0, 0), text, font=font, stroke_width=6)
        x = (w - (box[2] - box[0])) / 2
        draw.text((x, y), text, font=font, fill=color, stroke_width=6, stroke_fill="black")

    centered(a.line1, int(h * 0.60), int(w * 0.075), "white")
    centered(a.line2, int(h * 0.67), int(w * 0.082), a.accent)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(a.output, quality=95, subsampling=0)


if __name__ == "__main__":
    main()
