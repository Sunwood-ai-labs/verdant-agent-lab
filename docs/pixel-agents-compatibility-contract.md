# Pixel Agents compatibility contract

Status: runtime contract confirmed; 58 physical sprites / 61 runtime catalog
entries; live load, composed-room rendering, 28/28 editor-catalog discovery,
direct canvas placement, default-chair seat generation, agent walk/return,
collision rejection, four-way facing, mirror, and seated depth rules confirmed.
Every remaining rotation group still needs its own visual canvas inspection.

## Confirmed contract

- Tile size is exactly 16 px. Sprite width and height are explicit manifest
  values and footprints are expressed in 16 px tiles.
- An external pack has the shape
  `assets/furniture/<item>/manifest.json` plus one or more PNG files.
- Each loaded asset ID must be unique.
- Furniture is placed by integer `col` and `row` in layout version 1.
- A 2-way desk group uses `front` and `side` members.
- A 3-way mirrored chair uses `front`, `back`, and right-facing `side`; the
  runtime derives the left-facing variant from `mirrorSide: true`.
- `backgroundTiles` marks upper footprint rows that do not block placement or
  walking. Tall furniture still uses its full sprite bottom edge for depth.
- Chairs create seats from their footprint. Character facing follows chair
  orientation first, then adjacent desk detection, then the default direction.
- Runtime draw order is sorted by the sprite/character bottom Y coordinate;
  surface-placeable items receive a small offset above their supporting desk.
- External furniture is merged after bundled furniture. Matching asset IDs in
  the external pack replace the bundled catalog/sprite entries, so an existing
  default layout can be reskinned without rewriting its placement records.
- Editor discoverability is limited to `desks`, `chairs`, `storage`,
  `electronics`, `decor`, `wall`, and `misc`. Descriptive custom category names
  can load in a composed layout while silently disappearing from the editor
  catalog, so the source-zone builder restricts manifests to this set.
- The literal default layout produces 14/14 expected seats from 10 chair/sofa
  placements. A real `OfficeState` agent can spawn at an assigned Verdant seat,
  walk 15 tiles without crossing blocked furniture, reject a command into a
  desk footprint, and return to its seat with the declared facing.
- The Verdant chair rotation cycle is front → right → back → mirrored left →
  front. Front/right chairs sort behind a seated character; the back-facing
  chair sorts in front to occlude the character correctly.

## Primary-source evidence

- `docs/external-assets.md:14-31` — external directory layout
- `docs/external-assets.md:33-177` — manifest fields and rotations
- `webview-ui/src/constants.ts:3-8` — 16 px tile and grid limits
- `webview-ui/src/office/types.ts:36-68` — directions and bottom-edge sorting
- `webview-ui/src/office/types.ts:90-131` — catalog and layout types
- `webview-ui/src/office/layout/layoutSerializer.ts:28-97` — positions, z order,
  surface layering, and mirrored side variants
- `webview-ui/src/office/layout/layoutSerializer.ts:102-205` — collision and seats
- `webview-ui/public/assets/default-layout-1.json:54-90` — real placement records
- `server/src/assetLoader.ts:49-55` and
  `adapters/vscode/PixelAgentsViewProvider.ts:711-721` — external override order

Reference checkout audited at commit `928ccd463bf516d67e0700af7e767ca083f795d8`.
The checkout is read-only reference material and remains outside the new pack.

## Solarpunk replacement mapping

The first checkpoint replaces the primary workstation grammar, not the whole
office:

| Pixel Agents role | Original replacement | Runtime files |
|---|---|---|
| 3×2 / 1×4 desk | Verdant wood-and-vine desk | `DESK_*` override |
| 1×2 rotatable chair | Leaf-green brass chair | `WOODEN_CHAIR_*` override |
| 1×2 plant | Terracotta/brass planted foliage | `PLANT.png` override |

The default furniture IDs now have full audited coverage. Source-facing
reception, cafe, greenhouse, solar, and equipment-only AI-lab batches are also
available as independent grid assets. The remaining visual gap is the site
shell, directional studio/lounge variants, a robot-free diagnostic platform,
and a validated floor/wall bitmask atlas.

## Acceptance gate

Do not call an asset Pixel Agents compatible from HTML appearance alone. It
must pass all of the following:

1. PNG dimensions equal manifest dimensions and are 16 px-grid multiples.
2. Every visible alpha pixel stays inside the canvas; no edge clipping is hidden.
3. The pack loads through Pixel Agents external asset loading.
4. Each orientation is rotated in the editor and inspected in the actual canvas.
5. A chair spawns a usable seat and the character faces the intended desk.
6. Collision and depth order are checked with an agent walking around and
   sitting at the furniture.

For the default-office Verdant chair, gates 5–6 and the four-way runtime cycle
now pass through the actual Pixel Agents modules. Gate 4 is visually proven for
the Verdant Desk; visual editor inspection of every other rotation group remains
an explicit pack-wide follow-up rather than being inferred from the chair test.
