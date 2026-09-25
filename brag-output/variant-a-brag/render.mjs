// Render Jev launch video frames with Playwright.
// usage: node render.mjs stills <outdir> t1:name t2:name ...
//        node render.mjs plan <plan.json>            measure per-frame motion -> subframe count per output frame
//        node render.mjs adaptive <outdir> <plan.json> render S[n] subframes for frame n as g%06d.jpg (global order)
//        node render.mjs poster <file.jpg>
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const url = 'file://' + path.join(here, 'index.html');
const [mode, outDir, ...rest] = process.argv.slice(2);
if (mode !== 'poster' && mode !== 'plan') fs.mkdirSync(outDir, { recursive: true });
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
  await shot(pg, POSTER_T, outDir, 'jpeg');
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
if (mode === 'plan'){
  // motion over each frame's shutter interval [t, t+1/60): max screen displacement of any visible element box corner
  const pg = await openPage(browser);
  const S = [], D = [];
  const MIN = 4, MAX = 32, STEP_PX = 1.25;   // aim for <= 1.25 px between neighbouring subframes
  let prev = await pg.evaluate(t => window.probe(t), 0);
  for (let n = 0; n < NF; n++){
    const next = await pg.evaluate(t => window.probe(t), (n + 1) / FPS);
    let d = 0;
    for (let i = 0; i < prev.length; i++){ const a = prev[i], b = next[i]; if (!a || !b) continue;
      for (let j = 0; j < 4; j++) d = Math.max(d, Math.abs(a[j] - b[j])); }
    D.push(+d.toFixed(2));
    S.push(n === 0 ? 1 : Math.min(MAX, Math.max(MIN, Math.ceil(d / STEP_PX))));
    prev = next;
  }
  fs.writeFileSync(outDir, JSON.stringify({ S, D }));
  const tot = S.reduce((a, b) => a + b, 0);
  console.log('subframes total', tot, 'frames at max', S.filter(x => x === MAX).length, 'max disp px', Math.max(...D));
} else if (mode === 'adaptive'){
  const plan = JSON.parse(fs.readFileSync(rest[0], 'utf8'));
  const jobs = [];
  plan.S.forEach((sn, n) => { for (let k = 0; k < sn; k++) jobs.push(n === 0 ? POSTER_T : n / FPS + k / (FPS * sn)); });
  const pages = [await openPage(browser), await openPage(browser)];
  let next = 0, done = 0;
  await Promise.all(pages.map(async pg => {
    while (true){
      const idx = next++; if (idx >= jobs.length) break;
      await shot(pg, jobs[idx], path.join(outDir, `g${String(idx).padStart(6, '0')}.jpg`), 'jpeg');
      if (++done % 500 === 0) console.log(`${done}/${jobs.length}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
  }));
}
await browser.close();
console.log('done in', ((Date.now() - t0) / 1000).toFixed(1), 's');
