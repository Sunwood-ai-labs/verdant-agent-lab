#!/usr/bin/env python3
"""Validate the integrated Pixel Agents solarpunk default-office preset."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "pixel-agents-pack/solarpunk-default-layout.json"
LAYOUT = ROOT / "pixel-agents-solarpunk-default/layout.json"
PRESET = ROOT / "pixel-agents-solarpunk-default/preset.json"
CATALOG = ROOT / "pixel-agents-pack/catalog.json"
FURNITURE = ROOT / "pixel-agents-pack/assets/furniture"
FLOORS = ROOT / "pixel-agents-theme-v2/assets/floors"
WALLS = ROOT / "pixel-agents-theme-v2/assets/walls"
REPORT = ROOT / "proofs/pixel-agents-solarpunk-default/integrated-validation.json"


def main() -> None:
    source = json.loads(SOURCE.read_text())
    layout = json.loads(LAYOUT.read_text())
    preset = json.loads(PRESET.read_text())
    catalog = json.loads(CATALOG.read_text())

    normalized_source = deepcopy(source)
    normalized_layout = deepcopy(layout)
    for key in ("layoutRevision", "tileColors"):
        normalized_source.pop(key, None)
        normalized_layout.pop(key, None)

    manifests = sorted(FURNITURE.glob("*/manifest.json"))
    sprites = sorted(FURNITURE.glob("*/*.png"))
    floors = sorted(FLOORS.glob("floor_*.png"))
    walls = sorted(WALLS.glob("wall_*.png"))
    used_types = {item["type"] for item in layout["furniture"]}
    floor_sizes = {Image.open(path).size for path in floors}
    wall_sizes = {Image.open(path).size for path in walls}

    checks = {
        "onlyRevisionAndColorsChanged": normalized_source == normalized_layout,
        "gridIs21x22": (layout["cols"], layout["rows"]) == (21, 22),
        "tileSizeIs16": preset["tileSizePx"] == 16,
        "tileCountIs462": len(layout["tiles"]) == 462,
        "tileColorsCountIs462": len(layout["tileColors"]) == 462,
        "furnitureCountIs36": len(layout["furniture"]) == 36,
        "uniqueDefaultTypesIs25": len(used_types) == 25,
        "allDefaultTypesResolve": used_types <= set(catalog),
        "manifestCountIs53": len(manifests) == 53,
        "physicalSpriteCountIs64": len(sprites) == 64,
        "floorCountIs9": len(floors) == 9,
        "floorSizeIs16x16": floor_sizes == {(16, 16)},
        "wallAtlasCountIs1": len(walls) == 1,
        "wallAtlasSizeIs64x128": wall_sizes == {(64, 128)},
        "charactersAreNotEmbedded": not layout.get("characters") and not layout.get("pets"),
    }
    status = "passed" if all(checks.values()) else "failed"
    report = {
        "status": status,
        "claim": "Pixel Agents default geometry and furniture records are preserved while exact-ID furniture, nine floors, and a connected wall atlas provide a solarpunk reskin",
        "grid": "21x22",
        "tileSizePx": 16,
        "placements": len(layout["furniture"]),
        "uniqueDefaultFurnitureTypes": len(used_types),
        "catalogEntries": len(catalog),
        "furnitureManifests": len(manifests),
        "physicalFurnitureSprites": len(sprites),
        "floorTiles": len(floors),
        "wallAtlases": len(walls),
        "changedFields": ["layoutRevision", "tileColors"],
        "checks": checks,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if status != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
