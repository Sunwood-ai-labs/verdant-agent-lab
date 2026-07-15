# Build progress

## 2026-07-15 — direct similarity correction

- The prior 69.96% PASS is retracted: it was a weighted edge/palette diagnostic,
  not direct screenshot similarity.
- The movable-object mask was also rejected because it hid the very assets being
  evaluated. Current direct SSIM must use the character-only mask; the fresh
  result is recorded with its input hash in the v2 report.
- All thirteen ledger zones are open again after independent same-view review;
  generated 3x6 cells are implementation candidates, not visual sign-off.
- Current evidence is `proof/modular-office-v1.png` and the regenerated
  `proof/similarity/modular-office-direct-ssim-v2.json`.

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
# Directional asset rebuild checkpoint — 2026-07-15

## Zone 01 — solar wing 2×3 candidate sheet

- Generated a six-cell landscape chroma sheet with separate mounting frame,
  panel face, blank dashboard, rack, control base, and vine/stone edge.
- Deterministic gutter-aware splitting produced six alpha PNGs with zero
  cell-boundary alpha flags; prompts, masters, split report, and manifest are
  retained under `assets/intermediate/zone-01-solar-wing/`,
  `assets/generated/zones/solar-wing-v1/`, and `assets/manifests/zones/`.
- This remains a candidate: the generated panel face is 2×2 while the reference
  array is 2×3, and the blank dashboard still needs deterministic text.

- Retracted the source-guided 60.37% result as a completion claim; it does not prove independent asset fidelity.
- Rebuilt seven high-impact regions with one Image Gen sprite per source crop: reception, north lounge, cafe, meeting table, greenhouse, west workstation, and east workstation.
- Each generated source, prompt, chroma intermediate, and alpha output is preserved under `assets/intermediate/fidelity-v1/` and `assets/generated/furniture/`.
- The current reference-overlay-off screenshot scores 57.21% masked SSIM and remains `STRUCTURAL PROTOTYPE — NOT VERIFIED`.
- Remaining open regions: solar equipment, west studio, AI lab, south lounge, recycling bins, and independently authored architecture layers. Candidate regions still require final visual verification.
# Superseded historical checkpoint — directional decomposition

- Retracted: generated 3x6 cells are isolated candidates, not verified source
  content/facing matches in the final render.
- Twelve equipment/furniture zones use independent Image Gen sprites; fixed garden/wall topology is a dedicated extracted architecture layer with Image Gen empty-zone fills.
- Retracted: the 72.05% weighted value is diagnostic-only, not the requested
  screenshot-similarity result.
# Superseded historical checkpoint — crop-first 3x6 sheet

- Replaced the mixed single-asset generation route with the user-requested 3-column x 6-row Image Gen sheet route.
- Deterministic source sheet: `assets/intermediate/fidelity-v2/reference-crops-3x6-v1.png`.
- Image Gen sheet: `assets/intermediate/fidelity-v2/spritesheet-3x6-imagegen-v1-chroma.png` plus alpha version and 18 extracted cells under `assets/generated/sheet3x6-v1/`.
- All 18 cells preserve their source crop's row-major identity and facing; the builder now consumes the extracted sheet cells.
- Retracted: the earlier mask excluded movable-object regions and therefore
  cannot be used for object-fidelity scoring.
