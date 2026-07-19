# Publication log

Repository: <https://github.com/Sunwood-ai-labs/verdant-agent-lab>

| Commit | Description | Durable output |
|---|---|---|
| `4016921` | Base Verdant Lab scene | clean scene, HTML, 10 regions, 30 exact crops, proofs |
| `29d7509` | Furniture sprite pack | chroma/alpha masters, 12 sprites, furniture manifest |
| `151c618` | Technology sprite pack | chroma/alpha masters, 12 sprites, technology manifest |
| `0f8d015` | Independent desk props | chroma/alpha masters, 12 sprites, props manifest |
| `a2201f3` | Reproducible asset pipeline | prompts, workflow, alpha/crop details, provenance ledger |
| `e8b067c` | Architecture and QA lessons | runtime design, decisions, failure log, publication ledger |
| `21ca3b8` | Publication checkpoint ledger | synchronized public commit history |
| `9472823` | Modular pixel lab editor | 36-object catalog, placement, drag, persistence, export, tests |
| `549c829` | Builder publication checkpoint | public-state ledger and verified repository metadata |
| `6e8cf8a` | Hardened interaction and proof suite | keyboard parity, focus/state semantics, mobile layout, seven proof artifacts |
| `de15072` | Reference-anchor reconstruction | 41-instance photo-aligned layout, 94.2 structural-placement gate, cleaned sprites, v4 proofs |
| `7de05f1` | Semantic furniture separation | desk-only reception, table-only worktable, safe reference compositor, visual snapshot, v5 proofs |
| `2b149f3` | Negative-control regression gate | proves the sprite validator rejects both preserved known-bad furniture fixtures |
| `bf466b4` | Fidelity-claim correction | canonical characterless render, object-level failing ledger, rotation/aspect rendering, v6 comparison proof |
| `9b3735d` | Crop provenance correction | records that 30 derivative opaque crops are not runtime single-object source assets |
| `70af0e7` | Pixel Agents compatibility contract | locks 16px tiles, manifests, direction, collision, seat, and live-runtime acceptance gates |
| `a1507ea` | First solarpunk external asset pack | raw/alpha/split provenance, six runtime sprites, manifests, validator, and room proof |
| `686d105` | Default workstation ID override | changes the pack from additive IDs to actual `DESK` / `WOODEN_CHAIR` / `PLANT` replacements |
| `fe340d3` | First Pixel Agents QA receipt | validation, local registration, proof limits, and AYANO delivery record |
| `5f1d981` | Complete default furniture override pack | 30 physical sprites, 19 manifests, 25/25 default ID coverage, raw/alpha/split masters |
| `50d96c2` | Rejected floor/wall theme prototype | preserves generated theme inputs and failed repetitive live proof as QA evidence |
| `2e35887` | Coherent Verdant live room correction | 42x34 six-zone layout, 45 placements, runtime proof, and recurrence-prevention decision |
| `b6bac90` | Five source-guided Pixel Agents zone sheets | raw/alpha/split provenance, 28 approved grid assets, seven-category editor-safe manifests |
| `4f16392` | Source-zone room and editor verification | revision-5 room, 48 placements, two-page catalog, 28/28 editor discovery, direct placement proof |
| `69a818d` | Literal Pixel Agents default-office reskin | byte-identical 21×22 default layout, 36 unchanged placements, before/after runtime proof, rotated desk placement |
| `905d2d9` | Verdant runtime interaction verification | 14/14 seats, collision rejection, 15-tile path, seat return, four-way chair facing/mirror/depth proof |
| `3b45f4a` | Missing-core six-asset batch | raw/alpha/split provenance, six grid sprites, manifests, and 67-entry catalog |
| `3469136` | Revision-6 clipping correction | six live placements, rejected lower-frame proof, corrected runtime proof, collision/walkability and 6/6 editor checks |
| `6d88b8a` | Connected solarpunk theme candidate | nine unique floor tiles, sixteen mask-correct wall pieces, split intermediates, deterministic validator |
| `87dea2c` | Source-shaped revision-7 room correction | rejects the unrelated 21x22 theme render, restores 42x34 ten-zone topology, 65 placements, direct wall colors, accepted and rejected raster evidence |

Each checkpoint was pushed to `origin/main` immediately after validation. Add
new rows whenever a new public checkpoint is created.

AYANO delivery receipt: Discord channel `1526794078744744077`, message
`1528331042551889970`, attachment `room-16px-grid.png`. The report explicitly
labels this as the workstation batch and lists the still-missing office classes.

Corrected room delivery receipt: Discord channel `1526794078744744077`, message
`1528340047852470414`, attachment `live-verdant-room-v2.png`. The report states
42x34, six zones, 45 placements, 38/38 furniture loaded, zero browser errors,
and explicitly labels the image as a coherent current-asset room rather than a
complete reproduction.

Source-zone v5 delivery receipt: Discord channel `1526794078744744077`, message
`1528349981579280554`. Attachments are `live-source-zones-v2.png`, both accepted
source-zone catalog pages, and `editor-placement-proof.png`. The report states
the 28/30 acceptance boundary, pack counts, 28/28 editor discovery, zero browser
errors, and the remaining incomplete fidelity and interaction gates. An earlier
multipart draft (`1528349884715892828`) was deleted immediately because it
  incorrectly exposed `payload.json` as a user-visible attachment.

Default-office reskin delivery receipt: Discord channel `1526794078744744077`,
message `1528352757545963560`. Attachments are
`default-reskin-before-after-v1.png` and `editor-desk-side-placement.png`. The
report distinguishes the verified default-office exact-ID substitution from
the still-incomplete full 1280×960 reference reproduction.

Runtime-interaction delivery receipt: Discord channel `1526794078744744077`,
message `1528355085355192342`. Attachments are
`runtime-interaction-proof.png` and `runtime-interaction-proof.json`. The report
states the exact seat, walk, collision, return, rotation, facing, mirror, and
depth results and keeps remaining pack-wide visual rotation and source-asset
coverage open.

Missing-core revision-6 delivery receipt: Discord channel
`1526794078744744077`, message `1528360598478524527`. Attachments are the final
character-free room proof `live-missing-core-layout-clean-v3.png`, the raw 3×2
asset sheet, and `runtime-proof.json`. The report explicitly records the first
lower-frame clipping failure, the corrected 64-sprite / 53-manifest / 67-entry
runtime, 6/6 editor discovery, zero collision overlap, zero browser errors, and
the still-incomplete west-studio/site-shell coverage.

Revision-7 publication checkpoint: commit `87dea2c`. The accepted current-asset
proof is `proofs/pixel-agents-v7/live-source-shaped-layout-wall-fix.png`; the
three default-layout theme screenshots remain explicitly rejected evidence.
AYANO delivery receipt: Discord channel `1526794078744744077`, message
`1528367087288844431`. Attachments are the focused and full revision-7 runtime
rasters. The report explicitly rejects the 21x22 default-layout candidate and
labels revision 7 as a current-asset intermediate rather than complete fidelity.
