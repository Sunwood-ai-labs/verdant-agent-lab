# Zone 01 solar wing delivery log

Absolute path: `/Users/admin/Prj/sunwood-lab-recreation/docs/zone-delivery-log/zone-01-solar-wing-v1.md`.

## Artifacts

- Chroma master: `assets/intermediate/zone-01-solar-wing/solar-wing-2x3-v1-chroma.png`
- Alpha master: `assets/intermediate/zone-01-solar-wing/solar-wing-2x3-v1-alpha.png`
- Six children: `assets/generated/zones/solar-wing-v1/`
- Contract: `assets/layouts/zone-01-solar-wing-2x3.v1.json`
- Prompt: `assets/prompts/zone-01-solar-wing-2x3-v1.md`
- Split evidence: `proof/intermediate/zone-01-solar-wing-split-v1.json`
- Private source comparison raster: `proof/intermediate/zone-01-solar-wing-source-comparison-v1.png` (gitignored because it contains a source crop)

## Verification

- `python3 -m unittest tests/test_split_zone_2x3_sheet.py -v`: pass.
- Six children emitted in row-major order; all report `edgeFlags` false.
- `npm run audit:asset-provenance`: current builder runtime still uses only
  generated assets and no source-derived crop sprites.
- Candidate is **not source-verified**: the generated solar panel face uses a
  2×2 subdivision while the reference uses a 2×3 array. Dashboard text is
  deliberately blank pending deterministic HTML/Canvas overlay.

## AYANO delivery

Pending zone commit and push. The delivery must attach the chroma master and
private split comparison proof, name the commit SHA, and report the returned
Discord message id below.

- Channel: pending live verification
- Message id: pending
