# Source-direction regeneration audit

Absolute path: `/Users/admin/Prj/sunwood-lab-recreation/docs/source-direction-regeneration-audit.md`.

The acceptance question is whether every sprite can return to its source
position using translation and uniform scale without rotation, mirroring,
shearing, or camera correction. Clean alpha separation alone is insufficient.

## Existing detailed banks

| Bank | Disposition | Evidence |
|---|---|---|
| greenhouse v3 | reuse after cleanup | roof slopes, central bay, beams and verticals preserve source directions |
| AI lab v6 | reuse after cleanup | shelves, benches, terminal and test platform remain source-directed |
| studio west v2 | reuse cells 1–15; remap 16–18 | last-row semantic/output order is cyclically shifted |
| workstation east v1 | reuse after removing cell-3 stray post | primary desk, planter, chair and monitor directions match |
| workstation west v1 | regenerate | desk/planter changed to generic 3/4 angle; monitor visible face is reversed |
| meeting room v2 | regenerate | glass cells contain baked neighboring objects and cell mapping is inconsistent |
| garden cafe v3 | regenerated | fridge/coffee/bookshelf cells contained detached fragments |
| quiet lounge v5 | regenerate | side furniture rotated about 90 degrees and sofa/rug reconstruction is weak |

## Executed corrections

- Zone 01 uses 18 source-direction parts on three horizontal pages.
- Zone 02 was regenerated as 18 parts; four gutter-line components were removed.
- Zone 03 was regenerated character-free as six parts; 102 debris pixels were removed.
- Zone 04 was regenerated as twelve fixtures; a fridge semantic mismatch was
  rejected and replaced with a scale-normalized coffee machine.

Audit preview pages for the rejected existing cafe and quiet-lounge banks are
preserved under `proof/intermediate/source-direction-audit/`.

## Remaining gate

No bank is `runtimeEligible` until its source-position recomposition is rendered
and compared in the same view. AYANO delivery means reviewable candidate, not
placement-ready proof.
