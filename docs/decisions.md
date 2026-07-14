# Decision record

## D-001 — fidelity-first flattened base

Decision: keep a generated clean scene as the initial visual base instead of
rebuilding every floorboard and leaf immediately in DOM elements.

Reason: the first user requirement prioritizes complete visual reproduction.
The modular runtime can replace flattened regions progressively without losing
the verified base.

## D-002 — characters are excluded, not merely hidden

Decision: remove people, mascots, and humanoid robots from the public scene and
do not publish the original comparison UI.

Reason: this is an explicit user requirement and an originality boundary.

## D-003 — exact crops and generated sprites stay separate

Decision: preserve scene-derived rectangular crops under `object-crops/` and
transparent reusable sprites under `generated/`.

Reason: one family proves fidelity; the other enables game-style composition.
Mixing them would make provenance and evaluation ambiguous.

## D-004 — built-in Image Gen plus chroma removal

Decision: use built-in Image Gen on a flat magenta background, then remove the
key locally.

Reason: all sprites are opaque pixel-art objects, so native transparency was
not required and no CLI/API key fallback was justified.

## D-005 — modular manifests are project-owned

Decision: use independent JSON manifests inspired by generic asset-catalog
patterns, with project-specific field names and values.

Reason: Pixel Agents is a research reference, not a code or asset dependency.

## D-006 — publish small checkpoints directly

Decision: use a public `main` branch and push each cohesive checkpoint.

Reason: the user explicitly requested a public repository and frequent durable
commits. Intermediate masters and prompts are treated as valuable project data.

## D-007 — no automatic process cleanup under memory pressure

Decision: do not terminate VMs or user-visible applications without clear
ownership even when memory use exceeds 90%.

Reason: preserving user work is more important than reclaiming memory for a
noncritical local render.

## D-008 — reference imagery is opt-in inside the builder

Decision: the builder chrome and default stage do not use the source scene as a
decorative background. The clean scene is available only through the explicit
REFERENCE toggle.

Reason: the builder must read as an original product, while the reference
remains available as a practical placement guide when requested.

## D-009 — placement similarity is structural, not pixel-copy SSIM

Decision: normalize the reference to 40×30 and score semantic category, center
position, and footprint overlap against explicit anchors.

Reason: full-image SSIM would reward copying the source pixels and punish the
original modular sprites. Structural scoring moves furniture toward the photo
without weakening the originality boundary.

## D-010 — proof refresh is opt-in

Decision: normal Playwright runs write into ignored test output; only
`npm run test:update-proofs` writes fresh versioned public evidence.

Reason: random instance UIDs and animation timing previously dirtied tracked
proof files during an otherwise read-only verification run.

## D-011 — reject visually unsafe Image Gen cleanup output

Decision: preserve but do not ship the espresso cleanup candidate that baked a
checkerboard into the pixels and changed scale. Use an audited deterministic
alpha mask against the original transparent sprite.

Reason: a tool call succeeding is not evidence that the resulting asset still
satisfies transparency, size, fidelity, and independent-part constraints.

## D-012 — reference mode trades decorative shadow for compositing safety

Decision: disable CSS drop shadows on placed transparent sprites only while
the translucent reference layer is active, and guard that state with an image
snapshot.

Reason: Chromium rendered some filtered sprite layers as black rectangles over
the opacity-composited reference. Placement comparison is more important than
decorative depth in that explicit mode.

## D-013 — structural score never claims pixel similarity

Decision: call 94.2 the "14-anchor structural placement score" everywhere.

Reason: the scorer evaluates manifest semantics, centers, and footprints; it
does not inspect sprite content or full-image perceptual similarity.

## D-014 — visual-fidelity claim requires a per-instance ledger

Decision: do not call this project a complete reproduction until every
non-character reference instance is verified by content, facing, silhouette,
scale, count, layer, and canonical rendered evidence.

Reason: the prior 14-anchor score allowed wrong furniture, wrong directions,
and whole missing rooms to be labeled as close. The correction is encoded in
`reference-instance-ledger.v1.json` and the failing fidelity validator.
