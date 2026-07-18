# Zone 05 studio west source-direction packaging

This candidate reuses the previously generated Image Gen v2 bank rather than
inventing a new camera view. The source crop `assets/parts/work-studio.png` is
the authority for each object's local direction.

Operational constraints:

- preserve each object's visible face, rotation, and silhouette from the crop;
- no global front-facing conversion and no generic isometric conversion;
- remove transparent padding by cropping to the non-zero alpha bounds;
- correct the v2 splitter's cyclic semantic/output mismatch for cells 16–18;
- keep the candidate `runtimeEligible: false` until same-view reassembly is
  scored against the source crop.

The exact source-to-output remap is recorded in
`assets/layouts/studio-west-source-direction-trim-map.v1.json`.
