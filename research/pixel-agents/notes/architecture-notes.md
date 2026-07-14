# Pixel Agents primary-source notes

Checked: 2026-07-14 JST

Primary source: <https://github.com/pixel-agents-hq/pixel-agents>

Concepts adopted for an original implementation:

- normalize runtime events before projecting them into scene state
- keep domain state separate from render state
- store a versioned layout containing tile and object placement data
- keep furniture assets manifest-driven and independently addressable
- derive collision, seat, surface, and render ordering data at load time
- use integer-friendly pixel scaling and explicit depth ordering

Originality boundary:

- do not copy Pixel Agents assets, characters, layout, product name, UI copy, screenshots, or source code
- create independent visual assets and a different sustainable-lab world
- decompose desk bases, chairs, monitors, keyboards, mugs, lamps, notebooks, pots, and leaves into independent object IDs

Official references:

- README and architecture: <https://github.com/pixel-agents-hq/pixel-agents#readme>
- external asset format: <https://github.com/pixel-agents-hq/pixel-agents/blob/main/docs/external-assets.md>
- license: <https://github.com/pixel-agents-hq/pixel-agents/blob/main/LICENSE>
