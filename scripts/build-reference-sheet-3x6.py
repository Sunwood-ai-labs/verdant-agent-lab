#!/usr/bin/env python3
"""Assemble the 18 original-facing crops into a deterministic 3x6 sheet."""

import json
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "assets/layouts/reference-sheet-3x6.v1.json"
OUT_PATH = ROOT / "assets/intermediate/fidelity-v2/reference-crops-3x6-v1.png"


def main():
    spec = json.loads(SPEC_PATH.read_text())
    size = spec["cellSize"]
    gutter = 12
    sheet = Image.new("RGB", (spec["columns"] * size, spec["rows"] * size), "#FF00FF")
    base = SPEC_PATH.parent
    for cell in spec["cells"]:
        source = Image.open((base / cell["source"]).resolve()).convert("RGB")
        fitted = ImageOps.contain(source, (size - 2 * gutter, size - 2 * gutter), Image.Resampling.LANCZOS)
        x = (cell["index"] % spec["columns"]) * size + (size - fitted.width) // 2
        y = (cell["index"] // spec["columns"]) * size + (size - fitted.height) // 2
        sheet.paste(fitted, (x, y))
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUT_PATH)
    print(OUT_PATH)


if __name__ == "__main__":
    main()
