#!/usr/bin/env python3
"""Flatten pack manifests into a browser-preview catalog with virtual left IDs."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FURNITURE = ROOT / "pixel-agents-pack/assets/furniture"
OUTPUT = ROOT / "pixel-agents-pack/catalog.json"


def walk(node: dict, inherited: dict):
    current = {**inherited}
    for key in ("orientation", "state", "mirrorSide", "canPlaceOnSurfaces", "backgroundTiles", "category"):
        if key in node:
            current[key] = node[key]
    if node.get("type") == "asset":
        yield {**current, **node}
        return
    for child in node.get("members", []):
        yield from walk(child, current)


def main() -> None:
    catalog = {}
    for manifest_path in sorted(FURNITURE.glob("*/manifest.json")):
        manifest = json.loads(manifest_path.read_text())
        inherited = {
            "category": manifest["category"],
            "canPlaceOnSurfaces": manifest.get("canPlaceOnSurfaces", False),
            "backgroundTiles": manifest.get("backgroundTiles", 0),
        }
        for asset in walk(manifest, inherited):
            asset_id = asset["id"]
            entry = {
                "id": asset_id,
                "src": f"assets/furniture/{manifest_path.parent.name}/{asset.get('file', asset_id + '.png')}",
                "width": asset["width"],
                "height": asset["height"],
                "footprintW": asset["footprintW"],
                "footprintH": asset["footprintH"],
                "category": asset["category"],
                "canPlaceOnSurfaces": asset.get("canPlaceOnSurfaces", False),
                "backgroundTiles": asset.get("backgroundTiles", 0),
                "mirrored": False,
            }
            catalog[asset_id] = entry
            if asset.get("orientation") == "side" and asset.get("mirrorSide"):
                catalog[f"{asset_id}:left"] = {**entry, "id": f"{asset_id}:left", "mirrored": True}
    OUTPUT.write_text(json.dumps(catalog, indent=2) + "\n")
    print(f"Wrote {len(catalog)} catalog entries to {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
