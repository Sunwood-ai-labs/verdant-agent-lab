#!/usr/bin/env python3
"""Validate Pixel Agents manifest dimensions and safe alpha bounds."""

import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
FURNITURE = ROOT / "pixel-agents-pack/assets/furniture"


def main() -> None:
    seen: set[str] = set()
    failures: list[str] = []
    checked = 0

    for manifest_path in sorted(FURNITURE.glob("*/manifest.json")):
        data = json.loads(manifest_path.read_text())
        members = data.get("members", [data])
        for item in members:
            asset_id = item["id"]
            png_path = manifest_path.parent / item["file"]
            image = Image.open(png_path).convert("RGBA")
            expected = (item["width"], item["height"])
            bbox = image.getchannel("A").getbbox()
            edge_touch = bool(
                bbox
                and (
                    bbox[0] == 0
                    or bbox[1] == 0
                    or bbox[2] == image.width
                    or bbox[3] == image.height
                )
            )
            checks = {
                "unique_id": asset_id not in seen,
                "file_exists": png_path.exists(),
                "manifest_size": image.size == expected,
                "tile_multiple": image.width % 16 == 0 and image.height % 16 == 0,
                "visible": bbox is not None,
                "safe_alpha_border": not edge_touch,
            }
            seen.add(asset_id)
            checked += 1
            failed = [name for name, passed in checks.items() if not passed]
            print(f"{asset_id}: size={image.size} bbox={bbox} checks={checks}")
            if failed:
                failures.append(f"{asset_id}: {', '.join(failed)}")

    if failures:
        raise SystemExit("\n".join(failures))
    print(f"PASS: {checked} sprites across {len(list(FURNITURE.glob('*/manifest.json')))} manifests")


if __name__ == "__main__":
    main()
