#!/usr/bin/env python3
"""Render labeled direct-reference zone crops for private visual inspection."""

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "assets/layouts/reference-source-zones.v1.json"
OUT = ROOT / "proof/intermediate/reference-original-zones-v1.png"


def main():
    spec = json.loads(SPEC.read_text())
    reference = Image.open((SPEC.parent / spec["reference"]).resolve()).convert("RGB")
    columns, card_width, image_height, label_height, gap = 3, 404, 248, 42, 16
    rows = (len(spec["zones"]) + columns - 1) // columns
    sheet = Image.new(
        "RGB",
        (gap + columns * (card_width + gap), gap + rows * (image_height + label_height + gap)),
        "#152018",
    )
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for index, zone in enumerate(spec["zones"]):
        x = gap + (index % columns) * (card_width + gap)
        y = gap + (index // columns) * (image_height + label_height + gap)
        crop = reference.crop(tuple(zone["bbox"]))
        fitted = ImageOps.contain(crop, (card_width, image_height), Image.Resampling.NEAREST)
        surface = Image.new("RGB", (card_width, image_height), "#273528")
        surface.paste(fitted, ((card_width - fitted.width) // 2, (image_height - fitted.height) // 2))
        sheet.paste(surface, (x, y))
        draw.rectangle((x, y + image_height, x + card_width, y + image_height + label_height), fill="#0a100b")
        draw.text((x + 10, y + image_height + 14), f"{index + 1:02d}  {zone['id'].upper()}", fill="#dce6d2", font=font)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
