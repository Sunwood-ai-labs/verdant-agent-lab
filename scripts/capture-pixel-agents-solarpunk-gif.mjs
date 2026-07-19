#!/usr/bin/env node
/** Capture a real Pixel Agents character walking through the Verdant office. */

import { createRequire } from 'node:module';
import { mkdirSync, readFileSync, rmSync } from 'node:fs';
import { join } from 'node:path';

const require = createRequire(import.meta.url);
const reference = process.env.PIXEL_AGENTS_REFERENCE ?? '/Users/admin/Prj/pixel-agents';
const { chromium } = require(join(reference, 'node_modules/playwright'));

const root = process.cwd();
const variant = process.env.PIXEL_AGENTS_CAPTURE_VARIANT ?? 'default';
const isSpacious = variant === 'spacious';
if (!['default', 'spacious'].includes(variant)) throw new Error(`unsupported capture variant: ${variant}`);
const frameDir = join(
  root,
  isSpacious
    ? 'build/pixel-agents-solarpunk-spacious-character-walk-frames-v3'
    : 'build/pixel-agents-solarpunk-character-walk-frames-v3',
);
const url = process.env.PIXEL_AGENTS_URL ?? 'http://127.0.0.1:3101';
const serverConfig = JSON.parse(
  readFileSync(join(process.env.HOME ?? '/Users/admin', '.pixel-agents/server.json'), 'utf8'),
);
const remoteUrl = `${url}/api/remote/v1/hosts/${isSpacious ? 'verdant-spacious' : 'verdant-demo'}/agents/walker`;
const authorization = `Bearer ${serverConfig.remoteApiToken}`;

rmSync(frameDir, { recursive: true, force: true });
mkdirSync(frameDir, { recursive: true });

const remoteRequest = async (method, body) => {
  const response = await fetch(remoteUrl, {
    method,
    headers: {
      Authorization: authorization,
      ...(body ? { 'Content-Type': 'application/json' } : {}),
    },
    ...(body ? { body: JSON.stringify(body) } : {}),
  });
  if (!response.ok && response.status !== 404) {
    throw new Error(`remote agent ${method} failed: HTTP ${response.status}`);
  }
  return response.status === 204 || response.status === 404 ? null : response.json();
};

await remoteRequest('DELETE');

const browser = await chromium.launch({
  headless: true,
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
});
const page = await browser.newPage({
  viewport: isSpacious ? { width: 1200, height: 700 } : { width: 1000, height: 700 },
});
await page.addInitScript(() => {
  window.__PIXEL_AGENTS_E2E = true;
  // Keep proof runs reproducible and use built-in palette 0 (dark hair), so a
  // pale random skin cannot be confused with the selection outline under test.
  Math.random = () => 0.01;
});
const errors = [];
page.on('console', (message) => {
  if (message.type() === 'error') errors.push(message.text());
});

let frame = 0;
const screenshot = async () => {
  await page.screenshot({ path: join(frameDir, `${String(frame).padStart(4, '0')}.png`) });
  frame += 1;
};
const hold = async (count, delayMs = 100) => {
  for (let i = 0; i < count; i += 1) {
    await screenshot();
    await page.waitForTimeout(delayMs);
  }
};

let localAgentId = null;
try {
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(700);

  // Activity overlays are useful in normal operation but obscure the small
  // walking sprite in a proof GIF. Hide only that DOM layer in this capture.
  await page.addStyleTag({
    content: '[data-testid="agent-overlay"] { display: none !important; }',
  });
  if (isSpacious) {
    const stillDir = join(root, 'proofs/pixel-agents-solarpunk-spacious');
    mkdirSync(stillDir, { recursive: true });
    await page.screenshot({ path: join(stillDir, 'spacious-office-v3.png') });
  }
  await hold(5);

  const created = await remoteRequest('PUT', {
    displayName: 'Verdant Walker',
    task: 'Office walkthrough',
    status: 'active',
    activity: 'Walking through the solarpunk office',
    heartbeatTtlSeconds: 120,
  });
  localAgentId = created.localAgentId;
  await page.waitForFunction(
    (id) => window.__pixelAgentsTestHooks?.getCharacters?.().some((ch) => ch.id === id),
    localAgentId,
  );
  // agentCreated auto-selects the new character in normal UI. Clear that
  // selection before the spawn hold as well as after every walk command.
  await page.evaluate(() => window.__pixelAgentsTestHooks?.selectAgent?.(null));
  await page.mouse.move(4, 696);
  await hold(8); // capture the built-in spawn animation

  const canvas = page.locator('canvas').first();
  const box = await canvas.boundingBox();
  if (!box) throw new Error('Pixel Agents canvas is not visible');

  // These are open-floor waypoints in the checked Verdant 21x22 preset.
  // Right-click uses Pixel Agents' production walkToTile path, not a fake CSS move.
  const waypoints = isSpacious
    ? [
        { x: box.x + box.width * 0.30, y: box.y + box.height * 0.62 },
        { x: box.x + box.width * 0.50, y: box.y + box.height * 0.69 },
        { x: box.x + box.width * 0.72, y: box.y + box.height * 0.58 },
      ]
    : [
        { x: box.x + box.width * 0.70, y: box.y + box.height * 0.72 },
        { x: box.x + box.width * 0.47, y: box.y + box.height * 0.63 },
        { x: box.x + box.width * 0.73, y: box.y + box.height * 0.48 },
      ];
  const waypointHoldFrames = isSpacious ? 36 : 22;
  for (const point of waypoints) {
    await page.evaluate((id) => window.__pixelAgentsTestHooks?.selectAgent?.(id), localAgentId);
    await page.mouse.click(point.x, point.y, { button: 'right' });
    // Selection is needed only to issue walkToTile. Clear it immediately so
    // Pixel Agents' intentional white selected-character outline is never
    // baked into the animation proof.
    await page.evaluate(() => window.__pixelAgentsTestHooks?.selectAgent?.(null));
    await page.mouse.move(box.x + 4, box.y + box.height - 4);
    await hold(waypointHoldFrames);
  }

  if (errors.length) throw new Error(`browser errors: ${JSON.stringify(errors)}`);
  console.log(
    JSON.stringify(
      {
        status: 'passed',
        frameDir,
        frames: frame,
        localAgentId,
        browserErrors: errors.length,
        capture: 'real Pixel Agents built-in character spawn and walkToTile movement',
        variant,
      },
      null,
      2,
    ),
  );
} finally {
  await remoteRequest('DELETE');
  await browser.close();
}
