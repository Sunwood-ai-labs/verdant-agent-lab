# Verdant Builder

`builder.html` is the first usable original runtime built from the modular
assets. It is intentionally DOM-based while catalog behavior and data contracts
are still changing.

## Current features

- loads 36 reusable assets from three versioned manifests
- starts from 41 independently addressable instances aligned to reference anchors
- category chips and text search
- click an asset, then click the 40×30 world to place it
- drag any placed object between snapped grid cells
- select and inspect object UID, category, pack, grid position, and z bias
- delete with the inspector button, Delete, or Backspace
- clear selection with Escape
- place the selected catalog item from the keyboard with Enter or Space
- move the focused placed object with Arrow keys (Shift moves five tiles)
- persist layout to localStorage
- reset from `assets/layouts/starter.v1.json`
- export the current layout as JSON
- toggle the clean scene as a low-opacity reference layer

## Data flow

```text
furniture.v1.json ─┐
technology.v1.json ├─> catalog assets ─> asset cards
props.v1.json ─────┘

starter.v1.json ─> object instances ─> DOM scene
                             └───────> localStorage / exported JSON
```

## Why DOM first

The DOM version makes object identity, focus, keyboard behavior, inspection,
and rapid schema changes easy to verify. A Canvas renderer can replace the
scene projection later without changing manifests or saved layouts.

## Test contract

`tests/builder.spec.js` proves:

1. all 36 assets load
2. a coffee mug can be placed as a ninth independent object
3. the new object survives reload
4. a chair can be dragged to another grid cell
5. the reference layer toggles
6. a selected sofa can be deleted
7. filters and assets expose their pressed state
8. keyboard placement and keyboard movement update the inspector and label

`tests/proof.spec.js` captures the placement, inspector, drag, reference,
focus, exported JSON, and 390px-wide mobile states as durable proof artifacts.
Normal tests use ignored per-run output; `npm run test:update-proofs` is the
only command that intentionally refreshes public proof files.

Run:

```bash
npm install
npx playwright install chromium
npm test
```

## Next runtime increment

Use each desk's `surfaceAnchors` to snap monitors, keyboards, lamps, notebooks,
mugs, and plants onto named surface slots while keeping every item independently
addressable. After snapping is stable, add collision and Y-sort projection.
