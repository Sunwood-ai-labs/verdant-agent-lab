# Original runtime architecture

## Goal

Build an original, sustainable-lab pixel workspace where rooms, furniture, and
desk props are visible, independently addressable objects. Characters are
optional and disabled by default.

## Inspiration boundary

Primary-source research on Pixel Agents confirmed useful abstract patterns:

- a normalized event boundary before scene projection
- domain state outside the UI component tree
- a frame loop with pixel-friendly rendering
- versioned layout JSON
- manifest-driven furniture
- derived collision, seat, and render-order data

The implementation must not copy Pixel Agents code, images, names, copy, default
layout, or product presentation. See `research/pixel-agents/notes/architecture-notes.md`.

## Proposed pipeline

```text
runtime adapter
  -> normalized lab event
  -> domain store
  -> layout projection
  -> object instances
  -> DOM/canvas renderer
  -> accessibility overlay
```

### Runtime adapter

Future agent providers should map their native lifecycle into project-owned
events such as:

- `session_started`
- `task_started`
- `reading`
- `writing`
- `running`
- `waiting`
- `failed`
- `completed`

These names are original to this project and may change before a provider is
implemented.

### Domain store

The store owns:

- active work sessions
- object inventory
- versioned layout
- current selections
- persisted viewport state
- derived occupancy map

The renderer does not own this state.

### Layout document

Only source-of-truth placement data is persisted:

```json
{
  "version": 1,
  "world": { "cols": 48, "rows": 36, "tileSize": 32 },
  "objects": [
    {
      "uid": "desk-a1",
      "assetId": "single-desk",
      "col": 12,
      "row": 8,
      "rotation": 0,
      "state": "default"
    }
  ]
}
```

Collision cells, seat instances, surface slots, and draw order are reconstructed
from manifests at load time.

## Asset manifests

Each catalog item uses an independent asset ID. Current fields include:

- `id`
- `category`
- `sprite`
- `footprint`
- `surfaceAnchors`
- `seatAnchors`
- `mount`
- `wallMount`
- `ceilingMount`
- `stateVariants`
- `zBias`

## Object composition

A workstation is a recipe, not one asset:

```text
single-desk
  + rolling-office-chair
  + single-monitor
  + keyboard-mouse
  + coffee-mug
  + succulent
```

This lets users move, recolor, hide, or replace each object independently.

## Render layers

Suggested ordering:

1. floor and room base
2. wall/architecture segments
3. ground furniture
4. desk and table bases
5. surface-mounted technology
6. desk props
7. hanging lights and UI highlights
8. accessibility and interaction overlay

Within a layer, use `row/y + zBias` so front objects naturally overlap rear
objects without coupling layout data to a particular renderer.

## Current-to-future migration

Current HTML uses a flattened clean scene for maximum visual fidelity while
the catalog is being built. The migration path is incremental:

1. add a catalog drawer that loads all manifests
2. render selected transparent sprites above the base scene
3. persist user placement in layout JSON/local storage
4. replace more flattened furniture with composited sprites
5. move the world to a dedicated canvas when editing and collision require it

This avoids discarding the verified photo recreation while the original game
runtime matures.
