# Sunwood Lab Recreation Instructions

## Reference-direction asset decomposition

When decomposing the supplied reference office into reusable assets, preserve
the source image's viewing direction for every asset. Do not convert a
front-facing, elevation, or top-down source object into isometric/perspective
art merely because that is a common pixel-art default.

- Record each source object's direction in its layout manifest before
  generation or extraction.
- Treat a generated sprite with a changed camera angle as `orientation-mismatch`
  even if its semantic label, colors, and alpha split are otherwise valid.
- The acceptance gate is a same-view comparison against the corresponding
  source-zone crop, not only clean alpha bounds or a successful split.
- Keep prior mismatched assets as rejected intermediate provenance; do not use
  them in new manifests or present them as placement-ready.
