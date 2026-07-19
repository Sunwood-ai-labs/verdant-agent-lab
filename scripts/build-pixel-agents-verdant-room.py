#!/usr/bin/env python3
"""Build the source-shaped Verdant office for the Pixel Agents 42x34 runtime.

The reference office is the composition authority.  The layout keeps its
top-row reception/solar/lounge/cafe band, middle studio/meeting/lab band, and
bottom greenhouse/workstation/lounge band instead of shrinking the project
into Pixel Agents' unrelated default office.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "pixel-agents-pack" / "verdant-runtime-layout.json"
COLS, ROWS = 42, 34
VOID, WALL, SOFT_FLOOR, WOOD_FLOOR = 255, 0, 1, 7

# Keep wall colors unset so the connected solarpunk atlas is displayed directly.
# The old -100 brightness value crushed the living-wall art to black.
WALL_COLOR = None
WOOD_COLOR = {"h": 25, "s": 48, "b": -43, "c": -88}
AISLE_COLOR = {"h": 35, "s": 32, "b": -24, "c": -72}
LOUNGE_COLOR = {"h": 105, "s": 34, "b": -28, "c": -72}
LAB_COLOR = {"h": 158, "s": 32, "b": -30, "c": -74}


def furniture(type_: str, col: int, row: int, *, uid: str | None = None) -> dict:
    return {
        "uid": uid or f"verdant-{type_.lower().replace(':', '-')}-{col}-{row}",
        "type": type_,
        "col": col,
        "row": row,
    }


def build() -> dict:
    tiles = [VOID] * (COLS * ROWS)
    tile_colors: list[dict | None] = [None] * (COLS * ROWS)

    def put(col: int, row: int, tile: int, color: dict | None = None) -> None:
        index = row * COLS + col
        tiles[index] = tile
        tile_colors[index] = color

    # One coherent office shell. Rows 0-2 stay void for the Pixel Agents sign.
    for row in range(3, 33):
        for col in range(1, 41):
            border = row in (3, 32) or col in (1, 40)
            put(col, row, WALL if border else WOOD_FLOOR, WALL_COLOR if border else WOOD_COLOR)

    # Reference-shaped material zones.  These are contiguous floor fields, not
    # the rejected four-quadrant/default-office composition.
    for row in range(4, 11):
        for col in range(27, 40):
            put(col, row, SOFT_FLOOR, LOUNGE_COLOR)
    for row in range(19, 32):
        for col in range(2, 10):
            put(col, row, SOFT_FLOOR, LOUNGE_COLOR)
    for row in range(13, 26):
        for col in range(30, 40):
            put(col, row, SOFT_FLOOR, LAB_COLOR)
    for row in range(26, 32):
        for col in range(34, 40):
            put(col, row, SOFT_FLOOR, LOUNGE_COLOR)

    # Main horizontal and entrance circulation axes follow the source image.
    for row in (11, 12):
        for col in range(2, 40):
            put(col, row, WOOD_FLOOR, AISLE_COLOR)
    for row in range(13, 33):
        for col in (20, 21):
            put(col, row, WOOD_FLOOR, AISLE_COLOR)
    # Open the bottom-center entrance instead of sealing the room with a wall.
    for col in (20, 21):
        put(col, 32, WOOD_FLOOR, AISLE_COLOR)

    items = [
        # Solar wing, upper left. Panel and frame are separate catalog assets;
        # the room uses the panel variant directly because it already includes
        # a readable outer rim at 16px scale.
        furniture("SOLAR_PANEL", 2, 4),
        furniture("SOLAR_DASHBOARD", 6, 5),
        furniture("SOLAR_BATTERY_BANK", 2, 8),
        furniture("SOLAR_CONTROLLER", 8, 8),
        furniture("SOLAR_PLANTER", 2, 12),

        # Source-specific reception, upper center. Small pieces are intentionally
        # layered on the counter surface by Pixel Agents' surface placement.
        furniture("RECEPTION_COUNTER", 15, 5),
        furniture("RECEPTION_MONITOR", 17, 4),
        furniture("RECEPTION_TERMINAL", 19, 5),
        furniture("RECEPTION_PAPERS", 20, 5),
        furniture("RECEPTION_PLANTER", 15, 8),
        furniture("RECEPTION_EASEL", 22, 5),
        furniture("WOODEN_CHAIR_BACK", 18, 8),
        furniture("PLANT_2", 25, 6),

        # North lounge between reception and cafe, matching the source band.
        furniture("LOUNGE_SECTIONAL", 27, 5, uid="verdant-north-lounge-sectional"),
        furniture("LOUNGE_OVAL_TABLE", 28, 8, uid="verdant-north-lounge-table"),
        furniture("PLANT", 26, 7, uid="verdant-north-lounge-plant-left"),
        furniture("PLANT_2", 32, 7, uid="verdant-north-lounge-plant-right"),

        # Cafe, upper right.
        furniture("CAFE_LIVING_WALL", 36, 3),
        furniture("CAFE_PLANT_SHELF", 34, 6),
        furniture("CAFE_COUNTER", 34, 8),
        furniture("CAFE_DISPENSERS", 35, 7),
        furniture("CAFE_FRIDGE", 39, 7),
        furniture("CAFE_KIOSK", 39, 10),
        furniture("COFFEE", 37, 8),

        # Greenhouse, lower left. Left/right roof pieces remain individually
        # placeable catalog variants; this composition uses the ridge assembly.
        furniture("GREENHOUSE_ROOF", 2, 20),
        furniture("GREENHOUSE_GLASS_WALL", 2, 24),
        furniture("GREENHOUSE_DOOR", 5, 24),
        furniture("GREENHOUSE_PLANT_SHELF", 2, 28),
        furniture("HANGING_PLANT", 9, 24),

        # West studio, central meeting room, and two lower workstation islands.
        furniture("WHITEBOARD", 2, 15),
        furniture("DOUBLE_BOOKSHELF", 4, 14),
        furniture("TABLE_FRONT", 7, 15, uid="verdant-west-studio-table"),
        furniture("WOODEN_CHAIR_SIDE", 6, 17, uid="verdant-west-chair-left"),
        furniture("WOODEN_CHAIR_SIDE:left", 10, 17, uid="verdant-west-chair-right"),
        furniture("WOODEN_CHAIR_FRONT", 8, 19, uid="verdant-west-chair-front"),

        furniture("MEETING_GLASS_MODULE", 22, 13),
        furniture("TABLE_FRONT", 23, 17, uid="verdant-meeting-table"),
        furniture("WOODEN_CHAIR_SIDE", 22, 18, uid="verdant-meeting-chair-left"),
        furniture("WOODEN_CHAIR_SIDE:left", 26, 18, uid="verdant-meeting-chair-right"),

        furniture("DESK_FRONT", 11, 24, uid="verdant-southwest-desk"),
        furniture("PC_FRONT_ON_1", 12, 23, uid="verdant-southwest-pc"),
        furniture("WOODEN_CHAIR_BACK", 12, 26, uid="verdant-southwest-chair"),
        furniture("DESK_FRONT", 15, 24, uid="verdant-southcenter-desk"),
        furniture("PC_FRONT_ON_2", 16, 23, uid="verdant-southcenter-pc"),
        furniture("WOODEN_CHAIR_BACK", 16, 26, uid="verdant-southcenter-chair"),
        furniture("DESK_FRONT", 23, 24, uid="verdant-southeast-desk"),
        furniture("PC_FRONT_ON_3", 24, 23, uid="verdant-southeast-pc"),
        furniture("WOODEN_CHAIR_BACK", 24, 26, uid="verdant-southeast-chair"),
        furniture("DESK_FRONT", 27, 24, uid="verdant-east-desk"),
        furniture("PC_FRONT_ON_1", 28, 23, uid="verdant-east-pc"),
        furniture("WOODEN_CHAIR_BACK", 28, 26, uid="verdant-east-chair"),
        furniture("FLOWER_PLANTER_LONG", 12, 29),
        furniture("FLOWER_PLANTER_LONG", 23, 29, uid="verdant-flower-planter-right"),

        # AI lab, lower right. The rejected humanoid analysis-platform cell is
        # deliberately absent.  The empty diagnostic platform is the corrected
        # equipment-only replacement, with no character or robot baked in.
        furniture("AI_WHITEBOARD", 31, 13),
        furniture("AI_BOOKSHELF", 35, 13),
        furniture("AI_ELECTRONICS_BENCH", 30, 17),
        furniture("AI_ANALYZER_CART", 36, 18),
        furniture("WOODEN_CHAIR_SIDE", 29, 19),
        furniture("AI_DIAGNOSTIC_PLATFORM", 31, 21),
        furniture("RECYCLING_BIN", 37, 22),

        # South-east quiet lounge and the reference's exterior recycling band.
        furniture("SOFA_FRONT", 35, 27),
        furniture("SOFA_FRONT", 37, 27, uid="verdant-quiet-sofa-right"),
        furniture("COFFEE_TABLE", 36, 29),
        furniture("PLANT", 34, 28, uid="verdant-quiet-plant"),
        furniture("RECYCLING_BIN", 38, 29, uid="verdant-exterior-recycling"),
    ]

    return {
        "version": 1,
        "cols": COLS,
        "rows": ROWS,
        "layoutRevision": 7,
        "tiles": tiles,
        "tileColors": tile_colors,
        "furniture": items,
        "zones": [
            {"id": "solar-wing", "minCol": 2, "maxCol": 11, "minRow": 4, "maxRow": 13},
            {"id": "reception", "minCol": 14, "maxCol": 25, "minRow": 4, "maxRow": 10},
            {"id": "north-lounge", "minCol": 26, "maxCol": 33, "minRow": 4, "maxRow": 10},
            {"id": "cafe", "minCol": 34, "maxCol": 39, "minRow": 3, "maxRow": 12},
            {"id": "west-studio", "minCol": 2, "maxCol": 11, "minRow": 14, "maxRow": 21},
            {"id": "meeting-room", "minCol": 22, "maxCol": 28, "minRow": 13, "maxRow": 21},
            {"id": "greenhouse", "minCol": 2, "maxCol": 9, "minRow": 19, "maxRow": 31},
            {"id": "south-workstations", "minCol": 10, "maxCol": 29, "minRow": 22, "maxRow": 31},
            {"id": "ai-lab", "minCol": 29, "maxCol": 39, "minRow": 13, "maxRow": 25},
            {"id": "quiet-lounge", "minCol": 34, "maxCol": 39, "minRow": 26, "maxRow": 31},
        ],
    }


def main() -> None:
    layout = build()
    OUT.write_text(json.dumps(layout, indent=2) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(layout['furniture'])} furniture, {len(layout['zones'])} zones")


if __name__ == "__main__":
    main()
