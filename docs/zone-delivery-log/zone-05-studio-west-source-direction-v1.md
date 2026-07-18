# Zone 05 studio west source-direction regeneration

Absolute path: `/Users/admin/Prj/sunwood-lab-recreation/docs/zone-delivery-log/zone-05-studio-west-source-direction-v1.md`.

Eighteen existing Image Gen v2 parts were audited for source-local direction,
copied into a clean bank, and cropped to their non-zero alpha bounds. The v2
splitter had assigned the last row cyclically: the tiny device was stored under
the drawer filename, the drawer under the open-cabinet filename, and the open
cabinet under the tiny-device filename. The trim mapping corrects that without
rotating, mirroring, or redrawing any asset.

## AYANO delivery

Pending delivery after the asset commit. The delivery remains a
source-direction candidate; same-view reassembly scoring remains open and
`runtimeEligible` remains false.
