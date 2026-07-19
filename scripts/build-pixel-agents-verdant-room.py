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

    # The cafe gets a green rug-like field. Reception stays on warm timber.
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

    # Greenhouse foundation.
    for row in range(19, 32):
        for col in range(2, 11):
            put(col, row, SOFT_FLOOR, LOUNGE_COLOR)

    items = [
        # Solar wing, upper left. Panel and frame are separate catalog assets;
        # the room uses the panel variant directly because it already includes
        # a readable outer rim at 16px scale.
        furniture("SOLAR_PANEL", 2, 8),
        furniture("SOLAR_DASHBOARD", 5, 8),
        furniture("SOLAR_BATTERY_BANK", 5, 10),
        furniture("SOLAR_CONTROLLER", 11, 10),
        furniture("SOLAR_PLANTER", 2, 14),

        # Source-specific reception, upper center. Small pieces are intentionally
        # layered on the counter surface by Pixel Agents' surface placement.
        furniture("RECEPTION_COUNTER", 15, 10),
        furniture("RECEPTION_MONITOR", 17, 9),
        furniture("RECEPTION_TERMINAL", 19, 10),
        furniture("RECEPTION_PAPERS", 20, 10),
        furniture("RECEPTION_PLANTER", 16, 13),
        furniture("RECEPTION_EASEL", 23, 10),
        furniture("WOODEN_CHAIR_BACK", 18, 13),
        furniture("PLANT_2", 25, 12),

        # Cafe, upper right.
        furniture("CAFE_LIVING_WALL", 34, 7),
        furniture("CAFE_PLANT_SHELF", 28, 8),
        furniture("CAFE_COUNTER", 28, 11),
        furniture("CAFE_DISPENSERS", 29, 10),
        furniture("CAFE_FRIDGE", 34, 11),
        furniture("CAFE_KIOSK", 37, 10),
        furniture("COFFEE", 31, 11),
        furniture("PLANT", 39, 13),

        # Greenhouse, lower left. Left/right roof pieces remain individually
        # placeable catalog variants; this composition uses the ridge assembly.
        furniture("GREENHOUSE_ROOF", 2, 19),
        furniture("GREENHOUSE_GLASS_WALL", 2, 23),
        furniture("GREENHOUSE_DOOR", 5, 23),
        furniture("GREENHOUSE_PLANT_SHELF", 2, 28),
        furniture("HANGING_PLANT", 9, 24),

        # Collaboration and two desk islands, lower center.
        furniture("TABLE_FRONT", 11, 20),
        furniture("WOODEN_CHAIR_SIDE", 10, 21),
        furniture("WOODEN_CHAIR_SIDE:left", 14, 21),
        furniture("WOODEN_CHAIR_FRONT", 12, 24),
        furniture("DESK_FRONT", 16, 20),
        furniture("PC_FRONT_ON_1", 17, 19),
        furniture("WOODEN_CHAIR_BACK", 17, 22),
        furniture("DESK_FRONT", 23, 20),
        furniture("PC_FRONT_ON_2", 24, 19),
        furniture("WOODEN_CHAIR_BACK", 24, 22),

        # Source-facing lounge below the work islands.  The sectional and oval
        # table are generated as whole, grid-sized objects so the composition
        # does not depend on a loose cluster of generic sofa fragments.
        furniture("LOUNGE_SECTIONAL", 23, 27),
        furniture("LOUNGE_OVAL_TABLE", 24, 29),
        furniture("FLOWER_PLANTER_LONG", 12, 29),

        # The glass module follows the source image's central-right meeting-room
        # boundary.  Its two background rows leave the aisle visually enclosed
        # without turning the full four-row sprite into a collision wall.
        furniture("MEETING_GLASS_MODULE", 23, 16),

        # AI lab, lower right. The rejected humanoid analysis-platform cell is
        # deliberately absent.  The empty diagnostic platform is the corrected
        # equipment-only replacement, with no character or robot baked in.
        furniture("AI_WHITEBOARD", 30, 18),
        furniture("AI_BOOKSHELF", 34, 18),
        furniture("AI_ELECTRONICS_BENCH", 30, 22),
        furniture("AI_ANALYZER_CART", 36, 22),
        furniture("WOODEN_CHAIR_SIDE", 29, 23),
        furniture("AI_DIAGNOSTIC_PLATFORM", 31, 26),
        furniture("RECYCLING_BIN", 37, 28),
    ]

    return {
        "version": 1,
        "cols": COLS,
        "rows": ROWS,
        "layoutRevision": 6,
        "tiles": tiles,
        "tileColors": tile_colors,
        "furniture": items,
        "zones": [
            {"id": "solar-wing", "minCol": 2, "maxCol": 13, "minRow": 8, "maxRow": 15},
            {"id": "reception", "minCol": 14, "maxCol": 27, "minRow": 8, "maxRow": 15},
            {"id": "cafe", "minCol": 28, "maxCol": 39, "minRow": 8, "maxRow": 15},
            {"id": "greenhouse", "minCol": 2, "maxCol": 10, "minRow": 18, "maxRow": 31},
            {"id": "open-office-lounge", "minCol": 11, "maxCol": 29, "minRow": 18, "maxRow": 31},
            {"id": "ai-lab", "minCol": 30, "maxCol": 39, "minRow": 18, "maxRow": 31},
        ],
    }


def main() -> None:
    layout = build()
    OUT.write_text(json.dumps(layout, indent=2) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(layout['furniture'])} furniture, {len(layout['zones'])} zones")


if __name__ == "__main__":
    main()
