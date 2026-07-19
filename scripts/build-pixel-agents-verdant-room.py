#!/usr/bin/env python3
"""Build a single-zone Verdant office for the Pixel Agents 42x34 runtime.

This intentionally avoids the upstream four-quadrant demo layout.  The room is
one connected office with distinct reception, lounge, collaboration, workbench,
and AI-lab zones.  Built-in floors/walls remain in use until the custom theme
atlas has passed direct visual QA.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "pixel-agents-pack" / "verdant-runtime-layout.json"
COLS, ROWS = 42, 34
VOID, WALL, SOFT_FLOOR, WOOD_FLOOR = 255, 0, 1, 7

WALL_COLOR = {"h": 214, "s": 30, "b": -100, "c": -55}
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

    # One coherent office shell. Rows 0-6 stay void for the Pixel Agents sign.
    for row in range(7, 33):
        for col in range(1, 41):
            border = row in (7, 32) or col in (1, 40)
            put(col, row, WALL if border else WOOD_FLOOR, WALL_COLOR if border else WOOD_COLOR)

    # The lounge gets a green rug-like field. Reception stays on warm timber.
    for row in range(9, 16):
        for col in range(28, 40):
            put(col, row, SOFT_FLOOR, LOUNGE_COLOR)

    # A continuous circulation spine uses the same quiet plank texture, with a
    # lighter stain instead of the upstream black-and-white checker pattern.
    for row in (16, 17):
        for col in range(2, 40):
            put(col, row, WOOD_FLOOR, AISLE_COLOR)
    for row in range(18, 32):
        for col in (20, 21, 22):
            put(col, row, WOOD_FLOOR, AISLE_COLOR)

    # AI lab area: visually distinct but connected to the aisle.
    for row in range(19, 32):
        for col in range(30, 40):
            put(col, row, SOFT_FLOOR, LAB_COLOR)

    items = [
        # Top living wall / library line.
        furniture("HANGING_PLANT", 2, 7),
        furniture("DOUBLE_BOOKSHELF", 4, 7),
        furniture("SMALL_PAINTING", 8, 7),
        furniture("CLOCK", 10, 7),
        furniture("LARGE_PAINTING", 12, 7),
        furniture("SMALL_PAINTING_2", 37, 7),
        furniture("PLANT_2", 39, 7),

        # Cafe / ideas nook, upper left.
        furniture("SMALL_TABLE_FRONT", 5, 11),
        furniture("WOODEN_CHAIR_SIDE", 4, 11),
        furniture("WOODEN_CHAIR_SIDE:left", 7, 11),
        furniture("COFFEE", 6, 11),
        furniture("WHITEBOARD", 11, 9),
        furniture("PLANT", 2, 13),

        # Reception, upper center. PC intentionally sits on the desk surface.
        furniture("DESK_FRONT", 18, 11),
        furniture("PC_FRONT_OFF", 19, 10),
        furniture("WOODEN_CHAIR_BACK", 19, 13),
        furniture("CUSHIONED_BENCH", 23, 13),
        furniture("PLANT_2", 24, 10),

        # Lounge, upper right: one conversational cluster, no repeated quadrant.
        furniture("SOFA_FRONT", 32, 10),
        furniture("SOFA_SIDE", 30, 12),
        furniture("SOFA_SIDE:left", 35, 12),
        furniture("COFFEE_TABLE", 32, 12),
        furniture("CUSHIONED_BENCH", 32, 15),
        furniture("PLANT", 38, 13),

        # Collaboration table, lower left.
        furniture("TABLE_FRONT", 5, 21),
        furniture("WOODEN_CHAIR_SIDE", 4, 22),
        furniture("WOODEN_CHAIR_SIDE:left", 8, 22),
        furniture("WOODEN_CHAIR_FRONT", 6, 25),
        furniture("PLANT_2", 2, 28),
        furniture("BIN", 3, 30),

        # Two desk islands, lower center, oriented consistently toward the aisle.
        furniture("DESK_FRONT", 13, 21),
        furniture("PC_FRONT_ON_1", 14, 20),
        furniture("WOODEN_CHAIR_BACK", 14, 23),
        furniture("DESK_FRONT", 24, 21),
        furniture("PC_FRONT_ON_2", 25, 20),
        furniture("WOODEN_CHAIR_BACK", 25, 23),
        furniture("SMALL_TABLE_SIDE", 18, 26),
        furniture("PLANT", 18, 29),

        # AI lab, lower right. Side-facing workstation follows the source room.
        furniture("DESK_SIDE", 32, 22),
        furniture("PC_SIDE", 31, 23),
        furniture("WOODEN_CHAIR_SIDE", 30, 23),
        furniture("SMALL_TABLE_FRONT", 35, 25),
        furniture("PC_SIDE:left", 37, 25),
        furniture("PLANT_2", 38, 29),
        furniture("BIN", 36, 30),
    ]

    return {
        "version": 1,
        "cols": COLS,
        "rows": ROWS,
        "layoutRevision": 4,
        "tiles": tiles,
        "tileColors": tile_colors,
        "furniture": items,
        "zones": [
            {"id": "cafe-ideas", "minCol": 2, "maxCol": 14, "minRow": 8, "maxRow": 15},
            {"id": "reception", "minCol": 16, "maxCol": 27, "minRow": 8, "maxRow": 15},
            {"id": "lounge", "minCol": 29, "maxCol": 39, "minRow": 8, "maxRow": 15},
            {"id": "collaboration", "minCol": 2, "maxCol": 10, "minRow": 18, "maxRow": 31},
            {"id": "open-office", "minCol": 11, "maxCol": 29, "minRow": 18, "maxRow": 31},
            {"id": "ai-lab", "minCol": 30, "maxCol": 39, "minRow": 18, "maxRow": 31},
        ],
    }


def main() -> None:
    layout = build()
    OUT.write_text(json.dumps(layout, indent=2) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(layout['furniture'])} furniture, {len(layout['zones'])} zones")


if __name__ == "__main__":
    main()
