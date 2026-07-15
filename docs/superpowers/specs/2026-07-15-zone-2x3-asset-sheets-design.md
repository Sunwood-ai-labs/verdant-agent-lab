# Zone 2x3 asset-sheet design

Absolute path: `/Users/admin/Prj/sunwood-lab-recreation/docs/superpowers/specs/2026-07-15-zone-2x3-asset-sheets-design.md`.

## Goal

Create a reusable, non-character asset bank for the supplied office reference:
one landscape **2 columns × 3 rows** Image Gen sheet for each of the twelve
direct-reference zones, followed by deterministic six-cell splitting,
transparency cleanup, source comparison, and runtime registration.

## Boundary and provenance

- `assets/reference-original.jpg` and
  `assets/layouts/reference-source-zones.v1.json` are private source evidence.
  They guide generation and comparison but are never shipped as runtime art.
- Generated sheets and their split child PNGs are original project assets.
- Every child asset must record its source-zone id, sheet id, cell index, prompt,
  chroma/alpha derivation, source crop bbox, orientation, and alpha-bound audit.
- No people or character sprites are generated or registered.
- Never use a parent recomposed zone PNG in place of the six child assets.

## 2×3 sheet contract

Every sheet has two columns and three rows, exactly six independently
placeable, source-matched non-character assets, a flat `#ff00ff` chroma
background, and wide empty gutters. No floor, walls, neighbouring fixtures,
cast shadows, watermarks, or text are allowed inside a cell. Repeated source
instances reuse one child asset only when silhouette and facing match.

Text and information surfaces are blank generated panels with deterministic
HTML/Canvas overlays: the Sunwood branding, CAFE, AI LAB, IDEAS/IMPACT,
wayfinding, escape sign, dashboard numerals, and device UI. This prevents
Image Gen typography from becoming source-fidelity evidence.

## Zone sheets

| ID | Zone | Six independently placeable cell assets | Deterministic overlay |
|---:|---|---|---|
| 01 | solar wing | stone frame; six-panel face; output board; triple server bank; controller base; vine stone edging | dashboard text/numbers |
| 02 | reception and brand wall | curved counter; front planter; left tree pot; right tree pot; entry door + exit panel; brand wall + top vine | brand and exit text |
| 03 | north lounge | rug platform; L sofa; right sofa return; round table; tabletop plant; tabletop props | none |
| 04 | cafe | lower cabinet; greenery window + pot shelf; left fridge; right vending fridge; espresso-machine group; sign panel | CAFE |
| 05 | studio west | irregular desk; rear shelf; right shelf; whiteboard; rolling chair; monitor/device group | IDEAS, IMPACT, board marks |
| 06 | meeting room | glass wall + door frame; table; left chair; right chair; display; plants + pendant lights | display UI |
| 07 | AI lab | left bookcase; whiteboard; upper bench; microscope/robot platform; lower electronics bench; sign + plant | AI LAB, board/device UI |
| 08 | greenhouse | roof/frame shell; front glass wall; door; interior plant shelves; lamps; right planter + control panel | control panel UI |
| 09 | south workstation west | desk; rear planter shelf; three-screen group; chair; pot group; drawers + props | screen UI |
| 10 | south workstation east | desk; rear planter shelf; three-screen group; left chair; right chair; pot/drawers/props | screen UI |
| 11 | south lounge | rug platform; L sofa; armchair; left planting bench; right tall planting; books/cards | no readable book text |
| 12 | entry stairs and wayfinding | stairs; left wayfinding board; central green sign; left planter; right planter; foreground hedge/stone boundary | wayfinding and sign glyphs |

## Data and verification flow

`private source crop → Image Gen chroma sheet → saved chroma master → alpha
master → deterministic six-cell split → alpha-bound/cell-leak audit → per-cell
source comparison → child manifest entry → child layout placement → canonical
render + direct SSIM gate`

Generation fails if a cell contains a person, another cell's object, floor or
wall context, a cropped silhouette, or invented readable text. A zone cannot
be called complete until all six cell assets are individually runtime-addressable
and its reference-instance ledger rows pass content, orientation, count,
silhouette, scale, and layer review.

## Acceptance criteria

1. Twelve versioned landscape 2×3 chroma masters exist, one per zone.
2. Each produces six transparent child PNGs with no alpha touching the cell
   boundary unless the asset intentionally reaches it and is explicitly marked.
3. All 72 children have separate manifests and direct runtime placements or an
   explicit reusable-instance relation.
4. No runtime child uses the private original or derivative crop as its sprite.
5. Signage/UI text is rendered deterministically and checked against the source.
6. The existing reference-fidelity validator remains nonzero until every
   source-instance and direct-SSIM gate passes.
