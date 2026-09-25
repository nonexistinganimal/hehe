// Renderer for index.html: pure seek(t) -> screenshot.
//   node render.mjs qa                 -> qa/beatNN.png (settled, per beat) + qa/mid-*.png (mid-morph)
//   node render.mjs stills 1.23 4.5    -> qa/t1.230.png ...
//   node render.mjs full               -> work/frames/sNNNNN.jpg (60 fps x 4 subframes) then ffmpeg tmix -> work/video.mp4
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { mkdirSync, rmSync, existsSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const FFMPEG = '/tmp/claude-0/-home-user-hehe/7469c3b1-4606-5a3e-abcc-995cee3c0800/scratchpad/venv/lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2';
const FPS = 60, SUB = 4, NFRAMES = 720;   // 720 frames = 12.000 s; audio carries the full 12.008 s
const PAGES = 2;                           // shared 4-core box: never more than 2 pages
const mode = process.argv[2] || 'qa';

async function openPages(n) {
  const browser = await chromium.launch({ args: ['--force-color-profile=srgb', '--disable-lcd-text', '--hide-scrollbars'] });
  const url = pathToFileURL(path.join(DIR, 'index.html')).href;
  const pages = [];
  for (let i = 0; i < n; i++) {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1440 }, deviceScaleFactor: 1 });
    page.on('console', m => { if (m.type() === 'warning' || m.type() === 'error') console.log('[page]', m.text()); });
    page.on('pageerror', e => console.log('[pageerror]', e.message));
    await page.goto(url);
    await page.evaluate(() => window.ready);
    await page.evaluate(() => document.fonts.ready);
    pages.push(page);
  }
  return { browser, pages };
}

async function shot(page, t, file, type = 'png') {
  await page.evaluate(tt => window.seek(tt), t);
  const opts = { path: file, type, clip: { x: 0, y: 0, width: 1440, height: 1440 } };
  if (type === 'jpeg') opts.quality = 95;
  await page.screenshot(opts);
}

async function runJobs(pages, jobs) {
  let next = 0, done = 0; const t0 = Date.now();
  await Promise.all(pages.map(async page => {
    while (next < jobs.length) {
      const j = jobs[next++];
      await shot(page, j.t, j.file, j.type);
      done++;
      if (done % 200 === 0) console.log(`${done}/${jobs.length}  ${((Date.now() - t0) / done).toFixed(1)} ms/shot`);
    }
  }));
}

const BP = 0.50033;
if (mode === 'qa' || mode === 'stills') {
  const qa = path.join(DIR, 'qa'); mkdirSync(qa, { recursive: true });
  const jobs = [];
  if (mode === 'qa') {
    for (let n = 1; n <= 24; n++) {
      const tb = (n - 1) * BP;
      // settled look of each beat (just before the next beat), and the exact beat instant
      jobs.push({ t: Math.min(tb + 0.42, 11.99), file: path.join(qa, `beat${String(n).padStart(2, '0')}.png`) });
    }
    for (const t of [0.62, 1.58, 2.07, 2.56, 3.62, 4.02, 4.55, 5.04, 5.58, 6.5, 7.08, 7.55, 8.1, 9.06, 9.58, 10.07, 11.56, 11.66]) jobs.push({ t, file: path.join(qa, `mid-${t.toFixed(2)}.png`) });
    jobs.push({ t: 0, file: path.join(qa, 'frame-first.png') });
    jobs.push({ t: (NFRAMES - 1) / FPS, file: path.join(qa, 'frame-last.png') });
  } else {
    for (const a of process.argv.slice(3)) jobs.push({ t: +a, file: path.join(qa, `t${(+a).toFixed(3)}.png`) });
  }
  const { browser, pages } = await openPages(Math.min(PAGES, jobs.length));
  await runJobs(pages, jobs);
  await browser.close();
  console.log('wrote', jobs.length, 'stills');
} else if (mode === 'full') {
  const fdir = path.join(DIR, 'work', 'frames');
  if (existsSync(fdir)) rmSync(fdir, { recursive: true });
  mkdirSync(fdir, { recursive: true });
  const jobs = [];
  for (let f = 0; f < NFRAMES; f++) for (let k = 0; k < SUB; k++) {
    const i = f * SUB + k;
    jobs.push({ t: f / FPS + k / (FPS * SUB), file: path.join(fdir, `s${String(i).padStart(5, '0')}.jpg`), type: 'jpeg' });
  }
  const { browser, pages } = await openPages(PAGES);
  const t0 = Date.now();
  await runJobs(pages, jobs);
  await browser.close();
  console.log(`rendered ${jobs.length} subframes in ${((Date.now() - t0) / 1000).toFixed(1)} s`);
  // 4 subframes -> 1 frame (equal-weight tmix), keep every 4th averaged frame
  const out = path.join(DIR, 'work', 'video.mp4');
  const r = spawnSync(FFMPEG, ['-y', '-hide_banner', '-loglevel', 'error', '-framerate', String(FPS * SUB), '-i', path.join(fdir, 's%05d.jpg'),
    '-vf', `tmix=frames=${SUB}:weights='1 1 1 1',select='eq(mod(n\\,${SUB})\\,${SUB - 1})',setpts=N/(${FPS}*TB),format=yuv420p`,
    '-r', String(FPS), '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-threads', '2', out], { stdio: 'inherit' });
  if (r.status !== 0) process.exit(1);
  console.log('wrote', out);
}
