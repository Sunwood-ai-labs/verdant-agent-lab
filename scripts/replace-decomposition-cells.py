#!/usr/bin/env python3
import argparse
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def largest_component(image):
    rgba = np.array(image.convert("RGBA"))
    mask = (rgba[:, :, 3] > 0).astype(np.uint8)
    count, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    if count <= 1:
        return image
    keep = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    rgba[labels != keep, 3] = 0
    return Image.fromarray(rgba, "RGBA")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sheet")
    parser.add_argument("--blank", help="create a transparent 3x6 sheet, WIDTHxHEIGHT")
    parser.add_argument("--out", required=True)
    parser.add_argument("--replace", action="append", default=[], help="cell:path[:segment:count]")
    parser.add_argument("--largest", default="", help="comma-separated replacement cell ids")
    parser.add_argument("--margin", type=int, default=24)
    args = parser.parse_args()

    if args.blank:
        width, height = (int(value) for value in args.blank.lower().split("x", 1))
        sheet = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    elif args.sheet:
        sheet = Image.open(args.sheet).convert("RGBA")
    else:
        raise SystemExit("provide --sheet or --blank")
    if sheet.width % 3 or sheet.height % 6:
        raise SystemExit("sheet must be divisible by 3x6")
    cell_w, cell_h = sheet.width // 3, sheet.height // 6
    largest = {int(value) for value in args.largest.split(",") if value}

    for spec in args.replace:
        parts = spec.split(":")
        cell, path = int(parts[0]), parts[1]
        source = Image.open(path).convert("RGBA")
        if len(parts) == 4:
            segment, count = int(parts[2]), int(parts[3])
            x1 = round(source.width * segment / count)
            x2 = round(source.width * (segment + 1) / count)
            source = source.crop((x1, 0, x2, source.height))
        if cell in largest:
            source = largest_component(source)
        bbox = source.getchannel("A").getbbox()
        if not bbox:
            raise SystemExit(f"empty replacement for cell {cell}")
        source = source.crop(bbox)
        scale = min((cell_w - 2 * args.margin) / source.width, (cell_h - 2 * args.margin) / source.height, 1.0)
        source = source.resize((max(1, round(source.width * scale)), max(1, round(source.height * scale))), Image.Resampling.LANCZOS)
        index = cell - 1
        x0, y0 = (index % 3) * cell_w, (index // 3) * cell_h
        sheet.paste((0, 0, 0, 0), (x0, y0, x0 + cell_w, y0 + cell_h))
        x = x0 + (cell_w - source.width) // 2
        y = y0 + (cell_h - source.height) // 2
        sheet.alpha_composite(source, (x, y))

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.out)


if __name__ == "__main__":
    main()
