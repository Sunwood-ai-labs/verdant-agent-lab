#!/usr/bin/env python3
"""Render six-cell horizontal catalog pages from independent alpha sprites."""

import argparse
import json
from pathlib import Path

from PIL import Image


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--layout", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--prefix", required=True)
    parser.add_argument("--cell-size", type=int, default=320)
    parser.add_argument("--padding", type=int, default=28)
    parser.add_argument("--background", default="#ff00ff")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    layout = json.loads((root / args.layout).read_text())
    cells = layout["cells"]
    output = root / args.out_dir
    output.mkdir(parents=True, exist_ok=True)

    rendered = []
    for page_index, start in enumerate(range(0, len(cells), 6), 1):
        page_cells = cells[start : start + 6]
        canvas = Image.new("RGBA", (args.cell_size * 3, args.cell_size * 2), args.background)
        for local_index, cell in enumerate(page_cells):
            sprite = Image.open(root / "assets" / cell["output"]).convert("RGBA")
            bounds = sprite.getchannel("A").getbbox()
            if not bounds:
                raise ValueError(f"empty sprite: {cell['output']}")
            sprite = sprite.crop(bounds)
            max_size = args.cell_size - args.padding * 2
            scale = min(max_size / sprite.width, max_size / sprite.height, 1.0)
            if scale < 1.0:
                sprite = sprite.resize(
                    (max(1, round(sprite.width * scale)), max(1, round(sprite.height * scale))),
                    Image.Resampling.NEAREST,
                )
            column, row = local_index % 3, local_index // 3
            x = column * args.cell_size + (args.cell_size - sprite.width) // 2
            y = row * args.cell_size + (args.cell_size - sprite.height) // 2
            canvas.alpha_composite(sprite, (x, y))
        target = output / f"{args.prefix}-page-{page_index:02d}.png"
        canvas.convert("RGB").save(target)
        rendered.append(str(target.relative_to(root)))

    print(json.dumps({"pages": rendered, "cells": len(cells)}))


if __name__ == "__main__":
    main()
