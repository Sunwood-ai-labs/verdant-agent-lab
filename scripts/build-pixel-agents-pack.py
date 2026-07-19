#!/usr/bin/env python3
"""Split an Image Gen master sheet into exact Pixel Agents sprite canvases."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/generated/pixel-agents-v1/alpha/office-essentials-sheet.png"
SPLIT = ROOT / "assets/generated/pixel-agents-v1/split"
PACK = ROOT / "pixel-agents-pack/assets/furniture"

ASSETS = (
    # folder, id, measured connected-component bbox in the alpha master, runtime size
    ("DESK", "DESK_FRONT", (104, 160, 591, 417), (48, 32)),
    ("DESK", "DESK_SIDE", (759, 122, 921, 430), (16, 64)),
    ("WOODEN_CHAIR", "WOODEN_CHAIR_FRONT", (1176, 141, 1361, 425), (16, 32)),
    ("WOODEN_CHAIR", "WOODEN_CHAIR_BACK", (241, 613, 423, 882), (16, 32)),
    ("WOODEN_CHAIR", "WOODEN_CHAIR_SIDE", (741, 613, 919, 882), (16, 32)),
    ("PLANT", "PLANT", (1176, 584, 1340, 889), (16, 32)),
)


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("cell has no visible pixels")
    return bbox


def fit_nearest(sprite: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Fit visible pixels with a one-pixel safety border and no distortion."""
    target_w, target_h = size
    sprite = sprite.crop(alpha_bbox(sprite))
    inner_w, inner_h = target_w - 2, target_h - 2
    scale = min(inner_w / sprite.width, inner_h / sprite.height)
    width = max(1, round(sprite.width * scale))
    height = max(1, round(sprite.height * scale))
    sprite = sprite.resize((width, height), Image.Resampling.NEAREST)
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    x = max(1, (target_w - width) // 2)
    y = target_h - height - 1
    canvas.alpha_composite(sprite, (x, y))
    pixels = canvas.load()
    for py in range(target_h):
        for px in range(target_w):
            r, g, b, a = pixels[px, py]
            if a and r > 100 and b > 100 and g < 60 and r > g * 1.5 and b > g * 1.5:
                pixels[px, py] = (0, 0, 0, 0)
    return canvas


def main() -> None:
    source = Image.open(SOURCE).convert("RGBA")
    if source.size != (1536, 1024):
        raise ValueError(f"unexpected source size: {source.size}")

    SPLIT.mkdir(parents=True, exist_ok=True)
    for folder, asset_id, source_bbox, size in ASSETS:
        clean = source.crop(source_bbox)
        bbox = alpha_bbox(clean)
        clean = clean.crop(bbox)
        clean.save(SPLIT / f"{asset_id}.png")

        runtime = fit_nearest(clean, size)
        destination = PACK / folder
        destination.mkdir(parents=True, exist_ok=True)
        runtime.save(destination / f"{asset_id}.png")

        runtime_bbox = runtime.getchannel("A").getbbox()
        print(f"{asset_id}: source_bbox={bbox} runtime={size} alpha_bbox={runtime_bbox}")


if __name__ == "__main__":
    main()
