#!/usr/bin/env -S tsx
/** Validate the custom Verdant room with Pixel Agents' real catalog semantics. */

import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

const root = process.cwd();
const reference = process.env.PIXEL_AGENTS_REFERENCE ?? '/Users/admin/Prj/pixel-agents';
const source = (relative: string) => pathToFileURL(join(reference, 'webview-ui/src', relative)).href;
const catalogModule = await import(source('office/layout/furnitureCatalog.ts'));
const { OfficeState } = await import(source('office/engine/officeState.ts'));

type Json = Record<string, any>;
type Context = {
  name: string;
  category: string;
  groupId?: string;
  orientation?: string;
  state?: string;
  rotationScheme?: string;
  canPlaceOnSurfaces?: boolean;
  canPlaceOnWalls?: boolean;
  backgroundTiles?: number;
};

const loadedCatalog: Json[] = [];
const sprites: Record<string, string[][]> = {};

function visit(node: Json, context: Context): void {
  const next = { ...context };
  for (const key of ['orientation', 'state', 'rotationScheme', 'canPlaceOnSurfaces', 'canPlaceOnWalls', 'backgroundTiles'] as const) {
    if (node[key] !== undefined) (next as Json)[key] = node[key];
  }
  if (node.type === 'group' && node.groupType === 'rotation') next.groupId = node.id;
  if (node.type === 'asset') {
    sprites[node.id] = Array.from({ length: node.height }, () => Array(node.width).fill(''));
    loadedCatalog.push({
      id: node.id,
      label: next.name,
      category: next.category,
      width: node.width,
      height: node.height,
      footprintW: node.footprintW,
      footprintH: node.footprintH,
      isDesk: next.category === 'desks',
      ...(next.groupId ? { groupId: next.groupId } : {}),
      ...(next.orientation ? { orientation: next.orientation } : {}),
      ...(next.state ? { state: next.state } : {}),
      ...(next.rotationScheme ? { rotationScheme: next.rotationScheme } : {}),
      ...(node.mirrorSide ? { mirrorSide: true } : {}),
      ...(next.canPlaceOnSurfaces ? { canPlaceOnSurfaces: true } : {}),
      ...(next.canPlaceOnWalls ? { canPlaceOnWalls: true } : {}),
      ...(next.backgroundTiles ? { backgroundTiles: next.backgroundTiles } : {}),
    });
    return;
  }
  for (const member of node.members ?? []) visit(member, next);
}

const manifestRoot = join(root, 'pixel-agents-pack/assets/furniture');
for (const folder of readdirSync(manifestRoot).sort()) {
  const path = join(manifestRoot, folder, 'manifest.json');
  let manifest: Json;
  try { manifest = JSON.parse(readFileSync(path, 'utf8')); } catch { continue; }
  visit(manifest, {
    name: manifest.name,
    category: manifest.category,
    canPlaceOnSurfaces: manifest.canPlaceOnSurfaces,
    canPlaceOnWalls: manifest.canPlaceOnWalls,
    backgroundTiles: manifest.backgroundTiles,
    rotationScheme: manifest.rotationScheme,
  });
}
assert.equal(catalogModule.buildDynamicCatalog({ catalog: loadedCatalog, sprites }), true);

const layout = JSON.parse(readFileSync(join(root, 'pixel-agents-pack/verdant-runtime-layout.json'), 'utf8'));
const required = new Set([
  'AI_DIAGNOSTIC_PLATFORM', 'MEETING_GLASS_MODULE', 'LOUNGE_SECTIONAL',
  'LOUNGE_OVAL_TABLE', 'FLOWER_PLANTER_LONG', 'RECYCLING_BIN',
]);
const present = new Set<string>(layout.furniture.map((item: Json) => item.type));
assert.deepEqual([...required].filter((type) => !present.has(type)), []);

const unresolved = layout.furniture.filter((item: Json) => !catalogModule.getCatalogEntry(item.type));
assert.deepEqual(unresolved, []);

const collisionOwners = new Map<string, string>();
const collisions: Array<{ tile: string; first: string; second: string }> = [];
for (const item of layout.furniture) {
  const entry = catalogModule.getCatalogEntry(item.type)!;
  // Surface props intentionally share host tiles with counters/desks and do
  // not represent independent floor obstacles for overlap QA.
  if (entry.canPlaceOnSurfaces) continue;
  const bgRows = entry.backgroundTiles ?? 0;
  for (let dr = bgRows; dr < entry.footprintH; dr++) {
    for (let dc = 0; dc < entry.footprintW; dc++) {
      const tile = `${item.col + dc},${item.row + dr}`;
      const owner = collisionOwners.get(tile);
      if (owner) collisions.push({ tile, first: owner, second: item.uid });
      else collisionOwners.set(tile, item.uid);
    }
  }
}
assert.deepEqual(collisions, []);

const state = new OfficeState(layout);
const walkable = new Set(state.walkableTiles.map((tile: Json) => `${tile.col},${tile.row}`));
const remaining = new Set(walkable);
const componentSizes: number[] = [];
while (remaining.size) {
  const seed = remaining.values().next().value as string;
  const queue = [seed];
  let size = 0;
  remaining.delete(seed);
  while (queue.length) {
    const key = queue.shift()!;
    size++;
    const [col, row] = key.split(',').map(Number);
    for (const [dc, dr] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
      const next = `${col + dc},${row + dr}`;
      if (remaining.has(next)) {
        remaining.delete(next);
        queue.push(next);
      }
    }
  }
  componentSizes.push(size);
}
componentSizes.sort((a, b) => b - a);
const largestWalkableComponent = componentSizes[0] ?? 0;
assert.ok(largestWalkableComponent / state.walkableTiles.length >= 0.95);

console.log(JSON.stringify({
  status: 'passed',
  grid: `${layout.cols}x${layout.rows}`,
  layoutRevision: layout.layoutRevision,
  placements: layout.furniture.length,
  requiredBatchAssets: required.size,
  unresolvedTypes: unresolved.length,
  overlappingCollisionTiles: collisions.length,
  walkableTiles: state.walkableTiles.length,
  walkableComponents: componentSizes,
  largestWalkableComponent,
}, null, 2));
