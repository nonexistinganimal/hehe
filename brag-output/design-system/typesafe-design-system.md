# TypeSafe AI: design system (for the Jev launch video)

## Confidence legend (read first)

`typesafe.ai` is blocked by this container's network policy, so the live CSS couldn't be extracted. Each rule below is tagged:

- **[verified]**: stated in the design agency's case study (Celerart / Dmytro Masalov, on Behance, Muzli and Webflow Made-In) or in TypeSafe's own copy
- **[inferred]**: follows from the verified rules; exact values are my reconstruction

To lock exact hex values and the body font, add `typesafe.ai` to the environment's allowed domains (or drop in a screenshot) and I'll replace every **[inferred]** value with the site's real CSS. The tokens live in one file (`tokens.css`), so it's a one-file swap.

---

## 1. Brand idea

> "A code-native visual language anchored by Space Mono headings and a warm parchment palette that sidesteps the dark-mode clichés dominating the AI space." **[verified]**

- **Code-native.** It looks like a type signature, a terminal or a spec sheet. Not a sci-fi brain.
- **Warm parchment, not dark mode.** Paper-colored canvas and ink-colored type. It feels like a research lab's notebook, not a neon AI startup.
- **Structure is the aesthetic.** The homepage hero is an isometric machine: *data types flow into a processing engine and come out as structured outputs* **[verified]**. The brand's hero *is* the product's mental model.
- Site title: **"Structured Artificial Intelligence"** **[verified]**. Positioning: *models for automation, not conversation* **[verified]**.

**Anti-references (what TypeSafe deliberately isn't):** black canvas with neon gradients, glowing orbs and "intelligence" blobs, chat bubbles as hero art, purple-to-blue gradients.

## 2. Color

A monochrome warm system: ink on parchment. One signal color at most, and only for *data* (probabilities, the chosen answer). Never on chrome.

| Token | Value | Role | Status |
|---|---|---|---|
| `--ts-parchment` | `#F1ECE2` | Canvas, the page itself | [inferred] |
| `--ts-paper` | `#F8F5EE` | Raised cards / panels | [inferred] |
| `--ts-sunken` | `#E7E0D2` | Code wells, input fields, track of a bar | [inferred] |
| `--ts-rule` | `#D6CCBA` | Hairlines, 1px borders, grid lines | [inferred] |
| `--ts-ink` | `#1B1915` | Primary type, primary fills, the "typed value" | [inferred] |
| `--ts-ink-2` | `#5B554A` | Secondary type, labels | [inferred] |
| `--ts-ink-3` | `#948B7C` | Tertiary / comments / placeholders | [inferred] |
| `--ts-signal` | `var(--ts-ink)` | Reserved for one accent once confirmed from the site CSS; defaults to ink so nothing invented ships | placeholder |

Rules:

- The canvas is always parchment. Dark fills (`ink`) are used as *inverted blocks* (a filled type tag, a primary button, the chosen answer), never as the page background.
- No gradients on UI chrome. No glows. Shadows are allowed only as a hairline plus a soft, low contact shadow (paper on a desk), never as colored halos.
- Contrast: ink on parchment ≈ 15:1; ink-2 ≈ 6.8:1 (AA body); ink-3 only for non-essential text ≥ 20px.

## 3. Typography

| Role | Face | Weight | Notes | Status |
|---|---|---|---|---|
| Display / headings / kicker lines | **Space Mono** | 400 / 700 | Tight tracking (−0.02em) at display sizes, sentence case | [verified face] |
| Code, type tags, values, numbers | **Space Mono** | 400 / 700 | Tabular by nature. Numbers never jitter while counting | [verified face] |
| Small UI labels (buttons, legends) | **Geist** (stand-in) | 500 | Swap in the site's body face once confirmed | [inferred] |

Scale (video, 1440 px square canvas): `display 112 / h1 72 / h2 48 / code 34 / label 24 / micro 18`, line-height 1.05 for display and 1.35 for code.

Type voice: lowercase identifiers (`intent`, `is_urgent`, `jev-latest`), sentence-case prose, no exclamation marks. Numbers carry units in the lighter ink (`256` `ms`).

## 4. Shape & surface

| Token | Value | Status |
|---|---|---|
| `--ts-radius-sm` | 6px (tags, chips) | [inferred] |
| `--ts-radius-md` | 12px (cards, inputs) | [inferred] |
| `--ts-radius-lg` | 20px (hero panels) | [inferred] |
| `--ts-radius-pill` | 999px | [inferred] |
| `--ts-border` | 1px solid `--ts-rule` | [inferred] |
| `--ts-shadow` | `0 1px 0 rgba(27,25,21,.06), 0 12px 32px -12px rgba(27,25,21,.18)` | [inferred] |

- Cards read as **paper**: paper fill, hairline rule, soft contact shadow.
- **Type tags** are the signature component: a small ink-filled chip in Space Mono, e.g. `Choice` `Score` `Noul`. Use them wherever a value has a type.
- Layout grid: 8px base; generous margins; content sits on a visible or implied 12-column grid (spec-sheet feel).

## 5. Illustration: the isometric engine

**[verified]** The homepage centerpiece is a custom **isometric illustration on HTML5 Canvas**: data types flow into a processing engine and come out as structured outputs.

For the video (inferred execution):
- 30° isometric projection, line-drawn in ink on parchment, 1.5–2px strokes, flat tone fills (`paper` / `sunken`) and no gradients.
- Motifs: small typed blocks (`{}` `[]` `0.94` `"refund"`) travelling along isometric conveyors into a cube (the engine) and exiting as neat labelled tiles.
- Use it for **one beat only**, as the "engine" moment when Jev runs. It's the brand's own metaphor, and it earns the frame.

## 6. Motion language

| Pattern | Source | Video rule |
|---|---|---|
| **Text scramble** | GSAP on the site **[verified]** | Every kicker line resolves left→right from a glyph set `{}[]<>/_=:01#`. ~18 ms per char, deterministic (seeded by char index) so it's a pure function of time |
| **Scroll-triggered reveals** | GSAP **[verified]** | In the video these become beat-triggered reveals: offset 12–24px, opacity 0→1, spring settle |
| **Smooth transitions** | GSAP **[verified]** | Critically damped springs with ≤2% overshoot. No bounce, no elastic |
| **Logo comes alive on hover** | Lottie **[verified]** | End card: the wordmark draws in / scrambles in, then holds perfectly still |

Easing tokens (closed-form springs):
- `spring.snap`: ω=28, ζ=0.9 (tags, chips, toggles)
- `spring.move`: ω=18, ζ=0.95 (container morphs, camera)
- `spring.lazy`: ω=11, ζ=1.0 (big layout shifts, end-card settle)

Banned: bounce, elastic, particle bursts, glows, gradient sweeps, lens flares, 3D chrome, anything that looks like a template.

## 7. Sound (to match the look)

Dry, woody and paper-like, never glassy or sci-fi. From the brag library: `interface/click_00x`, `ui/click2` (taps), `interface/drop_00x` (tags landing, pitched into key), `impact/impactSoft_medium_00x` (the drop / reveal), `interface/bong_001` (end card, pitched to A). The track sits in A minor / C major, so pitched SFX get shifted onto A, C or E.

## 8. Components used in the video

1. **State card**: paper card, top label `state` in ink-3, body is the ticket string in Space Mono.
2. **Question row**: `name` · type tag (`Choice` / `Noul` / `Score`) · options in ink-3.
3. **Run button**: ink-filled pill, parchment label `Run ▸`.
4. **Answer row**: `name → value`, with the value in an ink chip and the probability in tabular mono.
5. **Probability bars**: `sunken` track, `ink` fill. The chosen option in full ink, others in ink-3.
6. **Confidence gate toggle**: pill track; knob rides two springs (leading edge ahead of trailing).
7. **Stat block**: huge Space Mono number, unit in ink-2.
8. **Wordmark end card**: `Jev` display with `by TypeSafe` below and `typesafe.ai` micro.
