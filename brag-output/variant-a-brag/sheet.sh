#!/bin/bash
# contact sheets (4x3, 480px tiles) of qa stills -> work/sheet-N.jpg
cd "$(dirname "$0")"
FF=/tmp/claude-0/-home-user-hehe/7469c3b1-4606-5a3e-abcc-995cee3c0800/scratchpad/venv/lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2
rm -rf work/sheet_tmp; mkdir -p work/sheet_tmp
i=0; for f in qa/B*.png qa/mid-*.png; do ln -s ../../$f work/sheet_tmp/$(printf %03d $i).png; i=$((i+1)); done
$FF -v error -y -framerate 1 -i work/sheet_tmp/%03d.png -vf "scale=480:480,tile=4x3" -fps_mode passthrough work/sheet-%d.jpg
rm -rf work/sheet_tmp
