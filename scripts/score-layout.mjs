#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const readJson = (relative) => JSON.parse(fs.readFileSync(path.join(root, relative), 'utf8'));
const anchors = readJson('assets/layouts/reference-anchors.v1.json');
const layout = readJson(process.argv[2] || 'assets/layouts/starter.v1.json');
const manifests = [
  readJson('assets/manifests/furniture.v1.json'),
  readJson('assets/manifests/technology.v1.json'),
  readJson('assets/manifests/props.v1.json')
];
const assets = new Map(manifests.flatMap((manifest) => manifest.items).map((item) => [item.id, item]));

const footprintBox = (object, asset) => {
  const width = asset.footprint.w;
  const height = asset.footprint.h;
  return [object.col - width / 2, object.row - height / 2, object.col + width / 2, object.row + height / 2];
};
const iou = (a, b) => {
  const intersection = Math.max(0, Math.min(a[2], b[2]) - Math.max(a[0], b[0]))
    * Math.max(0, Math.min(a[3], b[3]) - Math.max(a[1], b[1]));
  const areaA = (a[2] - a[0]) * (a[3] - a[1]);
  const areaB = (b[2] - b[0]) * (b[3] - b[1]);
  return intersection / Math.max(1, areaA + areaB - intersection);
};

const results = anchors.anchors.map((anchor) => {
  const exact = layout.objects.filter((object) => object.assetId === anchor.assetId);
  const candidates = exact.length ? exact : layout.objects.filter((object) => assets.get(object.assetId)?.category === anchor.category);
  const ranked = candidates.map((object) => {
    const asset = assets.get(object.assetId);
    const category = object.assetId === anchor.assetId ? 1 : asset?.category === anchor.category ? 0.75 : 0;
    const dc = object.col - anchor.col;
    const dr = object.row - anchor.row;
    const position = Math.exp(-0.5 * ((dc / 2) ** 2 + (dr / 2) ** 2));
    const occupancy = iou(footprintBox(object, asset), anchor.bbox);
    const score = 100 * (
      anchors.weights.category * category
      + anchors.weights.position * position
      + anchors.weights.occupancy * occupancy
    );
    return { object, score, delta: Math.hypot(dc, dr), category, position, occupancy };
  }).sort((a, b) => b.score - a.score);
  return { anchor, match: ranked[0] ?? null };
});

const overall = results.reduce((sum, result) => sum + (result.match?.score ?? 0), 0) / results.length;
for (const { anchor, match } of results) {
  const score = match?.score ?? 0;
  console.log(`${score >= anchors.acceptance.anchorMinimum ? 'PASS' : 'FAIL'} ${anchor.id.padEnd(17)} ${score.toFixed(1)} ${match?.object.uid ?? 'unmatched'}`);
}
console.log(`OVERALL ${overall.toFixed(1)} / minimum ${anchors.acceptance.overallMinimum}`);

if (overall < anchors.acceptance.overallMinimum || results.some(({ match }) => !match || match.score < anchors.acceptance.anchorMinimum || match.delta > anchors.acceptance.maxCenterDelta)) {
  process.exitCode = 1;
}
