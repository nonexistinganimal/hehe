// Render Jev launch video frames with Playwright.
// usage: node render.mjs stills <outdir> t1:name t2:name ...   |  node render.mjs frames <outdir>
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const url = 'file://' + path.join(here, 'index.html');
const [mode, outDir, ...rest] = process.argv.slice(2);
fs.mkdirSync(outDir, { recursive: true });
const FPS = 60, SUB = 4, DUR = 11.996, POSTER_T = 11.9;
const NF = Math.round(DUR * FPS);   // 720 output frames (the mux trims to 11.996 s)

async function openPage(browser){
  const page = await browser.newPage({ viewport: { width: 1440, height: 1440 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.error('PAGEERROR', e.message)); page.on('console', m => { if (m.type() === 'error') console.error('CONSOLE', m.text()); });
  await page.goto(url);
  await page.evaluate(() => window.__ready);
  return page;
}
async function shot(page, t, file, type){
  await page.evaluate(tt => window.seek(tt), t);
  await page.screenshot({ path: file, type, ...(type === 'jpeg' ? { quality: 95 } : {}), clip: { x: 0, y: 0, width: 1440, height: 1440 } });
}
const browser = await chromium.launch({ args: ['--disable-gpu', '--font-render-hinting=none', '--disable-lcd-text'] });
const t0 = Date.now();
if (mode === 'stills'){
  const jobs = rest.map(s => { const [t, name] = s.split(':'); return { t: parseFloat(t), name: name || t }; });
  const pages = [await openPage(browser), await openPage(browser)];
  let i = 0;
  await Promise.all(pages.map(async pg => { while (i < jobs.length){ const j = jobs[i++]; await shot(pg, j.t, path.join(outDir, j.name + '.png'), 'png'); } }));
} else if (mode === 'poster'){
  const pg = await openPage(browser);
  await shot(pg, POSTER_T, rest[0], 'jpeg');
} else if (mode === 'frames'){
  // subframe k of output frame n is at n/60 + k/240; output frame 0 is the poster (all 4 subframes at POSTER_T)
  const total = NF * SUB;
  const pages = [await openPage(browser), await openPage(browser)];
  let next = 0, done = 0;
  await Promise.all(pages.map(async pg => {
    while (true){
      const idx = next++; if (idx >= total) break;
      const n = Math.floor(idx / SUB), k = idx % SUB;
      const t = n === 0 ? POSTER_T : n / FPS + k / (FPS * SUB);
      await shot(pg, t, path.join(outDir, `f${String(idx).padStart(5, '0')}.jpg`), 'jpeg');
      if (++done % 240 === 0) console.log(`${done}/${total}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
  }));
}
await browser.close();
console.log('done in', ((Date.now() - t0) / 1000).toFixed(1), 's');
