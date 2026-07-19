# Sunwood Lab Recreation Instructions

## Pixel Agents compatibility gate

When the deliverable is intended for Pixel Agents, the Pixel Agents runtime
contract overrides this project's older 32px/40x30 HTML-builder conventions.
Use exact 16px tile multiples, external-pack folder structure, per-item
manifests, declared footprints, supported orientation groups, and runtime seat,
collision, mirroring, and depth semantics. Never claim compatibility from an
HTML screenshot or project-native manifest alone; load and inspect the pack in
the actual Pixel Agents canvas first. Treat the Pixel Agents checkout as
read-only reference material and create original art only.

## Reference-direction asset decomposition

When decomposing the supplied reference office into reusable assets, preserve
the source image's exact local viewing direction for every individual asset.
The goal is to turn the complete reference image into independently placeable
parts that reassemble into the same view. Do not normalize all parts to one
shared direction such as `front-facing`, and do not convert them to a generic
isometric/perspective view.

- Record each source object's own direction, visible face, rotation, and
  silhouette in its layout manifest before generation or extraction. Directions
  within one sheet may and often should differ.
- Treat a generated sprite with a changed camera angle as `orientation-mismatch`
  even if its semantic label, colors, and alpha split are otherwise valid.
- Treat a sheet that forces every asset to `front-facing`, `top-facing`, or any
  other common angle as rejected unless the source independently shows every
  listed object at that exact angle.
- Use the supplied source image's visible pixels as the primary asset evidence.
  Crop and mask each visible object in-place first. Image Gen may clean edges,
  remove neighboring objects, or infer occluded portions, but it must preserve
  the visible source-facing pixels, camera angle, scale relationship, and
  silhouette. A semantically similar redraw is not a decomposed source asset.
- The acceptance gate is a same-view comparison against the corresponding
  source-zone crop, not only clean alpha bounds or a successful split.
- Keep prior mismatched assets as rejected intermediate provenance; do not use
  them in new manifests or present them as placement-ready.

## HTML room assembly placement gate

When assembling decomposed or recomposed sprites into the HTML room, never fit
an asset to the full source-zone crop rectangle. A zone crop describes the
review area, not the sprite's visual footprint. Use the asset manifest's
center/anchor and visual footprint (or a measured alpha-aware placement box)
for position and scale. Preserve the sprite's declared direction with zero
rotation and zero mirroring.

- Keep rejected assembly screenshots and layouts as provenance, but remove
  them from the active runtime.
- Render a fresh clean 1280×960 screenshot after every placement revision.
- Compare that screenshot directly with the supplied reference for overlaps,
  scale, empty zones, and object order before calling the room coherent.
- A passing DOM/image-load test is not visual QA. If the rendered room is
  cluttered, stretched, overlapping, or visually disordered, the assembly is
  rejected even when all assets loaded successfully.
