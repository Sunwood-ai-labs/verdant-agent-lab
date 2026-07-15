#!/usr/bin/env python3
"""Chroma-key and split a landscape two-column by three-row asset sheet."""

import argparse
import json
import math
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image


def proportional_boundaries(length: int, divisions: int) -> list[int]:
    if length <= 0 or divisions <= 0:
        raise ValueError("length and divisions must be positive")
    return [round(index * length / divisions) for index in range(divisions + 1)]


def color_distance(left: tuple[int, int, int], right: tuple[int, int, int]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(left, right)))


def border_key(image: Image.Image) -> tuple[int, int, int]:
    rgb = image.convert("RGB")
    pixels = [rgb.getpixel((0, 0)), rgb.getpixel((rgb.width - 1, 0)), rgb.getpixel((0, rgb.height - 1)), rgb.getpixel((rgb.width - 1, rgb.height - 1))]
    return tuple(round(sum(pixel[channel] for pixel in pixels) / len(pixels)) for channel in range(3))


def make_alpha(image: Image.Image, key: tuple[int, int, int], threshold: int) -> Image.Image:
    rgba = image.convert("RGBA")
    converted = []
    for red, green, blue, alpha in rgba.getdata():
        converted.append((red, green, blue, 0 if color_distance((red, green, blue), key) <= threshold else alpha))
    rgba.putdata(converted)
    return rgba


def alpha_bbox(image: Image.Image) -> Optional[Tuple[int, int, int, int]]:
    return image.getchannel("A").getbbox()


def blank_runs(alpha: Image.Image, axis: str) -> list[tuple[int, int]]:
    width, height = alpha.size
    size, across = (width, height) if axis == "x" else (height, width)
    mask = alpha.getchannel("A")
    empty = []
    for position in range(size):
        count = sum(1 for other in range(across) if mask.getpixel((position, other) if axis == "x" else (other, position)))
        empty.append(count == 0)
    runs, start = [], None
    for index, value in enumerate(empty + [False]):
        if value and start is None:
            start = index
        if not value and start is not None:
            runs.append((start, index))
            start = None
    return runs


def grid_boundaries(alpha: Image.Image, divisions: int, axis: str) -> list[int]:
    length = alpha.width if axis == "x" else alpha.height
    defaults = proportional_boundaries(length, divisions)
    internal = [run for run in blank_runs(alpha, axis) if run[0] > 0 and run[1] < length]
    chosen = [0]
    max_offset = length / divisions / 2
    for target in defaults[1:-1]:
        if not internal:
            chosen.append(target)
            continue
        start, end = min(internal, key=lambda run: abs(((run[0] + run[1]) / 2) - target))
        midpoint = round((start + end) / 2)
        chosen.append(midpoint if abs(midpoint - target) <= max_offset else target)
    return chosen + [length]


def split_sheet(image: Image.Image, cells: list[dict], output: Path, threshold: int = 36) -> tuple[Image.Image, list[dict]]:
    if len(cells) != 6:
        raise ValueError("a 2x3 sheet requires exactly six cell definitions")
    output.mkdir(parents=True, exist_ok=True)
    alpha = make_alpha(image, border_key(image), threshold)
    xs, ys = grid_boundaries(alpha, 2, "x"), grid_boundaries(alpha, 3, "y")
    report = []
    for index, cell in enumerate(cells):
        column, row = index % 2, index // 2
        rectangle = (xs[column], ys[row], xs[column + 1], ys[row + 1])
        cell_image = alpha.crop(rectangle)
        bbox = alpha_bbox(cell_image)
        if bbox is None:
            raise ValueError(f"cell {index + 1} ({cell['id']}) has no opaque pixels")
        trimmed = cell_image.crop(bbox)
        target = output / f"{index + 1:02d}-{cell['id']}.png"
        trimmed.save(target)
        report.append({
            "cell": index + 1,
            "id": cell["id"],
            "sourceCellBbox": list(rectangle),
            "alphaBboxInCell": list(bbox),
            "alphaBboxInSheet": [rectangle[0] + bbox[0], rectangle[1] + bbox[1], rectangle[0] + bbox[2], rectangle[1] + bbox[3]],
            "edgeFlags": {
                "left": bbox[0] == 0,
                "top": bbox[1] == 0,
                "right": bbox[2] == cell_image.width,
                "bottom": bbox[3] == cell_image.height
            },
            "opaquePixels": sum(1 for value in cell_image.getchannel("A").getdata() if value),
            "output": str(target)
        })
    return alpha, report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--spec", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--alpha-out", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--threshold", type=int, default=36)
    args = parser.parse_args()
    spec = json.loads(Path(args.spec).read_text())
    alpha, cells = split_sheet(Image.open(args.input), spec["cells"], Path(args.out), args.threshold)
    alpha_path = Path(args.alpha_out)
    alpha_path.parent.mkdir(parents=True, exist_ok=True)
    alpha.save(alpha_path)
    report = {"version": 1, "input": args.input, "alphaMaster": str(alpha_path), "grid": spec["grid"], "chromaKey": list(border_key(Image.open(args.input))), "threshold": args.threshold, "cells": cells}
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"alphaMaster": str(alpha_path), "children": len(cells), "report": str(report_path)}))


if __name__ == "__main__":
    main()
