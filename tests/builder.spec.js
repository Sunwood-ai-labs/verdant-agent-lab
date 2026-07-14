import { expect, test } from '@playwright/test';

test.beforeEach(async ({ page }) => {
  await page.goto('/builder.html');
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await expect(page.locator('#assetCount')).toHaveText('42 / 42 OBJECTS');
});

test('loads every manifest and places an independent prop', async ({ page }) => {
  await expect(page.locator('#placementCount')).toHaveText('21 PLACED');

  await page.locator('[data-asset-id="coffee-mug"]').click();
  await page.locator('#stage').click({ position: { x: 600, y: 420 } });

  await expect(page.locator('#placementCount')).toHaveText('22 PLACED');
  await expect(page.locator('#inspectorName')).toHaveText('coffee mug');
  await expect(page.locator('#inspectorPanel')).toBeVisible();
  await expect(page.locator('#inspectorEmpty')).toBeHidden();

  await page.reload();
  await expect(page.locator('#placementCount')).toHaveText('22 PLACED');
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

  await expect(page.locator('#inspectorGrid')).not.toHaveText('14, 15');
  await expect(chair).toHaveClass(/is-selected/);
});

test('toggles the reference layer and deletes a selected object', async ({ page }) => {
  await page.locator('#referenceToggle').click();
  await expect(page.locator('#stage')).toHaveClass(/is-reference/);

  await page.locator('[data-uid="north-lounge-a1"]').focus();
  await page.keyboard.press('Enter');
  await expect(page.locator('#inspectorEmpty')).toBeHidden();
  await page.locator('#deleteButton').click();
  await expect(page.locator('#placementCount')).toHaveText('20 PLACED');
  await expect(page.locator('[data-uid="north-lounge-a1"]')).toHaveCount(0);
});

test('reports pressed state and supports keyboard placement and movement', async ({ page }) => {
  const plantFilter = page.locator('[data-category="plant"]');
  await plantFilter.click();
  await expect(plantFilter).toHaveAttribute('aria-pressed', 'true');
  await expect(plantFilter).toBeFocused();

  const succulent = page.locator('[data-asset-id="succulent"]');
  await succulent.click();
  await expect(succulent).toHaveAttribute('aria-pressed', 'true');
  await expect(succulent).toBeFocused();

  await page.locator('#stage').focus();
  await page.keyboard.press('Enter');
  await expect(page.locator('#placementCount')).toHaveText('22 PLACED');

  const chair = page.locator('[data-uid="chair-a1"]');
  await chair.focus();
  await page.keyboard.press('ArrowRight');
  await expect(page.locator('#inspectorGrid')).toHaveText('15, 15');
  await expect(chair).toHaveAttribute('aria-label', /列15、行15/);
});
