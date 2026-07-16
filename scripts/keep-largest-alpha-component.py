#!/usr/bin/env python3
"""Remove disconnected alpha debris while retaining one continuous sprite."""

import argparse
from pathlib import Path

from PIL import Image


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()

    for raw in args.paths:
        path = Path(raw)
        image = Image.open(path).convert("RGBA")
        alpha = image.getchannel("A")
        pixels = alpha.load()
        seen = set()
        components = []
        for y in range(image.height):
            for x in range(image.width):
                if pixels[x, y] == 0 or (x, y) in seen:
                    continue
                component = []
                stack = [(x, y)]
                seen.add((x, y))
                while stack:
                    cx, cy = stack.pop()
                    component.append((cx, cy))
                    for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
                        if 0 <= nx < image.width and 0 <= ny < image.height and pixels[nx, ny] > 0 and (nx, ny) not in seen:
                            seen.add((nx, ny))
                            stack.append((nx, ny))
                components.append(component)

        if not components:
            raise ValueError(f"no opaque pixels: {path}")
        largest = max(components, key=len)
        keep = set(largest)
        clean_alpha = Image.new("L", image.size, 0)
        clean_pixels = clean_alpha.load()
        for x, y in keep:
            clean_pixels[x, y] = pixels[x, y]
        image.putalpha(clean_alpha)
        bbox = clean_alpha.getbbox()
        image.crop(bbox).save(path)
        print(f"{path}: kept={len(largest)} removed={sum(map(len, components)) - len(largest)}")


if __name__ == "__main__":
    main()
