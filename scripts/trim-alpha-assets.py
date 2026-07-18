#!/usr/bin/env python3
"""Copy alpha sprites into a clean bank cropped to their visible bounds."""

import argparse
import json
from pathlib import Path

from PIL import Image


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mapping", required=True, help="JSON object: destination name -> source path")
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    mapping = json.loads((root / args.mapping).read_text())
    output = root / args.out_dir
    output.mkdir(parents=True, exist_ok=True)

    report = []
    for destination_name, source_path in mapping.items():
        source = root / source_path
        image = Image.open(source).convert("RGBA")
        bounds = image.getchannel("A").getbbox()
        if not bounds:
            raise ValueError(f"empty alpha sprite: {source}")
        trimmed = image.crop(bounds)
        destination = output / destination_name
        trimmed.save(destination)
        report.append(
            {
                "source": str(source.relative_to(root)),
                "output": str(destination.relative_to(root)),
                "before": list(image.size),
                "after": list(trimmed.size),
                "bounds": list(bounds),
            }
        )

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
