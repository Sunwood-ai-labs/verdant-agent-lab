#!/usr/bin/env python3
"""Remove known cross-cell fragments while preserving the generated sprite body."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
JOBS = {
    "assets/generated/technology/espresso-machine.png": [(280, 0, 362, 362)],
    "assets/generated/furniture/shared-worktable.png": [(0, 0, 120, 362)],
    "assets/generated/furniture/tall-indoor-plant.png": [(280, 0, 362, 362)],
}


def clean(relative_path: str, rectangles: list[tuple[int, int, int, int]]) -> None:
    path = ROOT / relative_path
    image = Image.open(path).convert("RGBA")
    pixels = image.load()
    removed = 0

    for left, top, right, bottom in rectangles:
        for y in range(top, bottom):
            for x in range(left, right):
                if pixels[x, y][3]:
                    removed += 1
                pixels[x, y] = (0, 0, 0, 0)

    image.save(path, optimize=True)
    print(f"{relative_path}: removed {removed} nontransparent pixels")


if __name__ == "__main__":
    for relative_path, rectangles in JOBS.items():
        clean(relative_path, rectangles)
