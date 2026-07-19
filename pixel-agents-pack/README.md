# Verdant Pixel Agents pack

Original solarpunk office sprites authored for Pixel Agents' documented
external-asset contract. No Pixel Agents artwork, characters, layout, logos, or
source files are redistributed here.

## Install

In Pixel Agents Settings, add this directory as an external asset directory:

```text
/Users/admin/Prj/sunwood-lab-recreation/pixel-agents-pack
```

The current pack contains 64 physical PNG sprites across 53 manifests (67
runtime catalog entries after mirrored/animated variants), including:

- `DESK`: front and side orientations, overriding the bundled desk IDs
- `WOODEN_CHAIR`: front, back, right side, and runtime-mirrored left side
- `PLANT`: compact tall decor overriding the bundled plant ID
- PC on/off/animation and directional variants
- sofas, benches, coffee/small/collaboration tables
- bookshelves, paintings, clock, whiteboard, coffee, bins, and additional plants
- 28 source-zone assets for reception, cafe, AI lab, greenhouse, and solar wing
- six missing-core assets for the empty diagnostic platform, meeting glass,
  sectional lounge, oval table, flowering planter, and tall recycling bin

The matching built-in IDs are intentional: Pixel Agents merges external assets
after built-ins and the later entry wins. Therefore the existing default layout
uses these replacements without editing its layout JSON.

All runtime canvases use exact 16 px tile multiples. Run the deterministic
build and metadata check from the repository root:

```bash
python3 scripts/build-pixel-agents-pack.py
python3 scripts/build-pixel-agents-default-overrides.py
python3 scripts/build-pixel-agents-source-zones.py
python3 scripts/build-pixel-agents-missing-core.py
python3 scripts/build-pixel-agents-catalog.py
python3 scripts/validate-pixel-agents-pack.py
python3 scripts/build-pixel-agents-verdant-room.py
npm run validate:pixel-agents-verdant-layout
```

`verdant-runtime-layout.json` is the current 42x34 revision-7, ten-zone Pixel
Agents room. Its 65 placements follow the reference's top solar/reception/
north-lounge/cafe band, middle west-studio/meeting/AI-lab band, and bottom
greenhouse/workstation/quiet-lounge band. The living-wall bitmask atlas is used
without the old `brightness: -100` override that had crushed it to black.

The unrelated 21x22 default-office theme render is retained only as rejected
compatibility evidence under `proofs/pixel-agents-theme-v2/`; it is not the
current room or a reference-reconstruction candidate.

The room demonstrates a coherent use of the current assets. It is not yet a
complete visual reproduction of every object in the supplied office reference.
The two rejected AI cells remain only in the raw/alpha provenance sheets and
are not in the runtime pack.

## Literal default-office reskin

`solarpunk-default-layout.json` is byte-for-byte identical to the audited
upstream `default-layout-1.json`: 21×22 tiles, 36 furniture placements, and 25
unique furniture IDs. The transformation is performed only by the exact-ID
sprites in this pack, so the same grid and furniture records render as the
Verdant solarpunk office without a layout rewrite.

Rebuild and audit it with:

```bash
npm run build:pixel-agents-default-reskin
```

The machine-readable audit is
`proofs/pixel-agents-default-reskin/layout-audit.json`; the accepted live
before/after comparison is
`proofs/pixel-agents-default-reskin/default-reskin-before-after-v1.png`.

Runtime interaction verification:

```bash
npm run verify:pixel-agents-runtime-interactions
```

This executes Pixel Agents' real catalog, seat, collision, pathfinding,
`OfficeState`, and depth-order modules against this pack. The current proof
passes 14/14 generated seats, a 15-tile walk avoiding blocked furniture,
blocked-desk rejection, return-to-seat facing, the four-way chair cycle, left
mirroring, and seated front/back depth behavior.
