# Zone 05 studio west source-direction regeneration

Absolute path: `/Users/admin/Prj/sunwood-lab-recreation/docs/zone-delivery-log/zone-05-studio-west-source-direction-v1.md`.

Eighteen existing Image Gen v2 parts were audited for source-local direction,
copied into a clean bank, and cropped to their non-zero alpha bounds. The v2
splitter had assigned the last row cyclically: the tiny device was stored under
the drawer filename, the drawer under the open-cabinet filename, and the open
cabinet under the tiny-device filename. The trim mapping corrects that without
rotating, mirroring, or redrawing any asset.

## AYANO delivery

Delivered after asset commit `bf88716` to `アヤノの部屋 /
#sunwood-lab-recreation` (`1526794078744744077`).

- Message id: `1528025409889767519`
- `zone-05-studio-west-parts-page-01.png` — 196,911 bytes
- `zone-05-studio-west-parts-page-02.png` — 92,336 bytes
- `zone-05-studio-west-parts-page-03.png` — 98,881 bytes
- `zone-05-studio-west-source-crop.png` — 129,267 bytes
- Delivery status: source-direction candidate; same-view reassembly scoring
  remains open and `runtimeEligible` remains false.
