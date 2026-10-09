#!/usr/bin/env node
// Web-build drive for the per-frame scale fix: load build/web, then walk,
// jump and whip at spawn while collecting console/page errors.
//   node tools/web_check3.js
const { chromium } = require('/home/hatch/workspace/breach-command-v2/node_modules/playwright-core');
const fs = require('fs');
const path = require('path');

const WEB = '/home/hatch/workspace/gothic-whip/game/build/web';
const OUT = '/tmp/shots_web3';
const MIME = {
  '.html': 'text/html', '.js': 'text/javascript', '.wasm': 'application/wasm',
  '.pck': 'application/octet-stream', '.png': 'image/png', '.json': 'application/json',
};

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const errors = [];
  const ctx = await chromium.launchPersistentContext('/tmp/pw-profile-gw3', {
    executablePath: '/opt/meta-chromium/chrome',
    args: ['--autoplay-policy=no-user-gesture-required', '--no-sandbox'],
    viewport: { width: 1280, height: 760 },
  });
  const page = await ctx.newPage();
  page.on('console', (m) => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
  await page.route('http://localhost:8901/**', (route) => {
    let p = decodeURIComponent(new URL(route.request().url()).pathname);
    if (p === '/') p = '/index.html';
    const file = path.join(WEB, p);
    if (!fs.existsSync(file)) return route.fulfill({ status: 404, body: 'nf' });
    route.fulfill({ status: 200, contentType: MIME[path.extname(file)] || 'application/octet-stream', body: fs.readFileSync(file) });
  });
  await page.goto('http://localhost:8901/');
  await page.waitForSelector('canvas', { timeout: 30000 });
  await page.waitForTimeout(12000); // engine boot + stage load
  await page.mouse.click(640, 380); // canvas focus
  await page.screenshot({ path: OUT + '/w3_a_stand.png' });
  // walk right
  await page.keyboard.down('ArrowRight');
  await page.waitForTimeout(900);
  await page.screenshot({ path: OUT + '/w3_b_walk.png' });
  await page.keyboard.up('ArrowRight');
  // jump
  await page.keyboard.press('Space');
  await page.waitForTimeout(350);
  await page.screenshot({ path: OUT + '/w3_c_jump.png' });
  await page.waitForTimeout(900);
  // whip
  await page.keyboard.down('KeyJ');
  await page.waitForTimeout(120);
  await page.keyboard.up('KeyJ');
  await page.waitForTimeout(250);
  await page.screenshot({ path: OUT + '/w3_d_whip.png' });
  console.log('CONSOLE_ERRORS:', errors.length);
  errors.slice(0, 10).forEach((e) => console.log('  ', e));
  await ctx.close();
})().catch((e) => { console.error('FATAL', e.message); process.exit(1); });
