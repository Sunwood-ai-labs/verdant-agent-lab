# Asset workspace

## Layers

- `scene-clean.png`: flattened 4:3 environment base
- `parts/`: 10 room/zone crops used by EXPLORE previews
- `object-crops/`: 30 opaque rectangular crops from the Image-Gen-cleaned
  derivative, for reference inventory only (not runtime assets)
- `generated/`: original image-generated sprite sheets, alpha versions, and split sprites
- `manifests/`: versioned asset metadata, footprints, seat anchors, and surface anchors

## Generated furniture pack v1

`generated/furniture/` contains 12 transparent sprites. The corresponding
`manifests/furniture.v1.json` keeps each desk, seat, plant, storage unit, and
glass segment independently addressable. The chroma source and alpha master
sheet are retained beside the split assets as reproducible intermediate data.

`generated/technology/` adds 12 independent energy, compute, display, input,
lighting, lab, cafe, and utility sprites. `manifests/technology.v1.json` records
surface mounting, state variants, footprints, anchors, and z-order hints.

`generated/props/` contains 12 desk-scale objects. Each mug, bottle, notebook,
book stack, tablet, phone, pen cup, paper pile, plant, clock, and lamp is a
separate transparent PNG and a separate entry in `manifests/props.v1.json`.

These family counts describe the current runtime library, **not** a complete
inventory of the supplied office reference. The source-required coverage audit
and its missing-component worklist are in
[`../docs/reference-asset-coverage-audit.md`](../docs/reference-asset-coverage-audit.md).

## Object crop inventory

Architecture and environment:

- `canopy-tree`, `exit-door`, `greenhouse-door`, `entrance-mat`
- `flower-planter-left`, `flower-planter-right`, `potted-plant`

Furniture:

- `curved-reception-desk`, `studio-desk`, `meeting-table`
- `workstation-left`, `workstation-right`, `rolling-chair`
- `lounge-sofa-top`, `quiet-lounge-sofa`, `round-coffee-table`, `bookshelf`

Technology and lab:

- `solar-panel`, `server-racks`, `server-dashboard`, `air-quality-board`
- `meeting-display`, `lab-bench`, `lab-platform`, `lab-console`

Cafe and information props:

- `cafe-counter`, `coffee-machines`, `ideas-whiteboard`, `recycling-bins`, `tall-planter`

These crops preserve nearby derivative-scene appearance but include rectangular
surroundings. They are not raw-original crops, transparent isolated sprites, or
builder runtime assets. Generated alpha sprites are a separate family and must
not be described as source-image decompositions.
