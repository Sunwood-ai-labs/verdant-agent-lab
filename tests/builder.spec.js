import { expect, test } from '@playwright/test';

test.beforeEach(async ({ page }) => {
  await page.goto('/builder.html');
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await expect(page.locator('#assetCount')).toHaveText('48 / 48 OBJECTS');
});

const starterCount = async (page) => page.evaluate(async () => {
  const layout = await fetch('/assets/layouts/starter.v1.json').then((response) => response.json());
  return layout.objects.length;
});

test('loads every manifest and places an independent prop', async ({ page }) => {
  const initialCount = await starterCount(page);
  await expect(page.locator('#placementCount')).toHaveText(`${initialCount} PLACED`);

  await page.locator('[data-asset-id="coffee-mug"]').click();
  await page.locator('#stage').click({ position: { x: 600, y: 420 } });

  await expect(page.locator('#placementCount')).toHaveText(`${initialCount + 1} PLACED`);
  await expect(page.locator('#inspectorName')).toHaveText('coffee mug');
  await expect(page.locator('#inspectorPanel')).toBeVisible();
  await expect(page.locator('#inspectorEmpty')).toBeHidden();

  await page.reload();
  await expect(page.locator('#placementCount')).toHaveText(`${initialCount + 1} PLACED`);
});

test('drags a placed directional sprite to a new grid cell', async ({ page }) => {
  const chair = page.locator('[data-uid="studio-west-a1"]');
  const stage = page.locator('#stage');
  const chairBox = await chair.boundingBox();
  const stageBox = await stage.boundingBox();

  await page.mouse.move(chairBox.x + chairBox.width / 2, chairBox.y + chairBox.height / 2);
  await page.mouse.down();
  await page.mouse.move(stageBox.x + stageBox.width * 0.72, stageBox.y + stageBox.height * 0.72, { steps: 8 });
  await page.mouse.up();

  await expect(page.locator('#inspectorGrid')).not.toHaveText('12, 12');
  await expect(chair).toHaveClass(/is-selected/);
});

test('toggles the reference layer and deletes a selected object', async ({ page }) => {
  const initialCount = await starterCount(page);
  await page.locator('#referenceToggle').click();
  await expect(page.locator('#stage')).toHaveClass(/is-reference/);

  await page.locator('[data-uid="north-lounge-a1"]').focus();
  await page.keyboard.press('Enter');
  await expect(page.locator('#inspectorEmpty')).toBeHidden();
  await page.locator('#deleteButton').click();
  await expect(page.locator('#placementCount')).toHaveText(`${initialCount - 1} PLACED`);
  await expect(page.locator('[data-uid="north-lounge-a1"]')).toHaveCount(0);
});

test('reports pressed state and supports keyboard placement and movement', async ({ page }) => {
  const initialCount = await starterCount(page);
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
  await expect(page.locator('#placementCount')).toHaveText(`${initialCount + 1} PLACED`);

  const chair = page.locator('[data-uid="studio-west-a1"]');
  await chair.focus();
  await page.keyboard.press('ArrowRight');
  await expect(page.locator('#inspectorGrid')).toHaveText('12.875, 11.875');
  await expect(chair).toHaveAttribute('aria-label', /列12.875、行11.875/);
});
