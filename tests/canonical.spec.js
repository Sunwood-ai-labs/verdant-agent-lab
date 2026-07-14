import { expect, test } from '@playwright/test';

const updateProofs = process.env.UPDATE_PROOFS === '1';

test('captures the no-UI characterless canonical render', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 1280, height: 960 });
  await page.goto('/canonical.html');
  await expect(page.locator('.canonical img')).toBeVisible();
  await page.screenshot({ path: updateProofs ? 'proof/canonical-characterless-v1.png' : testInfo.outputPath('canonical-characterless-v1.png') });
  await expect(page.locator('.canonical')).toHaveScreenshot('canonical-characterless.png', { animations: 'disabled', maxDiffPixels: 0 });
});
