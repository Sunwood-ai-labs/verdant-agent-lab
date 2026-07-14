import { expect, test } from '@playwright/test';

const updateProofs = process.env.UPDATE_PROOFS === '1';

test('captures only the modular reconstruction without a reference overlay', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 1280, height: 960 });
  await page.goto('/builder.html');
  await expect(page.locator('#placedObjects .placed-object').first()).toBeVisible();
  await page.evaluate(() => localStorage.removeItem('verdant-agent-lab-layout-v1'));
  await page.reload();
  await page.addStyleTag({ content: `
    html, body { width: 1280px !important; height: 960px !important; overflow: hidden !important; }
    .builder { display: block !important; width: 1280px !important; height: 960px !important; }
    .topbar, .catalog, .inspector, .workspace__meta, .workspace__hint { display: none !important; }
    .workspace { display: block !important; width: 1280px !important; height: 960px !important; padding: 0 !important; }
    .stage-shell { display: block !important; width: 1280px !important; height: 960px !important; }
    .stage { width: 1280px !important; height: 960px !important; max-width: none !important; border: 0 !important; border-radius: 0 !important; }
    .stage::after { display: none !important; }
  ` });
  await expect(page.locator('#stage')).not.toHaveClass(/is-reference/);
  await expect(page.locator('.stage__reference')).toHaveCSS('opacity', '0');
  await page.locator('#stage').screenshot({
    path: updateProofs ? 'proof/modular-office-v1.png' : testInfo.outputPath('modular-office-v1.png'),
    animations: 'disabled',
  });
});
