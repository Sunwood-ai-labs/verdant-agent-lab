#!/usr/bin/env python3
import argparse
from pathlib import Path

from PIL import Image


def parse_ints(value):
    return [int(part) for part in value.split(",")]


def parse_aspect_overrides(value):
    overrides = {}
    if not value:
        return overrides
    for item in value.split(","):
        cell, ratio = item.split(":", 1)
        overrides[int(cell)] = float(ratio)
    return overrides


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--cols", type=int, default=3)
    parser.add_argument("--rows", type=int, default=6)
    parser.add_argument("--row-cuts", required=True, help="comma-separated source y boundaries, rows+1 values")
    parser.add_argument("--margin", type=int, default=20)
    parser.add_argument(
        "--aspect-overrides",
        default="",
        help="comma-separated cell:width/height ratios applied before fitting, e.g. 2:1.13,3:1.13",
    )
    args = parser.parse_args()

    source = Image.open(args.input).convert("RGBA")
    cuts = parse_ints(args.row_cuts)
    aspect_overrides = parse_aspect_overrides(args.aspect_overrides)
    if len(cuts) != args.rows + 1 or cuts[0] != 0 or cuts[-1] != source.height:
        raise SystemExit("row cuts must span the full source and contain rows+1 values")
    if source.width % args.cols or source.height % args.rows:
        raise SystemExit("output dimensions must already be divisible by the requested grid")
    cell_w, cell_h = source.width // args.cols, source.height // args.rows
    canvas = Image.new("RGBA", source.size, (0, 0, 0, 0))
    for row in range(args.rows):
        for col in range(args.cols):
            x1, x2 = col * cell_w, (col + 1) * cell_w
            crop = source.crop((x1, cuts[row], x2, cuts[row + 1]))
            bbox = crop.getchannel("A").getbbox()
            if not bbox:
                # Empty cells are valid in a decomposition sheet when the
                # source contains fewer than 18 independent parts.
                continue
            crop = crop.crop(bbox)
            cell_index = row * args.cols + col + 1
            if cell_index in aspect_overrides:
                target_ratio = aspect_overrides[cell_index]
                target_width = max(1, round(crop.height * target_ratio))
                crop = crop.resize((target_width, crop.height), Image.Resampling.LANCZOS)
            max_w, max_h = cell_w - 2 * args.margin, cell_h - 2 * args.margin
            scale = min(1.0, max_w / crop.width, max_h / crop.height)
            size = (max(1, round(crop.width * scale)), max(1, round(crop.height * scale)))
            if size != crop.size:
                crop = crop.resize(size, Image.Resampling.LANCZOS)
            x = col * cell_w + (cell_w - crop.width) // 2
            y = row * cell_h + (cell_h - crop.height) // 2
            canvas.alpha_composite(crop, (x, y))
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    canvas.save(args.out)


if __name__ == "__main__":
    main()
