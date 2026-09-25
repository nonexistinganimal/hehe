#!/bin/sh
# one still per beat (B1..B24, sampled 0.42 s after each beat so the beat's action has landed) + mid-transition stills
cd "$(dirname "$0")"
ARGS=""
for n in $(seq 1 24); do t=$(python3 -c "print(round(($n-1)*0.49985+0.42,3))"); ARGS="$ARGS $t:B$(printf %02d $n)"; done
ARGS="$ARGS 2.06:mid-B05 4.06:mid-B09 4.46:mid-B10 6.05:mid-B13 8.05:mid-B17 10.04:mid-B21 1.02:mid-B03 6.62:mid-B14drag 7.03:mid-B15"
node render.mjs stills qa $ARGS
