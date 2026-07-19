# Pixel Agents compatible office essentials — generation prompt

Generated with the built-in Image Gen tool on 2026-07-19 JST.

References:

- Pixel Agents `webview-ui/public/Screenshot.jpg`: camera direction, sprite density, and game readability only
- private `assets/reference-original.jpg`: warm wood, leaf green, brass, and planted solarpunk design language only

Original prompt intent:

- original art; never copy Pixel Agents artwork, characters, layout, logos, or text
- 3 × 2 landscape sheet on solid `#FF00FF`
- top row: desk front, desk side, chair front
- bottom row: chair back, chair side facing right, potted plant
- hard pixel edges, no antialiasing, no baked room/floor/shadows
- keep every object centered and fully inside its cell

The unmodified generation is retained under `raw/`. Chroma removal produces
the `alpha/` master. `scripts/build-pixel-agents-pack.py` creates trimmed
intermediates under `split/` and exact-size runtime sprites under
`pixel-agents-pack/`.
