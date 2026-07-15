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

Delivered after the asset commit `bd836ec23022eb237a51b996feb89d05e947c84c`.
The embed explicitly labels this set as a candidate, includes the 2×2 versus
2×3 panel mismatch, and attaches both the generated master and private
source-to-child comparison proof.

- Guild: `アヤノの部屋` (`1515231898908098633`)
- Channel: `#sunwood-lab-recreation` (`1526794078744744077`), verified live
- Message id: `1526957577785839689`
- Attachments: `solar-wing-2x3-v1-chroma.png` (1,476,431 bytes) and
  `solar-wing-source-to-children-proof-v1.png` (506,359 bytes)
- Delivery method: Discord API multipart request with
  `User-Agent: codex-discord-ayano-bot-skill/1.0`; `payload_json` requires
  curl `--form-string` to remain valid JSON.
