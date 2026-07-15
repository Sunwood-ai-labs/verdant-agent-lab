#!/usr/bin/env python3
"""Create padded, tight-alpha runtime sprite variants without overwriting originals."""

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent.parent
MANIFESTS = [
    ROOT / "assets/manifests/furniture.v1.json",
    ROOT / "assets/manifests/technology.v1.json",
    ROOT / "assets/manifests/props.v1.json",
]
PADDING = 8
MIN_EXCESS_MARGIN = 35


def margin_and_edge(alpha):
    width, height = alpha.size
    x1, y1, x2, y2 = alpha.getbbox()
    margins = (x1, y1, width - x2, height - y2)
    return margins, any(value == 0 for value in margins)


def main():
    trimmed = []
    for manifest_path in MANIFESTS:
        manifest = json.loads(manifest_path.read_text())
        changed = False
        for item in manifest["items"]:
            if item.get("trimmedFrom"):
                continue
            original_rel = item["sprite"]
            source = ROOT / "assets" / original_rel.replace("../", "")
            image = Image.open(source).convert("RGBA")
            alpha = image.getchannel("A")
            bbox = alpha.getbbox()
            if not bbox:
                continue
            margins, touches_edge = margin_and_edge(alpha)
            if touches_edge or max(margins) < MIN_EXCESS_MARGIN:
                continue
            x1, y1, x2, y2 = bbox
            crop = image.crop((max(0, x1 - PADDING), max(0, y1 - PADDING), min(image.width, x2 + PADDING), min(image.height, y2 + PADDING)))
            output = ROOT / "assets/generated/trimmed" / f"{item['id']}-trimmed-v1.png"
            output.parent.mkdir(parents=True, exist_ok=True)
            crop.save(output)
            item["trimmedFrom"] = original_rel
            item["sprite"] = "../generated/trimmed/" + output.name
            item["trim"] = {"version": 1, "paddingPx": PADDING, "sourceSize": list(image.size), "alphaBBox": list(bbox), "sourceMargins": list(margins)}
            trimmed.append({"id": item["id"], "from": original_rel, "to": item["sprite"], "sourceMargins": margins})
            changed = True
        if changed:
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    report = {"version": 1, "paddingPx": PADDING, "trimmedCount": len(trimmed), "assets": trimmed}
    output = ROOT / "proof/runtime-sprite-trim-v1.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"trimmedCount": len(trimmed)}))


if __name__ == "__main__":
    main()
