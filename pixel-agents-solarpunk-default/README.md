# Verdant Solarpunk Default Office preset

This preset keeps Pixel Agents' default office at exactly 21×22 tiles with the
same 36 furniture placements. It changes the visible furniture through exact-ID
16px-grid assets, applies nine solarpunk floor tiles, and uses one connected
living-wall atlas with sixteen N/E/S/W masks.

Build the versioned preset:

```bash
npm run build:pixel-agents-solarpunk-default
```

Assemble a separate runnable development overlay without modifying the Pixel
Agents reference checkout:

```bash
npm run assemble:pixel-agents-solarpunk-runtime
```

The runnable directory and deterministic zip are written to ignored `build/`.
They require the reference checkout's installed Node dependencies. Pixel Agents
1.3 does not currently merge external floor/wall packs, so the furniture-only
pack remains installable through Settings while the complete theme uses this
separate overlay route.

`layout.json` is generated from the audited default layout. Only
`layoutRevision` and `tileColors` change; grid, tile IDs, and furniture records
remain unchanged.
