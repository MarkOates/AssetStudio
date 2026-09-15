const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  await page.goto('http://localhost:8000/pack.html');
  await page.waitForTimeout(2000);
  const content = await page.evaluate(() => {
     return Array.from(document.querySelectorAll('#pack-list a span')).map(s => s.innerText);
  });
  console.log("Found spans:", content.length);
  await browser.close();
})();
