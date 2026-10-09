#!/usr/bin/env node
// Chromium check for whip builds: load the fresh build/web export, walk
// to the training effigy, then MASH the whip key while capturing frames
// continuously (screenshots are slow under SwiftShader, ~1.8 s each, and
// the game clock crawls - a staggered single-shot approach misses the
// 500 ms swing; mashing guarantees crack frames land in the stream).
//   node tools/web_check2.js [outdir] [seconds]
const { chromium } = require('/home/hatch/workspace/breach-command-v2/node_modules/playwright-core');
const fs = require('fs');
const path = require('path');

const WEB = '/home/hatch/workspace/gothic-whip/game/build/web';
const OUT = process.argv[2] || '/tmp/whipwork';
const SECS = parseInt(process.argv[3] || '20', 10);
const MIME = {
  '.html': 'text/html', '.js': 'text/javascript', '.wasm': 'application/wasm',
  '.pck': 'application/octet-stream', '.png': 'image/png', '.json': 'application/json',
};

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const errors = [];
  const ctx = await chromium.launchPersistentContext('/tmp/pw-profile-gw2', {
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
  await page.waitForTimeout(13000); // engine boot + stage load
  await page.screenshot({ path: OUT + '/web2_spawn.png' });
  await page.mouse.click(640, 380); // canvas focus
  await page.keyboard.down('ArrowRight');
  await page.waitForTimeout(1300);
  await page.keyboard.up('ArrowRight');
  await page.waitForTimeout(300);
  const cdp = await page.context().newCDPSession(page);
  let n = 0;
  const t0 = Date.now();
  let nextPress = 0;
  while (Date.now() - t0 < SECS * 1000) {
    const now = Date.now() - t0;
    if (now >= nextPress) {
      nextPress = now + 1300;
      cdp.send('Input.dispatchKeyEvent', {
        type: 'keyDown', key: 'j', code: 'KeyJ',
        windowsVirtualKeyCode: 74, nativeVirtualKeyCode: 74,
      }).catch(() => {});
      setTimeout(() => cdp.send('Input.dispatchKeyEvent', {
        type: 'keyUp', key: 'j', code: 'KeyJ',
        windowsVirtualKeyCode: 74, nativeVirtualKeyCode: 74,
      }).catch(() => {}), 120);
    }
    const r = await cdp.send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(OUT, `web2_stream_${String(n).padStart(3, '0')}.png`),
      Buffer.from(r.data, 'base64'));
    n++;
  }
  console.log('captured', n, 'frames');
  console.log('CONSOLE_ERRORS:', errors.length);
  errors.slice(0, 10).forEach((e) => console.log('  ', e));
  await ctx.close();
})().catch((e) => { console.error('FATAL', e.message); process.exit(1); });
