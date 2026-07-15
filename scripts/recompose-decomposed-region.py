#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path

from PIL import Image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--cells", help="comma-separated subset of cell ids")
    parser.add_argument("--order", help="comma-separated explicit draw order")
    parser.add_argument("--stretch-to-bbox", action="store_true", help="resize each isolated sprite to its exact source bbox")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    root = manifest_path.parent.parent
    manifest = json.loads(manifest_path.read_text())
    canvas = Image.new("RGBA", tuple(manifest["sourceSize"]), (0, 0, 0, 0))
    by_cell = {item["cell"]: item for item in manifest["cells"]}
    # Structural surfaces first, attached storage next, then movable props.
    order = [1, 2, 3, 16, 17, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 18]
    if args.order:
        order = [int(value) for value in args.order.split(",")]
    if args.cells:
        selected = {int(value) for value in args.cells.split(",")}
        order = [cell for cell in order if cell in selected]
    for cell_id in order:
        item = by_cell[cell_id]
        sprite = Image.open(root / item["output"]).convert("RGBA")
        alpha_bbox = sprite.getchannel("A").getbbox()
        if not alpha_bbox:
            raise SystemExit(f"empty alpha for cell {cell_id}")
        sprite = sprite.crop(alpha_bbox)
        x1, y1, x2, y2 = item["sourceBbox"]
        box_w, box_h = x2 - x1, y2 - y1
        if args.stretch_to_bbox:
            size = (box_w, box_h)
        else:
            scale = min(box_w / sprite.width, box_h / sprite.height)
            size = (max(1, round(sprite.width * scale)), max(1, round(sprite.height * scale)))
        sprite = sprite.resize(size, Image.Resampling.LANCZOS)
        x = x1 + (box_w - size[0]) // 2
        y = y1 + (box_h - size[1]) // 2
        canvas.alpha_composite(sprite, (x, y))
        item["recomposedBbox"] = [x, y, x + size[0], y + size[1]]
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    canvas.save(args.out)
    manifest["recomposition"] = os.path.relpath(args.out, root)
    manifest["status"] = "recomposed-needs-reference-score"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
