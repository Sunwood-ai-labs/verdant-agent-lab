# Zone 04 cafe v2 comparison and regeneration log

Absolute path: `/Users/admin/Prj/sunwood-lab-recreation/docs/zone-delivery-log/zone-04-cafe-v2.md`.

## Why v1 was rejected

The authoritative source is `assets/reference-original.jpg` bbox
`[1023, 36, 1213, 245]`. Direct visual review rejected the v1 sheet because
the curved mug cabinet, tall glass coolers, full-height grinder espresso
machines, dense greenery, and deep sign did not preserve the source Cafe's
compact 3/4 top-down silhouettes or relative scale. All six v1 children also
retained visible magenta fringe after hard chroma removal.

## v2 regeneration

The entire six-cell sheet was regenerated in one built-in Image Gen pass with
the authoritative Cafe crop and rejected v1 sheet as separate references. V2
uses a straight cabinet, shallow seven-pot greenery fixture, slim left shelf,
blue-panel right vending cabinet, three compact countertop dispensers, and a
thin blank sign strip. `CAFE` remains a deterministic text overlay.

A strict second comparison found seven pots instead of the source's six and a
remaining brown bean-chamber shape in the three dispensers. A second
identity-preserving Image Gen edit changed only those two cells: the fixture
now has exactly six pots and the dispensers are short white/silver boxes with
no brown or transparent hopper. The pre-edit v2 masters remain alongside the
accepted master as `v2-initial-*` history.

The raw chroma result is preserved at
`assets/intermediate/zone-04-cafe/cafe-2x3-v2-chroma.png`. Chroma removal used
the installed `remove_chroma_key.py` helper with border auto-key, soft matte,
thresholds 12/220, and despill. The split script now preserves pre-existing
soft alpha rather than re-keying transparent RGB values.

## Verification

- Source comparison: `proof/intermediate/zone-04-cafe-source-comparison-v2.png`
  (private and gitignored because it contains the source crop).
- Split report: `proof/intermediate/zone-04-cafe-split-v2.json`.
- Six of six cell edge flags are false.
- Six of six children have zero nontransparent pixels within RGB distance 80
  of the sampled chroma key.
- Soft edge alpha is preserved; every child contains partial-alpha pixels.
- `python3 -m unittest tests/test_split_zone_2x3_sheet.py -v` passes 4/4.

V2 is accepted as the source-reviewed improved asset candidate for this sheet
comparison task. Runtime placement and deterministic `CAFE` text remain open
and must not be described as completed by this regeneration.

## AYANO delivery

Pending v2 commit/push and live receipt.
