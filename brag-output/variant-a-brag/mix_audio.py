"""Audio mix for the Jev launch video (Variant A).
Music slice 12.013-24.009 s + SFX cue sheet from brag-plan.md. Each SFX is pitch-shifted with
asetrate+aresample, its transient peak is measured after the shift, and it is placed so the peak
lands on the beat. The mix is loudness-normalised (two-pass loudnorm) to about -14 LUFS, TP -1 dBTP.
Output: work/mix.wav
"""
import json, subprocess, os, random
import numpy as np, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
FF = "/tmp/claude-0/-home-user-hehe/7469c3b1-4606-5a3e-abcc-995cee3c0800/scratchpad/venv/lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
ASSETS = "/home/user/hehe/.claude/skills/brag/assets"
MUSIC = f"{ASSETS}/music/happy-beats-business-moves-vol-1-by-ende-dot-app.mp3"
SFX = f"{ASSETS}/sfx"
WORK = os.path.join(HERE, "work")
SR = 48000
DUR = 11.996
SONG_START = 12.013
grid = json.load(open("/home/user/hehe/brag-output/work/beat-grid.json"))
BEATS = grid["beats"]
B = lambda n: BEATS[n - 1]          # beat n (1-based) in video seconds
S16 = grid["beatPeriod"] / 4

def decode(path, filt=None, start=None, dur=None):
    cmd = [FF, "-v", "error"]
    cmd += ["-i", path]
    if start is not None: cmd += ["-ss", f"{start:.4f}"]
    if dur is not None: cmd += ["-t", f"{dur:.4f}"]
    af = f"aresample={SR}" + (f",{filt}" if filt else "")
    cmd += ["-af", af, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()

def pitched(path, semis):
    if not semis: return decode(path)
    r = 2 ** (semis / 12)
    return decode(path, f"asetrate={SR * r:.3f},aresample={SR}")

# ---- cue sheet (video time of the transient peak, file, semitones, gain) ----
rng = random.Random(7)
keys = [f"keyboard/keypress-{i:03d}.wav" for i in range(1, 33)]
CUES = []
for k in range(8):                                   # streaming text ticks on 16ths, 0.000-0.875
    CUES.append((k * S16, rng.choice(keys), 0, 0.30))
CUES += [
    (1.000,          "interface/glitch_002.ogg", 0, 0.35),       # parse error
    (B(5),           "interface/click_003.ogg", 0, 0.55),        # click on the bubble
    (B(5) + S16*2,   "interface/drop_002.ogg", -0.81, 0.40),     # state card lands (2.25)
    (B(6),           "interface/drop_001.ogg", -2.39, 0.38),     # question rows
    (B(7),           "interface/drop_001.ogg", -2.39, 0.40),
    (B(8),           "interface/drop_001.ogg", -2.39, 0.42),
    (B(8) + S16*2,   "ui/rollover2.ogg", 0, 0.22),               # hover Run (3.75)
    (B(9),           "interface/click_003.ogg", 0, 0.42),        # Run on the drop
    (B(9),           "impact/impactSoft_medium_001.ogg", 0, 0.58),
    (B(10) + S16,    rng.choice(keys), 0, 0.45),                 # answers fill in (rows land on 32nds after the unfold)
    (B(10) + 1.5*S16, rng.choice(keys), 0, 0.45),
    (B(10) + 2*S16,  rng.choice(keys), 0, 0.45),
    (B(11),          "ui/rollover2.ogg", 0, 0.20),               # tooltip hover
    (B(13),          "interface/drop_002.ogg", -0.81, 0.35),     # code card
    (B(15),          "interface/switch_007.ogg", 1.44, 0.50, 60),  # toggle: 2nd click (raw 109.2 ms) lands on the beat
    (B(16),          "interface/drop_001.ogg", -2.39, 0.38),     # toast
    (B(17),          "impact/impactSoft_medium_004.ogg", 0, 0.45),  # stat block
    (B(18),          "interface/drop_002.ogg", -0.81, 0.32),     # price row
    (B(19),          "impact/impactGlass_light_001.ogg", -1.38, 0.28),  # "free" stamp
    (B(21),          "impact/impactSoft_medium_001.ogg", 0, 0.55),  # wordmark lands
    (B(21),          "interface/bong_001.ogg", -1.0, 0.45),
]

N = int(round(DUR * SR))
music = decode(MUSIC, start=SONG_START, dur=DUR)[:N]
if len(music) < N: music = np.pad(music, ((0, N - len(music)), (0, 0)))
t = np.arange(N) / SR
env = np.clip(t / 0.005, 0, 1) * np.clip((DUR - t) / 0.4, 0, 1)   # 5 ms in, 0.4 s out
MUSIC_GAIN = 1.0   # plan said 0.35; at 0.35 the SFX peaks sat ~9 dB above the bed, so the bed is raised instead
mix = music * MUSIC_GAIN * env[:, None]
sfx_bus = np.zeros_like(mix)

report = []
cache = {}
for cue in CUES:
    tp, f, semis, g = cue[:4]; after_ms = cue[4] if len(cue) > 4 else 0
    key = (f, semis)
    if key not in cache: cache[key] = pitched(f"{SFX}/{f}", semis)
    x = cache[key]
    a = np.abs(x).max(axis=1); off = int(after_ms * SR / 1000)
    peak = off + int(np.argmax(a[off:]))
    start = int(round(tp * SR)) - peak
    a0, b0 = max(0, start), min(N, start + len(x))
    if b0 > a0: sfx_bus[a0:b0] += x[a0 - start:b0 - start] * g
    report.append(f"{tp:7.3f}s  {f:40s} {semis:+5.2f}st  gain {g:.2f}  peak@{peak / SR * 1000:6.1f}ms  start {start / SR:7.4f}s")

mix = mix + sfx_bus
pre = os.path.join(WORK, "premix.wav"); sf.write(pre, mix.astype(np.float32), SR, subtype="FLOAT")

# gentle peak limiter first (a few isolated SFX/music peaks), so loudnorm can stay linear (no pumping)
lim = os.path.join(WORK, "premix_lim.wav")
subprocess.run([FF, "-v", "error", "-y", "-i", pre, "-af", "volume=1.2dB,alimiter=limit=0.83:attack=4:release=80:level=disabled:asc=1",
                "-c:a", "pcm_f32le", lim], check=True)
pre = lim
# two-pass loudnorm to -14 LUFS / -1 dBTP
p1 = subprocess.run([FF, "-hide_banner", "-i", pre, "-af", "loudnorm=I=-14:TP=-1.0:LRA=11:print_format=json", "-f", "null", "-"],
                    capture_output=True, text=True).stderr
m = json.loads(p1[p1.rindex("{"):p1.rindex("}") + 1])
af = (f"loudnorm=I=-14:TP=-1.0:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
      f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample={SR}")
out = os.path.join(WORK, "mix.wav")
r2 = subprocess.run([FF, "-hide_banner", "-y", "-i", pre, "-af", af.replace("linear=true", "linear=true:print_format=json"), "-ar", str(SR), "-c:a", "pcm_s24le", "-t", f"{DUR}", out], check=True, capture_output=True, text=True).stderr
print("normalization:", json.loads(r2[r2.rindex("{"):r2.rindex("}") + 1])["normalization_type"])
p2 = subprocess.run([FF, "-hide_banner", "-i", out, "-af", "loudnorm=I=-14:TP=-1.0:print_format=json", "-f", "null", "-"],
                    capture_output=True, text=True).stderr
m2 = json.loads(p2[p2.rindex("{"):p2.rindex("}") + 1])
y, _ = sf.read(out)
print("\n".join(report))
print(f"premix: I={m['input_i']} LUFS TP={m['input_tp']}  ->  final: I={m2['input_i']} LUFS TP={m2['input_tp']} dBTP, "
      f"sample peak {20*np.log10(np.abs(y).max()):.2f} dBFS, {len(y)/SR:.3f}s")
# SFX vs music level check (RMS in dB over the whole piece, where each is active)
def rms_db(a): a = a[np.abs(a).max(axis=1) > 1e-4]; return 20*np.log10(np.sqrt((a**2).mean()) + 1e-12)
print(f"music bus RMS {rms_db(music*MUSIC_GAIN):.1f} dB, sfx bus RMS (active) {rms_db(sfx_bus):.1f} dB, sfx peak {20*np.log10(np.abs(sfx_bus).max()):.1f} dB, music peak {20*np.log10(np.abs(music*MUSIC_GAIN).max()):.1f} dB")
