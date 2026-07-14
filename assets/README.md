# Asset workspace

## Layers

- `scene-clean.png`: flattened 4:3 environment base
- `parts/`: 10 room/zone crops used by EXPLORE previews
- `object-crops/`: 30 exact scene-derived crops for furniture and prop inventory
- `generated/`: original image-generated sprite sheets and alpha versions (next checkpoint)
- `manifests/`: versioned asset metadata and placement anchors (next checkpoint)

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

These crops preserve exact source appearance but include rectangular surroundings. Generated alpha sprites are kept separate so exact evidence and reusable game assets are not confused.
