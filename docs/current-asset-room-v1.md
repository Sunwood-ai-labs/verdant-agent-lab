# Current asset room v1

Absolute path: `/Users/admin/Prj/sunwood-lab-recreation/docs/current-asset-room-v1.md`.

`room.html` is an intermediate, character-free room assembled from the current
runtime candidate assets. It intentionally does not load the supplied reference
image or `assets/scene-clean.png` as an overlay. The foundation is the existing
Image Gen architecture-only layer, and each visible zone is a separate HTML
image layer described by `assets/layouts/current-room-composite.v1.json`.

This is a placement-review surface, not a fidelity completion claim:

- Zone 01–05 point to the latest source-direction candidate manifests, while
  their current recomposed zone images are used as the first integration proxy.
- Zone 06, 09, and 11 remain known regeneration targets.
- The layout keeps every zone at zero rotation and zero mirroring.
- `runtimeEligible` remains false until same-view comparison and the
  per-instance ledger pass.

Open `room.html` for the inspection UI or `room.html?clean=1` for a clean
1280×960 proof capture.

## Verification

- Clean proof: `proof/current-asset-room-v1.png`
- Inspection UI proof: `proof/current-asset-room-ui-v1.png`
- Direct same-view masked grayscale SSIM: `29.27%` — fail, below the `60%`
  project threshold.
- Diagnostics only: Edge F1 `72.25%`, Lab histogram `82.60%`, weighted pixel
  composite `43.20%`. These do not override the failed direct SSIM.
- `tests/current-room.spec.js`: pass. It confirms thirteen room layers and
  rejects both the private reference and `scene-clean.png` as runtime images.
- Full Playwright run: 12 passed, 1 existing builder reference-snapshot test
  failed with 12,470 differing pixels. The new room test and all other tests
  passed; the unrelated builder snapshot was not rewritten.
