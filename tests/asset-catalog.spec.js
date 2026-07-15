import { expect, test } from '@playwright/test';

const updateProofs = process.env.UPDATE_PROOFS === '1';

test('shows the first page of runtime assets without a vertically clipped proof', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 1440, height: 1100 });
  await page.goto('/asset-catalog.html?page=1');
  await expect(page.locator('#total')).toHaveText('48');
  await expect(page.locator('.asset-card')).toHaveCount(24);
  await expect(page.locator('#pageLabel')).toHaveText('PAGE 1 / 2');
  await expect(page.getByText('NOT SOURCE-COMPLETE')).toBeVisible();
  await expect(page.getByText(/EDGE-CUT RISK/)).toHaveCount(14);
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.screenshot({ path: updateProofs ? 'proof/runtime-asset-catalog-page-1-v3.png' : testInfo.outputPath('runtime-asset-catalog-page-1.png'), fullPage: true });
});

test('shows the second page as a separate readable proof', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 1440, height: 1100 });
  await page.goto('/asset-catalog.html?page=2');
  await expect(page.locator('.asset-card')).toHaveCount(24);
  await expect(page.locator('#pageLabel')).toHaveText('PAGE 2 / 2');
  await expect(page.getByText(/EDGE-CUT RISK/)).toHaveCount(11);
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.screenshot({ path: updateProofs ? 'proof/runtime-asset-catalog-page-2-v3.png' : testInfo.outputPath('runtime-asset-catalog-page-2.png'), fullPage: true });
});
