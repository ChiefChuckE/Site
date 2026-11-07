#!/usr/bin/env python3
"""Make the MAYDAY opening card and end card for any day.

usage: make_cards.py DAY "SUBTITLE" OUTDIR
  e.g. make_cards.py 8 "THE FOUR SIGNS" /tmp/cards
Writes OUTDIR/open.mp4 (1.5 s) and OUTDIR/end.mp4 (3.4 s), 1080x1920, 30 fps,
silent stereo 48 kHz AAC so they join the body with -c copy.
"""
import subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont

day, sub, out = int(sys.argv[1]), sys.argv[2].upper(), sys.argv[3]
os.makedirs(out, exist_ok=True)
B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
W, H = 1080, 1920
RED, LRED, GREY, WHITE = (200, 16, 46), (255, 45, 61), (190, 190, 190), (255, 255, 255)

def centered(d, text, y, size, fill, maxw=1000):
    while True:
        f = ImageFont.truetype(B, size)
        w = d.textlength(text, font=f)
        if w <= maxw or size < 20:
            break
        size -= 2
    d.text(((W - w) / 2, y), text, font=f, fill=fill)

# opening card
im = Image.new("RGB", (W, H), "black"); d = ImageDraw.Draw(im)
centered(d, "DifferentFireSameFight.com", 245, 58, WHITE)
centered(d, "MAYDAY", 650, 300, RED, maxw=1000)
centered(d, "DAY %02d OF 61" % day, 990, 84, WHITE)
centered(d, sub, 1100, 64, GREY)
im.save(out + "/open.png")

# end card (the 988 lines; "Responders" line sized to fit inside the margins)
im = Image.new("RGB", (W, H), "black"); d = ImageDraw.Draw(im)
centered(d, "STRUGGLING?", 500, 110, WHITE)
centered(d, "CALL OR TEXT 988", 680, 110, LRED)
centered(d, "Veterans: 988, press 1", 940, 66, WHITE)
centered(d, "Responders: Safe Call Now 206-459-3020", 1070, 58, WHITE, maxw=960)
im.save(out + "/end.png")

for name, secs in (("open", 1.5), ("end", 3.4)):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "30", "-t", str(secs),
        "-i", "%s/%s.png" % (out, name), "-f", "lavfi", "-t", str(secs),
        "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "18", "-r", "30",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "128k", "-shortest",
        "-movflags", "+faststart", "%s/%s.mp4" % (out, name)], check=True)
print("cards ready in", out)
