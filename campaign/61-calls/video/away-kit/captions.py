#!/usr/bin/env python3
"""words.json -> drawtext filter chain (big Inter Black captions, lower third).
usage: captions.py words.json out_vf.txt [offset_seconds]
words.json: [{"word": "...", "start": 1.2, "end": 1.5}, ...]  (seconds, relative to the clip)
Groups of up to 3 words; a group also ends at punctuation or a pause over 0.45 s.
The last group of the sign-off ("Call your mayday.") is shown in red.
"""
import json, sys, os
words = json.load(open(sys.argv[1])); outp = sys.argv[2]
off = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "InterBlk.ttf")
def clean(t):
    return t.upper().replace("'", "’").replace(":", "").replace("%", "").replace("\\", "").replace(",", "")
groups, cur = [], []
for i, w in enumerate(words):
    cur.append(w)
    nxt = words[i + 1] if i + 1 < len(words) else None
    end_punct = w["word"].rstrip()[-1:] in ".?!,;"
    pause = nxt is not None and nxt["start"] - w["end"] > 0.45
    if len(cur) >= 3 or end_punct or pause or nxt is None:
        groups.append(cur); cur = []
vf = []
for gi, g in enumerate(groups):
    a = g[0]["start"] - off
    b = (groups[gi + 1][0]["start"] if gi + 1 < len(groups) else g[-1]["end"] + 0.3) - off
    b = min(b, g[-1]["end"] + 0.6 - off)
    text = clean(" ".join(x["word"] for x in g))
    red = "MAYDAY" in text
    vf.append("drawtext=fontfile=%s:text='%s':fontsize=108:fontcolor=%s:shadowcolor=black@0.6:shadowx=0:shadowy=5:"
              "x=(w-text_w)/2:y=1400-text_h/2:enable='between(t\\,%.2f\\,%.2f)'" % (F, text, "0xFF2D3D" if red else "white", a, b))
open(outp, "w").write(",".join(vf))
print(len(groups), "caption groups ->", outp)
