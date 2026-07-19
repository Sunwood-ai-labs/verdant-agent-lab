#!/usr/bin/env python3
"""Validate Pixel Agents manifest dimensions and safe alpha bounds."""

import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
FURNITURE = ROOT / "pixel-agents-pack/assets/furniture"
REQUIRED_TYPES = ROOT / "pixel-agents-pack/default-layout-required-types.json"


def iter_assets(node: dict):
    if node.get("type") == "asset":
        yield node
        return
    for member in node.get("members", []):
        yield from iter_assets(member)


def main() -> None:
    seen: set[str] = set()
    runtime_ids: set[str] = set()
    failures: list[str] = []
    checked = 0

    for manifest_path in sorted(FURNITURE.glob("*/manifest.json")):
        data = json.loads(manifest_path.read_text())
        for item in iter_assets(data):
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
            magenta_pixels = sum(
                1
                for red, green, blue, alpha in image.getdata()
                if alpha
                and red > 100
                and blue > 100
                and green < 60
                and red > green * 1.5
                and blue > green * 1.5
            )
            checks = {
                "unique_id": asset_id not in seen,
                "file_exists": png_path.exists(),
                "manifest_size": image.size == expected,
                "tile_multiple": image.width % 16 == 0 and image.height % 16 == 0,
                "visible": bbox is not None,
                "safe_alpha_border": not edge_touch,
                "no_magenta_spill": magenta_pixels == 0,
            }
            seen.add(asset_id)
            runtime_ids.add(asset_id)
            if item.get("orientation") == "side" and item.get("mirrorSide"):
                runtime_ids.add(f"{asset_id}:left")
            checked += 1
            failed = [name for name, passed in checks.items() if not passed]
            print(f"{asset_id}: size={image.size} bbox={bbox} checks={checks}")
            if failed:
                failures.append(f"{asset_id}: {', '.join(failed)}")

    if failures:
        raise SystemExit("\n".join(failures))
    required = set(json.loads(REQUIRED_TYPES.read_text()))
    missing = sorted(required - runtime_ids)
    if missing:
        raise SystemExit(f"missing default-layout IDs: {', '.join(missing)}")
    print(
        f"PASS: {checked} sprites across {len(list(FURNITURE.glob('*/manifest.json')))} manifests; "
        f"default-layout coverage {len(required)}/{len(required)}"
    )


if __name__ == "__main__":
    main()
