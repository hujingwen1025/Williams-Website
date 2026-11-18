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

  const modelImage = topic => page.$eval(`#${topic} .model-canvas`, canvas => canvas.toDataURL());
  const modelAction = async (topic, key) => {
    await page.$eval('#' + topic, el => el.scrollIntoView({ block: 'start', behavior: 'instant' }));
    const stage = `#${topic} .model-stage`;
    if (key) {
      await page.focus(stage);
      await page.keyboard.press(key);
    } else {
      await page.click(stage);
    }
  };
  await page.setViewport({ width: 1440, height: 900 });
  await go('/');
  await page.waitForSelector('.model-canvas:not([hidden])');
  assert.equal(await page.$$eval('.topic-model button', els => els.length), 0);
  assert.equal(await page.$eval('.page-field', el => el.clientWidth), 1440);
  const heroField = await page.$eval('.page-field', el => el.toDataURL());
  for (const [topic, right] of [['technology', true], ['music', false], ['cubing', true]]) {
    const placement = await page.$eval('#' + topic, section => {
      const model = section.querySelector('figure');
      const topicCopy = section.querySelector('.topic-copy');
      const grid = section.querySelector('.topic-grid');
      const pin = parseFloat(getComputedStyle(model).top);
      const start = grid.getBoundingClientRect().top + scrollY - pin;
      const measure = y => { scrollTo({ top: y, behavior: 'instant' }); return model.getBoundingClientRect().top; };
      return { left: model.getBoundingClientRect().left, copy: topicCopy.getBoundingClientRect().left,
        width: model.clientWidth, first: measure(start + 40), second: measure(start + 100), released: measure(start + grid.offsetHeight) };
    });
    assert.equal(placement.left > placement.copy, right);
    assert(placement.width >= 800, topic + ' should use the wider drawing area');
    assert(Math.abs(placement.first - placement.second) < 2 && placement.released < placement.second - 30, topic + ' should pin and release');
    const initial = await modelImage(topic);
    await modelAction(topic, 'ArrowLeft');
    assert.notEqual(await modelImage(topic), initial);
    await modelAction(topic, 'Home');
    assert.equal(await modelImage(topic), initial);
  }
  const cubeStart = await modelImage('cubing');
  await modelAction('cubing');
  assert.notEqual(await modelImage('cubing'), cubeStart);
  const turned = await modelImage('cubing');
  await modelAction('cubing', 'ArrowRight');
  await modelAction('cubing', 'Home');
  assert.equal(await modelImage('cubing'), turned, 'A view reset must keep the applied turn');
  for (let i = 0; i < 3; i++) await modelAction('cubing', 'Enter');
  assert.equal(await modelImage('cubing'), cubeStart, 'Four turns must restore the puzzle');
  const steady = await modelImage('music');
  await modelAction('music');
  assert.notEqual(await modelImage('music'), steady);
  await page.waitForFunction(() => document.querySelector('#music [role="status"]').textContent.includes('Syncopated'));
  const unlit = await modelImage('technology');
  await modelAction('technology');
  assert.notEqual(await modelImage('technology'), unlit);
  await page.waitForFunction(() => document.querySelector('#technology [role="status"]').textContent.includes('contact'));
  await page.waitForFunction(initial => document.querySelector('.page-field').toDataURL() !== initial, {}, heroField);
  console.log('PASS full-width page field, larger unframed models, pinning, direct actions, and keyboard rotation');

  await page.keyboard.down('Control');
  await page.keyboard.press('k');
  await page.keyboard.up('Control');
  await page.waitForSelector('#section-jump[open]');
  await page.type('#section-jump input', 'missing topic');
  assert.equal(await page.$eval('.jump-empty', el => el.hidden), false);
  await page.keyboard.press('Escape');
  await page.waitForFunction(() => !document.querySelector('#section-jump').open && document.activeElement.matches('#technology .model-stage'));
  await page.click('.jump-trigger');
  await page.type('#section-jump input', 'music');
  await page.keyboard.press('ArrowDown');
  assert.equal(await page.evaluate(() => document.activeElement.hash), '#music');
  await page.keyboard.press('Enter');
  await page.waitForFunction(() => location.hash === '#music' && document.activeElement.id === 'music-heading');
  await page.click('.language-link');
  await page.waitForFunction(() => document.documentElement.lang === 'zh-Hans' && location.hash === '#music');
  console.log('PASS jump shortcut, search, empty state, Escape, arrows, Enter, and topic language anchor');

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
  assert.equal(await plain.$$eval('.model-fallback:not([hidden])', els => els.length), 3);
  assert.equal(await plain.$$eval('.model-stage[tabindex], .jump-trigger:not([hidden])', els => els.length), 0);
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
