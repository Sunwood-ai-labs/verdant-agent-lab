# Verdant Pixel Agents theme overlay

Original floor and wall files using Pixel Agents' bundled-theme dimensions:

- nine `assets/floors/floor_N.png` files at 16×16
- one `assets/walls/wall_0.png` atlas at 64×128, containing sixteen 16×32 pieces

Pixel Agents 1.3 only merges furniture, characters, and pets from external
directories. It does not currently merge external floor or wall files.
Therefore this directory is deliberately separate from `pixel-agents-pack/`.
It can be used in a development/runtime overlay or after Pixel Agents adds a
floor/wall external-loader contract. Do not copy it over an installation
without preserving the original installation assets.
