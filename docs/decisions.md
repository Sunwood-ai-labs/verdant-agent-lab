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
