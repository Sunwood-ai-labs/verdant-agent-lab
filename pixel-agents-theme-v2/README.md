# Verdant Pixel Agents theme v2

This version fixes the rejected v1 wall atlas. It retains the built-in Image
Gen floor and living-wall masters but deterministically constructs sixteen
distinct wall pieces in Pixel Agents bitmask order (`N=1, E=2, S=4, W=8`).

Contents:

- nine `assets/floors/floor_N.png` tiles at 16×16
- one `assets/walls/wall_0.png` atlas at 64×128
- sixteen distinct 16×32 wall pieces arranged as a 4×4 atlas

The original `pixel-agents-theme/` remains the rejected provenance checkpoint;
it duplicated one wall panel in every bitmask slot and is not current proof.

Pixel Agents 1.3 does not merge external floors/walls from the furniture pack.
The reproducible integration route is therefore
`npm run assemble:pixel-agents-solarpunk-runtime`, which creates a separate
development overlay and deterministic zip under ignored `build/` without
modifying the reference checkout. Runtime acceptance still requires a direct
screenshot.
