#!/usr/bin/env python3
"""Render a private source-to-generated zone proof sheet."""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


def checkerboard(size: tuple[int, int], cell: int = 12) -> Image.Image:
    image = Image.new("RGB", size, "#d5d5d5")
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill="#9e9e9e")
    return image


def fit(source: Image.Image, size: tuple[int, int], alpha: bool = False) -> Image.Image:
    fitted = ImageOps.contain(source, size, Image.Resampling.NEAREST)
    surface = checkerboard(size) if alpha else Image.new("RGB", size, "#253127")
    x, y = (size[0] - fitted.width) // 2, (size[1] - fitted.height) // 2
    surface.paste(fitted, (x, y), fitted if fitted.mode == "RGBA" else None)
    return surface


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", required=True)
    parser.add_argument("--bbox", required=True, help="x,y,right,bottom")
    parser.add_argument("--master", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    bbox = tuple(int(value) for value in args.bbox.split(","))
    reference = Image.open(args.reference).convert("RGB").crop(bbox)
    master = Image.open(args.master).convert("RGB")
    report = json.loads(Path(args.report).read_text())
    card_size, label_h, gap = (320, 220), 34, 14
    cards = [("PRIVATE SOURCE CROP", reference), ("GENERATED 2x3 MASTER", master)]
    cards.extend((f"{item['cell']:02d} {item['id'].upper()}", Image.open(item["output"]).convert("RGBA")) for item in report["cells"])
    columns, rows = 4, 2
    out = Image.new("RGB", (gap + columns * (card_size[0] + gap), gap + rows * (card_size[1] + label_h + gap)), "#101812")
    draw, font = ImageDraw.Draw(out), ImageFont.load_default()
    for index, (label, image) in enumerate(cards):
        x = gap + (index % columns) * (card_size[0] + gap)
        y = gap + (index // columns) * (card_size[1] + label_h + gap)
        out.paste(fit(image, card_size, image.mode == "RGBA"), (x, y))
        draw.rectangle((x, y + card_size[1], x + card_size[0], y + card_size[1] + label_h), fill="#070d08")
        draw.text((x + 8, y + card_size[1] + 11), label, fill="#dce6d2", font=font)
    destination = Path(args.out)
    destination.parent.mkdir(parents=True, exist_ok=True)
    out.save(destination)
    print(destination)


if __name__ == "__main__":
    main()
