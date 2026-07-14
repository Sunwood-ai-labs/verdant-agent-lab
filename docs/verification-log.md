# Verification and failure log

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

## Current automated gates

```bash
node --check script.js
jq empty assets/manifests/*.json
git diff --check
```

For every manifest, each `sprite` path must resolve to a real file. Every split
sprite must be 362×362 RGBA with both transparent and nontransparent pixels.
