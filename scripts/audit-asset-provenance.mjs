#!/usr/bin/env node
import fs from 'node:fs';

const read = (path) => JSON.parse(fs.readFileSync(path, 'utf8'));
const runtimeManifests = [
  'assets/manifests/furniture.v1.json',
  'assets/manifests/technology.v1.json',
  'assets/manifests/props.v1.json',
].map(read);
const crops = read('assets/manifests/source-crops.v1.json');

const runtimeItems = runtimeManifests.flatMap((manifest) => manifest.items);
const generatedRuntime = runtimeItems.filter((item) => item.sprite.includes('../generated/')).length;
const sourceCropRuntime = runtimeItems.filter((item) => item.sprite.includes('../object-crops/')).length;
const sourceCropFiles = crops.items.filter((item) => fs.existsSync(`assets/object-crops/${item.id}.png`)).length;

console.log(JSON.stringify({
  runtimeAssets: runtimeItems.length,
  runtimeGeneratedAssets: generatedRuntime,
  runtimeSourceCropAssets: sourceCropRuntime,
  registeredDerivativeCrops: crops.items.length,
  existingDerivativeCropFiles: sourceCropFiles,
  conclusion: sourceCropRuntime === 0
    ? 'Builder uses no source-derived crop assets; its runtime assets are generated.'
    : 'Builder mixes generated and source-derived crop assets.'
}, null, 2));
