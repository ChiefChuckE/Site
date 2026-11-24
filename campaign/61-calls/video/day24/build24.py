import subprocess, os, re, json
from PIL import Image, ImageDraw, ImageFont
os.chdir('/tmp/claude-0/d24/w'); os.makedirs('p', exist_ok=True)
def run(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    if r.returncode: print(c[:400]); print(r.stderr[-1800:]); raise SystemExit(1)
    return r.stdout + r.stderr
def dur(f): return float(run(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {f}').strip())
FI = '/tmp/claude-0/fonts/gf/ofl/montserrat/Montserrat-Italic[wght].ttf'
def MB(sz, v='Black Italic'):
    f = ImageFont.truetype(FI, sz); f.set_variation_by_name(v); return f
W_, Y_, RED = (255, 255, 255, 255), (255, 214, 0, 255), (214, 17, 36, 255)
ENC = '-r 30 -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -ac 2'
ST = 'aformat=channel_layouts=stereo'
VO = '/mnt/user-data/uploads/Movies/d24/'
INTRO, SIDE, MUSIC = VO + '138377.mp3', VO + '289678.mp3', VO + '1458322.mp3'
FIT = 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30'
VA = 'highpass=f=90,acompressor=threshold=-24dB:ratio=3:attack=5:release=120,loudnorm=I=-16:TP=-2:LRA=7,aresample=48000,' + ST

def ctext(d, t, y, f, fill, W=1080, o=0):
    x = (W - d.textlength(t, font=f)) / 2
    if o:
        for dx in range(-o, o + 1, 2):
            for dy in range(-o, o + 1, 2): d.text((x + dx, y + dy), t, font=f, fill=(0, 0, 0, 255))
    d.text((x, y), t, font=f, fill=fill)
def cap(name, txt, keys=(), size=70):
    d0 = ImageDraw.Draw(Image.new('RGBA', (10, 10))); f = MB(size); lines = []; cur = []
    for w in txt.split():
        if d0.textlength(' '.join(cur + [w]), font=f) > 980 and cur: lines.append(cur); cur = [w]
        else: cur.append(w)
    lines.append(cur); lh = int(size * 1.18); im = Image.new('RGBA', (1080, lh * len(lines) + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        x = (1080 - d0.textlength(' '.join(l), font=f)) / 2; y = 20 + i * lh
        for w in l:
            for dx, dy in ((-4, 0), (4, 0), (0, -4), (0, 4), (-3, -3), (3, 3), (-3, 3), (3, -3), (0, 6), (5, 6)): d.text((x + dx, y + dy), w, font=f, fill=(0, 0, 0, 255))
            d.text((x, y), w, font=f, fill=Y_ if w.strip('.,?!') in keys else W_); x += d0.textlength(w + ' ', font=f)
    im.save(f'p/{name}.png'); return im.height

# ---------- capsule + bottle art
def capsule(w=420, h=160):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], h // 2, fill=(214, 17, 36, 255))
    d.rounded_rectangle([w // 2, 0, w - 1, h - 1], h // 2, fill=(255, 214, 0, 255)); d.rectangle([w // 2, 0, w // 2 + h // 2, h - 1], fill=(255, 214, 0, 255))
    d.rounded_rectangle([0, 0, w - 1, h - 1], h // 2, outline=(0, 0, 0, 255), width=6); d.line([(w // 2, 3), (w // 2, h - 3)], fill=(0, 0, 0, 255), width=5)
    d.rounded_rectangle([40, 24, w // 2 - 20, 52], 14, fill=(255, 255, 255, 110)); return im
def card(name, lines_top, sub, tag):
    im = Image.new('RGB', (1080, 1920), (245, 248, 252)); d = ImageDraw.Draw(im)
    for y in range(1920):
        c = int(235 - 60 * y / 1920); d.line([(0, y), (1080, y)], fill=(c - 25, c, 255 - int(20 * y / 1920)))
    cp = capsule().rotate(18, expand=True, resample=Image.BICUBIC); im.paste(cp, ((1080 - cp.width) // 2, 470), cp)
    d = ImageDraw.Draw(im)
    f = MB(128); t = lines_top; x = (1080 - d.textlength(t, font=f)) / 2
    d.text((x + 5, 835), t, font=f, fill=(0, 30, 80)); d.text((x, 830), t, font=f, fill=(255, 255, 255))
    d.text((x + d.textlength(t, font=f) + 6, 830), "™", font=MB(48), fill=(255, 255, 255))
    ctext(d, sub, 990, MB(44, 'Bold Italic'), (10, 40, 100))
    y = 1110
    for ln in tag:
        ctext(d, ln, y, MB(54), (255, 255, 255), o=4); y += 74
    im.save(f'p/{name}.png')
card('card1', "LEADERSHIP", "(accountability, extended-release)", ["THE CURE NOBODY", "IS PRESCRIBING."])
card('card2', "LEADERSHIP", "(accountability, extended-release)", ["ASK YOUR CHIEF IF IT'S RIGHT", "FOR YOUR DEPARTMENT."])

# ---------- overlay (always on)
ov = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
d.rounded_rectangle([40, 150, 430, 236], 16, fill=RED)
for dx, dy in ((-3, 0), (3, 0), (0, -3), (0, 3), (4, 6)): d.text((62 + dx, 150 + dy), "MAYDAY", font=MB(66), fill=(0, 0, 0, 255))
d.text((62, 150), "MAYDAY", font=MB(66), fill=W_)
for dx, dy in ((-3, 0), (3, 0), (0, -3), (0, 3), (4, 6)): d.text((60 + dx, 244 + dy), "DAY 24 OF 61", font=MB(44), fill=(0, 0, 0, 255))
d.text((60, 244), "DAY 24 OF 61", font=MB(44), fill=Y_)
d.rounded_rectangle([40, 1560, 1040, 1606], 12, fill=(0, 0, 0, 150)); ctext(d, "LEADERSHIP is not a real drug. PTSD is a real injury.", 1568, MB(27, 'Bold Italic'), W_)
d.rectangle([0, 1630, 1080, 1716], fill=RED); ctext(d, "STRUGGLING? CALL OR TEXT 988", 1640, MB(56), W_, o=4)
d.rectangle([0, 1716, 1080, 1800], fill=(0, 0, 0, 215))
ctext(d, "VETERANS: 988, PRESS 1", 1722, MB(30), Y_); ctext(d, "RESPONDERS: SAFE CALL NOW 206-459-3020", 1758, MB(30), Y_)
ov.save('p/ov.png')

# ---------- segments
def vid(name, src, ss, t, extra='', speed=1.0, audio=True):
    sp = f',setpts={1/speed:.4f}*PTS' if speed != 1.0 else ''
    if audio:
        run(f'ffmpeg -v error -y -ss {ss} -t {t} -i {src} -vf "{FIT}{extra}" -af "{VA}" {ENC} p/{name}.mp4')
    else:
        run(f'ffmpeg -v error -y -ss {ss} -t {t} -i {src} -f lavfi -i anullsrc=r=48000:cl=stereo -vf "{FIT}{sp}{extra}" -map 0:v -map 1:a -shortest {ENC} p/{name}.mp4')
    return dur(f'p/{name}.mp4')
def still(name, png, t):
    run(f'ffmpeg -v error -y -loop 1 -framerate 30 -t {t} -i p/{png}.png -f lavfi -t {t} -i anullsrc=r=48000:cl=stereo -vf "zoompan=z=\'1+0.0006*on\':d=1:x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':s=1080x1920:fps=30,fade=t=in:d=0.25" -t {t} {ENC} p/{name}.mp4')
    return dur(f'p/{name}.mp4')
BW = ',hue=s=0,eq=contrast=1.15:brightness=-0.04'
side_d = dur(SIDE); TEMPO = 1.12; side_len = side_d / TEMPO
segs = []
segs.append(('s1a', vid('s1a', 'u13681.mov', 1.5, 4.2, BW, audio=False)))
segs.append(('s1b', vid('s1b', 'a13693.mov', 12.4, 3.9, BW, audio=False)))
segs.append(('s2', vid('s2', 'a13699.mov', 0.25, 12.7)))
segs.append(('s3', still('s3', 'card1', 2.6)))
segs.append(('s4', vid('s4', 'a13697.mov', 1.0, 2.75)))
q = (side_len + 0.6) / 4
segs.append(('s5a', vid('s5a', 'u13691.mov', 8.6, q / 2 + 0.02, speed=0.5, audio=False)))
segs.append(('s5b', vid('s5b', 'u13691.mov', 23.0, q, audio=False)))
segs.append(('s5c', vid('s5c', 'a13689.mov', 5.0, q, audio=False)))
segs.append(('s5d', vid('s5d', 'a13689.mov', 12.6, q, audio=False)))
segs.append(('s6a', vid('s6a', 'u13695.mov', 1.2, 8.75)))
segs.append(('s6b', vid('s6b', 'u13695.mov', 11.35, 6.35)))
segs.append(('s7', still('s7', 'card2', 3.6)))
off = {}; t = 0
for n, dd in segs: off[n] = t; t += dd
TOTAL = t; print({k: round(v, 2) for k, v in off.items()}, 'TOTAL', round(TOTAL, 2))
open('p/all.txt', 'w').write(''.join(f"file '{n}.mp4'\n" for n, _ in segs))
run(f'ffmpeg -v error -y -f concat -safe 0 -i p/all.txt {ENC} p/base.mp4')

# ---------- captions
caps = []
def add(txt, a, b, keys=(), size=70): caps.append((txt, a, b, keys, size))
# intro VO: split by characters over its duration
intro_d = dur(INTRO); i0 = off['s1a'] + 0.25
parts = [("IS YOUR DEPARTMENT SUFFERING FROM UNTREATED PTSD?", ("PTSD",)), ("SHORT TEMPERS. EMPTY BUNKS.", ()), ("GOOD PEOPLE LEAVING EARLY.", ("LEAVING",))]
tot = sum(len(p[0]) for p in parts); a = i0
for txt, k in parts:
    b = a + (intro_d - 0.3) * len(txt) / tot; add(txt, a, b - 0.05, k); a = b
o = off['s2'] - 0.25
add("I'M CHIEF CHUCK.", o + 0.45, o + 2.5); add("FOR YEARS I LOOKED FOR A CURE FOR PTSD.", o + 3.0, o + 5.3, ("CURE", "PTSD"))
add("TURNS OUT IT COMES IN A CAPSULE.", o + 5.7, o + 9.85, ("CAPSULE",)); add("IT'S CALLED LEADERSHIP.", o + 10.5, o + 12.9, ("LEADERSHIP",))
o = off['s4'] - 1.0
add("ONE CAPSULE. TAKEN DAILY. BY THE PEOPLE IN CHARGE.", o + 1.15, o + 3.7, ("CHARGE",))
s0 = off['s5a'] + 0.3
sp = ["SIDE EFFECTS MAY INCLUDE:", "CREWS WHO TALK TO EACH OTHER,", "CHIEFS WHO ASK \"HOW ARE YOU, REALLY?\"", "FEWER SICK DAYS,", "SUDDEN OUTBREAKS OF TRUST,", "AND PEOPLE ACTUALLY RETIRING HAPPY.", "DO NOT TAKE LEADERSHIP IF YOU ARE ALLERGIC TO ACCOUNTABILITY.", "LEADERSHIP IS NOT A REAL DRUG.", "PTSD IS A REAL INJURY."]
wts = [30, 30, 36, 17, 26, 36, 60, 30, 22]; a = s0
for txt, w in zip(sp, wts):
    b = a + side_len * w / sum(wts); add(txt, a, b - 0.04, ("TRUST", "HAPPY", "ACCOUNTABILITY", "REAL", "INJURY"), 58); a = b
o = off['s6a'] - 1.2
add("THERE'S NO PILL THAT PREVENTS PTSD, BUT LEADERSHIP DOES.", o + 1.4, o + 4.7, ("LEADERSHIP",)); add("CHIEFS, IT'S TIME TO CHECK ON YOUR PEOPLE", o + 5.05, o + 7.3, ("CHECK",)); add("BEFORE THE BAD CALL, NOT AFTER.", o + 7.6, o + 9.85, ("BEFORE",))
o = off['s6b'] - 11.35
add("LEADERSHIP.", o + 11.5, o + 13.2, ("LEADERSHIP",)); add("ASK YOUR CHIEF IF IT'S RIGHT FOR YOUR DEPARTMENT.", o + 13.25, o + 17.6, ("CHIEF",))
ins = '-i p/base.mp4 -loop 1 -framerate 30 -i p/ov.png '; fc = '[0:v][1:v]overlay=0:0:shortest=1[o0];'; last = 'o0'
for k, (txt, a, b, keys, size) in enumerate(caps):
    h = cap(f'c{k}', txt, keys, size); ins += f'-loop 1 -framerate 30 -i p/c{k}.png '
    fc += f"[{last}][{2+k}:v]overlay=0:{1540-h}:enable='between(t,{a:.2f},{b:.2f})'[o{k+1}];"; last = f'o{k+1}'
n = 2 + len(caps)
ins += f'-i {INTRO} -i {SIDE} -i {MUSIC} '
di, ds = int(i0 * 1000), int(s0 * 1000)
fc += (f"[{n}:a]aresample=48000,volume=1.5,{ST},adelay={di}|{di}[vi];[{n+1}:a]aresample=48000,atempo={TEMPO},volume=1.5,{ST},adelay={ds}|{ds}[vs];"
       f"[0:a][vi][vs]amix=inputs=3:duration=first:normalize=0,asplit[vx][sc];"
       f"[{n+2}:a]aresample=48000,{ST},volume=-11dB,afade=t=in:d=0.6,atrim=0:{TOTAL:.2f},afade=t=out:st={TOTAL-1.6:.2f}:d=1.6[mu];[mu][sc]sidechaincompress=threshold=0.04:ratio=3:attack=20:release=500[md];"
       f"[vx][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=11[a]")
open('p/fc.txt', 'w').write(fc)
run(f'ffmpeg -v error -y {ins}-filter_complex_script p/fc.txt -map "[{last}]" -map "[a]" -t {TOTAL:.2f} -r 30 -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 MAYDAY-Day-24-v1.mp4')
json.dump({'off': off, 'total': TOTAL, 'caps': [(c[0], round(c[1], 2), round(c[2], 2)) for c in caps]}, open('p/meta.json', 'w'), indent=1)
print(run('ffprobe -v error -show_entries format=duration,size -of csv=p=0 MAYDAY-Day-24-v1.mp4'))
