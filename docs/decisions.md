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

## D-015 — default asset loading is not a composed-room proof

Decision: reject the repeated four-quadrant Pixel Agents demo and the unverified
v3 floor/wall overlay as current room evidence. Use one connected six-zone
layout and keep built-in floors/walls until custom atlases pass direct runtime
inspection.

Reason: replacing IDs in a repetitive default layout proved loader compatibility
but produced a visually chaotic office. The authoritative proof surface is the
actual Pixel Agents screenshot, not manifest coverage or server logs alone.

## D-016 — the supplied office owns the accepted room coordinate system

Decision: never present a Pixel Agents default-layout reskin as the current
reconstruction of the supplied office. Compatibility diagnostics may use it,
but accepted room candidates must keep a named zone-to-grid mapping derived
from the 1280x960 reference and must be checked as a full runtime raster.

Reason: the rejected 21x22 render loaded valid assets but erased the solar,
greenhouse, studio, meeting, lab, lounge, cafe, and entrance relationships that
make the reference recognizable. Runtime compatibility and room composition are
separate acceptance gates.

## D-017 — default-office preset and source-office reconstruction are separate products

Decision: accept the 21×22 integrated preset as the Pixel Agents default-office
solarpunk reskin requested by the user, while continuing to treat the 42×34
source-shaped room and full 1280×960 reproduction as a separate fidelity track.
The preset may preserve Pixel Agents' MIT-licensed default layout, but all
Verdant furniture/floor/wall art remains project-authored and the reference
checkout remains read-only.

Reason: rejecting a default-layout proof as evidence for the supplied photo does
not make it invalid for the distinct goal of reskinning Pixel Agents' default
office. The two claims require different authoritative views and must not be
collapsed again.

## D-018 — a movement GIF must show the runtime character moving

Decision: when a Pixel Agents room request says to "move it" and asks for a
GIF/video, the default interpretation is an actual Pixel Agents character
walking in the room. Editor clicks, palette browsing, camera motion, cursor
animation, or CSS-only sprite translation are not substitutes unless the user
explicitly requests an editor demo.

Reason: the first capture plan incorrectly translated "move it" into layout
editor interaction. The accepted capture instead registers a temporary remote
agent, uses Pixel Agents' built-in character sprite and production
`OfficeState.walkToTile` path through real canvas context-menu input, and hides
only the activity-label DOM layer so it cannot cover the small sprite.

## D-019 — capture runtime motion without selection or hover decoration

Decision: selecting a character is allowed only for the instant required to
issue a real Pixel Agents walk command. Clear selection immediately afterward,
move the capture cursor away from the character, and visually inspect sampled
frames before accepting a movement GIF.

Reason: Pixel Agents intentionally renders a one-pixel white outline around a
selected character. The first walk GIF left the temporary remote Agent selected
throughout the recording, so a UI affordance was mistaken for part of the
sprite and baked into every walking frame.

## D-020 — spacious office is a separate additive preset

Decision: keep the accepted 21×22 default-office preset intact and publish the
wider office as a separate 35×22 variant. Insert a new 14-column central studio,
shift the original east lounge without changing its internal arrangement, and
retain the original west work area. New desks, PCs, chairs, shelving, and plants
must remain independent Pixel Agents placements.

Reason: "make the office wider" should increase usable floor and circulation,
not stretch raster assets or silently replace the already accepted compact
preset. The spacious variant is a Pixel Agents product layout; it remains
separate from the 42×34 source-photo reconstruction fidelity track.

## D-021 — screenshot owns spacious-layout acceptance

Decision: accept or reject room width, spacing, balance, clipping, overlap, and
animation cleanliness from the actual Pixel Agents runtime screenshot and GIF
frames. Layout dimensions, placement totals, collision results, and walkable
tile counts may explain the result but cannot replace visual inspection.

Reason: the user explicitly required screenshot-based confirmation after the
35×22 expansion. The same clean runtime image showed both the successful width
increase and the remaining visual polish notes: a deliberately sparse lower
east zone and repeated workstation-module language in the center.

## D-022 — place assets as readable functional clusters

Decision: improve spatial naturalness by giving each furniture group a visible
purpose, varying major silhouettes between adjacent zones, preserving open
circulation, and keeping every floor pocket reachable. Reuse an approved asset
when it fits the needed function and viewing direction; use Image Gen editing
only when the existing catalog cannot supply a coherent part.

Reason: screenshot QA of spacious v1 exposed two visual issues hidden by valid
counts: a repeated workstation module and an underused east-lounge floor. The
accepted v3 replaces the duplicate center table with an AI electronics bench,
adds a low planter and wall whiteboard, and turns the east floor into a coffee,
flower, and recycling corner. No new image generation was needed.

## D-023 — align surface props by visible support plane

Decision: for layered furniture, place the supporting asset first and align
surface props against the support's visible top plane in a runtime screenshot.
In the Pixel Agents 16 px grid, a 16×32 front-facing PC paired with a 48×32
`DESK_FRONT` must use an anchor one row above the desk. Apply the relationship
to every matching workstation, not only the first instance noticed.

Reason: placing `PC_FRONT_*` at the same row as `DESK_FRONT` made the monitors
render across the desk front instead of resting on the desktop. Placement and
collision data did not reveal the visual error; the authoritative check is the
actual composed runtime screenshot.
