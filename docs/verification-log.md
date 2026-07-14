# Verification and failure log

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
