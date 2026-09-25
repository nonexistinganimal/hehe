# /brag plan: Jev by TypeSafe (12 s launch video)

Built with **brag** (`latent-spaces/brag` @ `c893c5e`, installed at `.claude/skills/`). On Opus 5.5 `/brag` hands off to **`/brag-slim`**, so the whole video is code: one HTML file rendered frame by frame, with no Hyperframes and no After Effects. The creative laws, music bed, SFX library, cue sheet and SFX analysis all come from the brag repo.

Inputs: [`research/jev.md`](research/jev.md) · [`design-system/typesafe-design-system.md`](design-system/typesafe-design-system.md) · [`work/beat-grid.json`](work/beat-grid.json)

---

## Brief

| | |
|---|---|
| **What it is** | Jev, the first System One model: typed questions in, typed answers + probabilities out, in 70–500 ms |
| **Who for** | Developers wiring AI into software (routing, triage, agents, real-time loops) |
| **Angle** | *Your code never wanted a paragraph.* Every dev has had `JSON.parse` blow up on "Sure! Here's the JSON:". Jev answers in types. |
| **Hook (0–2 s)** | A chat model streams "Sure! Here's the JSON…" and `JSON.parse(reply)` throws. Painful, specific, funny. |
| **Highlights** | ① typed questions → typed answers + probabilities ② code branches on it with a confidence gate ③ 70–500 ms, $0.042/1M in, output free |
| **Punchline** | `Jev` · by TypeSafe · typesafe.ai |
| **Tone** | `polished` × `default`: confident, dry, code-native. The humor is the hook only. |
| **Format** | Square **1440×1440**, **60 fps** (4 subframes blended for motion blur), **11.996 s** |
| **Visual rule** | **One shape, never cut.** A single paper card morphs size, radius and fill through every state; content swaps with a short blur; a cursor drives every change; the camera re-frames each state. |
| **Look** | TypeSafe language: parchment canvas, ink type, Space Mono, type-tag chips, one isometric "engine" beat, text-scramble reveals. No gradients, glows or bounce. |

## Music: measured, not guessed

Track: `happy-beats-business-moves-vol-1-by-ende-dot-app.mp3` (brag bundle, ende.app). Analysed with numpy + librosa (`work/analyze_beats.py`):

- **120.04 BPM**, beat = 0.49985 s. Key ≈ **A minor / C major** (chroma).
- Low-band kick onsets are measured at 12.013, 14.022, **16.013** (the drums enter, bar energy ×2.3), 18.019 … 24.009.
- **Cut: song 12.013 → 24.009 = 24 beats = 6 bars = 11.996 s.** Starts on a downbeat, spends 2 bars in the airy pre-drop, and **the drop lands at 4.0 s, on the Run click.**
- Pre-drop hats are 16ths (0.125 s), so they share a grid with the streaming-text ticks and the text scramble.

## Beat grid storyboard

`B#` = beat (t = (B−1) × 0.5 s). Every beat has an event.

### Bar 1 · Hook, pre-drop (0.0–2.0)
| B | t | Shape state | Cursor / action | On screen text |
|---|---|---|---|---|
| 1 | 0.0 | **Chat bubble** (neutral gray, not TypeSafe's palette: it's "the other way"), text streaming: `Sure! Here's the JSON you asked for: ```json {"intent": "refu` | Idle, drifting in | timer chip `thinking 2.9s` counting up |
| 2 | 0.5 | Streaming continues, timer ticks | Cursor moves to the code line under the bubble | `const a = JSON.parse(reply)` |
| 3 | 1.0 | Parse **throws**: ink chip `SyntaxError: Unexpected token 'S'` snaps under the line | — | |
| 4 | 1.5 | Bubble dims | Cursor hovers bubble | Kicker scrambles in: **"Stop parsing paragraphs."** (holds to 3.0) |

### Bar 2 · Setup (2.0–4.0)
| B | t | Shape state | Cursor / action | Text |
|---|---|---|---|---|
| 5 | 2.0 | **Morph → state card** (gray → paper, r 28 → 12, reflows). Blur-swap to `state` · `"I was charged twice and need the duplicate refunded today."` | Click on the bubble | — |
| 6 | 2.5 | Row lands: `intent` `Choice` refund · technical_help · information · other | — | |
| 7 | 3.0 | Row lands: `is_urgent` `Noul` | — | |
| 8 | 3.5 | Row lands: `frustration` `Score` 0 · 1 · 2. Footer grows the ink pill `Run ▸` | Cursor glides to Run (hover at 3.75) | |

(This is the official SDK README example: same ticket, same three questions.)

### Bar 3 · The drop: Jev runs (4.0–6.0)
| B | t | Shape state | Cursor / action | Text |
|---|---|---|---|---|
| 9 | **4.0** | **Click on the drop.** Card folds into the **isometric engine cube** (TypeSafe's homepage motif); typed blocks slide in along iso rails; label `jev-latest · System One` | Press + release | ms counter races `0 → 256 ms` |
| 10 | 4.5 | Cube unfolds → **answers card**: `intent → "refund"` · `is_urgent → 0.97` · `frustration → 1.6`, staggered on 16ths (4.5 / 4.625 / 4.75) | — | |
| 11 | 5.0 | Choice row expands into **probability bars** that draw themselves: refund 0.94 · technical_help 0.03 · information 0.02 · other 0.01 | Hover refund bar → tooltip `p 0.94 · confidence 0.91` | Kicker: **"Typed answers. Real probabilities."** (5.0–6.5) |
| 12 | 5.5 | Bars settle; non-chosen bars fade to ink-3 | — | |

### Bar 4 · Your code branches (6.0–8.0)
| B | t | Shape state | Cursor / action | Text |
|---|---|---|---|---|
| 13 | 6.0 | **Morph → code card**: `if a.intent.choice == "refund"` / `and a.intent.confidence > 0.50:` / `route_to_billing()` | — | |
| 14 | 6.5 | Threshold slider appears in the gutter | **Drag** 0.50 → 0.90 (direct manipulation; value follows the cursor, springs on release; the number in the code updates live) | |
| 15 | 7.0 | **Toggle `auto-route` flips ON on the beat.** Knob rides two springs so the leading edge stretches ahead | Click | |
| 16 | 7.5 | Toast slides out of the card: `→ billing · 256 ms` | — | Kicker: **"Your code branches. No parsing."** (7.5–8.5) |

### Bar 5 · The numbers (8.0–10.0)
| B | t | Shape state | Cursor / action | Text |
|---|---|---|---|---|
| 17 | 8.0 | **Toast morphs → stat block.** Row 1 scrambles in: **`70–500 ms`** · end-to-end | — | |
| 18 | 8.5 | Row 2: **`$0.042`** / 1M input tokens | — | |
| 19 | 9.0 | Row 3: **`output tokens: free`**, "free" lands as an ink stamp chip | Cursor taps "free" | |
| 20 | 9.5 | Hold (all three rows readable ≥ 1 s) | Cursor drifts off | |

### Bar 6 · End card (10.0–12.0)
| B | t | Shape state | Cursor / action | Text |
|---|---|---|---|---|
| 21 | 10.0 | **Stat block collapses into the wordmark:** **`Jev`** scrambles in, Space Mono 700, display size | — | |
| 22 | 10.5 | `by TypeSafe` fades up beneath | — | |
| 23 | 11.0 | `early access · typesafe.ai` in micro | — | |
| 24 | 11.5 | Dead still. Music fades over the last 0.4 s | — | |

**Readability check** (≈0.3 s per word, counted from when the line is fully on screen): every kicker is ≤ 5 words and holds 1.0–1.5 s; each stat row holds ≥ 1.0 s; the end card holds 1.0–2.0 s. ✔

**Claims check:** 70–500 ms, $0.042/1M input and "output free" are TypeSafe's published numbers. `256 ms` is the measured median from 1kpapers.com. The probability values in the simulated run (0.94, 0.97, 1.6, 0.91) are illustrative UI output for a demo request, not a benchmark claim. No invented multipliers ("200× faster"). ✔

## Sound cue sheet

Mix: music bed 0.35, SFX 0.25–0.75, all SFX from brag's low/medium-HF-risk picks (`sfx-analysis.md`). Pitched SFX are shifted into **A minor** so they sit inside the track. Each start time is **beat time − measured peak offset**, so the transient lands exactly on the grid.

| Video t (peak) | File | Peak offset | Pitch | Gain | Why |
|---|---|---|---|---|---|
| 0.000–0.875 (16ths) | `keyboard/keypress-*` random | ~0 | — | 0.10 | text streaming, tucked under the hats |
| 1.000 | `interface/glitch_002` | 0 ms | — | 0.35 | parse error (the one "wrong" sound) |
| 2.000 | `interface/click_003` | 0.1 ms | — | 0.55 | click on the bubble |
| 2.250 | `interface/drop_002` | 0.5 ms | −0.81 st → A5 | 0.40 | state card lands |
| 2.5 / 3.0 / 3.5 | `interface/drop_001` | 0.3 ms | −2.39 st → E6 | 0.38 / 0.40 / 0.42 | question rows land (small crescendo into the drop) |
| 3.750 | `ui/rollover2` | 23.4 ms | — | 0.22 | hover Run |
| **4.000** | `interface/click_003` + `impact/impactSoft_medium_001` | 0.1 / 5.3 ms | — | 0.60 / 0.75 | **Run on the drop** |
| 4.5 / 4.625 / 4.75 | `keyboard/keypress-*` | ~0 | — | 0.20 | answers fill in |
| 5.000 | `ui/rollover2` | 23.4 ms | — | 0.20 | tooltip hover |
| 6.000 | `interface/drop_002` | 0.5 ms | −0.81 st | 0.35 | code card |
| **7.000** | `interface/switch_007` | 109.2 ms | +1.44 st → E6 | 0.50 | toggle flips on the beat |
| 7.500 | `interface/drop_001` | 0.3 ms | −2.39 st | 0.38 | toast |
| 8.000 | `impact/impactSoft_medium_004` | ~5 ms | — | 0.55 | stat block reveal |
| 8.500 | `interface/drop_002` | 0.5 ms | −0.81 st | 0.32 | price row |
| 9.000 | `impact/impactGlass_light_001` | 0.2 ms | −1.38 st → C6 | 0.28 | "free" stamp |
| **10.000** | `impact/impactSoft_medium_001` + `interface/bong_001` | 5.3 / 1.5 ms | bong −1.0 st → A3 | 0.70 / 0.55 | wordmark lands |
| 11.6–12.0 | music | — | — | fade → 0 | clean ending |

## Build (per brag-slim §3, plus the motion recipe from the reference)

1. **One HTML file, 1440×1440.** Every style is computed from `t` inside `seek(t)`. No CSS transitions, no timers, no state carried between frames.
2. **Springs are closed-form step responses.** A value retargeted many times is the *sum of one spring per change*, so it stays a pure function of time. Params come from the design tokens (`snap` ω28 ζ0.9, `move` ω18 ζ0.95, `lazy` ω11 ζ1.0).
3. **One morphing container**: x, y, w, h, radius and fill all ride springs. Inner content has its *own* enter/exit windows (exit blur 0→8px over 80 ms, enter 8→0 over 120 ms) so swaps never overlap.
4. **Dual-edge springs** for the toggle knob and the slider fill: the leading edge uses `snap`, the trailing edge `move`.
5. **Drags are direct manipulation**: while held, value = f(cursor x); on release, spring back from wherever it was.
6. **Text scramble**: deterministic glyph per (char index, frame), resolving left→right at 18 ms/char, in TypeSafe's GSAP style.
7. **Camera**: a separate spring-driven scale/translate so each state fills ~70% of the frame. **No `will-change` on anything the camera scales** (it blurs text).
8. **Render**: Playwright (pre-installed Chromium), 4 subframes per output frame → ffmpeg `tmix` → 60 fps. Audio assembled with ffmpeg (`adelay` + `asetrate`/`atempo` for pitch + `amix`), using the music slice 12.013–24.009 s.
9. **QA before the full render**: one still per beat (24 PNGs) plus mid-morph stills at B5, B9, B13, B17 and B21, checked for overflow, collisions, contrast and anything off the grid.
10. **Deliver** (brag §4): `brag.mp4`, a poster `brag.jpg` taken from the settled end card and baked in as frame 0, and `share-copy.txt`.

**Draft share copy:** *Your code never wanted a paragraph. Jev by TypeSafe answers in types, with probabilities, in 70–500 ms. Output tokens are free.*

## Open decisions (defaults in bold)

1. **Format:** **square 1440** (like the reference), or 16:9 1920×1080 (brag default, better for X/LinkedIn inline)?
2. **Exact palette:** allow `typesafe.ai` in the environment's network settings so I can pull the real hex values and body font, or **ship with the reconstructed parchment/ink tokens**.
3. **Accent:** **pure ink on parchment**, or one signal color on the chosen answer and probabilities only?
4. **Loop:** **end on the wordmark** (a launch video), or make frame 11.996 equal frame 0 so it loops on autoplay (the end card would then morph back into the chat bubble in B24)?
