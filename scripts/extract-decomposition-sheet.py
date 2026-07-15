#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from PIL import Image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sheet", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    manifest = json.loads(Path(args.manifest).read_text())
    cells = manifest["cells"]
    cols = manifest["grid"]["columns"]
    rows = manifest["grid"]["rows"]
    image = Image.open(args.sheet).convert("RGBA")
    if image.width % cols or image.height % rows:
        raise SystemExit(f"sheet {image.size} is not divisible by {cols}x{rows}")
    cell_w, cell_h = image.width // cols, image.height // rows
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for item in cells:
        index = item["cell"] - 1
        x, y = (index % cols) * cell_w, (index // cols) * cell_h
        slug = item["semantic"].lower().replace(" ", "-").replace("/", "-")
        slug = "".join(c for c in slug if c.isalnum() or c == "-")
        target = out / f"{item['cell']:02d}-{slug}.png"
        image.crop((x, y, x + cell_w, y + cell_h)).save(target)
        item["output"] = str(target.relative_to(Path(args.manifest).parent.parent))
        item["sheetBbox"] = [x, y, x + cell_w, y + cell_h]
    manifest["sheet"] = str(Path(args.sheet).relative_to(Path(args.manifest).parent.parent))
    manifest["cellSize"] = [cell_w, cell_h]
    manifest["status"] = "extracted-needs-independent-qa"
    Path(args.manifest).write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
