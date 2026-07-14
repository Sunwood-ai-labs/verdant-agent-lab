# Reference fidelity gate — incomplete

This project is **not yet a complete visual reproduction** of the supplied
reference. The earlier 14-anchor structural placement score is a diagnostic
for rough zone locations only. It does not inspect sprite contents, facing,
silhouette, count, room topology, or full-image similarity and must never be
used as a completion claim.

## Authoritative completion surface

The only authority for faithful-reproduction completion is a same-view,
1280×960 visual comparison between the private characterless canonical target
and a canonical HTML render with no editor UI, selected outlines, or reference
overlay. A translucent reference behind unrelated generated objects is invalid
evidence.

## Required gates

1. Every non-character source instance is present in
   `assets/layouts/reference-instance-ledger.v1.json`.
2. Every required instance has `status: verified`; semantic proxies are not
   allowed.
3. Object content, facing/orientation, silhouette, scale, count, and layer
   order all match the source record.
4. The renderer uses the layout `rotation` and footprint aspect ratio, or the
   instance owns a direction-specific sprite where rotation would be visually
   wrong.
5. Canonical side-by-side, overlay/blink, absolute-diff, zone-diff, and
   per-instance crop evidence are versioned and reviewed.
6. A validator exits nonzero for missing, proxy, unverified, orientation-fail,
   or count-mismatch ledger records.

Until all six gates pass, label the work **structural prototype**, not complete
reproduction.

## Confirmed current mismatches

- generic square-like rendering ignores manifest width/height and rotation
- reception counter, worktables, sofas, chairs, solar array, cafe, greenhouse,
  displays, server bank, and AI lab contents differ from the source
- room walls, shelves, cafe facade, greenhouse roof/trusses, garden borders,
  and most environment topology exist only in the faded source image, not as
  HTML reconstruction layers

The next implementation step is to replace these with source-derived or
direction-specific modular assets, beginning with the P0 ledger rows.

## Asset provenance correction

The builder currently consumes 36 generated sprites, not source crops. The 30
files under `assets/object-crops/` are opaque rectangular cuts from the
Image-Gen-cleaned derivative `scene-clean.png`; they are not raw-original crops
or isolated runtime assets. `assets/manifests/source-crops.v1.json` records
this explicitly, and `npm run audit:asset-provenance` checks it.
