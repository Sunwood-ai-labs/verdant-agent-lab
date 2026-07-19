#!/usr/bin/env python3
"""Build the themed Pixel Agents default-office preset without moving furniture."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "pixel-agents-pack" / "solarpunk-default-layout.json"
OUTPUT_DIR = ROOT / "pixel-agents-solarpunk-default"
OUTPUT = OUTPUT_DIR / "layout.json"
MANIFEST = OUTPUT_DIR / "preset.json"
AUDIT = ROOT / "proofs" / "pixel-agents-solarpunk-default" / "preset-audit.json"

PALETTE = {
    0: None,  # direct-color living wall atlas
    1: {"h": 32, "s": 46, "b": -5, "c": -18},   # moss work floor
    7: {"h": 102, "s": 34, "b": -8, "c": -22},  # warm timber lounge
    9: {"h": 36, "s": 18, "b": -24, "c": -30},  # dark threshold
    255: None,
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    source = json.loads(SOURCE.read_text())
    tile_ids = set(source["tiles"])
    unknown = tile_ids - set(PALETTE)
    if unknown:
        raise SystemExit(f"unmapped default-layout tile IDs: {sorted(unknown)}")

    themed = json.loads(json.dumps(source))
    themed["layoutRevision"] = int(source.get("layoutRevision", 0)) + 1
    themed["tileColors"] = [PALETTE[tile] for tile in source["tiles"]]

    checks = {
        "gridPreserved": (themed["cols"], themed["rows"]) == (source["cols"], source["rows"]),
        "tilesPreserved": themed["tiles"] == source["tiles"],
        "furniturePreserved": themed["furniture"] == source["furniture"],
        "placementCountIs36": len(themed["furniture"]) == 36,
        "tileColorCountMatchesGrid": len(themed["tileColors"]) == themed["cols"] * themed["rows"],
        "charactersAbsent": not themed.get("characters") and not themed.get("pets"),
        "onlySupportedTileIds": not unknown,
    }
    if not all(checks.values()):
        raise SystemExit(f"solarpunk default preset failed: {checks}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(themed, indent=2) + "\n")
    manifest = {
        "version": 1,
        "name": "Verdant Solarpunk Default Office",
        "target": "Pixel Agents 1.3",
        "tileSizePx": 16,
        "layout": "layout.json",
        "furniturePack": "../pixel-agents-pack",
        "theme": "../pixel-agents-theme-v2",
        "referenceInputs": [
            "assets/reference-original.jpg",
            "research/pixel-agents/sources/pixel-agents",
        ],
        "preserved": {
            "grid": "21x22",
            "tiles": len(themed["tiles"]),
            "placements": len(themed["furniture"]),
            "uniqueFurnitureTypes": len({item["type"] for item in themed["furniture"]}),
        },
        "changedFields": ["layoutRevision", "tileColors"],
        "paletteByTileId": {str(key): value for key, value in PALETTE.items()},
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    audit = {
        "status": "passed",
        "source": str(SOURCE.relative_to(ROOT)),
        "output": str(OUTPUT.relative_to(ROOT)),
        "sourceSha256": digest(SOURCE),
        "outputSha256": digest(OUTPUT),
        "grid": "21x22",
        "placements": len(themed["furniture"]),
        "uniqueFurnitureTypes": len({item["type"] for item in themed["furniture"]}),
        "tileIds": sorted(tile_ids),
        "changedFields": ["layoutRevision", "tileColors"],
        "checks": checks,
    }
    AUDIT.write_text(json.dumps(audit, indent=2) + "\n")
    print("PASS: built 21x22 solarpunk default preset; geometry and 36 placements preserved")


if __name__ == "__main__":
    main()
