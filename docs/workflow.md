# End-to-end production workflow

This document records the complete path from one 4:3 reference image to a
public, modular HTML pixel-office asset repository.

## 1. Preserve the reference boundary

1. Keep the user-supplied reference outside the public repository.
2. Record its dimensions and aspect ratio before editing.
3. Treat it as an edit target for composition, not as a public runtime asset.
4. State invariants explicitly: camera, footprint, rooms, furniture, garden,
   lighting, palette, and aspect ratio must remain stable.

The input was 1280×960. The generated clean scene is 1448×1086. Both are
exactly 4:3.

## 2. Remove all characters before building UI

The first image-generation edit removed humans, mascots, and humanoid robots.
A visual pass found one remaining humanoid robot in the AI lab, so a second,
single-change edit removed only that figure. The second pass preserved all
other pixels as aggressively as the image model allowed.

This two-step pattern was more reliable than asking the model to redesign the
whole scene and remove characters in one creative generation.

## 3. Build the HTML shell around the clean scene

The HTML version uses the clean scene as the visual base and adds independent
DOM layers for:

- semantic room hotspots
- persistent selection cards
- zone previews sourced from regional assets
- fit and zoom states
- drag-to-pan while zoomed
- pointer tilt on desktop
- reduced-motion behavior
- keyboard focus and Escape-to-clear

The public UI does not expose the original character-containing reference.

## 4. Split exact scene evidence from reusable sprites

Two asset families are intentionally kept separate:

- `object-crops/` preserves exact rectangular crops from the clean scene.
- `generated/` contains original transparent sprites designed for reuse.

This avoids presenting generated reconstructions as exact evidence and avoids
forcing game code to use background-filled rectangular crops.

## 5. Generate modular sprite sheets

Generate one coherent 4×3 sheet per category:

1. furniture
2. technology
3. desk props

Each sheet uses a uniform `#ff00ff` chroma background, even padding, consistent
scale, no characters, no text, and no overlaps. The built-in Image Gen path was
used; no API key or CLI fallback was needed.

## 6. Preserve intermediate data

For every generated pack, retain:

- chroma source sheet
- alpha-removed master sheet
- 12 split transparent PNGs
- versioned JSON manifest
- generation prompt in `imagegen-prompts.md`

Intermediate files are part of the reproducibility record, not disposable
scratch data.

## 7. Manifest every object independently

Every reusable object receives its own stable `id`, category, sprite path,
collision footprint, and z-order hint. When relevant it also receives:

- `surfaceAnchors`
- `seatAnchors`
- `mount: surface`
- `wallMount` or `ceilingMount`
- `stateVariants`

Desk sets are recipes composed from independent objects, never a mandatory
flattened mega-sprite.

## 8. Verify before each checkpoint

Run at least:

```bash
node --check script.js
jq empty assets/manifests/*.json
python3 -m http.server 4173 --directory .
npx playwright screenshot --browser=chromium --viewport-size="1440,1080" \
  http://127.0.0.1:4173 proof/desktop-clean.png
```

Also inspect the exact PNG, not only source code or command exit status.

## 9. Commit by durable milestone

The repository is public. Commit and push each cohesive layer independently:

- base scene and exact crops
- furniture pack
- technology pack
- props pack
- production notes
- runtime catalog/editor work

The worktree should return to clean after every pushed checkpoint.

## 10. Align composition with normalized reference anchors

Map the 1280×960 reference to a 40×30 world, making each grid cell correspond
to 32 reference pixels. Store the target centers and bounding boxes in
`assets/layouts/reference-anchors.v1.json`; do not hide them in CSS offsets.

The default reconstruction is evaluated with:

```bash
npm run score:layout
```

The score weights semantic category at 45%, center position at 35%, and
footprint overlap at 20%. Required anchors must score at least 75 and be within
two cells of the target. Pixel SSIM is deliberately not used because it would
penalize original sprite design rather than structural placement.

## 11. Separate normal tests from proof publication

`npm test` writes screenshots and downloads only to Playwright's ignored
per-run output, keeping a clean worktree clean. Publish fresh proof filenames
only through:

```bash
npm run test:update-proofs
```

This separation prevents random object UIDs and transition timing from silently
rewriting committed evidence.

## 12. Do not substitute structural alignment for visual reproduction

The first reconstruction attempt passed a 14-anchor location score but used
wrong furniture silhouettes, no rendered rotation, generic stage flooring, and
a faded source image as a backdrop. That was a structural prototype, not a
faithful recreation. The corrective contract is in
`docs/reference-fidelity-gate.md` and must pass before any complete-reproduction
claim.

Use `canonical.html` for the current no-UI characterless reference-oriented
render. Treat `builder.html` as a separate modular editor until its source
instance ledger is fully verified.
