import { expect, test } from '@playwright/test';

test.beforeEach(async ({ page }) => {
  await page.goto('/builder.html');
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await expect(page.locator('#assetCount')).toHaveText('36 OBJECTS');
});

test('loads every manifest and places an independent prop', async ({ page }) => {
  await expect(page.locator('#placementCount')).toHaveText('8 PLACED');

  await page.locator('[data-asset-id="coffee-mug"]').click();
  await page.locator('#stage').click({ position: { x: 600, y: 420 } });

  await expect(page.locator('#placementCount')).toHaveText('9 PLACED');
  await expect(page.locator('#inspectorName')).toHaveText('coffee mug');
  await expect(page.locator('#inspectorPanel')).toBeVisible();

  await page.reload();
  await expect(page.locator('#placementCount')).toHaveText('9 PLACED');
});

test('drags a placed chair to a new grid cell', async ({ page }) => {
  const chair = page.locator('[data-uid="chair-a1"]');
  const stage = page.locator('#stage');
  const chairBox = await chair.boundingBox();
  const stageBox = await stage.boundingBox();

  await page.mouse.move(chairBox.x + chairBox.width / 2, chairBox.y + chairBox.height / 2);
  await page.mouse.down();
  await page.mouse.move(stageBox.x + stageBox.width * 0.72, stageBox.y + stageBox.height * 0.72, { steps: 8 });
  await page.mouse.up();

  await expect(page.locator('#inspectorGrid')).not.toHaveText('11, 14');
  await expect(chair).toHaveClass(/is-selected/);
});

test('toggles the reference layer and deletes a selected object', async ({ page }) => {
  await page.locator('#referenceToggle').click();
  await expect(page.locator('#stage')).toHaveClass(/is-reference/);

  await page.locator('[data-uid="sofa-a1"]').click();
  await page.locator('#deleteButton').click();
  await expect(page.locator('#placementCount')).toHaveText('7 PLACED');
  await expect(page.locator('[data-uid="sofa-a1"]')).toHaveCount(0);
});
