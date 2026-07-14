import { expect, test } from '@playwright/test';

const updateProofs = process.env.UPDATE_PROOFS === '1';
const artifactPath = (testInfo, name) => updateProofs ? `proof/${name}` : testInfo.outputPath(name);

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => {
    Date.now = () => 1770000000000;
    Math.random = () => 0.123456;
  });
});

test('captures the complete desktop interaction proof set', async ({ page }, testInfo) => {
  await page.goto('/builder.html');
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await expect(page.locator('#assetCount')).toHaveText('36 / 36 OBJECTS');

  const mug = page.locator('[data-asset-id="coffee-mug"]');
  await mug.click();
  await page.locator('#stage').hover({ position: { x: 620, y: 410 } });
  await page.screenshot({ path: artifactPath(testInfo, 'builder-placing-v4.png') });

  await page.locator('#stage').click({ position: { x: 620, y: 410 } });
  await expect(page.locator('#inspectorName')).toHaveText('coffee mug');
  await expect(page.locator('#inspectorEmpty')).toBeHidden();
  await page.screenshot({ path: artifactPath(testInfo, 'builder-inspector-v4.png') });

  const chair = page.locator('[data-uid="chair-a1"]');
  const stageBox = await page.locator('#stage').boundingBox();
  const chairBox = await chair.boundingBox();
  await page.mouse.move(chairBox.x + chairBox.width / 2, chairBox.y + chairBox.height / 2);
  await page.mouse.down();
  await page.mouse.move(stageBox.x + stageBox.width * 0.72, stageBox.y + stageBox.height * 0.72, { steps: 8 });
  await page.mouse.up();
  await expect(page.locator('#inspectorGrid')).not.toHaveText('14, 15');
  await page.screenshot({ path: artifactPath(testInfo, 'builder-dragged-v4.png') });

  await page.locator('#referenceToggle').click();
  await expect(page.locator('#stage')).toHaveClass(/is-reference/);
  await expect(page.locator('.stage__reference')).toHaveCSS('opacity', '0.42');
  await page.screenshot({ path: artifactPath(testInfo, 'builder-reference-v4.png') });

  await page.locator('#referenceToggle').click();
  await expect(page.locator('.stage__reference')).toHaveCSS('opacity', '0');
  await mug.focus();
  await page.keyboard.press('Shift+Tab');
  await page.keyboard.press('Tab');
  await expect(mug).toBeFocused();
  await expect(mug).toHaveCSS('outline-style', 'solid');
  await page.screenshot({ path: artifactPath(testInfo, 'builder-focus-v4.png') });

  const downloadPromise = page.waitForEvent('download');
  await page.locator('#exportButton').click();
  const download = await downloadPromise;
  await download.saveAs(artifactPath(testInfo, 'verdant-layout-export-v2.json'));
  await expect(page.locator('#builderHint')).toHaveText('レイアウトJSONを書き出しました。');
});

test('captures the 390px mobile catalog, stage, and inspector flow', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/builder.html');
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await expect(page.locator('#assetCount')).toHaveText('36 / 36 OBJECTS');
  await page.locator('[data-uid="sofa-a1"]').focus();
  await page.keyboard.press('Enter');
  await expect(page.locator('#inspectorPanel')).toBeVisible();
  await expect(page.locator('#inspectorEmpty')).toBeHidden();
  await page.screenshot({ path: artifactPath(testInfo, 'builder-mobile-full-v4.png'), fullPage: true });
});
