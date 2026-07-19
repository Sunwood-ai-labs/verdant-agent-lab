#!/usr/bin/env python3
"""Build a wider original Pixel Agents office from the accepted 21x22 preset."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "pixel-agents-pack/solarpunk-default-layout.json"
CATALOG = ROOT / "pixel-agents-pack/catalog.json"
OUTPUT_DIR = ROOT / "pixel-agents-solarpunk-spacious"
OUTPUT = OUTPUT_DIR / "layout.json"
MANIFEST = OUTPUT_DIR / "preset.json"
AUDIT = ROOT / "proofs/pixel-agents-solarpunk-spacious/preset-audit.json"

INSERT_AT = 10
EXTRA_COLS = 14
TARGET_COLS = 35

PALETTE = {
    0: None,
    1: {"h": 32, "s": 46, "b": -5, "c": -18},
    7: {"h": 102, "s": 34, "b": -8, "c": -22},
    9: {"h": 36, "s": 18, "b": -24, "c": -30},
    255: None,
}

ADDITIONAL_FURNITURE = [
    {"uid": "spacious-hanging-plant-left", "type": "HANGING_PLANT", "col": 11, "row": 9},
    {"uid": "spacious-bookshelf", "type": "DOUBLE_BOOKSHELF", "col": 14, "row": 9},
    {"uid": "spacious-hanging-plant-right", "type": "HANGING_PLANT", "col": 21, "row": 9},
    {"uid": "spacious-desk-a", "type": "DESK_FRONT", "col": 11, "row": 12},
    {"uid": "spacious-pc-a", "type": "PC_FRONT_OFF", "col": 12, "row": 12},
    {"uid": "spacious-seat-a", "type": "CUSHIONED_BENCH", "col": 12, "row": 14},
    {"uid": "spacious-desk-b", "type": "DESK_FRONT", "col": 18, "row": 12},
    {"uid": "spacious-pc-b", "type": "PC_FRONT_OFF", "col": 19, "row": 12},
    {"uid": "spacious-seat-b", "type": "CUSHIONED_BENCH", "col": 19, "row": 14},
    {"uid": "spacious-chair-upper-left", "type": "WOODEN_CHAIR_SIDE", "col": 12, "row": 16},
    {"uid": "spacious-table", "type": "TABLE_FRONT", "col": 13, "row": 16},
    {"uid": "spacious-pc-upper-left", "type": "PC_SIDE", "col": 13, "row": 16},
    {"uid": "spacious-pc-upper-right", "type": "PC_SIDE:left", "col": 15, "row": 16},
    {"uid": "spacious-chair-upper-right", "type": "WOODEN_CHAIR_SIDE:left", "col": 16, "row": 16},
    {"uid": "spacious-chair-lower-left", "type": "WOODEN_CHAIR_SIDE", "col": 12, "row": 18},
    {"uid": "spacious-pc-lower-left", "type": "PC_SIDE", "col": 13, "row": 18},
    {"uid": "spacious-pc-lower-right", "type": "PC_SIDE:left", "col": 15, "row": 18},
    {"uid": "spacious-chair-lower-right", "type": "WOODEN_CHAIR_SIDE:left", "col": 16, "row": 18},
    {"uid": "spacious-plant", "type": "PLANT", "col": 22, "row": 18},
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inserted_tile(row: int) -> int:
    if row < 10 or row == 21:
        return 255
    if row == 10:
        return 0
    return 1


def expand_rows(values: list, rows: int, cols: int, inserted_values: list) -> list:
    expanded = []
    for row in range(rows):
        start = row * cols
        original = values[start : start + cols]
        expanded.extend(
            original[:INSERT_AT]
            + [inserted_values[row]] * EXTRA_COLS
            + original[INSERT_AT:]
        )
    return expanded


def main() -> None:
    source = json.loads(SOURCE.read_text())
    catalog = json.loads(CATALOG.read_text())
    if (source["cols"], source["rows"]) != (21, 22):
        raise SystemExit("spacious preset source must remain the audited 21x22 layout")

    layout = json.loads(json.dumps(source))
    layout["cols"] = TARGET_COLS
    layout["layoutRevision"] = int(source.get("layoutRevision", 0)) + 2
    inserted_tiles = [inserted_tile(row) for row in range(source["rows"])]
    layout["tiles"] = expand_rows(
        source["tiles"], source["rows"], source["cols"], inserted_tiles
    )
    layout["tileColors"] = [PALETTE[tile] for tile in layout["tiles"]]

    shifted = []
    for item in source["furniture"]:
        clone = dict(item)
        if clone["col"] >= INSERT_AT:
            clone["col"] += EXTRA_COLS
        shifted.append(clone)
    layout["furniture"] = shifted + ADDITIONAL_FURNITURE
    layout["zones"] = [
        {"id": "west-work", "name": "West Work", "minCol": 1, "maxCol": 9, "minRow": 11, "maxRow": 20},
        {"id": "central-studio", "name": "Central Studio", "minCol": 10, "maxCol": 23, "minRow": 11, "maxRow": 20},
        {"id": "east-lounge", "name": "East Lounge", "minCol": 25, "maxCol": 32, "minRow": 11, "maxRow": 20},
    ]

    used_types = {item["type"] for item in layout["furniture"]}
    placement_uids = [item["uid"] for item in layout["furniture"]]
    in_bounds = all(
        0 <= item["col"] < layout["cols"] and 0 <= item["row"] < layout["rows"]
        for item in layout["furniture"]
    )
    checks = {
        "gridIs35x22": (layout["cols"], layout["rows"]) == (35, 22),
        "tileCountIs770": len(layout["tiles"]) == 770,
        "tileColorCountMatches": len(layout["tileColors"]) == len(layout["tiles"]),
        "originalPlacementsPreserved": len(shifted) == len(source["furniture"]),
        "placementCountIs55": len(layout["furniture"]) == 55,
        "additionalPlacementCountIs19": len(ADDITIONAL_FURNITURE) == 19,
        "allTypesResolve": used_types <= set(catalog),
        "placementUidsUnique": len(placement_uids) == len(set(placement_uids)),
        "placementAnchorsInBounds": in_bounds,
        "threeActivityZones": len(layout["zones"]) == 3,
        "charactersAbsent": not layout.get("characters") and not layout.get("pets"),
    }
    if not all(checks.values()):
        raise SystemExit(f"spacious preset failed: {checks}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(layout, indent=2) + "\n")
    manifest = {
        "version": 1,
        "name": "Verdant Solarpunk Spacious Office",
        "target": "Pixel Agents 1.3",
        "tileSizePx": 16,
        "layout": "layout.json",
        "sourceLayout": str(SOURCE.relative_to(ROOT)),
        "expansion": {"insertAtColumn": INSERT_AT, "addedColumns": EXTRA_COLS},
        "grid": "35x22",
        "placements": len(layout["furniture"]),
        "zones": [zone["id"] for zone in layout["zones"]],
        "charactersEmbedded": False,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    audit = {
        "status": "passed",
        "source": str(SOURCE.relative_to(ROOT)),
        "output": str(OUTPUT.relative_to(ROOT)),
        "sourceSha256": digest(SOURCE),
        "outputSha256": digest(OUTPUT),
        "grid": "35x22",
        "placements": len(layout["furniture"]),
        "additionalPlacements": len(ADDITIONAL_FURNITURE),
        "checks": checks,
    }
    AUDIT.write_text(json.dumps(audit, indent=2) + "\n")
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()
