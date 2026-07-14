import { expect, test } from '@playwright/test';

test('captures the complete desktop interaction proof set', async ({ page }) => {
  await page.goto('/builder.html');
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await expect(page.locator('#assetCount')).toHaveText('36 / 36 OBJECTS');

  const mug = page.locator('[data-asset-id="coffee-mug"]');
  await mug.click();
  await page.locator('#stage').hover({ position: { x: 620, y: 410 } });
  await page.screenshot({ path: 'proof/builder-placing-v3.png' });

  await page.locator('#stage').click({ position: { x: 620, y: 410 } });
  await expect(page.locator('#inspectorName')).toHaveText('coffee mug');
  await page.screenshot({ path: 'proof/builder-inspector-v3.png' });

  const chair = page.locator('[data-uid="chair-a1"]');
  const stageBox = await page.locator('#stage').boundingBox();
  const chairBox = await chair.boundingBox();
  await page.mouse.move(chairBox.x + chairBox.width / 2, chairBox.y + chairBox.height / 2);
  await page.mouse.down();
  await page.mouse.move(stageBox.x + stageBox.width * 0.72, stageBox.y + stageBox.height * 0.72, { steps: 8 });
  await page.mouse.up();
  await expect(page.locator('#inspectorGrid')).not.toHaveText('11, 14');
  await page.screenshot({ path: 'proof/builder-dragged-v3.png' });

  await page.locator('#referenceToggle').click();
  await expect(page.locator('#stage')).toHaveClass(/is-reference/);
  await page.screenshot({ path: 'proof/builder-reference-v3.png' });

  await mug.focus();
  await page.screenshot({ path: 'proof/builder-focus-v3.png' });

  const downloadPromise = page.waitForEvent('download');
  await page.locator('#exportButton').click();
  const download = await downloadPromise;
  await download.saveAs('proof/verdant-layout-export-v1.json');
  await expect(page.locator('#builderHint')).toHaveText('レイアウトJSONを書き出しました。');
});

test('captures the 390px mobile catalog, stage, and inspector flow', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/builder.html');
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await expect(page.locator('#assetCount')).toHaveText('36 / 36 OBJECTS');
  await page.locator('[data-uid="sofa-a1"]').click();
  await expect(page.locator('#inspectorPanel')).toBeVisible();
  await page.screenshot({ path: 'proof/builder-mobile-full-v3.png', fullPage: true });
});
