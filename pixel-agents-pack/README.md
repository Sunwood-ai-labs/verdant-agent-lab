# Verdant Pixel Agents pack

Original solarpunk office sprites authored for Pixel Agents' documented
external-asset contract. No Pixel Agents artwork, characters, layout, logos, or
source files are redistributed here.

## Install

In Pixel Agents Settings, add this directory as an external asset directory:

```text
/Users/admin/Prj/sunwood-lab-recreation/pixel-agents-pack
```

The current pack contains 30 physical PNG sprites across 19 manifests (33
runtime catalog entries after mirrored/animated variants), including:

- `DESK`: front and side orientations, overriding the bundled desk IDs
- `WOODEN_CHAIR`: front, back, right side, and runtime-mirrored left side
- `PLANT`: compact tall decor overriding the bundled plant ID
- PC on/off/animation and directional variants
- sofas, benches, coffee/small/collaboration tables
- bookshelves, paintings, clock, whiteboard, coffee, bins, and additional plants

The matching built-in IDs are intentional: Pixel Agents merges external assets
after built-ins and the later entry wins. Therefore the existing default layout
uses these replacements without editing its layout JSON.

All runtime canvases use exact 16 px tile multiples. Run the deterministic
build and metadata check from the repository root:

```bash
python3 scripts/build-pixel-agents-pack.py
python3 scripts/validate-pixel-agents-pack.py
python3 scripts/build-pixel-agents-verdant-room.py
```

`verdant-runtime-layout.json` is the current 42x34, six-zone Pixel Agents room:
cafe/ideas, reception, lounge, collaboration, open office, and AI lab. It uses
the runtime's known-good floor and wall assets because the generated v3 theme
atlas failed direct visual QA. The custom theme is preserved separately as a
rejected/prototype checkpoint, not the current room proof.

The room demonstrates a coherent use of the current assets. It is not yet a
complete visual reproduction of every object in the supplied office reference.
