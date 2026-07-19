#!/usr/bin/env python3
"""Build Pixel Agents floor_N tiles and wall_0 bitmask atlas from Image Gen masters."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "assets/generated/pixel-agents-v3/raw"
ALPHA = ROOT / "assets/generated/pixel-agents-v3/alpha"
SPLIT = ROOT / "assets/generated/pixel-agents-v3/split"
THEME = ROOT / "pixel-agents-theme/assets"


def remove_magenta(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if a and r > 100 and b > 100 and g < 60 and r > g * 1.5 and b > g * 1.5:
                pixels[x, y] = (0, 0, 0, 0)
    return image


def build_floors() -> None:
    source = Image.open(RAW / "floors-3x3.png").convert("RGBA")
    if source.width % 3 or source.height % 3:
        raise ValueError(f"floor sheet is not divisible 3x3: {source.size}")
    cell_w, cell_h = source.width // 3, source.height // 3
    out = THEME / "floors"
    out.mkdir(parents=True, exist_ok=True)
    SPLIT.mkdir(parents=True, exist_ok=True)
    for index in range(9):
        col, row = index % 3, index // 3
        cell = source.crop((col * cell_w, row * cell_h, (col + 1) * cell_w, (row + 1) * cell_h))
        cell.save(SPLIT / f"floor_{index}-source.png")
        tile = cell.resize((16, 16), Image.Resampling.NEAREST)
        tile.save(out / f"floor_{index}.png")
        print(f"floor_{index}: source={cell.size} runtime={tile.size}")


def build_walls() -> None:
    source = Image.open(ALPHA / "wall-panel.png").convert("RGBA")
    bbox = source.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("wall panel is empty")
    panel_source = source.crop(bbox)
    panel_source.save(SPLIT / "wall-panel-source.png")
    panel = panel_source.resize((16, 32), Image.Resampling.NEAREST)
    panel = remove_magenta(panel)
    atlas = Image.new("RGBA", (64, 128), (0, 0, 0, 0))
    for mask in range(16):
        x, y = (mask % 4) * 16, (mask // 4) * 32
        atlas.alpha_composite(panel, (x, y))
    out = THEME / "walls"
    out.mkdir(parents=True, exist_ok=True)
    atlas.save(out / "wall_0.png")
    print(f"wall_0: panel_source={panel_source.size} atlas={atlas.size} pieces=16")


if __name__ == "__main__":
    build_floors()
    build_walls()
