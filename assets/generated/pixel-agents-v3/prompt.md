# Pixel Agents solarpunk floor and wall theme — generation record

Generated with built-in Image Gen on 2026-07-19 JST. Pixel Agents imagery was
used only for scale and camera language; the private office reference supplied
the solarpunk palette and material vocabulary.

- `floors-3x3.png`: nine original quiet, top-down, seamless material swatches
- `wall-panel.png`: one original 1:2 living-wall panel on magenta

`scripts/build-pixel-agents-theme.py` splits the nine floor swatches and
nearest-neighbor resizes them to 16×16 `floor_0.png` through `floor_8.png`. It
chroma-cleans and resizes the wall panel to 16×32, then assembles the exact
64×128 / 16-piece `wall_0.png` format required by Pixel Agents.

Current wall limitation: every bitmask slot uses the same framed living panel.
The atlas is loader-compatible and visually themed, but it does not yet draw
different join geometry for N/E/S/W neighbors. Keep that limitation explicit.
