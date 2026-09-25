"""Adaptive motion blur: equal-weight average of S[n] subframes per output frame (plan from `render.mjs plan`),
then encode 60 fps H.264 + the normalised mix. Frame 0 is the poster (S=1)."""
import json, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
FF = "/tmp/claude-0/-home-user-hehe/7469c3b1-4606-5a3e-abcc-995cee3c0800/scratchpad/venv/lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
W = H = 1440; FS = W * H * 3
plan = json.load(open(os.path.join(HERE, "work/plan.json")))["S"]
dec = subprocess.Popen([FF, "-v", "error", "-framerate", "1", "-i", os.path.join(HERE, "work/sub/g%06d.jpg"),
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-framerate", "60", "-i", "-",
    "-i", os.path.join(HERE, "work/mix.wav"),
    "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
    "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-af", "apad=whole_dur=12.0", "-t", "12.0",
    "-movflags", "+faststart", os.path.join(HERE, "brag.mp4")], stdin=subprocess.PIPE)
acc = np.zeros((H, W, 3), np.float32)
for n, s in enumerate(plan):
    acc[:] = 0
    for _ in range(s):
        buf = dec.stdout.read(FS)
        if len(buf) != FS: sys.exit(f"short read at frame {n}")
        acc += np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    enc.stdin.write(np.clip(np.rint(acc / s), 0, 255).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait(); dec.wait()
print("frames", len(plan), "subframes", sum(plan))
