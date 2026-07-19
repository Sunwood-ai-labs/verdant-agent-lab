#!/usr/bin/env python3
"""Promote approved 3x2 source-zone sheets into Pixel Agents assets.

Creative pixels come from Image Gen.  This script only performs deterministic
cell extraction, alpha-bound trimming, nearest-neighbour runtime scaling, and
manifest emission.  Two AI-lab cells are intentionally omitted because visual
QA found humanoid or robot-like content despite the no-character constraint.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/generated/pixel-agents-v4/alpha"
SPLIT = ROOT / "assets/generated/pixel-agents-v4/split"
RUNTIME = ROOT / "pixel-agents-pack/assets/furniture"


@dataclass(frozen=True)
class Asset:
    sheet: str
    cell: int
    asset_id: str
    name: str
    size: tuple[int, int]
    category: str
    wall: bool = False
    surface: bool = False
    background_tiles: int = 0
    crop_right: float = 1.0


ASSETS = [
    Asset("reception", 0, "RECEPTION_COUNTER", "Curved Verdant Reception Counter", (96, 48), "desks", background_tiles=1),
    Asset("reception", 1, "RECEPTION_PLANTER", "Reception Leaf Planter", (64, 16), "decor"),
    Asset("reception", 2, "RECEPTION_MONITOR", "Reception Monitor Back", (16, 32), "electronics", surface=True, background_tiles=1),
    Asset("reception", 3, "RECEPTION_TERMINAL", "Reception Tablet Terminal", (16, 16), "electronics", surface=True),
    Asset("reception", 4, "RECEPTION_PAPERS", "Reception Clipboard", (16, 16), "decor", surface=True),
    Asset("reception", 5, "RECEPTION_EASEL", "Reception Information Easel", (32, 48), "decor", background_tiles=1),
    Asset("cafe", 0, "CAFE_PLANT_SHELF", "Cafe Six-Plant Shelf", (80, 32), "decor", wall=True),
    Asset("cafe", 1, "CAFE_COUNTER", "Verdant Cafe Counter", (80, 32), "desks", background_tiles=1),
    Asset("cafe", 2, "CAFE_DISPENSERS", "Cafe Triple Dispensers", (48, 32), "electronics", surface=True, background_tiles=1),
    Asset("cafe", 3, "CAFE_FRIDGE", "Cafe Refrigerator", (32, 48), "storage", background_tiles=1),
    Asset("cafe", 4, "CAFE_KIOSK", "Cafe Control Kiosk", (16, 48), "electronics", background_tiles=1),
    Asset("cafe", 5, "CAFE_LIVING_WALL", "Cafe Framed Living Wall", (64, 48), "decor", wall=True),
    # ai-lab cell 0 rejected: it contains a humanoid robot.
    Asset("ai-lab", 1, "AI_ANALYZER_CART", "AI Lab Analyzer Cart", (32, 48), "electronics", background_tiles=1),
    Asset("ai-lab", 2, "AI_BOOKSHELF", "AI Lab Device Bookshelf", (32, 64), "storage", wall=True),
    Asset("ai-lab", 3, "AI_WHITEBOARD", "AI Lab Diagram Board", (48, 48), "wall", wall=True),
    Asset("ai-lab", 4, "AI_ELECTRONICS_BENCH", "AI Lab Electronics Bench", (80, 48), "desks", background_tiles=1),
    # ai-lab cell 5 rejected: the requested sensor still reads as a robot head/body.
    Asset("greenhouse", 0, "GREENHOUSE_ROOF", "Greenhouse Ridge Roof", (96, 64), "wall", background_tiles=2),
    Asset("greenhouse", 1, "GREENHOUSE_ROOF_LEFT", "Greenhouse Left Roof", (64, 64), "wall", background_tiles=2),
    Asset("greenhouse", 2, "GREENHOUSE_ROOF_RIGHT", "Greenhouse Right Roof", (64, 64), "wall", background_tiles=2),
    Asset("greenhouse", 3, "GREENHOUSE_GLASS_WALL", "Greenhouse Glass Wall", (48, 64), "wall", wall=True),
    Asset("greenhouse", 4, "GREENHOUSE_DOOR", "Greenhouse Entrance Door", (32, 64), "wall", wall=True),
    Asset("greenhouse", 5, "GREENHOUSE_PLANT_SHELF", "Greenhouse Grow Shelf", (96, 48), "decor", background_tiles=1),
    Asset("solar", 0, "SOLAR_PANEL", "Six-Module Solar Panel", (48, 80), "decor", background_tiles=2),
    Asset("solar", 1, "SOLAR_FRAME", "Solar Panel Mounting Frame", (48, 80), "misc", background_tiles=2),
    Asset("solar", 2, "SOLAR_DASHBOARD", "Solar Output Dashboard", (48, 32), "electronics", wall=True),
    Asset("solar", 3, "SOLAR_BATTERY_BANK", "Solar Battery Server Bank", (96, 64), "electronics", background_tiles=2),
    Asset("solar", 4, "SOLAR_CONTROLLER", "Solar Controller Cabinet", (32, 48), "electronics", background_tiles=1, crop_right=0.65),
    Asset("solar", 5, "SOLAR_PLANTER", "Solar Wing Vine Planter", (96, 32), "decor", background_tiles=1),
]


def cell_crop(image: Image.Image, index: int) -> Image.Image:
    col, row = index % 3, index // 3
    xs = [round(image.width * i / 3) for i in range(4)]
    ys = [round(image.height * i / 2) for i in range(3)]
    # Generated separators vary from 1-28 px.  Every subject has much larger
    # padding, so a fixed inset safely excludes them without touching content.
    inset = 20
    crop = image.crop((xs[col] + inset, ys[row] + inset, xs[col + 1] - inset, ys[row + 1] - inset))
    # Some Image Gen sheets use opaque white separators.  After the fixed
    # inset, a thin separator remnant can still touch the crop boundary and
    # inflate the alpha bbox.  Remove only alpha components connected to the
    # boundary; centered subjects are intentionally padded and remain intact.
    pixels = crop.load()
    width, height = crop.size
    stack: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()
    for x in range(width):
        stack.extend(((x, 0), (x, height - 1)))
    for y in range(height):
        stack.extend(((0, y), (width - 1, y)))
    while stack:
        x, y = stack.pop()
        if (x, y) in seen or not (0 <= x < width and 0 <= y < height):
            continue
        seen.add((x, y))
        red, green, blue, alpha = pixels[x, y]
        if alpha == 0 or not (red > 225 and green > 225 and blue > 225):
            continue
        pixels[x, y] = (0, 0, 0, 0)
        stack.extend(((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)))
    bbox = crop.getbbox()
    if bbox is None:
        raise ValueError(f"empty cell {index}")
    subject = crop.crop(bbox)
    padded = Image.new("RGBA", (subject.width + 4, subject.height + 4))
    padded.alpha_composite(subject, (2, 2))
    return padded


def runtime_fit(source: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    max_w, max_h = target_w - 2, target_h - 2
    scale = min(max_w / source.width, max_h / source.height)
    width = max(1, round(source.width * scale))
    height = max(1, round(source.height * scale))
    sprite = source.resize((width, height), Image.Resampling.NEAREST)
    canvas = Image.new("RGBA", size)
    x = max(1, (target_w - width) // 2)
    y = target_h - height - 1
    canvas.alpha_composite(sprite, (x, y))

    # Final key-spill gate after resampling.
    pixels = canvas.load()
    for py in range(target_h):
        for px in range(target_w):
            red, green, blue, alpha = pixels[px, py]
            if alpha and red > 100 and blue > 100 and green < 70 and red > green * 1.45 and blue > green * 1.45:
                pixels[px, py] = (0, 0, 0, 0)
    return canvas


def manifest(asset: Asset) -> dict:
    width, height = asset.size
    return {
        "id": asset.asset_id,
        "name": asset.name,
        "category": asset.category,
        "type": "asset",
        "file": f"{asset.asset_id}.png",
        "width": width,
        "height": height,
        "footprintW": width // 16,
        "footprintH": height // 16,
        "canPlaceOnWalls": asset.wall,
        "canPlaceOnSurfaces": asset.surface,
        "backgroundTiles": asset.background_tiles,
    }


def main() -> None:
    SPLIT.mkdir(parents=True, exist_ok=True)
    sheets: dict[str, Image.Image] = {}
    for asset in ASSETS:
        if asset.sheet not in sheets:
            sheets[asset.sheet] = Image.open(SOURCE / f"{asset.sheet}-sheet.png").convert("RGBA")
        source = cell_crop(sheets[asset.sheet], asset.cell)
        if asset.crop_right < 1:
            source = source.crop((0, 0, round(source.width * asset.crop_right), source.height))
            bbox = source.getbbox()
            if bbox is None:
                raise ValueError(f"empty targeted crop for {asset.asset_id}")
            subject = source.crop(bbox)
            source = Image.new("RGBA", (subject.width + 4, subject.height + 4))
            source.alpha_composite(subject, (2, 2))
        source_path = SPLIT / f"{asset.asset_id}.png"
        source.save(source_path)

        target_dir = RUNTIME / asset.asset_id
        target_dir.mkdir(parents=True, exist_ok=True)
        runtime = runtime_fit(source, asset.size)
        runtime.save(target_dir / f"{asset.asset_id}.png")
        (target_dir / "manifest.json").write_text(json.dumps(manifest(asset), indent=2) + "\n")
        print(f"{asset.asset_id}: source={source.size} runtime={runtime.size} bbox={runtime.getbbox()}")

    print(f"PASS: promoted {len(ASSETS)} approved source-zone assets; two AI robot-like cells remain rejected")


if __name__ == "__main__":
    main()
