# Verdant Pixel Agents pack

Original solarpunk office sprites authored for Pixel Agents' documented
external-asset contract. No Pixel Agents artwork, characters, layout, logos, or
source files are redistributed here.

## Install

In Pixel Agents Settings, add this directory as an external asset directory:

```text
/Users/admin/Prj/sunwood-lab-recreation/pixel-agents-pack
```

The current workstation checkpoint contains:

- `DESK`: front and side orientations, overriding the bundled desk IDs
- `WOODEN_CHAIR`: front, back, right side, and runtime-mirrored left side
- `PLANT`: compact tall decor overriding the bundled plant ID

The matching built-in IDs are intentional: Pixel Agents merges external assets
after built-ins and the later entry wins. Therefore the existing default layout
uses these replacements without editing its layout JSON.

All runtime canvases use exact 16 px tile multiples. Run the deterministic
build and metadata check from the repository root:

```bash
python3 scripts/build-pixel-agents-pack.py
python3 scripts/validate-pixel-agents-pack.py
```

`demo-layout.json` and `pixel-agents-room.html` are a no-character placement
proof for the current batch. They are not a claim that the entire reference
office has already been replaced.
