#!/usr/bin/env -S tsx
/** Verify Verdant assets with Pixel Agents' real seat, path, and depth logic. */

import assert from 'node:assert/strict';
import { mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

const root = process.cwd();
const reference = process.env.PIXEL_AGENTS_REFERENCE ?? '/Users/admin/Prj/pixel-agents';
const source = (relative: string) =>
  pathToFileURL(join(reference, 'webview-ui/src', relative)).href;

const catalogModule = await import(source('office/layout/furnitureCatalog.ts'));
const serializer = await import(source('office/layout/layoutSerializer.ts'));
const tileMapModule = await import(source('office/layout/tileMap.ts'));
const { OfficeState } = await import(source('office/engine/officeState.ts'));
const { CharacterState, Direction, TILE_SIZE, TileType } = await import(
  source('office/types.ts')
);
const { CHARACTER_Z_SORT_OFFSET } = await import(source('constants.ts'));

type Json = Record<string, any>;
type Context = {
  name: string;
  category: string;
  groupId?: string;
  orientation?: string;
  state?: string;
  rotationScheme?: string;
  animationGroup?: string;
  canPlaceOnSurfaces?: boolean;
  canPlaceOnWalls?: boolean;
  backgroundTiles?: number;
};

const manifestRoot = join(root, 'pixel-agents-pack/assets/furniture');
const loadedCatalog: Json[] = [];
const sprites: Record<string, string[][]> = {};

function visit(node: Json, context: Context): void {
  const next: Context = { ...context };
  if (node.orientation) next.orientation = node.orientation;
  if (node.state) next.state = node.state;
  if (node.rotationScheme) next.rotationScheme = node.rotationScheme;
  if (node.canPlaceOnSurfaces !== undefined)
    next.canPlaceOnSurfaces = node.canPlaceOnSurfaces;
  if (node.canPlaceOnWalls !== undefined) next.canPlaceOnWalls = node.canPlaceOnWalls;
  if (node.backgroundTiles !== undefined) next.backgroundTiles = node.backgroundTiles;
  if (node.type === 'group' && node.groupType === 'rotation') next.groupId = node.id;
  if (node.type === 'group' && node.groupType === 'animation') {
    next.animationGroup = `${next.groupId ?? context.name}:${next.orientation ?? 'none'}:${next.state ?? 'none'}`;
  }

  if (node.type === 'asset') {
    const width = node.width;
    const height = node.height;
    sprites[node.id] = Array.from({ length: height }, () => Array(width).fill(''));
    loadedCatalog.push({
      id: node.id,
      label: next.name,
      category: next.category,
      width,
      height,
      footprintW: node.footprintW,
      footprintH: node.footprintH,
      isDesk: next.category === 'desks',
      ...(next.groupId ? { groupId: next.groupId } : {}),
      ...(next.orientation ? { orientation: next.orientation } : {}),
      ...(next.state ? { state: next.state } : {}),
      ...(next.rotationScheme ? { rotationScheme: next.rotationScheme } : {}),
      ...(next.animationGroup ? { animationGroup: next.animationGroup } : {}),
      ...(node.frame !== undefined ? { frame: node.frame } : {}),
      ...(node.mirrorSide ? { mirrorSide: true } : {}),
      ...(next.canPlaceOnSurfaces ? { canPlaceOnSurfaces: true } : {}),
      ...(next.canPlaceOnWalls ? { canPlaceOnWalls: true } : {}),
      ...(next.backgroundTiles ? { backgroundTiles: next.backgroundTiles } : {}),
    });
    return;
  }
  for (const member of node.members ?? []) visit(member, next);
}

for (const folder of readdirSync(manifestRoot).sort()) {
  const path = join(manifestRoot, folder, 'manifest.json');
  let manifest: Json;
  try {
    manifest = JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    continue;
  }
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

const layout = JSON.parse(
  readFileSync(join(root, 'pixel-agents-pack/solarpunk-default-layout.json'), 'utf8'),
);
const usedTypes = new Set<string>(layout.furniture.map((item: Json) => item.type));
const unresolved = [...usedTypes].filter((type) => !catalogModule.getCatalogEntry(type));
assert.deepEqual(unresolved, []);

const seats = serializer.layoutToSeats(layout.furniture);
const seatTiles = serializer.getSeatTiles(seats);
const blockedTiles = serializer.getBlockedTiles(layout.furniture);
const chairPlacements = layout.furniture.filter(
  (item: Json) => catalogModule.getCatalogEntry(item.type)?.category === 'chairs',
);
const expectedSeatCount = chairPlacements.reduce((total: number, item: Json) => {
  const entry = catalogModule.getCatalogEntry(item.type)!;
  return total + entry.footprintW * (entry.footprintH - (entry.backgroundTiles ?? 0));
}, 0);
assert.equal(seats.size, expectedSeatCount);
assert.equal(seatTiles.size, seats.size);
assert.equal([...seatTiles].every((tile) => blockedTiles.has(tile)), true);

const state = new OfficeState(layout);
const [preferredSeatId, preferredSeat] = [...state.seats.entries()][0];
assert.ok(preferredSeatId && preferredSeat);
state.addAgent(9001, 0, 0, preferredSeatId, true, 'verdant-runtime-proof');
const agent = state.characters.get(9001)!;
assert.equal(agent.seatId, preferredSeatId);
assert.equal(agent.tileCol, preferredSeat.seatCol);
assert.equal(agent.tileRow, preferredSeat.seatRow);
assert.equal(agent.dir, preferredSeat.facingDir);
assert.equal(agent.state, CharacterState.TYPE);
assert.equal(state.seats.get(preferredSeatId)!.assigned, true);

const firstDesk = layout.furniture.find(
  (item: Json) => catalogModule.getCatalogEntry(item.type)?.isDesk,
)!;
const deskEntry = catalogModule.getCatalogEntry(firstDesk.type)!;
const blockedDeskTile = {
  col: firstDesk.col,
  row: firstDesk.row + (deskEntry.backgroundTiles ?? 0),
};
assert.equal(state.blockedTiles.has(`${blockedDeskTile.col},${blockedDeskTile.row}`), true);
assert.equal(state.walkToTile(9001, blockedDeskTile.col, blockedDeskTile.row), false);
// Active agents intentionally return to their workstation; mark this proof agent
// inactive so an explicit walk command can complete before testing seat return.
state.setAgentActive(9001, false);

let walkTarget: { col: number; row: number } | null = null;
for (const candidate of state.walkableTiles) {
  if (candidate.col === agent.tileCol && candidate.row === agent.tileRow) continue;
  if (state.walkToTile(9001, candidate.col, candidate.row)) {
    walkTarget = candidate;
    break;
  }
}
assert.ok(walkTarget);
const commandedPath = [...agent.path];
assert.ok(commandedPath.length > 0);
assert.equal(
  commandedPath.every((tile) => !state.blockedTiles.has(`${tile.col},${tile.row}`)),
  true,
);
for (let i = 0; i < 3000 && agent.path.length > 0; i++) state.update(0.02);
assert.equal(agent.tileCol, walkTarget.col);
assert.equal(agent.tileRow, walkTarget.row);
state.sendToSeat(9001);
for (let i = 0; i < 3000 && agent.state !== CharacterState.TYPE; i++) state.update(0.02);
assert.equal(agent.tileCol, preferredSeat.seatCol);
assert.equal(agent.tileRow, preferredSeat.seatRow);
assert.equal(agent.dir, preferredSeat.facingDir);
assert.equal(agent.state, CharacterState.TYPE);

const synthetic = {
  version: 1,
  cols: 12,
  rows: 10,
  tiles: new Array(120).fill(TileType.FLOOR_1),
  tileColors: new Array(120).fill(null),
  layoutRevision: 1,
  furniture: [
    { uid: 'front', type: 'WOODEN_CHAIR_FRONT', col: 2, row: 2 },
    { uid: 'back', type: 'WOODEN_CHAIR_BACK', col: 4, row: 2 },
    { uid: 'right', type: 'WOODEN_CHAIR_SIDE', col: 6, row: 2 },
    { uid: 'left', type: 'WOODEN_CHAIR_SIDE:left', col: 8, row: 2 },
  ],
};
const syntheticSeats = serializer.layoutToSeats(synthetic.furniture);
assert.equal(syntheticSeats.get('front')!.facingDir, Direction.DOWN);
assert.equal(syntheticSeats.get('back')!.facingDir, Direction.UP);
assert.equal(syntheticSeats.get('right')!.facingDir, Direction.RIGHT);
assert.equal(syntheticSeats.get('left')!.facingDir, Direction.LEFT);
assert.equal(catalogModule.getRotatedType('WOODEN_CHAIR_FRONT', 'cw'), 'WOODEN_CHAIR_SIDE');
assert.equal(catalogModule.getRotatedType('WOODEN_CHAIR_SIDE', 'cw'), 'WOODEN_CHAIR_BACK');
assert.equal(catalogModule.getRotatedType('WOODEN_CHAIR_BACK', 'cw'), 'WOODEN_CHAIR_SIDE:left');
assert.equal(catalogModule.getRotatedType('WOODEN_CHAIR_SIDE:left', 'cw'), 'WOODEN_CHAIR_FRONT');

const instances = serializer.layoutToFurnitureInstances(synthetic.furniture);
const frontZY = instances[0].zY;
const backZY = instances[1].zY;
const rightZY = instances[2].zY;
const leftMirrored = instances[3].mirrored === true;
const seatedCharacterZY = syntheticSeats.get('front')!.seatRow * TILE_SIZE + TILE_SIZE + CHARACTER_Z_SORT_OFFSET;
assert.ok(frontZY < seatedCharacterZY);
assert.ok(rightZY < seatedCharacterZY);
assert.ok(backZY > seatedCharacterZY);
assert.equal(leftMirrored, true);

const proof = {
  status: 'passed',
  pixelAgentsReference: reference,
  pack: 'pixel-agents-pack',
  realModules: [
    'furnitureCatalog.buildDynamicCatalog',
    'layoutSerializer.layoutToSeats',
    'layoutSerializer.getBlockedTiles',
    'layoutSerializer.layoutToFurnitureInstances',
    'OfficeState.addAgent',
    'OfficeState.walkToTile',
    'OfficeState.sendToSeat',
  ],
  defaultLayout: {
    grid: `${layout.cols}x${layout.rows}`,
    placements: layout.furniture.length,
    usedTypes: usedTypes.size,
    unresolvedTypes: unresolved,
    chairPlacements: chairPlacements.length,
    generatedSeats: seats.size,
    expectedSeats: expectedSeatCount,
    allSeatTilesCollisionProtected: [...seatTiles].every((tile) => blockedTiles.has(tile)),
  },
  liveState: {
    preferredSeatId,
    assignedAtSpawn: true,
    spawnFacing: preferredSeat.facingDir,
    rejectedBlockedDeskCommand: true,
    successfulWalkPathLength: commandedPath.length,
    walkPathAvoidedBlockedTiles: true,
    returnedToAssignedSeat: true,
    returnedFacingMatchesSeat: true,
  },
  chairRotation: {
    cycle: [
      'WOODEN_CHAIR_FRONT',
      'WOODEN_CHAIR_SIDE',
      'WOODEN_CHAIR_BACK',
      'WOODEN_CHAIR_SIDE:left',
      'WOODEN_CHAIR_FRONT',
    ],
    facings: { front: 'DOWN', back: 'UP', right: 'RIGHT', left: 'LEFT' },
    leftUsesRuntimeMirror: leftMirrored,
  },
  depth: {
    seatedCharacterZY,
    frontChairZY: frontZY,
    rightChairZY: rightZY,
    backChairZY: backZY,
    frontAndSideRenderBehindCharacter: frontZY < seatedCharacterZY && rightZY < seatedCharacterZY,
    backRendersInFrontOfCharacter: backZY > seatedCharacterZY,
  },
};

const output = join(root, 'proofs/pixel-agents-runtime-interactions/runtime-interaction-proof.json');
mkdirSync(join(root, 'proofs/pixel-agents-runtime-interactions'), { recursive: true });
writeFileSync(output, `${JSON.stringify(proof, null, 2)}\n`);
console.log(
  `PASS: ${seats.size} seats; agent walked ${commandedPath.length} tiles and returned; ` +
    '4-way chair rotation/facing/depth verified',
);
