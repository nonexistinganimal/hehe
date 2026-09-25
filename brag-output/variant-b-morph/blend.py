"""Equal-weight average of a variable number of subframes per output frame (adaptive motion blur).
Reads work/frames/s%06d.jpg in order + work/subframes.json ([N per frame]); pipes 60 fps frames into x264."""
import json, subprocess, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).parent
FF = '/tmp/claude-0/-home-user-hehe/7469c3b1-4606-5a3e-abcc-995cee3c0800/scratchpad/venv/lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2'
W = H = 1440; FS = W * H * 3
counts = json.loads((HERE / 'work/subframes.json').read_text())
dec = subprocess.Popen([FF, '-loglevel', 'error', '-framerate', '240', '-i', str(HERE / 'work/frames/s%06d.jpg'), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, bufsize=FS * 4)
enc = subprocess.Popen([FF, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-framerate', '60', '-i', '-',
                        '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-threads', '2', '-r', '60', str(HERE / 'work/video.mp4')], stdin=subprocess.PIPE)
acc = np.zeros(FS, np.float32)
for f, n in enumerate(counts):
    acc[:] = 0
    for _ in range(n):
        buf = dec.stdout.read(FS)
        if len(buf) != FS: sys.exit(f'short read at frame {f}')
        acc += np.frombuffer(buf, np.uint8)
    enc.stdin.write(np.clip(acc / n + 0.5, 0, 255).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait(); dec.wait()
print('blended', len(counts), 'frames from', sum(counts), 'subframes')
