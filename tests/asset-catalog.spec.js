import { expect, test } from '@playwright/test';

const updateProofs = process.env.UPDATE_PROOFS === '1';

test('shows every runtime asset with an explicit provenance warning', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 1440, height: 1100 });
  await page.goto('/asset-catalog.html');
  await expect(page.locator('#total')).toHaveText('48');
  await expect(page.locator('.asset-card')).toHaveCount(48);
  await expect(page.getByText('GENERATED DERIVATIVES')).toBeVisible();
  await expect(page.getByText(/EDGE-CUT RISK/)).toHaveCount(25);
  await page.screenshot({ path: updateProofs ? 'proof/runtime-asset-catalog-v3.png' : testInfo.outputPath('runtime-asset-catalog.png'), fullPage: true });
});
