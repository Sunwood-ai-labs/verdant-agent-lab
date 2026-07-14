# Asset provenance ledger

## Public runtime assets

| Asset family | Count | Provenance | Public status |
|---|---:|---|---|
| Clean scene | 1 | Image Gen edit of user-provided reference | Included |
| Region crops | 10 | Deterministic crops from clean scene | Included |
| Exact object crops | 30 | Deterministic crops from clean scene | Included |
| Furniture sprites | 12 | Original Image Gen output for this project | Included |
| Technology sprites | 12 | Original Image Gen output for this project | Included |
| Desk-prop sprites | 12 | Original Image Gen output for this project | Included |
| Chroma master sheets | 3 | Original Image Gen intermediate output | Included |
| Alpha master sheets | 3 | Local chroma-removal derivative | Included |
| Proof screenshots | 4 | Local browser renders of this project | Included |

## Excluded inputs

| Input | Reason | Repository handling |
|---|---|---|
| User-provided reference JPG | Contains the original character-bearing scene and is not needed at runtime | `.gitignore`; not published |
| Local clone of Pixel Agents | Research-only primary source; no code or assets are incorporated | `.gitignore`; not published |

## External inspiration

Pixel Agents is used only as an architectural research source. This repository
does not ship its furniture, characters, layout JSON, screenshots, logo, UI
copy, or source code. See `research/pixel-agents/notes/architecture-notes.md`.

## Release gate for future assets

Every new asset must record:

- creator or generator
- source/reference role
- generation prompt or transformation command
- license or project-use status
- whether it contains third-party text, logo, character, or recognizable design
- validation path and exact public file
