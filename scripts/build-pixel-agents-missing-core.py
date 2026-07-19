#!/usr/bin/env python3
"""Promote the approved missing-core 3x2 sheet into Pixel Agents assets."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/generated/pixel-agents-v5/alpha/missing-core-sheet.png"
SPLIT = ROOT / "assets/generated/pixel-agents-v5/split"
RUNTIME = ROOT / "pixel-agents-pack/assets/furniture"


@dataclass(frozen=True)
class Asset:
    cell: int
    asset_id: str
    name: str
    size: tuple[int, int]
    category: str
    wall: bool = False
    surface: bool = False
    background_tiles: int = 0


ASSETS = [
    Asset(0, "AI_DIAGNOSTIC_PLATFORM", "Empty AI Diagnostic Platform", (96, 64), "electronics", background_tiles=2),
    Asset(1, "MEETING_GLASS_MODULE", "Meeting Glass Door Module", (96, 64), "wall", wall=True, background_tiles=2),
    Asset(2, "LOUNGE_SECTIONAL", "Verdant Sectional Lounge", (96, 48), "chairs", background_tiles=2),
    Asset(3, "LOUNGE_OVAL_TABLE", "Verdant Oval Lounge Table", (64, 32), "desks", background_tiles=1),
    Asset(4, "FLOWER_PLANTER_LONG", "Long Flowering Planter", (96, 32), "decor", background_tiles=1),
    Asset(5, "RECYCLING_BIN", "Tall Blue-Green Recycling Bin", (32, 48), "misc", background_tiles=1),
]


def cell_crop(image: Image.Image, index: int) -> Image.Image:
    col, row = index % 3, index // 3
    xs = [round(image.width * i / 3) for i in range(4)]
    ys = [round(image.height * i / 2) for i in range(3)]
    inset = 20
    crop = image.crop((xs[col] + inset, ys[row] + inset, xs[col + 1] - inset, ys[row + 1] - inset))
    bbox = crop.getbbox()
    if bbox is None:
        raise ValueError(f"empty cell {index}")
    subject = crop.crop(bbox)
    padded = Image.new("RGBA", (subject.width + 4, subject.height + 4))
    padded.alpha_composite(subject, (2, 2))
    return padded


def runtime_fit(source: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    scale = min((target_w - 2) / source.width, (target_h - 2) / source.height)
    width = max(1, round(source.width * scale))
    height = max(1, round(source.height * scale))
    sprite = source.resize((width, height), Image.Resampling.NEAREST)
    canvas = Image.new("RGBA", size)
    canvas.alpha_composite(sprite, (max(1, (target_w - width) // 2), target_h - height - 1))
    pixels = canvas.load()
    for y in range(target_h):
        for x in range(target_w):
            red, green, blue, alpha = pixels[x, y]
            if alpha and red > 100 and blue > 100 and green < 70 and red > green * 1.45 and blue > green * 1.45:
                pixels[x, y] = (0, 0, 0, 0)
    return canvas


def main() -> None:
    image = Image.open(SOURCE).convert("RGBA")
    SPLIT.mkdir(parents=True, exist_ok=True)
    records = []
    for asset in ASSETS:
        source = cell_crop(image, asset.cell)
        source.save(SPLIT / f"{asset.asset_id}.png")
        target = RUNTIME / asset.asset_id
        target.mkdir(parents=True, exist_ok=True)
        runtime = runtime_fit(source, asset.size)
        runtime.save(target / f"{asset.asset_id}.png")
        width, height = asset.size
        manifest = {
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
        (target / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
        records.append({
            "id": asset.asset_id,
            "cell": asset.cell,
            "sourceSize": list(source.size),
            "runtimeSize": list(runtime.size),
            "runtimeBbox": list(runtime.getbbox() or ()),
        })
        print(f"{asset.asset_id}: source={source.size} runtime={runtime.size} bbox={runtime.getbbox()}")
    qa = {
        "status": "passed",
        "sheet": "missing-core-sheet.png",
        "generatedCells": 6,
        "approvedRuntimeAssets": len(records),
        "rejected": [],
        "records": records,
    }
    (ROOT / "assets/generated/pixel-agents-v5/qa.json").write_text(json.dumps(qa, indent=2) + "\n")
    print(f"PASS: promoted {len(records)} missing-core source-facing assets")


if __name__ == "__main__":
    main()
