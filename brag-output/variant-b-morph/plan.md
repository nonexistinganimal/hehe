# Jev: Variant B "morph", state list on the beat grid
Music slice song 16.013 → 28.021 s · 24 beats · period 0.50033 s · beat n at (n−1)×0.50033 · 12.008 s loop · one shape, never cut

B1  0.000  Ink pill "Ask Jev ▸" at rest (camera 2.3×); cursor leaves its rest spot on the downbeat. Frame 0 == last frame.
B2  0.500  Cursor press (click): pill scales .96; on release (0.58) it contracts to a 112 px circle; loader ring starts spinning.
B3  1.001  Ring closes to a full circle and the check draws itself (dashoffset). Drop A5.
B4  1.501  Circle stretches into an ink island: live dot · jev-latest · "70 ms" (scramble). Camera 1.65×. Drop E6.
B5  2.001  Island becomes a paper ⌘K palette: "Ask a typed question…", 5 typed rows, key-hint footer. Camera 1.22×.
B6  2.502  Type u / r / g on 16ths (2.502, 2.627, 2.752): intent drops out, then frustration; matches bold; highlight on is_urgent.
B7  3.002  Cursor hovers is_urgent · Noul: highlight inverts to ink, chip inverts to paper. Rollover.
B8  3.502  ⏎ chip depresses (keypress); palette collapses, is_urgent + Noul chip glide into the toggle-card header.
B9  4.002  Cursor clicks the toggle: ON exactly on the beat; knob's leading edge on a stiffer spring stretches ahead; 0.97 scrambles in.
B10 4.503  Toggle knob grows into the ink tab indicator under Choice | Score | Noul (on Noul); card becomes a pill tab bar.
B11 5.003  Cursor clicks Score: indicator slides, left (leading) edge ahead of the right edge.
B12 5.503  Score opens the rubric slider: frustration · 0 calm · 1 civil · 2 angry (card grows down, tabs stay).
B13 6.004  Cursor grabs the knob (knob swells) and drags right; value = f(cursor x) live. Camera leans in 1.6×.
B14 6.504  Drag passes max: knob resists, track rubber-bands (stretches longer and thinner), value pinned at 2.0.
B15 7.004  Release: knob springs back from wherever it was to 1.6; value counts down to 1.6; track un-stretches.
B16 7.505  Cursor clicks Choice: indicator slides left, leading edge first. Camera back to 1.5×.
B17 8.005  Chart opens: intent bars draw themselves (refund 0.94 in ink; 0.03 / 0.02 / 0.01 in ink-3), numbers scramble.
B18 8.505  Cursor hovers refund: tooltip "p 0.94 · conf 0.91" lands ON the beat (enters 80 ms early), settled a full beat.
B19 9.006  Chart exits, fill flips paper→ink in 3 frames inside the size morph, ink stat pill "70–500 ms" · end-to-end scrambles in. Bong A3.
B20 9.506  Pill grows downward (top fixed, stat never moves): ✓ "$0.042 / 1M input · output free" row drops in. Stat settled ~0.75 s.
B21 10.006 Exit → 3-frame ink→paper flip → wordmark card: "Jev" scrambles in, price line re-enters as the footer. Warm impact.
B22 10.507 "by TypeSafe" fades up; "System One model" micro label + Choice/Score/Noul chips.
B23 11.007 Footer swaps to "typesafe.ai · early access" (swap 10.88–11.03, settled until 11.54); cursor starts home.
B24 11.507 Content exits, card shrinks, 3-frame paper→ink flip, "Ask Jev ▸" enters; all springs at rest by ~11.95 s → last frame identical to frame 0.

Colour rule: every ink↔paper change = old content exits (≤80 ms) → fill cuts through in 50 ms (3 frames) during the size morph → new content enters. No legible content on a mid-grey fill.
Motion blur: 4/8/16/32 subframes per frame from measured screen motion (step ≤ 2.5 px), equal-weight average (blend.py).
