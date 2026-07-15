import { expect, test } from '@playwright/test';
const updateProofs = process.env.UPDATE_PROOFS === '1';
test('review desk exposes score and unresolved object directions', async ({ page }, testInfo) => {
  await page.goto('/review.html');
  await expect(page.locator('#score')).toHaveText(/^[0-5]\d\.\d\d%$/);
  await expect(page.locator('#ssim')).toHaveText(/^[0-5]\d\.\d\d%$/);
  await expect(page.locator('#status')).toHaveText('DIRECT MASKED SSIM < 60% · NOT VERIFIED');
  await expect(page.locator('.pane-canonical img')).toBeVisible();
  await expect(page.locator('#zoneRows tr')).toHaveCount(13);
  await page.screenshot({ path: updateProofs ? 'proof/similarity-review-desktop-v1.png' : testInfo.outputPath('review.png'), fullPage: true });
});
test('review desk remains image-first on mobile', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/review.html');
  await expect(page.locator('.pane-original img')).toBeVisible();
  await page.screenshot({ path: updateProofs ? 'proof/similarity-review-mobile-v1.png' : testInfo.outputPath('review-mobile.png'), fullPage: true });
});
