# Build progress

## Checkpoint 1 — base recreation

Status: complete

- [x] remove people, mascots, and humanoid robots from the 4:3 scene
- [x] preserve the lab footprint, greenhouse, solar wing, cafe, lab, desks, paths, and garden
- [x] add HTML exploration overlays without making the background image the only interactive layer
- [x] add accessible EXPLORE controls and persistent object cards
- [x] add mobile fit/zoom/pan states
- [x] export 10 region parts
- [x] export 30 object-level crops
- [x] capture desktop and mobile proof images

Evidence:

- `proof/desktop-clean.png`
- `proof/desktop-explore.png`
- `proof/mobile-clean.png`
- `proof/mobile-zoom-corner.png`

## Checkpoint 2 — modular object catalog

Status: in progress

- [ ] generate original chroma-key furniture sprite sheets
- [ ] remove chroma key and validate alpha
- [ ] split sheets into addressable sprites
- [ ] add versioned asset manifests with independent IDs
- [ ] add surface anchors, collision footprints, and z-bias metadata

## Checkpoint 3 — original builder runtime

Status: planned

- [ ] render scene objects from layout JSON
- [ ] select, move, and persist furniture
- [ ] snap monitors, keyboards, mugs, lamps, and plants to desk surfaces
- [ ] keep characters optional and disabled by default
- [ ] add original branding and visual-non-similarity QA
