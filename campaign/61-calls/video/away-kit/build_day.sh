#!/usr/bin/env bash
# Away-mode build: phone clip in, finished MAYDAY video out.
# usage: build_day.sh RAW.mp4 DAY "SUBTITLE" OUTDIR [captions_vf.txt]
# Steps: crop/scale to 1080x1920 -> wind cleanup (150 Hz double high-pass, gate, compress)
#        -> two-pass loudnorm -15.5 LUFS -> optional captions -> opening + end cards
#        -> phone encode (about 12-25 MB). Output: OUTDIR/MAYDAY-Day-NN-final.mp4
set -euo pipefail
RAW="$1"; DAY="$2"; SUB="$3"; OUT="$4"; VF="${5:-}"
# MODE=cards (simplest): leave the video and its sound exactly as recorded; just add the cards.
# MUSIC=/path/song.mp3 : optional exit music under the end card (fades out).
MODE="${MODE:-full}"; MUSIC="${MUSIC:-}"
KIT="$(cd "$(dirname "$0")" && pwd)"; N=$(printf "%02d" "$DAY"); mkdir -p "$OUT"
python3 -I "$KIT/make_cards.py" "$DAY" "$SUB" "$OUT"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$RAW")
AF0="aformat=channel_layouts=stereo:sample_rates=48000,highpass=f=150,highpass=f=150,agate=threshold=0.02:ratio=2:attack=5:release=150:range=0.3,acompressor=threshold=0.04:ratio=3.5:attack=8:release=200:makeup=1"
# pass 1: measure
M=$(ffmpeg -hide_banner -nostats -i "$RAW" -af "$AF0,loudnorm=I=-15.5:TP=-1.5:LRA=9:print_format=json" -vn -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$M" | python3 -c "import sys,json;print(json.load(sys.stdin)['$1'])"; }
AF="$AF0,loudnorm=I=-15.5:TP=-1.5:LRA=9:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aformat=channel_layouts=stereo:sample_rates=48000,apad"
VFC="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p"
[ -n "$VF" ] && VFC="$VFC,$(cat "$VF")"
[ "$MODE" = cards ] && AF="aformat=channel_layouts=stereo:sample_rates=48000,apad"
ffmpeg -v error -y -i "$RAW" -vf "$VFC" -af "$AF" -t "$DUR" -c:v libx264 -profile:v high -crf 18 -r 30 -c:a aac -ar 48000 -ac 2 -b:a 128k -movflags +faststart "$OUT/body.mp4"
printf "file '%s'\nfile '%s'\nfile '%s'\n" "$OUT/open.mp4" "$OUT/body.mp4" "$OUT/end.mp4" > "$OUT/list.txt"
ffmpeg -v error -y -f concat -safe 0 -i "$OUT/list.txt" -c copy "$OUT/joined.mp4"
ENDMIX="alimiter=limit=0.84"
MIN=()
if [ -n "$MUSIC" ]; then T=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/joined.mp4"); S=$(python3 -c "print(max(0,$T-3.4))")
  MIN=(-i "$MUSIC"); ENDMIX="[0:a][1:a]amix=inputs=2:duration=first:normalize=0[x]" ; fi
if [ -n "$MUSIC" ]; then FC=(-filter_complex "[1:a]atrim=0:3.4,volume=0.5,afade=t=in:d=0.3,afade=t=out:st=2.4:d=1.0,adelay=$(python3 -c "print(int($S*1000))")|$(python3 -c "print(int($S*1000))"),apad[m];[0:a][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.84[a]" -map 0:v -map "[a]"); else FC=(-af "$ENDMIX"); fi
ffmpeg -v error -y -i "$OUT/joined.mp4" "${MIN[@]}" "${FC[@]}" -c:v libx264 -profile:v high -level 4.0 -crf 24 -maxrate 6M -bufsize 12M -c:a aac -b:a 128k -movflags +faststart "$OUT/MAYDAY-Day-$N-final.mp4"
ls -la "$OUT/MAYDAY-Day-$N-final.mp4"
ffmpeg -hide_banner -nostats -i "$OUT/MAYDAY-Day-$N-final.mp4" -af ebur128=peak=true -vn -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tail -2
