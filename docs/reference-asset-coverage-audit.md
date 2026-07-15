# Reference-required asset coverage audit

Absolute path: `/Users/admin/Prj/sunwood-lab-recreation/docs/reference-asset-coverage-audit.md`.

## Verdict — incomplete

The supplied 1280×960 reference is exactly the local
`assets/reference-original.jpg` (SHA-256
`3eaeeb787a3e9d10f2612c7f20f2d963e38bae3870d1b03d03e3b57290868c5d`).
For private visual inspection, `scripts/render-reference-zone-contact-sheet.py`
uses `assets/layouts/reference-source-zones.v1.json` to create direct crops
from that reference. Its raster output is intentionally gitignored because it
contains the user-supplied original image; it is evidence only, never a public
runtime asset.
The current **48-entry manifest library is not an inventory of every
source-required asset** and must not be described that way.

- 48 manifest records: 20 furniture, 16 technology, 12 props.
- 14 are in `starter.v1.json`; 34 are library-only candidates.
- 13 records use a decomposed-region **parent composite**, not individually
  placeable children. The linked decomposition sheets contain 218 child cells,
  but the runtime loads the parent sprite only.
- One fixed architecture background (`office-architecture-extracted-v3.png`) is
  loaded directly by CSS and is not in the 48-entry manifest library.
- The 30 `object-crops/` files are non-runtime opaque cuts from `scene-clean`,
  not source-original isolated assets.

## Existing split-image bank — present, but not wired into the builder

There is a substantial bank of individually named split PNGs under
`assets/generated/decomposed/`. It includes 18-cell sets for the solar wing,
AI lab, reception, meeting room, greenhouse, cafe/north lounge, south lounge,
studio, and workstations (plus a three-bin set). The matching
`assets/layouts/*-parts-3x6*.json` files identify the intended child names and
paths. These files are **not missing**.

Their current problem is different: `builder.js` does not load child paths from
`assets/generated/decomposed/`; it loads parent recomposed zone sprites from
the 48-entry manifest. Therefore the existing split bank must be reviewed
against the source and promoted, with its own manifest records and placements,
before it can count as independently runtime-addressable coverage.

## New 2×3 zone-sheet candidates

Zone 01 solar wing now has a new six-child generated candidate set under
`assets/generated/zones/solar-wing-v1/`, with source-crop mapping and split
proof. It is not runtime-wired and is not source-verified: its panel face has a
2×2 subdivision while the reference has 2×3, and its dashboard deliberately
awaits deterministic text. This is recorded as a candidate, not as resolved
coverage.

## Required source assets not independently runtime-addressable or source-verified

| Priority | Reference requirement | Current state |
|---|---|---|
| P0 | Site shell: floor tiles, paving, exterior walls/columns/fences, front stairs, entrance doors, exit sign, perimeter trees/hedges/flowerbeds | Baked into one architecture image; not independent |
| P0 | Main branding and wayfinding: Sunwood wall sign, CAFE sign, AI LAB sign, reception direction board, IDEAS board | Not catalogued as individual runtime assets; split candidates require source-match review |
| P0 | Solar wing: panel frame + six modules, output display, battery/server bank, controller, vine/planter pieces | Split child bank exists; builder loads one parent composite instead |
| P0 | Reception: curved counter, front planter, monitor, tablets, phone, papers, desk plants, easel | Split child bank exists; small props are not independently placed |
| P0 | Glass meeting enclosure: frame segments, three door/window panels, pendant, display, table, direction-specific chairs, plants | Split child bank exists; builder uses a parent composite |
| P0 | Greenhouse: roof glass panes, ridge and cross beams, wall panes, door, handle, control panel, lamps, interior shelving/foliage | Split child bank exists; no child is directly runtime-addressable |
| P1 | Cafe: shelf, greenery window, plant ledge, counter, three coffee machines, refrigerator, vending unit, display, books/pots | Split child bank exists; generic candidates still require source-match review |
| P1 | Studio and two distinct workstations: desk frames, drawers, monitors, direction-specific chairs, shelves, whiteboard, keyboards, papers, mugs, plants | Split child bank exists; counts/facing are not source-verified and children are not wired |
| P1 | AI lab: bookcase, whiteboard, benches, analyser cart, platform, devices, shelf displays, plants | Split child bank exists; builder loads a parent composite |
| P1 | North and south lounges: platform/rug, sectional sofa pieces, tables, board, benches, trees, flowering planters, tabletop props | Split child bank exists; source layout is not individually rebuilt |
| P2 | Site-wide lighting, hanging vines, pots, long planters, garden borders, shelf contents, small paper/device variants | Some candidates exist; others remain baked or need source-match review |

## Correct next implementation boundary

Do not add more generic catalog sprites. First split the fixed architecture
layer into named runtime segments; then promote approved 3×6 child cells into
their own manifest records with original-image bbox, direction, alpha-boundary
audit, and placement. Only after every row above has a direct runtime asset and
source-crop comparison can the catalog be called source-complete.
