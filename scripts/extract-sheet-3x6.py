#!/usr/bin/env python3
"""Extract and trim the 18 alpha sprites from the generated 3x6 sheet."""

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "assets/layouts/reference-sheet-3x6.v1.json"
SHEET = ROOT / "assets/intermediate/fidelity-v2/spritesheet-3x6-imagegen-v1-alpha.png"
OUT = ROOT / "assets/generated/sheet3x6-v1"


def main():
    spec = json.loads(SPEC.read_text())
    sheet = Image.open(SHEET).convert("RGBA")
    OUT.mkdir(parents=True, exist_ok=True)
    for cell in spec["cells"]:
        col = cell["index"] % spec["columns"]
        row = cell["index"] // spec["columns"]
        left = round(col * sheet.width / spec["columns"])
        right = round((col + 1) * sheet.width / spec["columns"])
        top = round(row * sheet.height / spec["rows"])
        bottom = round((row + 1) * sheet.height / spec["rows"])
        sprite = sheet.crop((left, top, right, bottom))
        bbox = sprite.getchannel("A").getbbox()
        if not bbox:
            raise SystemExit(f"empty cell: {cell['id']}")
        x1, y1, x2, y2 = bbox
        padding = 6
        x1, y1 = max(0, x1 - padding), max(0, y1 - padding)
        x2, y2 = min(sprite.width, x2 + padding), min(sprite.height, y2 + padding)
        output = sprite.crop((x1, y1, x2, y2))
        output.save(OUT / f"{cell['id']}.png")
        print(f"{cell['index']:02d} {cell['id']} {output.width}x{output.height}")


if __name__ == "__main__":
    main()
