#!/usr/bin/env python3
"""Build a connected Pixel Agents solarpunk floor/wall theme.

Creative texture sources remain the built-in Image Gen masters from the v3
theme batch.  This script is deterministic: it crops/resizes those textures and
constructs sixteen distinct N/E/S/W wall pieces in Pixel Agents bitmask order.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "assets/generated/pixel-agents-v3/raw"
ALPHA = ROOT / "assets/generated/pixel-agents-v3/alpha"
SPLIT = ROOT / "assets/generated/pixel-agents-theme-v2/split"
THEME = ROOT / "pixel-agents-theme-v2/assets"
PROOF = ROOT / "proofs/pixel-agents-theme-v2"

TILE = 16
WALL_H = 32
OUTLINE = (45, 34, 24, 255)
BRASS = (185, 139, 52, 255)


def nearest_crop(image: Image.Image, box: tuple[int, int, int, int], size: tuple[int, int]) -> Image.Image:
    return image.crop(box).resize(size, Image.Resampling.NEAREST).convert("RGBA")


def build_floors() -> list[Image.Image]:
    source = Image.open(RAW / "floors-3x3.png").convert("RGBA")
    if source.width % 3 or source.height % 3:
        raise ValueError(f"floor sheet is not divisible 3x3: {source.size}")
    cell_w, cell_h = source.width // 3, source.height // 3
    out = THEME / "floors"
    out.mkdir(parents=True, exist_ok=True)
    SPLIT.mkdir(parents=True, exist_ok=True)
    tiles: list[Image.Image] = []
    for index in range(9):
        col, row = index % 3, index // 3
        cell = source.crop((col * cell_w, row * cell_h, (col + 1) * cell_w, (row + 1) * cell_h))
        cell.save(SPLIT / f"floor_{index}-source.png")
        tile = cell.resize((TILE, TILE), Image.Resampling.NEAREST).convert("RGBA")
        tile.save(out / f"floor_{index}.png")
        tiles.append(tile)
        print(f"floor_{index}: source={cell.size} runtime={tile.size}")
    return tiles


def build_wall_piece(mask: int, cap: Image.Image, face: Image.Image) -> Image.Image:
    north, east, south, west = (bool(mask & bit) for bit in (1, 2, 4, 8))
    piece = Image.new("RGBA", (TILE, WALL_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(piece)

    # Top eight pixels form the living cap. A south connection continues the
    # cap material downward; a free south edge exposes the wood wall face.
    piece.alpha_composite(cap.crop((0, 0, TILE, 8)), (0, 0))
    if south:
        for y in range(8, WALL_H, 8):
            piece.alpha_composite(cap.crop((0, 0, TILE, min(8, WALL_H - y))), (0, y))
    else:
        piece.alpha_composite(face, (0, 8))

    # The E+S+W T-junction needs a visible front face below the crossing bar,
    # matching the way Pixel Agents exposes the open south-facing wall face.
    if mask == 14:
        piece.alpha_composite(face.crop((0, 8, TILE, 24)), (0, 16))

    # Connection-aware outline. E/W openings remain open in the cap band; a
    # south-running wall closes its vertical stem below that band.
    if not north:
        draw.line((0, 0, TILE - 1, 0), fill=OUTLINE)
    if not west:
        draw.line((0, 0, 0, WALL_H - 1), fill=OUTLINE)
    elif south:
        draw.line((0, 8, 0, WALL_H - 1), fill=OUTLINE)
    if not east:
        draw.line((TILE - 1, 0, TILE - 1, WALL_H - 1), fill=OUTLINE)
    elif south:
        draw.line((TILE - 1, 8, TILE - 1, WALL_H - 1), fill=OUTLINE)
    if not south:
        draw.line((0, WALL_H - 1, TILE - 1, WALL_H - 1), fill=OUTLINE)

    # A narrow brass rail distinguishes the solarpunk theme without breaking
    # joins; only free south-facing wall fronts receive it.
    if not south:
        draw.line((1, 7, TILE - 2, 7), fill=BRASS)
    return piece


def build_walls() -> list[Image.Image]:
    source = Image.open(ALPHA / "wall-panel.png").convert("RGBA")
    bbox = source.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("wall panel is empty")
    panel = source.crop(bbox)
    panel.save(SPLIT / "wall-panel-source.png")

    # Living cap: upper plant field, excluding the lower emblem. Wall face:
    # dark wood floor swatch, already generated from the same two references.
    cap = nearest_crop(panel, (0, 0, panel.width, int(panel.height * 0.62)), (TILE, 8))
    wood = Image.open(SPLIT / "floor_8-source.png").convert("RGBA")
    face = wood.resize((TILE, 24), Image.Resampling.NEAREST)
    cap.save(SPLIT / "wall-cap-16x8.png")
    face.save(SPLIT / "wall-face-16x24.png")

    pieces = [build_wall_piece(mask, cap, face) for mask in range(16)]
    atlas = Image.new("RGBA", (64, 128), (0, 0, 0, 0))
    for mask, piece in enumerate(pieces):
        atlas.alpha_composite(piece, ((mask % 4) * TILE, (mask // 4) * WALL_H))
        piece.save(SPLIT / f"wall-mask-{mask:02d}.png")
    out = THEME / "walls"
    out.mkdir(parents=True, exist_ok=True)
    atlas.save(out / "wall_0.png")
    print("wall_0: 64x128 atlas, 16 connection-aware pieces")
    return pieces


def build_catalog(floors: list[Image.Image], walls: list[Image.Image]) -> None:
    PROOF.mkdir(parents=True, exist_ok=True)
    scale = 6
    canvas = Image.new("RGBA", (1120, 760), (8, 20, 13, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((32, 24), "VERDANT PIXEL AGENTS THEME V2", fill=(224, 246, 220, 255))
    draw.text((32, 48), "9 floor tiles + 16 N/E/S/W wall masks", fill=(140, 184, 148, 255))
    for index, tile in enumerate(floors):
        x = 32 + (index % 9) * 116
        y = 90
        canvas.alpha_composite(tile.resize((TILE * scale, TILE * scale), Image.Resampling.NEAREST), (x, y))
        draw.text((x, y + TILE * scale + 8), f"F{index}", fill=(190, 221, 190, 255))
    for mask, piece in enumerate(walls):
        x = 32 + (mask % 8) * 132
        y = 250 + (mask // 8) * 226
        canvas.alpha_composite(piece.resize((TILE * scale, WALL_H * scale), Image.Resampling.NEAREST), (x, y))
        label = f"M{mask:02d} N{int(bool(mask&1))}E{int(bool(mask&2))}S{int(bool(mask&4))}W{int(bool(mask&8))}"
        draw.text((x, y + WALL_H * scale + 6), label, fill=(190, 221, 190, 255))
    canvas.save(PROOF / "theme-catalog-v2.png")


def main() -> None:
    floors = build_floors()
    walls = build_walls()
    build_catalog(floors, walls)
    print("PASS: built Pixel Agents theme v2")


if __name__ == "__main__":
    main()
