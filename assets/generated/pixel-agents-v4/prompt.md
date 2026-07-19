# Pixel Agents source-zone Image Gen prompts — v4

Generated with the built-in Image Gen tool on 2026-07-19.

Reference roles:

- `assets/reference-original.jpg`: authoritative solarpunk office contents and facing
- `proofs/pixel-agents-v2/live-pixel-agents-before-reload.png`: Pixel Agents scale, camera, silhouette, and pixel rendering reference

Shared contract:

- horizontal sheet, exactly 3 columns by 2 rows
- one independent object per cell
- preserve the object's facing from the office reference
- top-down-leaning 3/4 orthographic, never isometric
- crisp Pixel Agents-scale retro pixel art
- flat `#FF00FF` chroma background; no floor, shadow, text, logo, character, or humanoid robot

## Reception

Cells: curved counter body; front planter; monitor back; angled terminal; clipboard/papers; information easel.

## Cafe

Cells: shelf with exactly six pots; straight service counter; exactly three white/silver dispensers; refrigerator; narrow kiosk; framed living wall.

## AI lab

Cells requested: robot-free diagnostic platform; analyzer cart; device bookshelf; diagram board; electronics bench; non-humanoid sensor pedestal.

QA disposition: cell 1 was rejected because Image Gen added a humanoid robot.
Cell 6 was also rejected because the sensor pedestal still reads as a robot
head/body. Both remain in the raw/alpha sheet but are not split or runtime-wired.
The four equipment-only cells are accepted as candidates.

## Greenhouse

Cells: ridge roof; left roof slope; right roof slope; glass wall panel; entrance door; plant/grow shelf.

## Solar wing

Cells: vertical 2x3 solar panel; separate frame; output dashboard without text; battery/server bank; controller; vine planter.

The complete prompts were supplied directly in the built-in tool calls. This file preserves the cell specification and rejection decision used by the deterministic processor.
