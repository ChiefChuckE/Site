import subprocess, os, json, random, sys
from PIL import Image, ImageDraw, ImageFont
def run(c): subprocess.run(c, shell=True, check=True)
os.chdir('/tmp/claude-0/d21'); os.makedirs('w', exist_ok=True)
SD = '/tmp/claude-0/d20g/'
FI = '/tmp/claude-0/fonts/gf/ofl/montserrat/Montserrat-Italic[wght].ttf'
def MB(sz, var='Black Italic'):
    f = ImageFont.truetype(FI, sz); f.set_variation_by_name(var); return f
FLIP = {'A', 'B', 'C', 'E', 'G', 'L'}
def off(c):
    o = subprocess.check_output(f'ffprobe -v error -select_streams a:0 -show_entries stream=start_time -of csv=p=0 {c}.mov', shell=True).decode().strip()
    return float(o or 0)
OFF = {c: off(c) for c in 'ABCDEFGHIJKLM'}
# normalized audio masters
for c, extra in (('A', ''), ('B', ''), ('E', 'afftdn=nf=-28,'), ('G', ''), ('L', '')):
    if not os.path.exists(f'w/n{c}.wav'):
        run(f'ffmpeg -v error -y -i {c}.mov -map 0:a:0 -ac 2 -ar 48000 -af "highpass=f=100,{extra}loudnorm=I=-17:TP=-2:LRA=9" w/n{c}.wav')
Y = (255, 214, 0, 255)
# seg: v clip, vs (wav-time of same clip unless vraw), a clip, as, dur, zoom, grade, caps[(text,t0,t1,size,keys)]
S = []
def seg(v, vs, d, a=None, as_=None, zoom=1.0, grade='hot', caps=(), black=False, vraw=False, label=None, name=None, freeze=False, rev=False, zramp=0):
    S.append(dict(v=v, vs=vs, d=d, a=a, as_=as_, zoom=zoom, grade=grade, caps=list(caps), black=black, vraw=vraw, label=label, name=name, freeze=freeze, rev=rev, zramp=zramp))
# HOOK
seg('E', 19.95, 1.25, 'E', 19.95, caps=[("SAME CALL.", 0.05, 1.25, 170, {"CALL."})])
seg('F', 3.0, 2.75, 'E', 21.15, vraw=True, caps=[("EVERY RED LIGHT.", 0, 1.35, 140, {"LIGHT."}), ("YEARS LATER.", 1.4, 2.75, 150, {"LATER."})])
# CATCHPHRASE
seg('E', 26.3, 3.0, 'E', 26.3, name='c1', zoom=1.0, caps=[("I TOLD YOU I'M GONNA", 0.1, 1.5, 100, set()), ("GET LOUDER", 1.5, 3.0, 140, {"LOUDER"})])
seg('E', 29.3, 2.6, 'E', 29.3, name='c2', zoom=1.12, caps=[("AND LOUDER", 0.1, 1.3, 170, {"LOUDER"}), ("AND LOUDER", 1.3, 2.6, 200, {"LOUDER"})])
seg('E', 31.9, 4.6, 'E', 31.9, zoom=1.22, caps=[("UNTIL YOU ALL START", 0.1, 1.3, 105, set()), ("LISTENING.", 1.3, 2.2, 150, {"LISTENING."}), ("I'M TALKING ABOUT", 2.3, 3.6, 105, set()), ("FIRST RESPONDER", 3.0, 4.5, 105, set())])
seg('E', 36.5, 3.3, 'E', 36.5, zoom=1.35, name='pt', caps=[("P", 0.45, 1.1, 300, {"P"}), ("PT", 1.1, 1.75, 300, {"PT"}), ("PTS", 1.75, 2.4, 300, {"PTS"}), ("PTSD!", 2.4, 3.3, 300, {"PTSD!"})])
seg('E', 38.0, 0.9, rev=True, name='rew', caps=[("REPLAY", 0.0, 0.9, 210, {"REPLAY"})])
# GAG
seg('B', 0.45, 1.65, 'B', 0.45, caps=[("EVERYBODY REPLAYS STUFF.", 0.1, 1.65, 112, {"REPLAYS"})])
seg('B', 3.05, 2.65, 'B', 3.05, name='g2', caps=[("THE CASHIER SAYS:", 0.1, 1.2, 112, set()), ("\"ENJOY YOUR DONUTS.\"", 1.2, 2.65, 100, {"DONUTS.\""})])
seg('B', 6.15, 2.0, 'B', 6.15, caps=[("YOU TOO!", 0.9, 2.0, 190, {"TOO!"})], label=('REPLAY #1', 0.0, 2.0))
seg('B', 7.3, 0.85, 'B', 7.3, caps=[("YOU TOO!", 0.0, 0.85, 190, {"TOO!"})], label=('REPLAY #2', 0, 0.85))
seg('B', 7.3, 0.85, 'B', 7.3, caps=[("YOU TOO!", 0.0, 0.85, 190, {"TOO!"})], label=('REPLAY #3', 0, 0.85))
seg('B', 8.95, 0.55, 'B', 8.95, caps=[("HA!", 0.0, 0.55, 220, {"HA!"})])
seg('B', 10.25, 1.4, 'B', 10.25, name='g7', caps=[("THAT'S THE FREE VERSION.", 0.1, 1.4, 105, {"FREE"})])
# TWIST
seg(None, 0, 1.0, black=True)
seg('A', 2.5, 1.25, 'A', 2.5, grade='sad', caps=[("NOW THE OTHER ONE.", 0.15, 1.25, 105, {"OTHER"})])
seg('A', 6.7, 1.7, 'A', 6.7, grade='sad', caps=[("THE ONE WITH", 0.1, 0.9, 110, set()), ("THE SIRENS.", 0.9, 1.7, 150, {"SIRENS."})])
# HARD HALF
seg('A', 16.3, 1.5, 'A', 16.3, grade='sad', caps=[("NOBODY ASKED", 0.1, 0.8, 120, set()), ("FOR THIS REPLAY.", 0.8, 1.5, 120, {"REPLAY."})])
seg('A', 19.95, 1.45, 'A', 19.95, grade='sad', caps=[("IT STARTS", 0.1, 0.8, 130, set()), ("ON ITS OWN.", 0.8, 1.45, 130, {"OWN."})])
seg('J', 1.6, 1.2, 'A', 25.9, vraw=True, grade='sad', caps=[("BRUSHING MY TEETH.", 0.1, 1.2, 110, {"TEETH."})])
seg('M', 0.5, 0.95, 'A', 28.3, vraw=True, grade='sad', caps=[("A RED LIGHT.", 0.0, 0.95, 140, {"LIGHT."})])
seg('K', 0.55, 1.15, 'A', 29.95, vraw=True, grade='sad', caps=[("A SMELL.", 0.1, 1.15, 190, {"SMELL."})])
seg('A', 34.4, 1.35, 'A', 34.4, grade='sad', caps=[("HERE'S WHAT NOBODY", 0.05, 0.8, 100, set()), ("TOLD ME.", 0.8, 1.35, 140, {"ME."})])
seg('A', 42.3, 1.45, 'A', 42.3, grade='sad', caps=[("IT'S NOT", 0.1, 0.7, 150, set()), ("WEAKNESS.", 0.7, 1.45, 170, {"WEAKNESS."})])
seg('A', 53.0, 2.0, 'A', 53.0, grade='sad', caps=[("YOUR BRAIN IS TRYING", 0.1, 1.0, 100, set()), ("TO FINISH THE REPORT.", 1.0, 2.0, 100, {"REPORT."})])
seg('D', 8.0, 1.7, 'A', 60.0, vraw=True, grade='sad', caps=[("IT KEEPS HITTING", 0.05, 1.0, 105, set()), ("REPLAY.", 1.0, 1.7, 170, {"REPLAY."})])
seg('D', 30.0, 1.4, 'A', 65.45, vraw=True, grade='sad', caps=[("NOBODY EVER", 0.05, 0.8, 120, set()), ("HIT STOP.", 0.8, 1.4, 170, {"STOP."})])
# ASK
seg('G', 1.7, 2.2, 'G', 1.7, name='ask', caps=[("SAY IT OUT LOUD", 0.05, 1.2, 130, {"LOUD"}), ("TO SOMEBODY WHO GETS IT.", 1.2, 2.2, 90, {"GETS"})])
seg('A', 86.15, 3.3, 'A', 86.15, name='spi', zramp=0.3, caps=[("A REPLAY LOSES ITS POWER", 0.05, 1.9, 100, {"POWER"}), ("WHEN IT HAS COMPANY.", 1.9, 3.3, 100, {"COMPANY."})])
# SIGN-OFF
seg('E', 2.95, 5.65, 'E', 2.95, name='sign', caps=[("DAY 21", 0.15, 1.2, 150, {"21"}), ("OF 61.", 1.2, 2.0, 180, {"61."}), ("CALL YOUR MAYDAY.", 2.3, 3.3, 110, {"MAYDAY."}), ("SEND IT TO SOMEONE WHO WORE THE UNIFORM.", 3.45, 5.6, 100, {"UNIFORM."})])
seg('L', 0.0, 2.15, 'L', 0.0, vraw=True, name='tease')
FOLLOW_LAST = 2.15
# ---------- build segments ----------
FPS = 30
t = 0.0; vl = []; al = []; caps_out = []; labels = []; T0 = []
for i, s in enumerate(S):
    n = round(s['d'] * FPS); d = n / FPS; s['d'] = d; s['t0'] = t; T0.append(t)
    if s['black']:
        run(f'ffmpeg -v error -y -f lavfi -i color=c=black:s=1080x1920:r=30 -frames:v {n} -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p w/v{i}.mp4')
        run(f'ffmpeg -v error -y -f lavfi -i anullsrc=r=48000:cl=stereo -t {d} w/a{i}.wav')
    elif s['freeze'] or s['rev']:
        c = s['v']; vs = s['vs'] + OFF[c]; flip = 'hflip,' if c in FLIP else ''
        z = s['zoom']; zf = f'crop=iw/{z}:ih/{z},' if z > 1 else ''
        base = f'{flip}scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,{zf}scale=1080:1920,fps=30'
        if s['freeze']: vf = base + f',trim=end_frame=1,tpad=stop_mode=clone:stop_duration={d:.3f},format=yuv420p'; ti = '0.2'
        else: vf = base + f',trim=duration={d:.3f},reverse,setpts=PTS-STARTPTS,format=yuv420p'; ti = f'{d+0.2:.2f}'
        run(f'ffmpeg -v error -y -ss {vs:.3f} -t {ti} -i {c}.mov -map 0:v:0 -an -vf "{vf}" -frames:v {n} -c:v libx264 -preset veryfast -crf 18 w/v{i}.mp4')
        run(f'ffmpeg -v error -y -f lavfi -i anullsrc=r=48000:cl=stereo -t {d} w/a{i}.wav')
    elif s['name'] == 'tease':
        c = 'L'; flip = 'hflip,'
        run(f'ffmpeg -v error -y -ss 0 -i L.mov -map 0:v:0 -an -vf "{flip}scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p" -frames:v {n} -c:v libx264 -preset veryfast -crf 18 w/v{i}.mp4')
        run(f'ffmpeg -v error -y -f lavfi -i anullsrc=r=48000:cl=stereo -t {d} w/a{i}.wav')
    else:
        c = s['v']; vs = s['vs'] if s['vraw'] else s['vs'] + OFF[c]
        flip = 'hflip,' if c in FLIP else ''
        z = s['zoom']; zf = f'crop=iw/{z}:ih/{z},' if z > 1 else ''
        zr = s['zramp']; zrf = f"scale=w='trunc(1080*(1+{zr}*t/{d:.3f})/2)*2':h='trunc(1920*(1+{zr}*t/{d:.3f})/2)*2':eval=frame,crop=1080:1920," if zr else ''
        gr = ',eq=saturation=0.25:brightness=-0.07:contrast=1.0,vignette=PI/3.2' if s['grade'] == 'sad' else ''
        run(f'ffmpeg -v error -y -ss {vs:.3f} -i {c}.mov -map 0:v:0 -an -vf "{flip}scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,{zf}scale=1080:1920,{zrf}fps=30{gr},format=yuv420p" -frames:v {n} -c:v libx264 -preset veryfast -crf 18 w/v{i}.mp4')
        a = s['a']; run(f'ffmpeg -v error -y -ss {s["as_"]:.3f} -t {d:.3f} -i w/n{a}.wav -af "afade=t=in:d=0.012,afade=t=out:st={d-0.012:.3f}:d=0.012,apad=whole_dur={d:.3f}" -t {d:.3f} -ar 48000 -ac 2 w/a{i}.wav')
    vl.append(f"file 'v{i}.mp4'"); al.append(f"file 'a{i}.wav'")
    for (txt, a0, a1, sz, keys) in s['caps']: caps_out.append((txt, t + a0, t + min(a1, d), sz, keys))
    if s['label']: labels.append((s['label'][0], t + s['label'][1], t + s['label'][2]))
    t += d
TOT = t
open('w/vl.txt', 'w').write('\n'.join(vl)); open('w/al.txt', 'w').write('\n'.join(al))
run('cd w && ffmpeg -v error -y -f concat -safe 0 -i vl.txt -c copy vcat.mp4 && ffmpeg -v error -y -f concat -safe 0 -i al.txt -c copy acat.wav')
print('TOTAL', TOT)
# ---------- overlays ----------
def mbtext(im, xy, txt, font, stroke=11, sh=(9, 11), col=(255, 255, 255, 255)):
    x, y = xy; d = ImageDraw.Draw(im)
    d.text((x + sh[0], y + sh[1]), txt, font=font, fill=(0, 0, 0, 255), stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    d.text((x, y), txt, font=font, fill=col, stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
def brush(d, box, col=(214, 18, 36, 255), seed=1):
    rnd = random.Random(seed); x0, y0, x1, y1 = box
    pts = [(x, y0 + rnd.uniform(-9, 9)) for x in range(int(x0), int(x1), 26)] + [(x1 + rnd.uniform(-4, 26), y) for y in range(int(y0), int(y1), 22)] + [(x, y1 + rnd.uniform(-9, 9)) for x in range(int(x1), int(x0), -26)] + [(x0 - rnd.uniform(-4, 26), y) for y in range(int(y1), int(y0), -22)]
    d.polygon([(px + 8, py + 10) for px, py in pts], fill=(0, 0, 0, 235)); d.polygon(pts, fill=col)
ovs = []  # (png, t0, t1)
for i, (txt, a, b, sz, keys) in enumerate(caps_out):
    im = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); dd = ImageDraw.Draw(im); font = MB(sz); lines = []; cu = ''
    for w in txt.split():
        tt = (cu + ' ' + w).strip()
        if dd.textlength(tt, font=font) > 960 and cu: lines.append(cu); cu = w
        else: cu = tt
    lines.append(cu); lh = int(sz * 1.14); y = 1290 - len(lines) * int(lh / 2)
    for L in lines:
        x = (1080 - dd.textlength(L, font=font)) / 2
        for w in L.split():
            mbtext(im, (x, y), w, font, stroke=max(8, sz // 10), sh=(max(6, sz // 12), max(7, sz // 10)), col=(Y if w in keys else (255, 255, 255, 255))); x += dd.textlength(w + ' ', font=font)
        y += lh
    im.save(f'w/cap{i}.png'); ovs.append((f'w/cap{i}.png', a, b))
for j, (txt, a, b) in enumerate(labels):
    im = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); dd = ImageDraw.Draw(im); f = MB(84); w = dd.textlength(txt, font=f); cx, cy = 540, 520
    brush(dd, [cx - w / 2 - 34, cy - 52, cx + w / 2 + 34, cy + 66], seed=j + 3); mbtext(im, (cx - w / 2, cy - 46), txt, f, stroke=5, sh=(5, 6))
    im.save(f'w/lab{j}.png'); ovs.append((f'w/lab{j}.png', a, b))
tag = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); dd = ImageDraw.Draw(tag); brush(dd, [48, 128, 470, 196], seed=3); mbtext(tag, (64, 126), "MAYDAY", MB(60), stroke=5, sh=(5, 6)); mbtext(tag, (60, 204), "DAY 21 OF 61", MB(40), stroke=7, sh=(5, 6), col=Y); tag.save('w/tag.png')
st = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); dd = ImageDraw.Draw(st); brush(dd, [40, 1590, 1040, 1700], seed=5); f = MB(60); s1 = "STRUGGLING? CALL OR TEXT 988"; mbtext(st, ((1080 - dd.textlength(s1, font=f)) / 2, 1602), s1, f, stroke=5, sh=(5, 6))
f = MB(33)
for s_, yy in (("VETERANS: 988, PRESS 1", 1716), ("RESPONDERS: SAFE CALL NOW 206-459-3020", 1762)): mbtext(st, ((1080 - dd.textlength(s_, font=f)) / 2, yy), s_, f, stroke=6, sh=(4, 5), col=Y)
st.save('w/strip.png')
fo = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); dd = ImageDraw.Draw(fo); f = MB(70); s_ = "FOLLOW FOR DAY 22"; w = dd.textlength(s_, font=f); mbtext(fo, ((1080 - w) / 2, 1420), s_, f, stroke=12, col=Y); fo.save('w/follow.png')
tw = T0[[i for i, s in enumerate(S) if s['black']][0]]
N = {s['name']: T0[i] for i, s in enumerate(S) if s['name']}
D_T = N['rew'] + 0.55
# ---- extra art ----
import math
rnd = random.Random(7)
import numpy as np
from PIL import ImageFilter
A0 = N['g2'] + 2.2
FX, FY = 470, 860
def shade(M):
    """glossy red jelly from an L mask (numpy 0-255 float)"""
    mi = Image.fromarray(M.astype(np.uint8)); depth = np.asarray(mi.filter(ImageFilter.GaussianBlur(10)), dtype=np.float32) / 255
    d2 = np.asarray(mi.filter(ImageFilter.GaussianBlur(3)), dtype=np.float32) / 255
    hi = np.clip((np.roll(np.roll(d2, 5, 0), 5, 1) - d2) * -6, 0, 1) * (d2 > 0.5)       # upper-left rim light
    spec = np.clip((np.asarray(mi.filter(ImageFilter.GaussianBlur(22)), dtype=np.float32)/255 - 0.55) * 3, 0, 1)
    rgb = np.zeros(M.shape + (3,), np.float32)
    rgb[..., 0] = 120 + 110 * depth; rgb[..., 1] = 4 + 22 * depth; rgb[..., 2] = 18 + 30 * depth
    sp_ = np.asarray(mi.filter(ImageFilter.GaussianBlur(6)), dtype=np.float32)/255
    gl = np.clip((np.roll(np.roll(sp_, -14, 0), -14, 1) - sp_) * 5, 0, 1) * (sp_ > 0.3)  # gloss
    rgb += (hi[..., None] * 120 + gl[..., None] * 160 + spec[..., None] * 40)
    alpha = np.clip(np.asarray(mi.filter(ImageFilter.GaussianBlur(1.2)), dtype=np.float32) * 0.96, 0, 245)
    out = np.dstack([np.clip(rgb, 0, 255), alpha]).astype(np.uint8); return Image.fromarray(out, 'RGBA')
def splat_mask(q, seed, big=1.0):
    r = random.Random(seed); m = Image.new('L', (1080, 1920), 0); d = ImageDraw.Draw(m)
    for k in range(150):
        a = r.uniform(0, 6.283); dist = r.uniform(30, 1250) * q * big; sz = r.uniform(10, 70) * (0.4 + q) * (1.2 - dist / 1800)
        x = FX + dist * math.cos(a); y = FY + dist * math.sin(a) * 1.25
        d.ellipse([x - sz, y - sz, x + sz, y + sz], fill=255)
        if r.random() < 0.55:  # streak toward the center
            d.line([x, y, FX + dist * 0.5 * math.cos(a), FY + dist * 0.5 * math.sin(a) * 1.25], fill=255, width=int(sz * 0.55))
    d.ellipse([FX - 150 * q - 20, FY - 150 * q - 20, FX + 150 * q + 20, FY + 150 * q + 20], fill=255)
    return np.asarray(m, dtype=np.float32)
def bitten_donut(im, cx, cy, r):
    d = ImageDraw.Draw(im); base = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); bd = ImageDraw.Draw(base)
    for k in range(14): bd.ellipse([cx-r+k*2, cy-r+k*2, cx+r-k*2, cy+r-k*2], fill=(150+k*5, 85+k*5, 30+k*3, 255))  # shaded dough
    bd.ellipse([cx-r*0.28, cy-r*0.28, cx+r*0.28, cy+r*0.28], fill=(40, 20, 8, 255))
    for _ in range(90):
        a = random.uniform(0, 6.283); rr = random.uniform(0.35, 0.95) * r; bd.ellipse([cx+rr*math.cos(a)-3, cy+rr*math.sin(a)-3, cx+rr*math.cos(a)+3, cy+rr*math.sin(a)+3], fill=(250, 245, 235, 255))
    bd.ellipse([cx+r*0.35, cy-r*0.9, cx+r*1.2, cy-r*0.1], fill=(0, 0, 0, 0))  # bite
    base = base.filter(ImageFilter.GaussianBlur(1)); im.alpha_composite(base)
NF = 16
for f in range(NF):
    im = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    if f < 7:
        bitten_donut(im, FX + 40, FY + 330 - f * 40, 150)
    if f >= 5:
        q = min(1.0, (f - 4) / 9.0); sh = shade(splat_mask(q, 3, 1.0)); im.alpha_composite(sh)
    im.save(f'w/dn{f:02d}.png')
shade(splat_mask(1.0, 3, 1.0)).save('w/splat.png')
for k, al in enumerate((255, 255, 210, 150, 95, 45)): Image.new('RGBA', (1080, 1920), (255, 255, 255, al)).save(f'w/fl{k}.png')
im = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); dd = ImageDraw.Draw(im); f = MB(92); t_ = "NOTHING'S FREE."; w = dd.textlength(t_, font=f)
brush(dd, [540-w/2-34, 480, 540+w/2+34, 610], seed=9); mbtext(im, (540-w/2, 486), t_, f, stroke=5, sh=(5, 6)); im.save('w/free.png')
run(f'ffmpeg -v error -y -loop 1 -framerate 30 -t {S[[i for i,s in enumerate(S) if s["name"]=="spi"][0]]["d"]:.3f} -i w_spiral.png -loop 1 -framerate 30 -t 3.4 -i w_hole.png -filter_complex "[0:v]rotate=a=1.8*t:ow=1080:oh=1920:c=black,format=rgba[s];[1:v]format=gray,lut=y=val*0.88[m];[s][m]alphamerge[o]" -map "[o]" -c:v qtrle w/spiral.mov')
# ---- compose ----
spi_d = S[[i for i, s in enumerate(S) if s['name'] == 'spi'][0]]['d']
ovs += [('w/tag.png', 0, TOT), ('w/strip.png', tw, TOT), ('w/follow.png', TOT - FOLLOW_LAST, TOT)]
g7 = [i for i, s in enumerate(S) if s['name'] == 'g7'][0]; g_end = T0[g7] + S[g7]['d']
ovs += [('w/free.png', N['g7'] + 0.3, g_end)]
for k in range(6):
    a, b = D_T + 0.08 * k, D_T + 0.08 * (k + 1)
    ovs.append((f'w/fl{k}.png', a, b))
inputs = ['-i w/spiral.mov', '-framerate 60 -i w/dn%02d.png'] + [f'-i {p}' for p, _, _ in ovs]
fc = f"[2:v]setpts=PTS+{A0:.3f}/TB[dn];[1:v]setpts=PTS+{N['spi']:.3f}/TB[sp];[0:v][sp]overlay=0:0:enable='between(t,{N['spi']:.3f},{N['spi']+spi_d:.3f})'[b0];"
last = 'b0'
for k, (p, a, b) in enumerate(ovs):
    fc += f"[{last}][{k+3}:v]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'[o{k}];"; last = f'o{k}'
fc += f"[{last}][dn]overlay=0:0:enable='between(t,{A0:.3f},{A0+NF/60:.3f})'[fin]"
run(f'ffmpeg -v error -y -i w/vcat.mp4 {" ".join(inputs)} -filter_complex "{fc}" -map "[fin]" -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p w/vid.mp4')
# ---------- audio mix ----------
ins = '-i w/acat.wav'; fl = ''; n = 1; mix = ['[0:a]']
def sfx(name, at, gain, rate=1.0):
    global ins, fl, n
    ins += f' -i {SD}{name}.wav'; ms = int(max(0, at) * 1000); rr = f'asetrate={int(48000*rate)},aresample=48000,' if rate != 1.0 else ''
    fl += f'[{n}:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,{rr}volume={gain}dB,adelay={ms}|{ms},apad=whole_dur={TOT:.2f}[x{n}];'; mix.append(f'[x{n}]'); n += 1
# louder x3: ascending slams, then backfire + freeze
for at, rt, g in ((N['c1'] + 2.45, 0.8, 0), (N['c2'] + 0.8, 0.95, 2), (N['c2'] + 1.85, 1.12, 4)):
    sfx('punch', at, g, rt); sfx('thump', at + 0.02, g - 3, rt)
# P-T-S-D: ascending slams, D = explosion
for k, rt in enumerate((0.8, 0.92, 1.05, 1.2)):
    at = N['pt'] + 0.45 + 0.65 * k; sfx('punch', at, k * 1.5, rt); sfx('thump', at + 0.02, -3, rt)
sfx('bomb', D_T, 5); sfx('screech', N['pt'] + 2.4, -8)
sfx('rewind', N['rew'], -2)
# donuts hit
rew = [i for i, s in enumerate(S) if s['label'] and s['label'][0] in ('REPLAY #2', 'REPLAY #3')]
for i in rew: sfx('rewind', T0[i] - 0.5, -6)
sfx('slap', A0 + 0.1, 2); sfx('thump', A0 + 0.1, 0)
sfx('screech', tw, 0); sfx('thump', tw + 0.9, -2)
sfx('whoosh', T0[1] - 0.05, -6)
sfx('car_tr', N['rew'] - 0.5, 0)
sfx('car_end', N['tease'] - 0.1, 0)
sfx('dod_hit', TOT - 0.75, -3)
ins += f' -stream_loop -1 -i {SD}hard1.wav'; hs = tw + 1.0; ms = int(hs * 1000)
fl += f'[{n}:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,volume=-24dB,atrim=0:{TOT-hs:.2f},afade=t=in:d=1.5,adelay={ms}|{ms},apad=whole_dur={TOT:.2f}[x{n}];'; mix.append(f'[x{n}]'); n += 1
fl = fl.replace('', '')
a0, b0 = N['ask'], N['ask'] + 2.2
mix[0] = '[v0]'
fl = f"[0:a]volume='if(between(t,{a0:.2f},{b0:.2f}),1.8,1)':eval=frame[v0];" + fl
fl += ''.join(mix) + f'amix=inputs={len(mix)}:normalize=0:duration=first,alimiter=limit=0.95,loudnorm=I=-15.5:TP=-1.5:LRA=11[m]'
run(f'ffmpeg -v error -y {ins} -filter_complex "{fl}" -map "[m]" -t {TOT:.3f} -ar 48000 w/mix.wav')
run('ffmpeg -v error -y -i w/vid.mp4 -i w/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -shortest MAYDAY-Day-21-THE-REPLAY.mp4')
print('DONE', TOT, N)
