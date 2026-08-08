const { chromium } = require('playwright');
const path = require('path');

const files = [
  'loop_diagram.html',
  'auto_council_option1_architecture.html',
  'auto_council_option2_meme.html',
  'auto_council_option3_judges.html',
];

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1140, height: 1140 },
    deviceScaleFactor: 2,
  });
  for (const f of files) {
    const page = await context.newPage();
    await page.goto('file://' + path.resolve(f));
    await page.waitForLoadState('networkidle');
    const stage = await page.$('.stage');
    const out = f.replace('.html', '.png');
    await stage.screenshot({ path: out });
    console.log('wrote', out);
    await page.close();
  }
  await browser.close();
})();
