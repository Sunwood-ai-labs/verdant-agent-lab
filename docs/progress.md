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

- [x] generate the first 12-object furniture chroma-key sheet
- [x] remove its chroma key and validate alpha
- [x] split the furniture sheet into 12 addressable sprites
- [x] add the first versioned furniture manifest with independent IDs
- [x] generate, alpha-key, split, and manifest 12 technology sprites
- [ ] generate, alpha-key, split, and manifest 12 small-prop sprites
- [ ] add surface anchors, collision footprints, and z-bias metadata

## Checkpoint 3 — original builder runtime

Status: planned

- [ ] render scene objects from layout JSON
- [ ] select, move, and persist furniture
- [ ] snap monitors, keyboards, mugs, lamps, and plants to desk surfaces
- [ ] keep characters optional and disabled by default
- [ ] add original branding and visual-non-similarity QA
