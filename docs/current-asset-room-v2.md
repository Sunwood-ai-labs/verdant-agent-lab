# Current asset room v2

Absolute path: `/Users/admin/Prj/sunwood-lab-recreation/docs/current-asset-room-v2.md`.

This is the corrected character-free HTML assembly loaded by `room.html`.
Unlike rejected v1, it does not fit a sprite to its full source-zone crop.
Every zone uses the established center anchor and manifest footprint from the
Builder layout, with zero rotation and zero mirroring.

## Verification

- Active layout: `assets/layouts/current-room-composite.v2.json`
- Clean proof: `proof/current-asset-room-v2.png` (1280×960)
- UI proof: `proof/current-asset-room-ui-v2.png` (1440×1050)
- Direct masked grayscale SSIM: `42.02%` — improved from v1's `29.27%`, but
  still below the project's `60%` completion gate.
- Diagnostics only: Edge F1 `78.93%`, Lab histogram `95.18%`, weighted pixel
  composite `54.72%`. These do not override the failed direct SSIM.
- The clean raster was inspected after rendering. Cross-zone overlap and the
  large top-zone stretching from v1 are removed.
- The current remaining mismatch comes primarily from weak candidate content
  inside the meeting room, workstation west, and south lounge, not from fitting
  assets to whole zone rectangles.
- `tests/current-room.spec.js`: pass with fourteen independent HTML layers and
  no private reference or `scene-clean.png` runtime overlay.

This remains an intermediate assembly, not a complete reproduction.
