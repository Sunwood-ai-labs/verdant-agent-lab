#!/usr/bin/env node
/** Capture a real Pixel Agents character walking through the Verdant office. */

import { createRequire } from 'node:module';
import { mkdirSync, readFileSync, rmSync } from 'node:fs';
import { join } from 'node:path';

const require = createRequire(import.meta.url);
const reference = process.env.PIXEL_AGENTS_REFERENCE ?? '/Users/admin/Prj/pixel-agents';
const { chromium } = require(join(reference, 'node_modules/playwright'));

const root = process.cwd();
const frameDir = join(root, 'build/pixel-agents-solarpunk-character-walk-frames-v1');
const url = process.env.PIXEL_AGENTS_URL ?? 'http://127.0.0.1:3101';
const serverConfig = JSON.parse(
  readFileSync(join(process.env.HOME ?? '/Users/admin', '.pixel-agents/server.json'), 'utf8'),
);
const remoteUrl = `${url}/api/remote/v1/hosts/verdant-demo/agents/walker`;
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
const page = await browser.newPage({ viewport: { width: 1000, height: 700 } });
await page.addInitScript(() => {
  window.__PIXEL_AGENTS_E2E = true;
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
  await hold(8); // capture the built-in spawn animation

  await page.evaluate((id) => window.__pixelAgentsTestHooks?.selectAgent?.(id), localAgentId);
  const canvas = page.locator('canvas').first();
  const box = await canvas.boundingBox();
  if (!box) throw new Error('Pixel Agents canvas is not visible');

  // These are open-floor waypoints in the checked Verdant 21x22 preset.
  // Right-click uses Pixel Agents' production walkToTile path, not a fake CSS move.
  const waypoints = [
    { x: box.x + box.width * 0.70, y: box.y + box.height * 0.72 },
    { x: box.x + box.width * 0.47, y: box.y + box.height * 0.63 },
    { x: box.x + box.width * 0.73, y: box.y + box.height * 0.48 },
  ];
  for (const point of waypoints) {
    await page.mouse.click(point.x, point.y, { button: 'right' });
    await hold(22);
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
      },
      null,
      2,
    ),
  );
} finally {
  await remoteRequest('DELETE');
  await browser.close();
}
