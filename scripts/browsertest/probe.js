// Headless probe: open dist/index.html, click every tab (and every indicator),
// confirm each Plotly chart rendered an SVG with path content, report console errors.
//   cd scripts/browsertest && npm i puppeteer-core@22 && node probe.js
const puppeteer = require('puppeteer-core');
const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));
const target = process.argv[2] || 'file:///' + path.resolve(__dirname, '../../dist/index.html').split(path.sep).join('/');
(async () => {
  const browser = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new', args: ['--no-sandbox', '--window-size=1400,1000'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1400, height: 1000 });
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  page.on('requestfailed', r => errors.push('requestfailed: ' + r.url()));
  await page.goto(target, { waitUntil: 'networkidle0', timeout: 60000 });
  await sleep(800);
  const plotStatus = () => page.evaluate(() => [...document.querySelectorAll('.view.on .plot')].map(p => ({ id: p.id, paths: p.querySelectorAll('svg path').length, text: '' })));
  let bad = 0;
  const report = (tab, st) => st.forEach(s => { const ok = s.paths > 5; if (!ok) bad++; console.log(`${ok ? 'OK  ' : 'FAIL'} ${tab.padEnd(14)} ${s.id.padEnd(8)} paths=${s.paths}`); });
  // Indicators: every entry
  const slugs = await page.evaluate(() => [...document.querySelectorAll('#ind-list button')].map(b => b.dataset.s));
  for (const s of slugs) {
    await page.click(`#ind-list button[data-s="${s}"]`); await sleep(500);
    const st = await plotStatus(); report('ind:' + s, st);
    if (!st.length) console.log('    (no plots) ' + s);
  }
  // crop / texture selectors
  await page.click('#ind-list button[data-s="ec"]'); await sleep(400);
  await page.select('#rf-opt', 'maize'); await sleep(400); report('ec:maize', await plotStatus());
  for (const v of ['practices', 'trajectories', 'targets', 'sources']) {
    await page.click(`nav button[data-v="${v}"]`); await sleep(700);
    report(v, await plotStatus());
    const txt = await page.evaluate(v => document.getElementById(v).innerText.length, v);
    console.log(`     ${v} text length ${txt}`);
    await page.screenshot({ path: path.join(__dirname, v + '.png'), fullPage: true });
  }
  // dark mode
  await page.click('#theme'); await page.click('#theme'); await sleep(500);
  await page.click('nav button[data-v="indicators"]'); await sleep(700);
  report('dark:ind', await plotStatus());
  await page.screenshot({ path: path.join(__dirname, 'dark.png'), fullPage: true });
  // phone width
  await page.setViewport({ width: 390, height: 844 }); await sleep(600);
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
  console.log('phone horizontal overflow:', overflow);
  console.log(`\n${bad} failing charts; ${errors.length} errors`); errors.forEach(e => console.log('  ' + e));
  await browser.close();
})();
