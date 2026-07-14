# Image Gen prompt record

Execution mode: built-in Image Gen. The local CLI fallback was not used.

## Clean scene — pass 1

```text
Use case: precise-object-edit
Asset type: responsive HTML scene background for a pixel-art website
Input images: Image 1 is the edit target and must remain the exact composition anchor.
Primary request: remove every character-like figure from the scene: all human pixel sprites, all humanoid robot figures, and all mascot/cartoon creature drawings or logos. Naturally reconstruct the furniture, floorboards, rugs, walls, counters, desks, chairs, plants, lab equipment, windows, glass partitions, shelves, and signs behind them.
Style/medium: preserve the original crisp detailed 32-bit pixel-art/isometric game-environment style exactly.
Composition/framing: preserve the exact 4:3 canvas, top-down isometric viewpoint, building footprint, room layout, furniture placement, exterior garden border, and entrance stairs.
Lighting/mood: preserve the original warm indoor lighting, shadows, and rich green garden atmosphere.
Constraints: change only the character-like figures and the tiny areas directly occluded by them; keep all architecture, objects, text panels, plants, solar panel, greenhouse, desks, cafe, lab, server racks, recycling bins, paths, colors, scale, and camera angle unchanged. No new objects. No people. No characters. No robots. No mascots. No watermark. Preserve the original image resolution and aspect ratio.
```

## Clean scene — pass 2

```text
Use case: precise-object-edit
Asset type: final responsive HTML scene background
Input images: Image 1 is the current nearly-finished edit target.
Primary request: remove only the single remaining white humanoid robot standing in the upper-right AI laboratory room, on the circular work platform beside the lab bench. Reconstruct the circular platform, machine parts, wall diagram, floor, and nearby bench naturally behind it.
Constraints: change only that one humanoid robot and the pixels it occludes. Preserve absolutely everything else unchanged: exact 4:3 composition, architecture, furniture, all plants, text, signs, solar panel, greenhouse, desks, cafe, server racks, recycling bins, lighting, palette, pixel-art style, image framing, and resolution/aspect ratio. Do not remove the small non-humanoid equipment carts or lab instruments. No people, no humanoid robots, no mascot figures, no characters, no new objects, no watermark.
```

## Shared sprite-sheet constraints

All three pack prompts use this contract:

```text
Style/medium: crisp original 32-bit pixel art, top-down three-quarter/isometric view, consistent scale, warm wood-and-moss palette.
Composition/framing: exactly 12 separate objects in a clean evenly spaced 4x3 sprite-sheet grid; each object centered in its own equal cell with generous empty padding and no overlap.
Scene/backdrop: perfectly flat solid #ff00ff chroma-key background for local removal.
Constraints: no people, no characters, no humanoid robots, no mascots, no logos, no labels, no readable text, no watermark; one uniform background; do not use #ff00ff inside objects; crisp pixel edges; every sprite fully contained.
```

## Furniture object list

```text
curved wooden reception desk; rectangular shared wooden worktable; compact
single wooden desk; olive-green two-seat sofa; olive-green armchair; round
wooden coffee table; black rolling office chair; wooden bookshelf; low flower
planter; tall potted indoor plant; glass meeting-room wall segment; greenhouse
glass door segment
```

## Technology object list

```text
blue solar panel on wooden mount; dark server rack with green status lights;
single flat monitor; dual-monitor screens; slim laptop; keyboard and mouse;
brass desk lamp; icon-only environmental display; AI lab console; circular
robotics test platform without robot; espresso machine; three recycling bins
```

## Desk-prop object list

```text
ceramic coffee mug; reusable water bottle; open blank notebook; two closed blank
books; dark blank-screen tablet; label-free desk phone; wooden pen cup; blank
paper and sticky notes; small succulent; leafy desk plant; number-free wall
clock; warm hanging pendant lamp
```

## Prompting lessons

- Use one category per sheet to maintain coherent scale.
- Require an exact grid and cell count; do not use a vague collage request.
- Repeat the character/text/logo prohibition for every sheet.
- Keep text out of reusable sprites; add UI labels in HTML.
- Preserve source and alpha masters so later masking improvements remain possible.

## Single-object replacement — curved reception desk

```text
Create one original reusable pixel-art game asset on a perfectly flat solid
#FF00FF chroma-key background: a single curved wooden reception desk, top-down
3/4 orthographic view, warm oak panels, subtle brass trim, broad semicircular
counter, empty clean desktop. Exactly one centered fully visible object. No
chair, person, character, plant, laptop, phone, mug, stationery, wall, floor,
text, logo, shadow outside the object, border, or checkerboard.
```

## Single-object replacement — shared worktable

```text
Create one original reusable pixel-art game asset on a perfectly flat solid
#FF00FF chroma-key background: a single long rectangular shared wooden
worktable, top-down 3/4 orthographic view, warm oak surface, sturdy simple legs,
empty clean tabletop, designed for independently placed chairs and props.
Exactly one centered fully visible object. No chair, bench, plant, planter,
monitor, laptop, keyboard, mug, book, stationery, person, character, floor,
wall, text, logo, or checkerboard.
```

## Rejected cleanup attempt

The espresso-machine semantic edit requested preservation of the original
transparent 362×362 sprite while removing only the far-right fragment. The
result changed scale and baked a checkerboard into the raster. It remains under
`assets/intermediate/sprite-cleanup/` as negative evidence and was replaced by
the deterministic alpha-mask repair.
