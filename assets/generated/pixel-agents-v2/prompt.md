# Pixel Agents default-office overrides v2 — generation record

Generated with the built-in Image Gen tool on 2026-07-19 JST.

Shared references:

- Pixel Agents `webview-ui/public/Screenshot.jpg`: viewing direction, compact
  pixel density, and runtime readability only
- private `assets/reference-original.jpg`: reclaimed wood, leaf green, brass,
  terracotta, glass, and planted solarpunk design language only

Shared constraints: original art, no copied Pixel Agents artwork, no
characters, landscape 3×2 sheet, flat magenta background, one centered fully
visible object per cell, hard pixel edges, no room/floor background.

## `pc-sheet.png`

PC front-off; front-on frames 1–3; back; right side suitable for runtime mirror.

## `lounge-sheet.png`

Sofa front/back/right side; cushioned bench; coffee table; small table front.

## `storage-sheet.png`

Small table side; communal table; double bookshelf; hanging plant; alternate
plant; recycling bin.

## `decor-sheet.png`

Two small paintings; large landscape; clock; coffee cup; whiteboard.

The raw sheets are unmodified. `alpha/` keeps chroma-removed masters. The decor
sheet used corner-sampled chroma removal because Image Gen rendered the nominal
magenta background as `#f905e1` rather than exact `#ff00ff`. Measured connected
component bounds are encoded in
`scripts/build-pixel-agents-default-overrides.py`; `split/` keeps original-scale
isolated components and `pixel-agents-pack/` keeps 16px-grid runtime exports.
