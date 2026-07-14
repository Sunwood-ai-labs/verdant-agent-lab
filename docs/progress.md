# Build progress

## Checkpoint 1 — base recreation

Status: characterless base complete; HTML visual reconstruction incomplete

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
- [x] generate, alpha-key, split, and manifest 12 small-prop sprites
- [x] add surface anchors, collision footprints, and z-bias metadata

## Checkpoint 3 — original builder runtime

Status: first usable version complete

### Fidelity correction (2026-07-15)

Status: incomplete. The builder's 14-anchor score was only a structural
diagnostic. It did not validate asset contents, direction, scale, counts, or
site topology. `assets/layouts/reference-instance-ledger.v1.json` currently
contains 13 unresolved source instances, and `npm run
validate:reference-fidelity` must fail until each is visually verified.

- [x] add a no-UI characterless canonical render
- [x] make builder footprint aspect ratio and layout rotation renderable
- [x] add the failing object-level fidelity ledger and validator
- [ ] replace all source-mismatched assets and directional variants
- [ ] reconstruct missing room/topology layers in HTML
- [ ] produce canonical target/render diffs and obtain all-instance signoff

- [x] render scene objects from layout JSON
- [x] select, move, delete, and persist furniture
- [x] load 36 objects from three independent manifests
- [x] export the current layout as JSON
- [x] keep characters disabled and absent
- [x] add Playwright coverage for load/place/persist/drag/reference/delete
- [x] add keyboard placement/movement and programmatic selected-state coverage
- [x] capture desktop placement/inspector/drag/reference/focus proof states
- [x] capture a complete 390px mobile catalog/stage/inspector proof
- [x] add original VERDANT BUILDER branding and visual-non-similarity QA
- [x] realign 41 instances to normalized photo anchors
- [x] add a reproducible 94.2/100 structural-placement similarity gate
- [x] remove neighboring-cell fragments from three generated sprites
- [x] replace the mixed reception cell with a desk-only sprite
- [x] replace the composite shared-worktable cell with a table-only sprite
- [x] add a visual snapshot for the REFERENCE compositing state
- [ ] snap monitors, keyboards, mugs, lamps, and plants to declared desk surfaces
- [ ] keep characters optional and disabled by default
