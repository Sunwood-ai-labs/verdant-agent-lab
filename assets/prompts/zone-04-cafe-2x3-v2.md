# Zone 04 — cafe, 2x3 sheet prompt v2

Use case: stylized-concept

Asset type: source-faithful pixel-office sprite sheet for deterministic splitting.

Input image 1: authoritative Cafe crop from `assets/reference-original.jpg` bbox
`[1023, 36, 1213, 245]`; it defines the exact silhouettes, 3/4 top-down
camera, palette, compact scale, and relative proportions.

Input image 2: rejected v1 sheet; retain only its clean 3-column x 2-row
chroma-sheet organization, not its oversized or ornate designs.

Primary request: regenerate one landscape 3-column x 2-row sheet containing
exactly six separate non-character Cafe assets in row-major order:

1. Compact straight lower wooden counter cabinet, shallow 3/4 top-down view,
   simple three-bay front, no curved bar ends, mugs, or machines.
2. Compact upper greenery wall/window planter fixture with a thin rectangular
   surround, shallow green living-wall panel, and an even row of exactly six small
   pale pots; not a freestanding tall window.
3. Slim short pale-gray left shelf/fridge case matching the left side of the
   reference, with simple small shelves.
4. Taller pale-gray right vending refrigerator with a blue/light product-button
   panel and visible right-side depth; not a dark glass beverage cooler.
5. Three small matching white/silver coffee dispensers side by side, each a
   short countertop box with a round dark opening; no transparent or brown
   chamber, beans, tall espresso body, grinder, hopper, steam wand, or
   floor-standing appliance.
6. Very thin compact blank green horizontal sign strip with a simple warm wood
   border; no letters or symbols because `CAFE` is overlaid deterministically.

Style: crisp small-scale isometric pixel art, consistent 3/4 top-down camera,
low-detail 2–4 pixel clusters, warm wood, pale gray metal, muted green, and
strong silhouettes. Preserve the source-relative scale so the six assets can
recompose into the compact Cafe silhouette.

Backdrop: perfectly flat uniform `#ff00ff`. Exactly one centered asset per
cell, with large empty gutters and no grid lines.

Constraints: no people, hands, characters, floor, walls, adjacent furniture,
shadows, reflections, watermark, logo, readable text, labels, UI, or extra
objects. Never use `#ff00ff` inside an asset. Keep every object clear of all
cell edges. Source fidelity overrides creative embellishment.
