import { expect, test } from '@playwright/test';

test('renders the current asset room without a reference overlay', async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 960 });
  await page.goto('/room.html?clean=1');
  await expect(page.locator('.room-layer')).toHaveCount(13);
  await expect(page.locator('.room-layer[data-layer-id="studio-west"]')).toBeVisible();
  await expect(page.locator('img[src*="reference-original"]')).toHaveCount(0);
  await expect(page.locator('img[src*="scene-clean"]')).toHaveCount(0);
  await expect(page.locator('#foundation')).toHaveAttribute('src', /office-architecture-empty-imagegen-v2\.png$/);
});
