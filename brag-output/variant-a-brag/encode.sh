#!/bin/sh
# 240 subframes/s -> tmix(4) motion blur -> keep the last of each group of 4 -> 60 fps; mux with the normalised mix
cd "$(dirname "$0")"
FF=/tmp/claude-0/-home-user-hehe/7469c3b1-4606-5a3e-abcc-995cee3c0800/scratchpad/venv/lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2
$FF -v error -y -framerate 240 -i work/frames/f%05d.jpg -i work/mix.wav \
  -filter_complex "[0:v]tmix=frames=4,select='eq(mod(n\,4)\,3)',setpts=N/(60*TB),scale=in_range=full:in_color_matrix=bt601:out_range=tv:out_color_matrix=bt709,format=yuv420p[v]" \
  -map "[v]" -map 1:a -r 60 -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv \
  -c:a aac -b:a 192k -ar 48000 -af apad=whole_dur=12.0 -t 12.0 -movflags +faststart brag.mp4
