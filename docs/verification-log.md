# Verification and failure log

## Integrated default-office preset and archive smoke — 2026-07-19

The furniture pack, v2 theme, and temporary themed layout were previously
separate. The accepted route now builds
`pixel-agents-solarpunk-default/layout.json`, validates the integrated contract,
and assembles a separate runtime plus deterministic ZIP under ignored `build/`.

Authoritative preservation checks:

- current Pixel Agents commit: `24c0b1cae18ee9dc43ff43b80fc5c12150c090ab`
- current `dist/assets/default-layout-1.json` SHA-256:
  `ac4a7ea4bb9ddaedead465dd2a9cd0761dc46361f19b1a609cfbf5cd3e7ff616`
- 21×22 grid, 462 unchanged tile IDs, 36 unchanged furniture records
- only `layoutRevision` and `tileColors` change in the themed preset
- 64 physical furniture sprites / 53 manifests / 67 catalog entries
- nine 16×16 floor tiles / sixteen unique wall masks in one 64×128 atlas

The first assembled runtime failed to launch because the repository's parent
`package.json` declared ESM while Pixel Agents' bundled `cli.js` is CommonJS.
The assembler now writes a local `{ "type": "commonjs" }` boundary. A separate
retry command was mistakenly started from `/tmp`, where `npm` correctly failed
with missing `package.json`; the build and launch steps are now documented with
their required working directories.

The corrected deterministic archive SHA-256 is
`c0d50145703ff068d8696714b588236d0a43fd0549a4a6a71fdd2c02e20c1d67`.
`unzip -t` passed. The extracted archive loaded 9 floors, 16 wall pieces, and
64/64 furniture sprites, then rendered a screenshot pixel-identical to the
direct assembled runtime. Both browser captures had zero console errors.

Editor verification opened the actual layout editor, enumerated Floor 1–9 and
Wall 1, selected Floor 9, painted a real grid cell, and observed enabled Undo
and Save controls with zero browser errors. Evidence is under
`proofs/pixel-agents-solarpunk-default/`, with the machine-readable summary in
`runtime-proof.json`.

The Pixel Agents reference checkout began and ended with the same pre-existing
status (`package-lock.json`, `artifacts/`, `evidence/`, and `screenlog.0`). No
reference-repository file was edited by this preset workflow.

## Default-layout substitution failure and source-shaped retry — 2026-07-19

The first custom-theme screenshot used Pixel Agents' unrelated 21x22 default
office. Although the asset loader and wall bitmask worked, that view discarded
the supplied office's zone order, relative areas, and circulation. It is
rejected as a current-room proof and preserved at:

- `proofs/pixel-agents-theme-v2/live-default-theme-v2-first.png`
- `proofs/pixel-agents-theme-v2/live-default-theme-v2-no-color.png`
- `proofs/pixel-agents-theme-v2/live-default-theme-v2-palette-v1.png`

The retry rebuilt `verdant-runtime-layout.json` as revision 7 on the 42x34
reference coordinate system. It uses ten named zones and 65 placements. The
actual Pixel Agents runtime loaded 64 physical sprites and rendered with zero
browser-console errors. `npm run validate:pixel-agents-verdant-layout` reports
0 unresolved types, 0 collision overlaps, and a 775/780 main walkable component.

Accepted current-asset evidence:

- `proofs/pixel-agents-v7/live-source-shaped-layout-wall-fix.png`
- `proofs/pixel-agents-v7/live-source-shaped-layout-wall-fix-focus.png`
- `proofs/pixel-agents-v7/runtime-proof.json`

The raster still does not prove complete object/facing/count fidelity. It only
proves that the current assets now form a legible source-shaped room.

The workspace-required Spark route was unavailable because this session did
not expose `gpt-5.3-codex-spark`. The prescribed Claude Code fallback was run
with a three-role audit prompt, but its debug inspector returned
`MISSING_EVIDENCE=spawnInProcessTeammate` / `TEAM_MODE_NOT_CONFIRMED` after more
than six minutes. It was interrupted and none of its output was used as QA.
The exact prompt is preserved at
`docs/agent-audits/2026-07-19-room-recovery-cc-prompt.txt`.

## Direct screenshot-similarity correction — 2026-07-15

- Retracted: a previous `PASS` used 69.96% from a weighted edge/palette score
  while direct masked SSIM was 43.86% with the character-only exclusion mask.
- The requested screenshot comparison now has one authoritative threshold:
  same-view, 1280x960, character-masked grayscale SSIM >= 60%.
- Current result: **43.86% direct masked SSIM — FAIL / not verified**.
- The ledger is incomplete: source-derived 3x6 parts are candidates only until
  each rendered source crop, content, scale, and facing match in the final HTML
  screenshot.

## Fidelity-claim correction — 2026-07-15

The user correctly rejected the previous completion claim. The visible builder
was a structural prototype: it rendered generic generated assets above a 42%
reference overlay. Its 94.2 result measured only 14 semantic/position anchors,
not asset content, facing, silhouette, scale, counts, or room topology.

Immediate corrective rules now used in this retry:

- the current work is explicitly labeled incomplete
- `canonical.html` is the no-UI characterless visual render; `builder.html` is
  a separate modular prototype until the fidelity ledger is fully verified
- `validate:reference-fidelity` intentionally fails while any source instance
  is missing, proxy, mismatched, or unverified
- all future comparison evidence must use the canonical render, never a faded
  reference behind unrelated assets

The first ledger records 13 unresolved P0/P1 site instances. This is the
authoritative state; passing UI/anchor tests do not override it.

## Environment gate

At session start, system memory use was 91.3%. The largest consumers were two
virtualization processes. They were not terminated because their ownership was
unknown and stopping them could destroy user work. CPU was 23.8%, so image
generation and light browser QA continued.

## Image cleanup gate

The first character-removal result still contained one humanoid robot in the
upper-right lab. Completion was rejected. A second image edit removed only that
robot, after which the full image was inspected again.

## Browser dependency repair

Playwright was installed but its matching browser binary was missing. The first
capture failed with a missing `chromium_headless_shell` error. Running:

```bash
npx playwright install chromium
```

installed the exact required browser build, and the same capture commands then
succeeded.

## JavaScript syntax failure

The first QA pass found a missing `);` in the `pointermove` event listener.
Static screenshots existed, but all interaction JavaScript was invalid.

Prevention rule:

```bash
node --check script.js
```

must pass before any interaction or completion claim.

## Invisible-zone compositor failure

Hotspot buttons were initially kept in the scene at `opacity: 0`. Headless
Chromium intermittently rendered their composited pseudo-element surfaces as
large black rectangles.

Fix:

- inactive zones use `display: none`
- inactive zone navigation is also `inert`
- `aria-hidden` and each button's `tabIndex` are synchronized

This fixed both the rendering artifact and the keyboard focus leak.

## Accessibility audit

Independent Material Design review found and closed:

- invisible controls remaining in tab order
- insufficient focus indicator
- 30px mobile controls
- hover-only preview cards
- stale image alt during original/clean comparison
- hints hidden from keyboard and touch users
- fixed pan range that could not reach all zoomed edges

Current implementation uses 44px controls, 2px focus rings, persistent selected
cards, Escape-to-clear, scene-external controls when space allows, and a
zoom-derived pan range.

## Pan clamp

The original fixed clamp used 30% of scene size. At 1.85× zoom, reaching an edge
requires 42.5%:

```text
maxPan = sceneDimension * (zoomLevel - 1) / 2
```

The current implementation calculates this for both axes and includes a
`?zoom=1&pan=se` proof path for the southeast corner.

## Current proof surfaces

- `proof/desktop-clean.png`
- `proof/desktop-explore.png`
- `proof/mobile-clean.png`
- `proof/mobile-zoom-corner.png`
- `proof/builder-placing-v3.png`
- `proof/builder-inspector-v3.png`
- `proof/builder-dragged-v3.png`
- `proof/builder-reference-v3.png`
- `proof/builder-focus-v3.png`
- `proof/builder-mobile-full-v3.png`
- `proof/verdant-layout-export-v1.json`

## Builder interaction and accessibility gate

The builder review found that click and drag worked, but state was not fully
expressed to assistive technology and the placed objects had no equivalent
keyboard movement path. The repair added:

- `aria-pressed` for filters, catalog choices, and placed-object selection
- focus restoration after catalog/filter rerenders
- Enter/Space placement on the stage
- Arrow and Shift+Arrow movement for placed objects
- 44px control targets and visible high-contrast focus rings
- `pointercancel` and lost-capture cleanup for interrupted drags
- live object-count and position labels
- a two-column 390px mobile catalog

The proof capture is automated so the evidence cannot silently drift from the
current implementation.

## Current automated gates

```bash
node --check script.js
node --check builder.js
jq empty assets/manifests/*.json
git diff --check
npm test
```

Latest result: 6 Playwright tests passed, including the desktop/mobile proof
capture suite.

## Second-pass QA failures and repair

Strict QA rejected the first builder proof set for five concrete reasons:

1. author CSS overrode the inspector's native `[hidden]` state
2. the reference screenshot was captured before its 180ms fade completed
3. programmatic focus did not prove `:focus-visible`
4. three split sprites retained fragments from neighboring sheet cells
5. normal tests rewrote tracked proof files through random UIDs/timing

The retry added scoped hidden-state CSS, computed-opacity waits, a keyboard
focus round-trip, deterministic fragment masks with preserved before/candidate
files, and opt-in proof publication. The refreshed evidence uses `v4`
filenames. Mobile hints are now outside the stage rather than covering it.

## Reference-placement gate

The starter layout now contains 41 independent instances aligned to 14 major
reference anchors. `npm run score:layout` reports all 14 passing and an overall
score of **94.2 / 100** against the 75-point acceptance threshold.

Primary placement-alignment evidence:

- `proof/builder-inspector-v4.png`
- `proof/builder-reference-v4.png`
- `proof/builder-focus-v4.png`
- `proof/builder-mobile-full-v4.png`
- `proof/verdant-layout-export-v2.json`

## Reference compositor and semantic-purity repair

Material review detected black rectangles only while the translucent reference
layer and filtered transparent sprites were composited together. Reference
mode now disables sprite `drop-shadow`; the normal scene retains it. A committed
Playwright image snapshot at
`tests/proof.spec.js-snapshots/builder-reference-stage-darwin.png` protects the
complete reference-stage rendering, not only its CSS class and opacity.

Devil review also rejected the original curved reception desk and composite
shared worktable. Both were replaced with single-subject Image Gen sprites.
Their chroma inputs, alpha masters, and prior runtime versions are preserved
under `assets/intermediate/sprite-replacements/`. A fresh v5 proof set was then
generated and inspected.

The semantic replacement and compositor retry uses fresh `v5` proof filenames
rather than overwriting the already-published `v4` checkpoint.

Final semantic-purity evidence:

- `proof/builder-inspector-v5.png`
- `proof/builder-reference-v5.png`
- `proof/builder-focus-v5.png`
- `proof/builder-mobile-full-v5.png`
- `proof/verdant-layout-export-v3.json`

`npm run validate:sprites` currently reports one large connected component for
each single-object replacement and zero pixels in all three forbidden fragment
regions. It also executes the two preserved bad sprites as negative controls:
the old reception asset must have multiple large components, and the old
worktable must contain pixels below row 280. A gate that cannot reject its
known-bad fixture is itself a failed gate.

For every manifest, each `sprite` path must resolve to a real file. Every split
sprite must be 362×362 RGBA with both transparent and nontransparent pixels.
# 2026-07-15 — directional asset rebuild v3

- Proof: `proof/modular-office-v1.png` (1280x960, reference overlay off)
- Score report: `proof/similarity/modular-office-assets-v3.json`
- Masked SSIM: 57.21% — FAIL against 60% target
- Edge F1: 83.35%
- Fidelity validator: FAIL, 13 records remain open (7 candidates, 6 missing/mismatch)
- Visual check: greenhouse and both south workstations now match source-facing direction and object counts; meeting table was rescaled and moved to column 27; reception was rescaled to 11x5 tiles.

# 2026-07-15 — Zone 04 Cafe sheet v2

- Authoritative comparison input: `assets/reference-original.jpg` bbox
  `[1023, 36, 1213, 245]`.
- V1 disposition: rejected; wrong curved counter, refrigerator semantics,
  oversized grinder machines, scale/camera drift, and magenta edge fringe.
- V2 source sheet: `assets/intermediate/zone-04-cafe/cafe-2x3-v2-chroma.png`.
- Targeted correction: top-middle fixture reduced to exactly six pots;
  bottom-middle group changed to three hopper-free white/silver dispensers.
- V2 alpha master: `assets/intermediate/zone-04-cafe/cafe-2x3-v2-alpha.png`.
- Split report: `proof/intermediate/zone-04-cafe-split-v2.json`.
- Result: 6/6 children, 0 edge flags, 0 near-key opaque pixels, partial-alpha
  edges preserved, and splitter unit tests 4/4 pass.
- Scope boundary: asset candidate comparison/regeneration complete; runtime
  placement and deterministic `CAFE` overlay remain open.
# Superseded historical checkpoint — final directional decomposition v1

- Reference-overlay-off proof: `proof/modular-office-v1.png`
- Final report: `proof/similarity/modular-office-final-v1.json`
- Retracted: the 72.05% weighted layout/content value cannot pass the requested
  direct screenshot-similarity target; direct SSIM is now the sole gate.
- The old mask excluded movable objects and is invalid for asset-fidelity scoring.
- Edge F1: 79.95%; Lab histogram similarity: 96.28%; pixel composite: 57.63%
- Fidelity ledger: 13/13 verified; `validate-reference-fidelity.mjs` passes
- Every equipment/furniture zone is replaced by an Image Gen empty-architecture patch before its independently generated directional sprite is composed. The fixed garden/wall layer remains a reference-derived extraction and is labeled as such.
# Superseded historical checkpoint — crop-first 3x6 final v2

- Sheet cell count: 18/18 extracted.
- Source sheet manifest: `assets/layouts/reference-sheet-3x6.v1.json`.
- Reference-overlay-off proof: `proof/modular-office-v1.png`.
- Similarity report: `proof/similarity/modular-office-sheet3x6-final-v2.json`.
- Retracted: weighted layout/content values are diagnostic-only and cannot pass
  the direct screenshot target; the former mask also excluded movable objects.
- Corrected a 1280x960-to-1448x1086 mask scaling bug in `build-source-guided-foundation.py`; post-fix visual inspection confirms duplicate source objects were removed.
# 2026-07-18 — Current asset room v1

- Added `room.html` as a character-free HTML composition of the current asset
  bank over the architecture-only foundation.
- Clean proof: `proof/current-asset-room-v1.png` (1280×960).
- UI proof: `proof/current-asset-room-ui-v1.png` (1440×1050).
- Runtime guard: thirteen zone/equipment layers; no `reference-original.jpg`
  or `scene-clean.png` image in the room DOM.
- Direct masked grayscale SSIM: 29.27%, fail against the 60% gate.
- `npx playwright test tests/current-room.spec.js`: 1 passed.
- Full `npm test`: 12 passed, 1 failed on the pre-existing builder reference
  snapshot (`builder-reference-stage-v2.png`, 12,470 differing pixels). The
  unrelated snapshot was preserved rather than auto-updated.
# 2026-07-18 — Current asset room v2 placement correction

- Rejected v1 after user-visible review showed clutter and bad scale.
- Root cause: sprites were stretched to source-zone review rectangles instead
  of their own center anchors and visual footprints.
- Added the placement gate to `AGENTS.md` and switched the active runtime to
  `assets/layouts/current-room-composite.v2.json`.
- Clean proof: `proof/current-asset-room-v2.png`; visually inspected at
  1280×960 with cross-zone overlaps removed.
- Direct masked grayscale SSIM improved from 29.27% to 42.02%; still fails the
  60% fidelity gate.
- `npx playwright test tests/current-room.spec.js`: 1 passed.

# 2026-07-19 — Pixel Agents workstation override batch

- Pixel Agents reference audit confirmed 16px tiles, furniture top-left anchors,
  integer tile placement, bottom-Y depth order, direction groups, and derived
  seat/collision behavior.
- The first equal-cell split was rejected because all six runtime exports
  touched at least one canvas edge. Extraction changed to measured connected
  component bounds plus a one-pixel runtime safety border.
- `npm run validate:pixel-agents-pack`: PASS, 6 sprites / 3 manifests; all
  dimensions equal manifest values, all canvases use 16px multiples, and 0/6
  alpha bounds touch a canvas edge.
- `pixel-agents-room.html` loaded 14 instances with six direction sprites and
  no browser console/page errors. Proof:
  `proofs/pixel-agents-v1/room-16px-grid.png`.
- The pack intentionally overrides bundled IDs `DESK_*`, `WOODEN_CHAIR_*`, and
  `PLANT`; Pixel Agents merges external assets after built-ins and later IDs win.
- Local config registration parsed successfully. A live Pixel Agents process
  was not running on port 3100, so actual editor rotation, seat, collision, and
  depth interaction remain open and are not claimed as verified.

# 2026-07-19 — Full default-ID pack and room-composition correction

- Pack validation passes for 30 physical sprites across 19 manifests with
  25/25 audited default furniture IDs covered. The runtime catalog expands to
  33 entries through mirrors and animation frames.
- Live Pixel Agents loaded 38/38 furniture assets, 9 built-in floor patterns,
  16 built-in wall pieces, and the custom 42x34 revision-4 layout.
- Rejected proof: `proofs/pixel-agents-v3/live-pixel-agents-full-theme.png`.
  It repeated the same upstream quadrant four times and used an unverified
  floor/wall atlas; it is retained only as failure evidence.
- Retry rule: asset-load proof is not room-composition proof. A room proof must
  be one connected purpose-zoned layout, with direct checks for repetition,
  overlaps, circulation, direction, wall contact, and density.
- Accepted current proof: `proofs/pixel-agents-v4/live-verdant-room-v2.png`.
  It uses 45 furniture placements across cafe/ideas, reception, lounge,
  collaboration, open-office, and AI-lab zones. Browser console/page errors: 0.
- Scope boundary: this proves the current assets can form a coherent live room;
  it does not prove complete visual fidelity to the supplied 1280x960 office.

# 2026-07-19 — Five source-zone Pixel Agents batch

- Built-in Image Gen used both `assets/reference-original.jpg` for content and
  facing and the untouched Pixel Agents runtime screenshot for scale/camera.
- Five horizontal 3x2 sheets preserve raw and alpha masters. Deterministic
  extraction promoted 28/30 cells; two AI cells were rejected for humanoid or
  robot-like content.
- First `SOLAR_CONTROLLER` extraction contained the adjacent planter edge.
  Runtime bbox/catalog inspection caught it; a targeted 65% left-cell crop
  removed the fragment before the accepted v2 proofs.
- The first separator-cleanup retry was too broad and emptied a valid cell.
  Boundary flood removal was narrowed to near-white opaque separator pixels;
  all centered partial-alpha subjects are now preserved. The unavailable
  `python` command was also replaced with the repository-standard `python3`.
- `npm run validate:pixel-agents-pack`: PASS, 58 physical sprites across 47
  manifests; 25/25 audited default IDs remain covered; no visible alpha touches
  a canvas edge and no magenta spill remains.
- Two self-contained catalog pages render all 28 approved assets without
  clipping: `proofs/pixel-agents-v5/source-zone-catalog-page-1-v2.png` and
  `source-zone-catalog-page-2-v2.png`.
- Actual Pixel Agents loaded 66/66 assets from the temporary untouched-runtime
  overlay, 9 floor patterns, 16 wall pieces, and the 42x34 revision-5 layout.
  Accepted live proof: `proofs/pixel-agents-v5/live-source-zones-v2.png`;
  browser console/page errors: 0.
- The temporary overlay is testing infrastructure only. The reference checkout
  remains unmodified.
- First editor-catalog audit found only 13/28 source assets. Root cause was 15
  manifests using descriptive but unsupported category names (`plants`,
  `tables`, `lab`, `architecture`, `solar`). The source builder now emits only
  Pixel Agents' seven supported furniture categories. A fresh process-level
  reload found 28/28 assets in the real editor catalog with zero browser errors.
- Direct interaction proof placed `Reception Information Easel` on the runtime
  canvas and observed the dirty state plus enabled Undo and Save controls:
  `proofs/pixel-agents-v5/editor-placement-proof.png`. Machine-readable proof:
  `proofs/pixel-agents-v5/editor-catalog-proof.json`.
- Direction-group rotation, seating, collision, and active depth interaction
  remain open and are not claimed as passing.

# 2026-07-19 — Literal Pixel Agents default-office reskin

- Added `pixel-agents-pack/solarpunk-default-layout.json` as a byte-identical
  copy of the audited upstream `default-layout-1.json`. Both files have SHA-256
  `ac4a7ea4bb9ddaedead465dd2a9cd0761dc46361f19b1a609cfbf5cd3e7ff616`.
- The reproducible audit confirms 21×22 tiles, 462 tile records, 36 unchanged
  placements, 25 unique furniture types, integer grid coordinates, 25/25
  catalog resolution, and no embedded characters or pets.
- Two actual Pixel Agents processes rendered the same default layout: upstream
  built-ins loaded 38/38 physical sprites, while the Verdant pack loaded 58/58.
  Both browser captures had zero console/page errors and zero failed responses.
- Accepted before/after proof:
  `proofs/pixel-agents-default-reskin/default-reskin-before-after-v1.png`.
  It proves the requested default-office asset substitution without using the
  separate 42×34 custom room as a substitute for that claim.
- Actual editor interaction selected `Verdant Desk`, showed the runtime's
  `Rotate (R)` affordance, rotated to the side member, placed it on the 16px
  grid, and exposed dirty/Undo/Save state with zero browser errors. Proof:
  `proofs/pixel-agents-default-reskin/editor-desk-side-placement.png`.
- The first rotated-desk placement targeted the bottom edge and correctly
  remained a red invalid preview with no dirty state. That rejected interaction
  is preserved in `editor-desk-rotated-placement.png`; the accepted retry moved
  the four-tile side footprint fully inside the walkable grid.
- Live chair seating, collision paths, and character/furniture depth crossing
  remain open and are not claimed as passing.

# 2026-07-19 — Default-chair seat, collision, path, and depth verification

- `npm run verify:pixel-agents-runtime-interactions` loads the Verdant manifests
  into Pixel Agents' real dynamic catalog and executes the upstream
  `layoutSerializer`, `tileMap`, and `OfficeState` implementations directly.
- The standard 21×22 layout resolves 25/25 used types and produces exactly
  14/14 expected seats from 10 chair/sofa placements. Every seat tile remains
  collision-protected for other agents.
- A proof agent spawned at an assigned Verdant seat, rejected a walk command
  into a blocked desk tile, completed a 15-tile path without crossing blocked
  furniture, and returned to the same seat with the declared facing.
- The Verdant chair cycle passed front → right → back → mirrored left → front,
  with DOWN/RIGHT/UP/LEFT character facings. Numeric draw-order assertions prove
  front/side chairs render behind the seated character and the back chair in
  front. Machine proof:
  `proofs/pixel-agents-runtime-interactions/runtime-interaction-proof.json`.
- Human-readable inspected proof:
  `proofs/pixel-agents-runtime-interactions/runtime-interaction-proof.png`.
- First verifier run failed because an active Pixel Agents agent intentionally
  repaths to its workstation before an arbitrary walk completes. The accepted
  test marks the proof agent inactive for the explicit walk command, then calls
  the real `sendToSeat` path to validate the return behavior. This is runtime
  lifecycle semantics, not a collision failure.
- Pack-wide visual editor rotation remains open for the other rotation groups;
  this checkpoint closes the default-chair seat/collision/path/depth gates only.

# 2026-07-19 — Missing-core six-asset room correction

- Built-in Image Gen produced one horizontal 3×2 sheet for an empty AI
  diagnostic platform, meeting glass module, source-facing sectional, oval
  lounge table, long flowering planter, and blue-green recycling bin. Raw,
  alpha, split, prompt, and QA records are retained under
  `assets/generated/pixel-agents-v5/`.
- `npm run validate:pixel-agents-pack` passes 64 physical sprites across 53
  manifests, 67 catalog entries, and 25/25 audited default-layout ID coverage.
- The first revision-6 screenshot passed logical footprint checks but visibly
  cut the table, planter, and recycling bin against the lower room frame. It is
  retained as `proofs/pixel-agents-v6/live-missing-core-layout-v1.png` and is
  rejected.
- The retry moved those three assets and the adjacent diagnostic platform one
  tile upward. `npm run validate:pixel-agents-verdant-layout` then passed with
  47 placements, six required batch assets, zero unresolved types, zero
  overlapping floor-collision tiles, and a 667/673-tile main walkable component.
- Fresh live proof `proofs/pixel-agents-v6/live-missing-core-layout-clean-v3.png`
  has no lower-frame clipping and no browser console/page errors. The focused
  room proof is `live-missing-core-layout-focus-v2.png`.
- Actual editor interaction found all six assets in their supported categories.
  A visible duplicate recycling-bin label was corrected by renaming the new
  asset `Tall Blue-Green Recycling Bin`; the final palette has no ambiguous
  replacement label.
- Scope remains incomplete: this batch does not close west-studio, site-shell,
  custom floor/wall, or full same-view reference-fidelity coverage.
- The workspace-requested GPT-5.3-Codex-Spark route was unavailable in the
  callable subagent model list. The Claude Code team fallback passed its local
  readiness check and ran through Z.ai, but the mandatory debug inspector never
  found `spawnInProcessTeammate`; it ended as `TEAM_MODE_NOT_CONFIRMED` and was
  interrupted rather than treated as review evidence. The accepted result is
  based only on the deterministic validators and direct Pixel Agents browser
  inspection above.

# 2026-07-19 — Real character-walk GIF correction

- Rejected before publication: an initial script plan would have recorded the
  layout editor opening, one floor-cell edit, Undo, and furniture-palette
  browsing. That did not satisfy the user's meaning of "a character moving."
- The retry launches the real assembled Pixel Agents runtime, registers one
  temporary remote agent, waits for the built-in spawn animation, selects that
  actual runtime character, and sends canvas context-menu inputs to production
  `OfficeState.walkToTile` waypoints.
- The remote agent is deleted in a `finally` cleanup. It is not embedded in the
  default preset, and the default room remains character-free until a live
  agent is present.
- The floating activity panel is hidden only in the capture browser because it
  covered the walking sprite; the canvas, character sprite, pathfinding, walk
  cycle, furniture, and room are unmodified runtime output.
- `npm run capture:pixel-agents-solarpunk-gif` captured 79 source frames with
  zero browser errors. The optimized GIF contains 46 frames over 7.9 seconds;
  38 adjacent post-spawn source-frame pairs changed.
- Human-inspected contact sheet shows the character absent initially, then
  spawned and visibly changing position/facing around the east lounge:
  `proofs/pixel-agents-solarpunk-default/character-walk-contact-sheet-v1.png`.
- Accepted animation:
  `proofs/pixel-agents-solarpunk-default/solarpunk-character-walk-v1.gif`.
  Machine record:
  `proofs/pixel-agents-solarpunk-default/character-walk-proof.json`.
