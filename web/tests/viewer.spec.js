const { test, expect } = require('@playwright/test');

test('Asset Viewer loads and navigates', async ({ page }) => {
  const exceptions = [];
  const networkErrors = [];
  const consoleErrors = [];

  page.on('pageerror', error => {
    exceptions.push(error.message);
  });

  page.on('response', response => {
    if (response.status() === 404) {
      networkErrors.push(response.url());
    }
  });
  
  page.on('console', msg => {
    if (msg.type() === 'error') {
      consoleErrors.push(msg.text());
    }
  });

  await page.goto('http://localhost:8000');

  await expect(page).toHaveTitle('Asset Viewer');

  expect(exceptions).toEqual([]);
  expect(networkErrors).toEqual([]);

  const firstAssetLink = page.locator('.card-body div a').first();
  await firstAssetLink.click();

  await expect(page).toHaveURL(/.*asset\.html\?id=.*/);
});
