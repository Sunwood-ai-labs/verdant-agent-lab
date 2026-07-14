# Reference-derived placement diagnostic

> This is a structural location diagnostic only. It does not establish visual
> fidelity or complete reproduction. The authoritative gate is
> `docs/reference-fidelity-gate.md`.

## Coordinate model

The 1280×960 input and the 40×30 builder world share a 4:3 aspect ratio. One
builder cell therefore represents 32 source pixels. Object coordinates are
center anchors, matching the runtime's `translate(-50%, -50%)` projection.

## Major anchors

| Zone | Asset | Grid center |
|---|---|---:|
| Solar wing | solar array | 3, 4 |
| Reception | curved reception desk | 20, 6 |
| North lounge | olive sofa / coffee table | 29, 6 / 29, 8 |
| Cafe | espresso machine | 35, 6 |
| Studio | shared worktable | 14, 12 |
| Meeting room | shared worktable | 25, 12 |
| AI lab | lab console / robotics platform | 31, 12 / 34, 13 |
| Work area | two shared worktables | 15, 20 / 23, 20 |
| Greenhouse | greenhouse door | 4, 24 |
| South lounge | olive sofa | 32, 23 |
| Utility | recycling bins | 34, 27 |

The full machine-readable list, target bounding boxes, acceptance values, and
known asset gaps live in `assets/layouts/reference-anchors.v1.json`.

## Score

```text
score = 100 × (0.45 × category + 0.35 × position + 0.20 × footprint IoU)
```

- exact asset/category match scores 1.0; same-category proxy scores 0.75
- position is a two-cell Gaussian around the target center
- occupancy uses intersection-over-union between the candidate footprint and
  the target box
- every major anchor must score at least 75 and remain within two cells
- the overall mean must be at least 75

Current starter result: **94.2 / 100 structural placement score**, with all 14
required anchors passing. This is not a full-image perceptual similarity score.

## Known gaps

- The current cafe counter uses `shared-worktable` as an explicit proxy.
- The greenhouse pack has no vertical glass-wall rotation variant yet.

These remain named gaps instead of being hidden by an inflated similarity
claim.
