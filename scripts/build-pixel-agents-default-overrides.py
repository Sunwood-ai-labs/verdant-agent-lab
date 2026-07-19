#!/usr/bin/env python3
"""Build exact-size default-ID overrides from four Image Gen alpha masters."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ALPHA = ROOT / "assets/generated/pixel-agents-v2/alpha"
SPLIT = ROOT / "assets/generated/pixel-agents-v2/split"
PACK = ROOT / "pixel-agents-pack/assets/furniture"

# sheet, folder, asset id, measured connected-component bbox, runtime canvas
ASSETS = (
    ("pc-sheet.png", "PC", "PC_FRONT_OFF", (106, 106, 462, 444), (16, 32)),
    ("pc-sheet.png", "PC", "PC_FRONT_ON_1", (566, 106, 942, 444), (16, 32)),
    ("pc-sheet.png", "PC", "PC_FRONT_ON_2", (1046, 106, 1422, 444), (16, 32)),
    ("pc-sheet.png", "PC", "PC_FRONT_ON_3", (87, 579, 462, 917), (16, 32)),
    ("pc-sheet.png", "PC", "PC_BACK", (581, 579, 962, 917), (16, 32)),
    ("pc-sheet.png", "PC", "PC_SIDE", (1099, 569, 1363, 917), (16, 32)),
    ("lounge-sheet.png", "SOFA", "SOFA_FRONT", (91, 146, 577, 433), (32, 16)),
    ("lounge-sheet.png", "SOFA", "SOFA_BACK", (680, 180, 1141, 433), (32, 16)),
    ("lounge-sheet.png", "SOFA", "SOFA_SIDE", (1258, 145, 1426, 431), (16, 32)),
    ("lounge-sheet.png", "CUSHIONED_BENCH", "CUSHIONED_BENCH", (182, 646, 360, 836), (16, 16)),
    ("lounge-sheet.png", "COFFEE_TABLE", "COFFEE_TABLE", (588, 596, 943, 883), (32, 32)),
    ("lounge-sheet.png", "SMALL_TABLE", "SMALL_TABLE_FRONT", (1126, 585, 1352, 871), (32, 32)),
    ("storage-sheet.png", "SMALL_TABLE", "SMALL_TABLE_SIDE", (190, 157, 290, 452), (16, 48)),
    ("storage-sheet.png", "TABLE_FRONT", "TABLE_FRONT", (491, 120, 932, 503), (48, 64)),
    ("storage-sheet.png", "DOUBLE_BOOKSHELF", "DOUBLE_BOOKSHELF", (1072, 159, 1416, 474), (32, 32)),
    ("storage-sheet.png", "HANGING_PLANT", "HANGING_PLANT", (158, 563, 321, 915), (16, 32)),
    ("storage-sheet.png", "PLANT_2", "PLANT_2", (620, 616, 855, 910), (16, 32)),
    ("storage-sheet.png", "BIN", "BIN", (1170, 760, 1279, 906), (16, 16)),
    ("decor-sheet.png", "SMALL_PAINTING", "SMALL_PAINTING", (228, 155, 362, 413), (16, 32)),
    ("decor-sheet.png", "SMALL_PAINTING_2", "SMALL_PAINTING_2", (656, 154, 792, 413), (16, 32)),
    ("decor-sheet.png", "LARGE_PAINTING", "LARGE_PAINTING", (1019, 153, 1402, 412), (32, 32)),
    ("decor-sheet.png", "CLOCK", "CLOCK", (211, 557, 377, 845), (16, 32)),
    ("decor-sheet.png", "COFFEE", "COFFEE", (675, 667, 794, 788), (16, 16)),
    ("decor-sheet.png", "WHITEBOARD", "WHITEBOARD", (1032, 578, 1392, 865), (32, 32)),
)


def fit_nearest(sprite: Image.Image, size: tuple[int, int]) -> Image.Image:
    bbox = sprite.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("empty source component")
    sprite = sprite.crop(bbox)
    target_w, target_h = size
    inner_w, inner_h = target_w - 2, target_h - 2
    scale = min(inner_w / sprite.width, inner_h / sprite.height)
    width = max(1, round(sprite.width * scale))
    height = max(1, round(sprite.height * scale))
    sprite = sprite.resize((width, height), Image.Resampling.NEAREST)
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    canvas.alpha_composite(sprite, (max(1, (target_w - width) // 2), target_h - height - 1))
    pixels = canvas.load()
    for py in range(target_h):
        for px in range(target_w):
            r, g, b, a = pixels[px, py]
            if a and r > 100 and b > 100 and g < 60 and r > g * 1.5 and b > g * 1.5:
                pixels[px, py] = (0, 0, 0, 0)
    return canvas


def main() -> None:
    SPLIT.mkdir(parents=True, exist_ok=True)
    cache: dict[str, Image.Image] = {}
    for sheet, folder, asset_id, source_bbox, size in ASSETS:
        source = cache.setdefault(sheet, Image.open(ALPHA / sheet).convert("RGBA"))
        clean = source.crop(source_bbox)
        split_path = SPLIT / f"{asset_id}.png"
        clean.save(split_path)
        runtime = fit_nearest(clean, size)
        destination = PACK / folder
        destination.mkdir(parents=True, exist_ok=True)
        runtime.save(destination / f"{asset_id}.png")
        print(f"{asset_id}: source={clean.size} runtime={size} alpha={runtime.getchannel('A').getbbox()}")


if __name__ == "__main__":
    main()
