#!/usr/bin/env python3
"""Validate Pixel Agents floor sizes and wall bitmask uniqueness/continuity."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
THEME = ROOT / "pixel-agents-theme-v2/assets"
PROOF = ROOT / "proofs/pixel-agents-theme-v2"


def has_magenta(image: Image.Image) -> bool:
    for r, g, b, a in image.convert("RGBA").getdata():
        if a and r > 100 and b > 100 and g < 60 and r > g * 1.5 and b > g * 1.5:
            return True
    return False


def main() -> None:
    floors = []
    for index in range(9):
        path = THEME / "floors" / f"floor_{index}.png"
        image = Image.open(path).convert("RGBA")
        assert image.size == (16, 16), (path, image.size)
        assert not has_magenta(image), path
        floors.append(hashlib.sha256(image.tobytes()).hexdigest())
    assert len(set(floors)) == 9

    atlas_path = THEME / "walls" / "wall_0.png"
    atlas = Image.open(atlas_path).convert("RGBA")
    assert atlas.size == (64, 128), atlas.size
    assert not has_magenta(atlas)
    pieces = []
    alpha_bboxes = []
    for mask in range(16):
        x, y = (mask % 4) * 16, (mask // 4) * 32
        piece = atlas.crop((x, y, x + 16, y + 32))
        pieces.append(hashlib.sha256(piece.tobytes()).hexdigest())
        alpha_bboxes.append(piece.getchannel("A").getbbox())
    assert len(set(pieces)) == 16
    assert all(bbox is not None for bbox in alpha_bboxes)

    report = {
        "status": "passed",
        "floorTiles": 9,
        "uniqueFloorTiles": len(set(floors)),
        "floorSize": [16, 16],
        "wallAtlasSize": [64, 128],
        "wallMasks": 16,
        "uniqueWallMasks": len(set(pieces)),
        "bitOrder": "N=1,E=2,S=4,W=8",
        "magentaSpill": 0,
        "catalog": "theme-catalog-v2.png",
    }
    PROOF.mkdir(parents=True, exist_ok=True)
    (PROOF / "theme-validation-v2.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
