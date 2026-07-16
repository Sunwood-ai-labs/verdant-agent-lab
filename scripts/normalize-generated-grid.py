#!/usr/bin/env python3
"""Replace generator-added near-white grid gutters with the chroma color."""

import argparse
from pathlib import Path

from PIL import Image


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--background", default="ff00ff")
    parser.add_argument("--white", type=int, default=238)
    parser.add_argument("--fraction", type=float, default=0.85)
    args = parser.parse_args()

    image = Image.open(args.input).convert("RGB")
    pixels = image.load()
    background = tuple(bytes.fromhex(args.background))

    white_columns = []
    for x in range(image.width):
        count = sum(all(channel >= args.white for channel in pixels[x, y]) for y in range(image.height))
        if count / image.height >= args.fraction:
            white_columns.append(x)
    white_rows = []
    for y in range(image.height):
        count = sum(all(channel >= args.white for channel in pixels[x, y]) for x in range(image.width))
        if count / image.width >= args.fraction:
            white_rows.append(y)

    for x in white_columns:
        for y in range(image.height):
            pixels[x, y] = background
    for y in white_rows:
        for x in range(image.width):
            pixels[x, y] = background

    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    image.save(target)
    print(f"white_columns={len(white_columns)} white_rows={len(white_rows)} output={target}")


if __name__ == "__main__":
    main()
