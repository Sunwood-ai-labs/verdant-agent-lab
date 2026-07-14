# Asset generation and extraction pipeline

## Tooling

- Built-in Image Gen for scene edits and new sprite sheets
- `remove_chroma_key.py` from the installed `imagegen` skill
- macOS `sips` for deterministic grid and scene crops
- Pillow for alpha-channel inspection only
- `jq` for manifest validation

## Chroma removal

```bash
python3 /Users/admin/.codex/skills/.system/imagegen/scripts/remove_chroma_key.py \
  --input <sheet-chroma.png> \
  --out <sheet-alpha.png> \
  --auto-key border \
  --soft-matte \
  --transparent-threshold 12 \
  --opaque-threshold 220 \
  --despill
```

Detected source key colors:

| Pack | Detected key | Transparent pixels | Partial-alpha pixels |
|---|---:|---:|---:|
| Furniture | `#fb03fb` | 1,109,770 / 1,572,528 | 31,031 |
| Technology | `#f604f3` | 1,136,370 / 1,572,528 | 20,351 |
| Props | `#f803f2` | 1,234,696 / 1,572,528 | 20,687 |

The model did not return exact `#ff00ff`, so border sampling was essential.
Hard-coding the requested key would have left fringes and holes.

## Grid split

Every generated sheet is 1448×1086 and uses a 4×3 grid.

- cell width: `1448 / 4 = 362`
- cell height: `1086 / 3 = 362`

```bash
y=$((row * 362))
x=$((col * 362))
sips --cropToHeightWidth 362 362 \
  --cropOffset "$y" "$x" \
  assets/generated/<pack>-sheet-alpha.png \
  --out assets/generated/<pack>/<id>.png
```

### `sips` zero-offset pitfall

On this macOS build, some crops with `--cropOffset <y> 0` unexpectedly copied
the full image. Using `x=1` for the first column produced the expected 362×362
crop with a negligible one-pixel shift. Always verify every output dimension
after splitting.

## Alpha validation

```python
from pathlib import Path
from PIL import Image

for path in Path("assets/generated/furniture").glob("*.png"):
    image = Image.open(path).convert("RGBA")
    alpha = image.getchannel("A")
    assert image.size == (362, 362)
    assert any(value == 0 for value in alpha.getdata())
    assert any(value > 0 for value in alpha.getdata())
```

Required gates:

- RGBA output
- transparent corners
- nonzero opaque subject coverage
- no magenta fringe at normal display size
- one object per cell
- no characters, mascots, labels, or watermark

## Cross-cell contamination repair

The second QA pass found neighboring-cell fragments in three otherwise valid
sprites. The original split files are preserved under
`assets/intermediate/sprite-cleanup/`. A semantic Image Gen edit was attempted
for the espresso machine, but the returned checkerboard was baked into the
raster and the scale changed, so that candidate is retained as rejected
evidence and is not used at runtime.

The accepted repair is the deterministic alpha-mask script:

```bash
python3 scripts/clean_sprite_fragments.py
```

It clears only audited rectangles outside each subject and prints the number
of removed nontransparent pixels. The current jobs cover `espresso-machine`,
`shared-worktable`, and `tall-indoor-plant`. Always inspect the resulting PNGs
at original resolution after running it.

## Exact scene crop pipeline

Exact crops are taken from `scene-clean.png`, not from the original reference.
They intentionally retain nearby floor or wall pixels and are stored separately
from transparent sprites.

```bash
sips --cropToHeightWidth <height> <width> \
  --cropOffset <y> <x> \
  assets/scene-clean.png \
  --out assets/object-crops/<id>.png
```

The current inventory has 30 exact object crops, 10 region crops, and 36
transparent generated sprites: 76 addressable assets before counting master
sheets and proof images.
