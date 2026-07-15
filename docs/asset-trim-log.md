# Runtime sprite trim log

This record tracks transparent-margin cleanup separately from source-crop
repair. Absolute path: `/Users/admin/Prj/sunwood-lab-recreation/docs/asset-trim-log.md`.

## 2026-07-15 — v1 transparent margin pass

- Command: `npm run trim:runtime-sprites`
- Policy: crop only sprites with a fully transparent alpha boundary, preserve an
  8px transparent pad, and never overwrite the source PNG.
- Result: 22 runtime assets gained `assets/generated/trimmed/*-trimmed-v1.png`
  variants. Their manifests retain `trimmedFrom`, source dimensions, alpha bbox,
  and pre-trim margins.
- Excluded: 25 runtime assets have opaque pixels on one or more canvas edges.
  They remain `EDGE-CUT RISK` and require regeneration/re-extraction rather
  than further automatic trimming.
- Verification: `npm run audit:sprite-bounds`; `npx playwright test
  tests/builder.spec.js tests/similarity.spec.js`; and visual inspection of
  `proof/runtime-asset-catalog-v4.png`.
