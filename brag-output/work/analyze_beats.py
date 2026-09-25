"""Measure the beat grid of the brag music bed and write the 12 s cut's grid.

Usage: python analyze_beats.py <track.mp3|wav> > beat-grid.json
Needs numpy + librosa (+ an ffmpeg for mp3). Downbeats are taken from low-band
(30-160 Hz) kick onsets; the drop is the first bar whose kick energy doubles.
"""
import json, sys
import numpy as np, librosa

y, sr = librosa.load(sys.argv[1], sr=22050)
hop = 64
S = np.abs(librosa.stft(y, n_fft=1024, hop_length=hop))
f = librosa.fft_frequencies(sr=sr, n_fft=1024)
kick = S[(f > 30) & (f < 160)].sum(0)
t = librosa.frames_to_time(np.arange(len(kick)), sr=sr, hop_length=hop)
d = np.diff(kick, prepend=kick[0])
pk = librosa.util.peak_pick(d, pre_max=40, post_max=40, pre_avg=40, post_avg=40,
                            delta=d.max() * 0.1, wait=60)
kicks = t[pk]

START, BEATS = 12.013, 24          # measured downbeat; 24 beats = 6 bars ~= 12 s
END = kicks[np.argmin(abs(kicks - (START + 12.0)))]  # kick nearest 12 s later
period = (END - START) / BEATS
grid = [round(i * period, 3) for i in range(BEATS)]
print(json.dumps({
    "track": "happy-beats-business-moves-vol-1-by-ende-dot-app.mp3",
    "songStart": START, "songEnd": round(float(END), 3),
    "bpm": round(60 / period, 2), "beatPeriod": round(period, 5),
    "videoDuration": round(float(END - START), 3),
    "dropAtVideoTime": grid[8], "downbeats": grid[::4],
    "beats": grid, "key": "A minor / C major (chroma estimate)",
}, indent=2))
