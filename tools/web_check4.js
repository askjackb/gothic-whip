#!/usr/bin/env node
// Web-build drive for the crouch-zoom + boss torso fix (round 5): load
// build/web, screenshot the hunter standing, then fully crouched (Down
// held through enter -> crouch_idle), then F9-warp to the boss arena and
// screenshot the boss standing, while collecting console/page errors.
//   node tools/web_check4.js
const { chromium } = require('/home/hatch/workspace/breach-command-v2/node_modules/playwright-core');
const fs = require('fs');
const path = require('path');

const WEB = '/home/hatch/workspace/gothic-whip/game/build/web';
const OUT = '/home/hatch/workspace/gothic-whip/game/tests/shots/fix5';
const MIME = {
  '.html': 'text/html', '.js': 'text/javascript', '.wasm': 'application/wasm',
  '.pck': 'application/octet-stream', '.png': 'image/png', '.json': 'application/json',
};

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const errors = [];
  const ctx = await chromium.launchPersistentContext('/tmp/pw-profile-gw4', {
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
  await page.screenshot({ path: OUT + '/web5_a_stand.png' });
  // crouch: hold Down through enter (4 x 50 ms) into crouch_idle
  await page.keyboard.down('ArrowDown');
  await page.waitForTimeout(900);
  await page.screenshot({ path: OUT + '/web5_b_crouch.png' });
  await page.keyboard.up('ArrowDown');
  await page.waitForTimeout(600); // stand back up
  await page.screenshot({ path: OUT + '/web5_c_standagain.png' });
  // F9 dev warp to the boss arena approach, then let the boss idle
  await page.keyboard.down('F9');
  await page.waitForTimeout(300);
  await page.keyboard.up('F9');
  await page.waitForTimeout(800);
  // cross the arena gate (x=5632) and close to confrontation range; the
  // boss then stands in his idle between decisions - burst-capture it
  await page.keyboard.down('ArrowRight');
  await page.waitForTimeout(2400);
  await page.keyboard.up('ArrowRight');
  for (let i = 0; i < 8; i++) {
    await page.screenshot({ path: OUT + `/web5_d_boss_${i}.png` });
    await page.waitForTimeout(300);
  }
  console.log('CONSOLE_ERRORS:', errors.length);
  errors.slice(0, 10).forEach((e) => console.log('  ', e));
  await ctx.close();
})().catch((e) => { console.error('FATAL', e.message); process.exit(1); });
