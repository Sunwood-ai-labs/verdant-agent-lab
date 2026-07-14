#!/usr/bin/env python3
"""Heuristic QA for audited single-subject sprites and cleared edge regions."""

from collections import deque
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SINGLE_SUBJECTS = [
    "assets/generated/furniture/curved-reception-desk.png",
    "assets/generated/furniture/shared-worktable.png",
]
FORBIDDEN_REGIONS = {
    "assets/generated/technology/espresso-machine.png": (280, 0, 362, 362),
    "assets/generated/furniture/shared-worktable.png": (0, 280, 362, 362),
    "assets/generated/furniture/tall-indoor-plant.png": (280, 0, 362, 362),
}
NEGATIVE_COMPONENT_CONTROL = "assets/intermediate/sprite-replacements/curved-reception-desk-before.png"
NEGATIVE_REGION_CONTROL = (
    "assets/intermediate/sprite-replacements/shared-worktable-composite-before.png",
    (0, 280, 362, 362),
)


def large_components(path: Path, threshold: int = 100, minimum_area: int = 500) -> list[int]:
    alpha = Image.open(path).convert("RGBA").getchannel("A")
    width, height = alpha.size
    pixels = alpha.load()
    seen: set[tuple[int, int]] = set()
    components: list[int] = []

    for y in range(height):
        for x in range(width):
            if (x, y) in seen or pixels[x, y] < threshold:
                continue
            queue = deque([(x, y)])
            seen.add((x, y))
            area = 0
            while queue:
                px, py = queue.popleft()
                area += 1
                for nx, ny in ((px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)):
                    if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in seen and pixels[nx, ny] >= threshold:
                        seen.add((nx, ny))
                        queue.append((nx, ny))
            if area >= minimum_area:
                components.append(area)
    return sorted(components, reverse=True)


def nontransparent_in_region(path: Path, box: tuple[int, int, int, int]) -> int:
    alpha = Image.open(path).convert("RGBA").getchannel("A")
    return sum(value > 0 for value in alpha.crop(box).getdata())


if __name__ == "__main__":
    failed = False
    for relative in SINGLE_SUBJECTS:
        components = large_components(ROOT / relative)
        print(f"{relative}: large_components={components}")
        failed |= len(components) != 1

    for relative, box in FORBIDDEN_REGIONS.items():
        count = nontransparent_in_region(ROOT / relative, box)
        print(f"{relative}: forbidden_region_pixels={count}")
        failed |= count != 0

    negative_components = large_components(ROOT / NEGATIVE_COMPONENT_CONTROL)
    print(f"negative-control {NEGATIVE_COMPONENT_CONTROL}: large_components={negative_components}")
    failed |= len(negative_components) == 1

    negative_path, negative_box = NEGATIVE_REGION_CONTROL
    negative_pixels = nontransparent_in_region(ROOT / negative_path, negative_box)
    print(f"negative-control {negative_path}: forbidden_region_pixels={negative_pixels}")
    failed |= negative_pixels == 0

    raise SystemExit(1 if failed else 0)
