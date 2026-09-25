"""Audio mix for jev-morph: music slice (song 16.013 -> 28.021 s) + SFX placed by measured peak.
Writes work/mix_raw.wav and loudness-normalised work/mix.wav (-14 LUFS, TP -1.5), 48 kHz stereo, 12.008 s."""
import json, re, subprocess
from pathlib import Path
import numpy as np, soundfile as sf
from scipy.signal import resample

HERE = Path(__file__).parent
WORK = HERE / 'work'; WORK.mkdir(exist_ok=True)
FF = '/tmp/claude-0/-home-user-hehe/7469c3b1-4606-5a3e-abcc-995cee3c0800/scratchpad/venv/lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2'
ASSETS = Path('/home/user/hehe/.claude/skills/brag/assets')
SR = 48000
T = 12.008
SONG_START = 16.013
BP = 0.50033
b = [0] + [(n - 1) * BP for n in range(1, 25)]
K1, K2, K3 = b[6], b[6] + BP / 4, b[6] + BP / 2
COLL = b[8] + 0.06
N = int(round(T * SR))
SFX_BUS = 0.5   # -6 dB: SFX sit under the music


def decode(path):
    raw = subprocess.run([FF, '-loglevel', 'error', '-i', str(path), '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


# ---- music: sample-accurate slice of the full decode
music = decode(ASSETS / 'music/happy-beats-business-moves-vol-1-by-ende-dot-app.mp3')
s0 = int(round(SONG_START * SR))
mus = music[s0:s0 + N].copy()
fade = int(0.005 * SR)
ramp = np.linspace(0, 1, fade)[:, None]
mus[:fade] *= ramp; mus[-fade:] *= ramp[::-1]
mix = mus * 0.38

# ---- sfx: (event time s, file, semitones, gain)
EV = [
    (b[2], 'ui/click2.ogg', 0, .55),                 # press "Ask Jev"
    (0.58, 'interface/click_003.ogg', 0, .22),       # release -> contract
    (b[3], 'interface/drop_002.ogg', -0.81, .38),    # check lands (A5)
    (b[4], 'interface/drop_001.ogg', -2.39, .32),    # island (E6)
    (b[5], 'interface/select_008.ogg', 0, .32),      # palette opens
    (K1, 'keyboard/keypress-003.wav', 0, .42), (K2, 'keyboard/keypress-007.wav', 0, .38), (K3, 'keyboard/keypress-011.wav', 0, .40),
    (b[7], 'ui/rollover2.ogg', 0, .32),              # hover confirm
    (b[8], 'keyboard/keypress-020.wav', 0, .5),      # Enter
    (COLL, 'interface/drop_001.ogg', -2.39, .22),    # palette collapses
    (b[9], 'ui/mouseclick1.ogg', 0, .42),            # click toggle
    (b[9], 'interface/switch_007.ogg', 1.44, .36),   # toggle ON (E6)
    (b[10], 'interface/drop_001.ogg', -2.39, .28),   # knob -> indicator
    (b[11], 'ui/click2.ogg', 0, .5),                 # click Score
    (b[12], 'interface/drop_002.ogg', -0.81, .34),   # slider opens
    (b[13], 'ui/mouseclick1.ogg', 0, .45),           # grab knob
    (b[14], 'interface/click_003.ogg', 0, .26),      # past max, rubber band
    (b[15], 'interface/click_003.ogg', 0, .32),      # release
    (b[15] + 0.02, 'interface/drop_002.ogg', -0.81, .22),
    (b[16], 'ui/click2.ogg', 0, .5),                 # click Choice
    (b[17], 'interface/drop_002.ogg', -0.81, .32),   # chart opens
    *[(b[17] + 0.07 + i * 0.05 + 0.06, 'interface/click_003.ogg', 0, .14 - .02 * i) for i in range(4)],  # bars land
    (b[18], 'ui/rollover2.ogg', 0, .32),             # tooltip
    (b[19], 'interface/bong_001.ogg', -1, .42),      # stat pill (A3)
    (b[20], 'interface/select_008.ogg', 0, .34),     # toast
    (b[21], 'impact/impactSoft_medium_001.ogg', 0, .7),  # wordmark, warm hit
    (b[22], 'interface/drop_002.ogg', -0.81, .2),    # by TypeSafe
    (b[23], 'interface/select_008.ogg', 0, .24),     # typesafe.ai
    (b[24], 'interface/drop_001.ogg', -2.39, .3),    # back to the button
]

placed = []
for t, f, st, g in EV:
    x = decode(ASSETS / 'sfx' / f)
    peak = int(np.argmax(np.abs(x).max(axis=1)))
    if st:
        ratio = 2 ** (st / 12)          # == asetrate*ratio + aresample: pitch and speed move together
        x = resample(x, int(round(len(x) / ratio)), axis=0).astype(np.float32)
        peak = int(round(peak / ratio))
    x = x / max(1e-6, np.abs(x).max()) * g * SFX_BUS   # normalise each sfx peak, then gain, then sfx bus
    start = int(round(t * SR)) - peak
    idx = (np.arange(len(x)) + start) % N   # wrap tails over the loop point so the loop is seamless
    np.add.at(mix, idx, x)
    placed.append({'t': round(t, 4), 'file': f, 'semitones': st, 'gain': g, 'peak_ms': round(peak / SR * 1000, 1), 'start': round(start / SR, 4)})

sf.write(WORK / 'mix_raw.wav', mix, SR, subtype='FLOAT')
(WORK / 'sfx_placement.json').write_text(json.dumps(placed, indent=1))
print('raw peak', float(np.abs(mix).max()))

# ---- loudness: gain + look-ahead limiter (latency-compensated, keeps length and sync), iterated to -14 LUFS
def lufs(path):
    e = subprocess.run([FF, '-hide_banner', '-i', str(path), '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', e)[-1]); P = float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', e)[-1])
    return I, P

# pad with the loop's own wrap so the limiter sees continuous audio at both edges, then trim back exactly
pad = int(0.5 * SR)
padded = np.concatenate([mix[-pad:], mix, mix[:pad]])
sf.write(WORK / 'mix_pad.wav', padded, SR, subtype='FLOAT')
I0, _ = lufs(WORK / 'mix_raw.wav')
gain = -14.0 - I0
for it in range(4):
    af = (f"volume={gain:.3f}dB,alimiter=limit=0.84:attack=4:release=60:level=false:latency=1,"
          f"atrim=start_sample={pad}:end_sample={pad + N},asetpts=N/SR/TB")
    subprocess.run([FF, '-y', '-hide_banner', '-loglevel', 'error', '-i', str(WORK / 'mix_pad.wav'), '-af', af, '-ar', str(SR), '-c:a', 'pcm_s16le', str(WORK / 'mix.wav')], check=True)
    I, P = lufs(WORK / 'mix.wav')
    print(f'iter {it}: gain {gain:+.2f} dB -> {I} LUFS, true peak {P} dBFS')
    if abs(I + 14) < 0.15: break
    gain += -14.0 - I
y, _ = sf.read(WORK / 'mix.wav')
print('samples', len(y), 'expected', N, 'duration', len(y) / SR)
