/* Optional browser regression checks. Supply PUPPETEER_ROOT and a local preview URL. */
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { join } from 'node:path';
const require = createRequire(join(process.env.PUPPETEER_ROOT || process.cwd(), 'browser-check.cjs'));
const puppeteer = require('puppeteer-core').default;
const base = process.argv[2] || 'http://127.0.0.1:4825';
const browser = await puppeteer.launch({ executablePath: process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
const errors = [];
const page = await browser.newPage();
page.on('pageerror', error => errors.push(error.message));
const go = async (path = '/') => { const response = await page.goto(base + path, { waitUntil: 'networkidle0' }); await page.evaluate(() => document.fonts.ready); return response; };
const count = () => page.$$eval('.repo-card:not([hidden])', els => els.length);
const input = value => page.$eval('#project-search', (el, value) => { el.value = value; el.dispatchEvent(new Event('input', { bubbles: true })); }, value);
try {
  await page.setViewport({ width: 1440, height: 900 });
  await go();
  assert.equal(await count(), 28);
  assert.deepEqual(await page.$$eval('.feature-card h3', els => els.map(e => e.textContent)), ['Resona Lite', 'Cubers', 'CAICP Academy', 'Dorm Pass Manager']);
  await input('calendar'); assert.equal(await count(), 2);
  await page.click('[data-filter="music"]'); assert.equal(await count(), 0);
  assert.equal(await page.$eval('.empty-state', el => el.hidden), false);
  await page.click('.reset-search'); assert.equal(await count(), 28);
  assert.equal(await page.$eval('#project-search', el => el === document.activeElement), true);
  await input('ＲＥＳＯＮＡ'); assert.equal(await count(), 2);
  await page.click('[data-filter="exabyte"]'); assert.equal(await count(), 2);
  await input('not-a-project'); assert.equal(await count(), 0);
  await go('/#project-whaos');
  assert.equal(await page.$eval('#project-whaos details', el => el.open), true);
  assert.equal(await page.$eval('#project-whaos', el => el.hidden), false);
  await page.click('[data-filter="music"]');
  await page.evaluate(() => { location.hash = 'about'; location.hash = 'project-whaos'; });
  await page.waitForFunction(() => !document.querySelector('#project-whaos').hidden);
  assert.equal(await count(), 28);
  console.log('PASS search, Unicode normalization, combined filters, reset/focus, and legacy project deep links');

  for (const route of ['/', '/zh/']) {
    for (const width of [320, 375, 768, 1280, 1440, 1920]) {
      await page.setViewport({ width, height: width >= 1280 ? 900 : 812 });
      await go(route);
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true, `${route} overflows at ${width}`);
      await page.$$eval('img', els => els.forEach(el => { el.loading = 'eager'; }));
      await page.waitForFunction(() => [...document.images].every(el => el.complete && el.naturalWidth > 0));
      if (width >= 1280) {
        const bounds = await page.$eval('.hero-links', el => ({ bottom: el.getBoundingClientRect().bottom, height: innerHeight }));
        assert(bounds.bottom <= bounds.height, 'Hero actions fall below the fold');
      }
    }
  }
  assert.equal(await page.evaluate(() => document.fonts.check('600 32px "Familjen Grotesk"') && document.fonts.check('400 16px "IBM Plex Sans"')), true);
  console.log('PASS both languages at 320, 375, 768, 1280, 1440, and 1920px; images, fonts, and hero visibility');

  await page.setViewport({ width: 375, height: 812 });
  await go();
  await page.click('.menu-toggle');
  assert.equal(await page.$eval('.menu-toggle', el => el.getAttribute('aria-expanded')), 'true');
  await page.keyboard.press('Escape');
  assert.equal(await page.$eval('.menu-toggle', el => el.getAttribute('aria-expanded')), 'false');
  assert.equal(await page.$eval('.menu-toggle', el => el === document.activeElement), true);
  await page.click('.menu-toggle');
  await page.click('.navigation a[href="#beyond"]');
  assert.equal(await page.$eval('.menu-toggle', el => el.getAttribute('aria-expanded')), 'false');
  await page.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: 'reduce' }]);
  await go('/#interest-video');
  await page.click('.language-link');
  await page.waitForFunction(() => document.documentElement.lang === 'zh-Hans');
  assert.equal(new URL(page.url()).hash, '#interest-video');
  await page.evaluate(() => document.fonts.ready);
  const still = await page.$eval('#ascii-field', el => el.toDataURL());
  await page.mouse.move(350, 300);
  await new Promise(resolve => setTimeout(resolve, 100));
  assert.equal(await page.$eval('#ascii-field', el => el.toDataURL()), still);
  console.log('PASS mobile menu, Escape/focus, section-preserving language switch, and reduced-motion still field');

  const fallback = await browser.newPage();
  fallback.on('pageerror', error => errors.push(error.message));
  await fallback.evaluateOnNewDocument(() => { delete window.IntersectionObserver; });
  await fallback.goto(base, { waitUntil: 'networkidle0' });
  assert.equal(await fallback.$$eval('.repo-card:not([hidden])', els => els.length), 28);
  await fallback.close();
  const plain = await browser.newPage();
  await plain.setJavaScriptEnabled(false);
  await plain.goto(base + '/zh/', { waitUntil: 'networkidle0' });
  assert.equal(await plain.$$eval('.repo-card', els => els.filter(el => !el.hidden).length), 28);
  assert.equal(await plain.$eval('.directory-controls', el => getComputedStyle(el).display), 'none');
  await plain.click('#project-whaos summary');
  assert.equal(await plain.$eval('#project-whaos details', el => el.open), true);
  await plain.close();
  console.log('PASS native disclosures and complete content without JavaScript or IntersectionObserver');

  for (const route of ['/missing/nested/path', '/zh/missing/nested/path']) {
    const response = await go(route);
    assert.equal(response.status(), 404);
    assert.equal(await page.$eval('html', el => el.lang), route.startsWith('/zh/') ? 'zh-Hans' : 'en');
    assert.equal(await page.$eval('meta[name="robots"]', el => el.content.includes('noindex')), true);
  }
  for (const route of ['/403.html', '/500.html', '/503.html', '/zh/403.html', '/zh/500.html', '/zh/503.html']) {
    assert.equal((await go(route)).status(), 200);
    assert.equal(await page.$eval('h1', el => !!el.textContent.trim()), true);
  }
  assert.deepEqual(errors, [], 'Browser runtime errors');
  console.log('PASS bilingual error pages, nested 404 recovery, and no browser runtime errors');
} finally { await browser.close(); }
