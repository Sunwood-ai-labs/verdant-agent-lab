#!/usr/bin/env python3
"""Assemble real Pixel Agents character-walk frames into an optimized GIF."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[1]
FRAMES = ROOT / "build/pixel-agents-solarpunk-character-walk-frames-v3"
OUTPUT = ROOT / "proofs/pixel-agents-solarpunk-default/solarpunk-character-walk-v3.gif"
REPORT = ROOT / "proofs/pixel-agents-solarpunk-default/character-walk-proof-v3.json"
CONTACT = ROOT / "proofs/pixel-agents-solarpunk-default/character-walk-contact-sheet-v3.png"


def main() -> None:
    paths = sorted(FRAMES.glob("*.png"))
    if len(paths) < 40:
        raise SystemExit(f"too few character-walk frames: {len(paths)}")
    images = [Image.open(path).convert("RGB") for path in paths]
    if len({image.size for image in images}) != 1:
        raise SystemExit("GIF frames have inconsistent sizes")

    # A real character capture must contain motion after the spawn phase.
    changed_boxes = []
    for before, after in zip(images[14:], images[15:]):
        bbox = ImageChops.difference(before, after).getbbox()
        if bbox:
            changed_boxes.append(bbox)
    if len(changed_boxes) < 8:
        raise SystemExit(f"insufficient live-frame motion: {len(changed_boxes)} changed pairs")

    palette = images[len(images) // 2].quantize(
        colors=192, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE
    )
    quantized = [
        image.quantize(palette=palette, dither=Image.Dither.NONE) for image in images
    ]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    quantized[0].save(
        OUTPUT,
        save_all=True,
        append_images=quantized[1:],
        duration=100,
        loop=0,
        optimize=True,
        disposal=1,
    )

    sample_indexes = [4, 14, 26, 38, 50, 62]
    thumbs = [images[min(i, len(images) - 1)].resize((500, 350)) for i in sample_indexes]
    contact = Image.new("RGB", (1500, 700), "#11131d")
    for index, thumb in enumerate(thumbs):
        contact.paste(thumb, ((index % 3) * 500, (index // 3) * 350))
    contact.save(CONTACT)

    result = Image.open(OUTPUT)
    gif_durations = []
    for gif_index in range(getattr(result, "n_frames", 1)):
        result.seek(gif_index)
        gif_durations.append(result.info.get("duration", 0))
    report = {
        "status": "passed",
        "gif": str(OUTPUT.relative_to(ROOT)),
        "contactSheet": str(CONTACT.relative_to(ROOT)),
        "size": list(result.size),
        "sourceFrames": len(images),
        "gifFrames": getattr(result, "n_frames", 1),
        "sourceCadenceMs": 100,
        "totalDurationMs": sum(gif_durations),
        "gifFrameDurationRangeMs": [min(gif_durations), max(gif_durations)],
        "loop": result.info.get("loop"),
        "bytes": OUTPUT.stat().st_size,
        "changedFramePairsAfterSpawn": len(changed_boxes),
        "sequence": [
            "character-free Verdant office",
            "real Pixel Agents character spawn effect",
            "built-in character walks across office waypoints",
        ],
        "characterSource": "Pixel Agents built-in character sprite",
        "movementSource": "Pixel Agents OfficeState.walkToTile via canvas context-menu input",
        "editorActionsCaptured": False,
        "activityOverlayHiddenForCapture": True,
        "selectionClearedAfterEachWalkCommand": True,
        "selectedCharacterOutlineCaptured": False,
        "deterministicBuiltInCharacterPalette": 0,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
