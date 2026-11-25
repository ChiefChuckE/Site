"""MAYDAY Day 25 "The PTSD Thanksgiving Recipe". Sync-safe: whole-frame segments, video/audio separate, then mux."""
import subprocess, os, re, json, wave, glob, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
os.chdir('/tmp/claude-0/d25/w')
s24 = open('/tmp/claude-0/d24/w/build24.py').read()
exec(s24[s24.index('def run'):s24.index('# ---------- capsule')].replace("'p/", "'q/").replace("f'p/", "f'q/"))
_run = run
def run(c):
    last = c.split()[-1]
    pass
    return _run(c)
MUSIC = '/mnt/user-data/uploads/Movies/d24/1458322.mp3'
SR = 48000
VENC = '-r 30 -c:v libx264 -preset veryfast -crf 17 -pix_fmt yuv420p -an'
import collections
VOFF = collections.defaultdict(float, {'ccopy': 0.685})
VAF = 'highpass=f=100,afftdn=nf=-28,acompressor=threshold=-24dB:ratio=3:attack=5:release=120,loudnorm=I=-16:TP=-2:LRA=7'
def fr(d): return max(1, round(d * 30))
for c in ('c3064','c3068','c3076','c3060','c3061','c3062','c3063','c3065','c3067','c3069','c3070','c3071','c3072','c3073','c3077','c3080','c3084','ccopy'):
    run(f'ffmpeg -v error -y -i src/{c}.mov -vn -af "{VAF},aresample={SR}" -ar {SR} -ac 2 q/{c}_p.wav')

det = cv2.FaceDetectorYN.create('yunet.onnx', '', (1080, 1920), 0.45, 0.3, 200)
def bald(im, x, y, w, h):
    y0, y1 = max(0, int(y - 0.55 * h)), max(1, int(y - 0.05 * h)); r = im[y0:y1, max(0, int(x + 0.15 * w)):int(x + 0.85 * w)].astype(int)
    if r.size == 0: return 0
    B, G, R = r[..., 0], r[..., 1], r[..., 2]
    return float(np.mean((R > 110) & (R > G + 8) & (G > B - 5) & (R - B > 20)))
STATIC = {k: [(0, 1330, 620, 1920)] for k in ('c1', 'c2', 'c3', 'c4', 'c5')}
def blurseg(name, n, mode):
    fs = sorted(glob.glob(f'q/{name}_f/*.jpg'))[:n]; dets = []
    for f in fs:
        if mode == 'static': dets.append([]); continue
        im = cv2.imread(f); _, res = det.detect(im); res = [] if res is None else [tuple(float(v) for v in r[:4]) for r in res]
        dets.append([(x, y, w, h, bald(im, x, y, w, h) if mode != 'largest' else w * h) for x, y, w, h in res])
    me = [None] * len(fs)
    if mode == 'largest':
        for i, ds in enumerate(dets):
            if ds: me[i] = max(range(len(ds)), key=lambda k: ds[k][4])
        posl = [None] * len(fs)
    else:
        best = max(((d[4] + min(d[2], 200) / 400, i, k) for i, ds in enumerate(dets) for k, d in enumerate(ds)), default=None)
        posl = [None] * len(fs)
        if best and best[0] > 0.35:
            _, i0, k0 = best
            for rng in (range(i0, len(fs)), range(i0, -1, -1)):
                x, y, w, h, _ = dets[i0][k0]; pos = (x + w / 2, y + h / 2); sz = w
                for i in rng:
                    c = [(((d[0] + d[2] / 2 - pos[0]) ** 2 + (d[1] + d[3] / 2 - pos[1]) ** 2) ** .5, k) for k, d in enumerate(dets[i])]
                    c = [q for q in c if q[0] < max(160, 1.6 * sz)]
                    if c: k = min(c)[1]; d = dets[i][k]; pos = (d[0] + d[2] / 2, d[1] + d[3] / 2); sz = d[2]; me[i] = k
                    posl[i] = (pos, sz)
    boxes = []
    for i, ds in enumerate(dets):
        bx = []
        for k, (x, y, w, h, _) in enumerate(ds):
            if k == me[i] and mode != 'all': continue
            if mode != 'all' and posl[i] and abs(x + w / 2 - posl[i][0][0]) < max(110, posl[i][1]) and abs(y + h / 2 - posl[i][0][1]) < max(110, posl[i][1]): continue
            if mode == 'all': pass
            elif mode != 'largest' and posl[i] is None: continue      # never blur blind
            if mode == 'right' and not (x + w / 2 > posl[i][0][0] + 90 or w < 40): continue
            bx.append((int(x - 0.4 * w), int(y - 0.5 * h), int(x + 1.4 * w), int(y + 1.4 * h)))
        boxes.append(bx)
    log = [(len(d), m is not None) for d, m in zip(dets, me)]
    P = 7
    for i, f in enumerate(fs):
        allb = [b for j in range(max(0, i - P), min(len(fs), i + P + 1)) for b in boxes[j]] + STATIC.get(name, [])
        if not allb: continue
        im = cv2.imread(f); H, W = im.shape[:2]
        for x0, y0, x1, y1 in allb:
            x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
            if x1 - x0 < 4 or y1 - y0 < 4: continue
            roi = im[y0:y1, x0:x1]; k = max(9, ((x1 - x0) // 2) | 1); sm = cv2.resize(roi, (max(2, (x1 - x0) // 14), max(2, (y1 - y0) // 14)), interpolation=cv2.INTER_AREA)
            im[y0:y1, x0:x1] = cv2.GaussianBlur(cv2.resize(sm, (x1 - x0, y1 - y0), interpolation=cv2.INTER_LINEAR), (k, k), 0)
        cv2.imwrite(f, im, [cv2.IMWRITE_JPEG_QUALITY, 95])
    print(name, 'frames', len(fs), 'me found in', sum(1 for l in log if l[1]), 'blur frames', sum(1 for b in boxes if b), flush=True)
def vseg(name, clip, vt, d, pre='', extra='', blur=None):
    n = fr(d)
    if os.path.exists(f'q/{name}.mp4') and os.path.getsize(f'q/{name}.mp4') > 1000:
        c_ = subprocess.run(f'ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames -of csv=p=0 q/{name}.mp4', shell=True, capture_output=True, text=True).stdout.strip()
        if c_ == str(n): return n
    if os.path.exists(f'q/{name}.mp4'): os.remove(f'q/{name}.mp4')
    if blur:
        os.makedirs(f'q/{name}_f', exist_ok=True)
        for f in glob.glob(f'q/{name}_f/*.jpg'): os.remove(f)
        _run(f'ffmpeg -v error -y -ss {vt:.3f} -i src/{clip}.mov -vf "{pre}{FIT}{extra}" -frames:v {n} -q:v 2 q/{name}_f/%04d.jpg')
        blurseg(name, n, blur); _run(f'ffmpeg -v error -y -framerate 30 -i q/{name}_f/%04d.jpg -frames:v {n} {VENC} q/{name}.mp4')
    else: run(f'ffmpeg -v error -y -ss {vt:.3f} -i src/{clip}.mov -vf "{pre}{FIT}{extra}" -frames:v {n} {VENC} q/{name}.mp4')
    return n
def wav_exact(name, n, inp, filt):
    run(f'ffmpeg -v error -y {inp} -af "{filt},aresample={SR},aformat=sample_fmts=s16:channel_layouts=stereo,apad,atrim=0:{n/30:.5f}" -ar {SR} -ac 2 q/{name}.wav')
def silence(name, n): run(f'ffmpeg -v error -y -f lavfi -t {n/30:.5f} -i anullsrc=r={SR}:cl=stereo -ar {SR} -ac 2 q/{name}.wav')
def talk(name, clip, a, d, pre='', extra='', blur=None, af=''):
    n = vseg(name, clip, a + VOFF[clip], d, pre, extra, blur); dd = n / 30
    wav_exact(name, n, f'-ss {a:.3f} -t {dd + 0.2:.3f} -i q/{clip}_p.wav', f'{af}afade=t=in:d=0.03,afade=t=out:st={dd-0.05:.3f}:d=0.05'); return n
def quiet(name, clip, vt, d, pre='', extra='', blur=None):
    n = vseg(name, clip, vt, d, pre, extra, blur); silence(name, n); return n
def still(name, png, d, zoom=0.0005):
    n = fr(d)
    run(f'ffmpeg -v error -y -loop 1 -framerate 30 -i q/{png}.png -vf "zoompan=z=\'1+{zoom}*on\':d=1:x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':s=1080x1920:fps=30,fade=t=in:d=0.2" -frames:v {n} {VENC} q/{name}.mp4'); silence(name, n); return n

# ---------- graphics
exec(open('list.py').read().split("im.save(")[0].replace("im=Image.new", "im=Image.new"))   # builds the handwritten list as `im`
LIST = im.convert('RGB')
def desk():
    bg = Image.new('RGB', (1080, 1920), (58, 40, 28)); d = ImageDraw.Draw(bg)
    for y in range(0, 1920, 6): d.line([(0, y), (1080, y)], fill=(58 + (y * 7 % 13), 40 + (y * 5 % 9), 28 + (y * 3 % 7)))
    return bg
def paper(crop, w, ang):
    p = LIST.crop(crop); p = p.resize((w, int(p.height * w / p.width)), Image.LANCZOS).convert('RGBA')
    sh = Image.new('RGBA', (p.width + 60, p.height + 60), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle([30, 30, p.width + 30, p.height + 30], fill=(0, 0, 0, 150)); sh = sh.filter(ImageFilter.GaussianBlur(14))
    sh.alpha_composite(p, (18, 14)); return sh.rotate(ang, expand=True, resample=Image.BICUBIC)
c1 = desk(); p = paper((0, 0, 2550, 3300), 900, 2.5); c1.paste(p, ((1080 - p.width) // 2, 330), p); c1.save('q/cardlist.png')
c2 = desk(); p = paper((250, 2110, 2550, 3300), 1000, -2); c2.paste(p, ((1080 - p.width) // 2, 560), p); d = ImageDraw.Draw(c2)
ctext(d, "THE REAL RECIPE", 380, MB(84), W_, o=4); ctext(d, "SERVES EVERYONE AT YOUR TABLE.", 1250, MB(50), Y_, o=4)
ctext(d, "SEND THIS TO WHOEVER'S", 1340, MB(50), W_, o=4); ctext(d, "HOSTING TOMORROW.", 1400, MB(50), W_, o=4); ctext(d, "TOMORROW · DAY 26: THE THANKSGIVING SIZE-UP", 1490, MB(34, 'Bold Italic'), Y_, o=3); c2.save('q/cardend.png')
ov = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
d.rounded_rectangle([40, 150, 430, 236], 16, fill=RED)
for dx, dy in ((-3, 0), (3, 0), (0, -3), (0, 3), (4, 6)): d.text((62 + dx, 150 + dy), "MAYDAY", font=MB(66), fill=(0, 0, 0, 255))
d.text((62, 150), "MAYDAY", font=MB(66), fill=W_)
for dx, dy in ((-3, 0), (3, 0), (0, -3), (0, 3), (4, 6)): d.text((60 + dx, 244 + dy), "DAY 25 OF 61", font=MB(44), fill=(0, 0, 0, 255))
d.text((60, 244), "DAY 25 OF 61", font=MB(44), fill=Y_)
d.rounded_rectangle([40, 1560, 1040, 1606], 12, fill=(0, 0, 0, 150)); ctext(d, "Comedy with a point. Not sponsored by or affiliated with any store.", 1568, MB(25, 'Bold Italic'), W_)
d.rectangle([0, 1630, 1080, 1716], fill=RED); ctext(d, "STRUGGLING? CALL OR TEXT 988", 1640, MB(56), W_, o=4)
d.rectangle([0, 1716, 1080, 1800], fill=(0, 0, 0, 215))
ctext(d, "VETERANS: 988, PRESS 1", 1722, MB(30), Y_); ctext(d, "RESPONDERS: SAFE CALL NOW 206-459-3020", 1758, MB(30), Y_)
ov.save('q/ov.png')

# ---------- segments
S = []
def T(name, clip, a, d, **k): S.append((name, talk(name, clip, a, d, **k), clip, a))
def Q(name, n): S.append((name, n, None, 0))
hat = Image.open('/mnt/user-data/attachments/033fd7c1-a08e-567c-b674-2e8ca0b3a350/33cbae9f-image.jpg').convert('RGB'); sc = 1920 / hat.height; hat = hat.resize((int(hat.width * sc), 1920), Image.LANCZOS)
x0 = int(hat.width * 0.58) - 540; hat.crop((x0, 0, x0 + 1080, 1920)).save('q/hat.png')
# store PA voice (Sally): split the one take into two announcements, give it a ceiling-speaker sound
PA = '/mnt/user-data/uploads/Movies/d25/pa.mp3'
_run(f'ffmpeg -v error -y -i {PA} -af "highpass=f=320,lowpass=f=3300,acompressor=threshold=-20dB:ratio=4,aecho=0.8:0.5:55|110:0.35|0.22,loudnorm=I=-17:TP=-2,aresample={SR}" -ar {SR} -ac 2 q/pa_all.wav')
p = subprocess.run('ffmpeg -hide_banner -i q/pa_all.wav -af silencedetect=noise=-40dB:d=0.7 -f null -', shell=True, capture_output=True, text=True).stderr
ss = [float(v) for v in re.findall(r'silence_start: ([\d.]+)', p)]; ee = [float(v) for v in re.findall(r'silence_end: ([\d.]+)', p)]; PD = dur('q/pa_all.wav')
mid = max([(e - a_, a_, e) for a_, e in zip(ss, ee) if a_ > 2 and e < PD - 1.5]); PA1 = (0.0, mid[1] + 0.25); PA2 = (mid[2] - 0.1, PD)
PA1 = (0.0, 6.45)
print('PA split', PA1, PA2, flush=True)
Z = ",crop=930:1654,scale=1080:1920"
T('k1', 'c3069', 3.35, 2.4, extra=Z); T('k2', 'c3069', 10.35, 3.35, extra=Z); T('k2b', 'c3069', 13.7, 1.45, extra=",crop=760:1351:170:120,scale=1080:1920")
Q('pa1', still('pa1', 'cardlist', PA1[1] - PA1[0] + 0.5))
T('o', 'c3060', 4.65, 5.3)
T('g1', 'c3070', 1.85, 2.9); T('g2', 'c3067', 1.65, 4.1); T('i1', 'c3072', 2.05, 2.0); T('g3', 'c3071', 1.0, 5.3); T('g3b', 'c3071', 7.2, 2.2)
T('i2', 'c3076', 0.2, 2.6); T('e', 'c3061', 2.7, 2.5); T('i3', 'c3073', 1.35, 3.6); T('i3b', 'c3073', 5.6, 5.6)
T('p1', 'c3064', 4.9, 1.9, blur='all'); T('p2', 'c3064', 15.0, 1.8, blur='all')
T('f', 'c3068', 4.8, 4.3); T('s', 'c3062', 0.95, 3.3)
T('l1', 'c3063', 1.85, 1.6); T('l2', 'c3063', 19.8, 1.65); T('l2b', 'c3063', 21.45, 0.9, extra=",crop=820:1458:130:140,scale=1080:1920")
T('m1', 'c3077', 1.3, 1.0); T('m2', 'c3077', 6.25, 4.7); T('m3', 'c3077', 11.3, 4.1); T('m4', 'c3077', 15.85, 3.6); T('m5', 'c3077', 20.0, 2.0)
Q('hat', still('hat', 'hat', 1.0, 0.0015))
T('c1', 'c3080', 4.05, 4.9, blur='static', af="volume=10dB:enable='lt(t,1.2)',volume=3dB,"); T('c2', 'c3080', 11.2, 1.4, blur='right', af='volume=9dB,'); T('c3', 'c3080', 14.05, 6.45, blur='right'); T('c4', 'c3080', 20.8, 5.5, blur='right')
T('c5', 'c3080', 27.9, 4.6, blur='static', af="volume=9dB:enable='lt(t,2.85)',")
Q('pa2', quiet('pa2', 'c3083', 3.0, PA2[1] - PA2[0] + 0.6, blur='bald'))
T('r', 'ccopy', 36.25, 12.5, pre='hflip,', blur='largest')
Q('end', still('end', 'cardend', 2.0))
nt = fr(0.9)
run(f'ffmpeg -v error -y -f lavfi -i "smptebars=s=1080x1920:r=30" -frames:v {nt} {VENC} q/tr.mp4')
wav_exact('tr', nt, f'-f lavfi -t 1.2 -i "sine=frequency=1000:sample_rate={SR}"', 'volume=0.18,afade=t=in:d=0.02,afade=t=out:st=0.82:d=0.06'); Q('tr', nt)
T('b1', 'c3084', 0.0, 5.6); T('b2', 'c3084', 20.6, 5.3)
T('bl', 'c3065', 1.5, 9.4)
_run('ffmpeg -v error -y -ss 10.38 -i src/c3065.mov -vf "' + FIT + '" -frames:v 1 q/suck.png')
Q('fz', still('fz', 'suck', 1.6, 0.0025))

off = {}; A = {}; t = 0
for nme, n, clip, a in S: off[nme] = t / 30; A[nme] = a; t += n
TOTAL = t / 30; print({k: round(v, 2) for k, v in off.items()}, 'TOTAL', round(TOTAL, 2))
open('q/v.txt', 'w').write(''.join(f"file '{s[0]}.mp4'\n" for s in S))
_run('ffmpeg -v error -y -f concat -safe 0 -i q/v.txt -c copy q/basev.mp4')
buf = []
for nme, n, _, _ in S:
    w = wave.open(f'q/{nme}.wav'); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2); want = n * SR // 30
    buf.append(x[:want] if len(x) >= want else np.vstack([x, np.zeros((want - len(x), 2), np.int16)]))
allx = np.vstack(buf).astype(np.int32)
def rdw(f):
    w_ = wave.open(f); return np.frombuffer(w_.readframes(w_.getnframes()), dtype=np.int16).reshape(-1, 2).astype(np.int32)
pa = rdw('q/pa_all.wav')
for seg_, (a_, b_) in (('pa1', PA1), ('pa2', PA2)):
    x_ = pa[int(a_ * SR):int(b_ * SR)].astype(np.float64); fo = int(0.25 * SR); x_[-fo:] *= np.linspace(1, 0, fo)[:, None]; x_ = x_.astype(np.int32); o_ = int((off[seg_] + 0.25) * SR); x_ = x_[:len(allx) - o_]; allx[o_:o_ + len(x_)] += x_
tt = np.arange(int(0.085 * SR)) / SR; beep = (np.sin(2 * np.pi * 1180 * tt) * 5200 * np.minimum(1, np.minimum(tt, tt[-1] - tt) / 0.006)).astype(np.int32)
BEEPS = ['g1', 'g2', 'i1', 'g3', 'i2', 'e', 'i3', 'p1', 'f', 's', 'l1']
for seg_ in BEEPS:
    o_ = int((off[seg_] + 0.06) * SR); allx[o_:o_ + len(beep)] += beep[:, None]
allx = np.clip(allx, -32767, 32767).astype(np.int16); w = wave.open('q/basea.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(allx.tobytes()); w.close()
print('video frames', t, 'audio s', round(len(allx) / SR, 4), 'video s', round(TOTAL, 4))

# ---------- captions (times on each clip's WAV clock, from the per-phrase ASR spans)
caps = []
def add(seg, txt, a, b, keys=(), size=70, y=None):
    o = off[seg] - A[seg]; s0, s1 = off[seg], off[seg] + dict((s[0], s[1]) for s in S)[seg] / 30
    caps.append((txt, max(s0, o + a), min(s1 - 0.02, o + b), keys, size, y))
def spread(seg, chunks, a, b, keys=()):
    tot = sum(len(c[1]) for c in chunks); t0 = a
    for shown, spoken in chunks:
        t1 = t0 + (b - a) * len(spoken) / tot; add(seg, shown, t0, t1 - 0.03, keys); t0 = t1
spread('k1', [("I'M LOOKING FOR MY MIND.", "I'm looking for my mind."), ("I LOST IT.", "I lost it.")], 3.45, 5.7, ("MIND.",))
add('k2', "ANYBODY SEE MY MIND?", 10.4, 11.7, ("MIND?",)); add('k2', "I LOST MY MIND.", 11.95, 13.3); add('k2b', "PTSD STOLE IT.", 13.75, 15.15, ("PTSD",), 96)
pd1 = PA1[1] - PA1[0]
caps.append(("STORE PA: \"ATTENTION SHOPPERS. A MIND HAS BEEN REPORTED MISSING.\"", off['pa1'] + 0.25, off['pa1'] + 4.3, ("STORE", "PA:"), 52, None))
caps.append(("\"LAST SEEN ABOUT 20 YEARS AGO.\"", off['pa1'] + 4.35, off['pa1'] + 0.45 + pd1, ("20", "YEARS"), 60, None))
add('o', "THANKSGIVING'S TOMORROW.", 4.75, 6.0); add('o', "I'M IN COSTCO,", 6.15, 7.2); add('o', "SHOPPING FOR A PTSD THANKSGIVING MEAL.", 7.3, 9.95, ("PTSD",))
spread('g1', [("WE'LL NEED THIS AT 3 IN THE MORNING.", "We'll need this at 3 in the morning."), ("AT LEAST I WILL.", "At least I will.")], 1.95, 4.7, ("3",))
spread('g2', [("FOR ALL THE TEARS I'M ABOUT TO SPILL...", "For all the tears I'm about to spill out"), ("I DON'T KNOW WHICH ONE.", "I don't know which one")], 1.75, 4.5, ("TEARS",)); add('g2', "PROBABLY BOTH.", 4.7, 5.75, ("BOTH.",))
add('i1', "DEFINITELY GONNA NEED THIS TONIGHT.", 2.25, 4.0, ("TONIGHT.",))
add('g3', "ANTI-STRESS SHOTS. $9.88.", 1.1, 3.3, ("ANTI-STRESS",)); add('g3', "I'LL TAKE THE WHOLE THING!", 3.45, 6.3, ("WHOLE",))
add('i2', "STRENGTH AND ENERGY. ADD THAT TO THE MEAL.", 0.3, 2.75, ("STRENGTH", "ENERGY."))
add('e', "I WON'T HAVE TO LISTEN TO UNCLE FREDDY THIS YEAR.", 2.78, 5.2, ("UNCLE", "FREDDY"))
add('i3', "DEFINITELY NEED THESE FOR AFTER THAT PTSD DINNER.", 1.45, 4.9, ("PTSD",)); add('i3b', "SMOOTH.", 8.6, 11.1)
add('p1', "LOOK AT ALL THE PTSD PIE!", 4.95, 6.75, ("PTSD", "PIE!")); add('p2', "PTSD PIE EVERYWHERE.", 15.05, 16.75, ("EVERYWHERE.",))
add('f', "OUT OF MY MIND FOR 20 YEARS.", 5.9, 9.05, ("20", "YEARS."))
add('s', "A GOOD NIGHT'S SLEEP.", 1.0, 2.5, ("SLEEP.",)); add('s', "HAVEN'T HAD ONE OF THOSE IN YEARS.", 2.85, 4.25, ("YEARS.",))
add('l1', "THIS USED TO BE THE FIRST AISLE.", 1.9, 3.45, ("FIRST",)); add('l2', "THIS USED TO BE THE MAIN INGREDIENT.", 19.85, 21.4, ("MAIN",)); add('l2b', "NOT THIS YEAR.", 21.47, 22.35, ("NOT", "THIS", "YEAR."), 96)
add('m1', "PRE-WORKOUT.", 1.4, 2.3)
add('m2', "GET YOUR MIND RIGHT FIRST.", 6.35, 8.6, ("MIND",)); add('m2', "IT'S TIME TO GET IN FRONT OF PTSD.", 8.9, 10.95, ("FRONT", "PTSD."))
add('m3', "PREVENTATIVE.", 11.4, 12.8, ("PREVENTATIVE.",)); add('m3', "NOT POST-VENTATIVE. THAT'S ALL WE DO NOW.", 12.95, 15.4)
add('m4', "INTERVENTION.", 15.95, 16.95); add('m4', "PREVENTION.", 17.05, 18.2, ("PREVENTION.",)); add('m4', "POSTVENTION.", 18.5, 19.45)
add('m5', "WHERE ARE YOU AT IN YOUR MENTAL HEALTH?", 20.1, 22.0, ("YOU",))
add('hat', "MEANWHILE, AT CHECKOUT...", 0, 9, ("CHECKOUT...",), 62)
spread('c1', [("I'M LOOKING FOR MY...", "I'm looking for my"), ("CAN I ORDER MY BRAIN?", "can I order my brain"), ("I'M LOOKING FOR MY MIND.", "I'm looking for my mind")], 5.26, 8.9, ("BRAIN?", "MIND."))
add('c2', "CASHIER: \"DO WE HAVE THOSE?\"", 11.25, 12.6, ("CASHIER:",), 62)
add('c3', "\"AISLE 7.\"", 14.3, 16.4, (), 70); add('c3', "I THOUGHT IT WAS IN THE FOOD COURT.", 16.6, 18.9, ("FOOD", "COURT.")); add('c3', "NO?", 19.05, 20.4)
spread('c4', [("I'VE BEEN LOOKING FOR 20 YEARS FOR MY BRAIN.", "I've been looking for 20 years for my brain."), ("I CAN'T FIND IT.", "I've been I can't find it.")], 20.98, 26.25, ("20", "YEARS", "BRAIN."))
add('c5', "CASHIER: \"MAYBE ANOTHER LOCATION.\"", 28.0, 30.8, ("CASHIER:", "LOCATION.\""), 62); add('c5', "OH. AND NO BRAIN.", 30.95, 32.5, ("BRAIN.",))
caps.append(("STORE PA: \"CLEAN UP AT THE EXIT. ONE CART. NO BRAIN.\"", off['pa2'] + 0.25, off['pa2'] + 0.5 + PA2[1] - PA2[0], ("STORE", "PA:", "BRAIN.\""), 58, None))
R = [(36.4, "HERE'S THE REAL RECIPE.", ("REAL",)), (37.86, "A SEAT NEAR THE DOOR.", ("DOOR.",)), (39.12, "A WALK AFTER DINNER.", ("WALK",)), (40.68, "ONE PERSON YOU CAN TEXT.", ("TEXT.",)), (42.38, "AND IT'S OKAY TO LEAVE EARLY.", ("OKAY",)), (44.48, "SERVES EVERYONE AT THE TABLE.", ()), (46.64, "CALL OR TEXT 988 IF YOU NEED HELP.", ("988",)), (48.75, '', ())]
for (a, txt, k), nx in zip(R, R[1:]): add('r', txt, a - 0.05, nx[0] - 0.12, k)
add('b1', "BLOOPER: I FORGOT THE MAIN INGREDIENT.", 0.05, 1.85, ("BLOOPER:",), 62); add('b1', "MY BRAIN!", 1.9, 5.5, ("BRAIN!",), 90)
add('b2', "AND I FORGOT A COUPLE SHOTS OF COURAGE.", 20.75, 23.9, ("COURAGE.",), 62)
add('bl', "I'M BLENDING IN. THEY'LL NEVER KNOW.", 4.4, 6.0, ("BLENDING",)); add('bl', "SUCKERS.", 10.15, 10.95, ("SUCKERS.",), 110); add('fz', "SUCKERS.", 0, 9, ("SUCKERS.",), 120)

# ---- extra overlays: running checklist tag (top right) and the stacking REAL list
GL = lambda z: ImageFont.truetype('GloriaHallelujah.ttf', z)
def tag(name, txt, ok):
    im_ = Image.new('RGBA', (1080, 190), (0, 0, 0, 0)); pp = Image.new('RGBA', (590, 130), (255, 255, 255, 245)); dd = ImageDraw.Draw(pp)
    dd.rectangle([0, 0, 589, 129], outline=(150, 190, 235, 255), width=4); dd.rectangle([20, 38, 70, 88], outline=(25, 35, 120, 255), width=6)
    if ok: dd.line([(26, 60), (42, 82)], fill=(20, 130, 40, 255), width=10); dd.line([(42, 82), (78, 26)], fill=(20, 130, 40, 255), width=10)
    else: dd.line([(22, 36), (72, 90)], fill=(200, 20, 20, 255), width=10); dd.line([(72, 36), (22, 90)], fill=(200, 20, 20, 255), width=10)
    f_ = GL(46)
    while dd.textlength(txt, font=f_) > 480: f_ = GL(f_.size - 3)
    dd.text((92, 22), txt, font=f_, fill=(25, 35, 120, 255)); pp = pp.rotate(-2.5, expand=True, resample=Image.BICUBIC); im_.alpha_composite(pp, (462, 14)); im_.save(f'q/{name}.png')
extra = []
TAGS = [('g1', 'coffee', 1, None), ('g2', 'paper towels', 1, None), ('i1', 'antacid', 1, None), ('g3', 'anti-stress shots', 1, 'g3b'), ('i2', 'strength + energy', 1, None), ('e', 'earplugs (uncle)', 1, None), ('i3', 'wipes', 1, 'i3b'),
        ('p1', 'pie', 1, 'p2'), ('f', 'my mind: not here', 0, None), ('s', 'sleep: SOLD OUT', 0, None), ('l1', 'wine: NOPE', 0, 'l2b')]
segn = dict((x[0], x[1]) for x in S)
for k_, (sg, txt, ok, last_) in enumerate(TAGS):
    tag(f'tg{k_}', txt, ok); e_ = off[last_ or sg] + segn[last_ or sg] / 30; extra.append((f'tg{k_}', 136, off[sg] + 0.15, e_ - 0.05))
o_ = off['r'] - A['r']; rl = Image.new('RGBA', (1080, 470), (0, 0, 0, 0))
for k_, (t_, txt) in enumerate([(37.86, 'seat near the door'), (39.12, 'walk after dinner'), (40.68, 'one person you can text'), (42.38, 'ok to leave early')]):
    dd = ImageDraw.Draw(rl); y_ = 20 + k_ * 108; dd.rounded_rectangle([430, y_, 1050, y_ + 94], 10, fill=(255, 255, 255, 240))
    dd.line([(448, y_ + 46), (466, y_ + 70)], fill=(20, 130, 40, 255), width=10); dd.line([(466, y_ + 70), (500, y_ + 18)], fill=(20, 130, 40, 255), width=10)
    dd.text((516, y_ + 6), txt, font=GL(40), fill=(25, 35, 120, 255)); rl.save(f'q/rl{k_}.png'); nx_ = [39.12, 40.68, 42.38, 48.7][k_]
    extra.append((f'rl{k_}', 310, o_ + t_ + 0.35, o_ + nx_ + 0.35 if k_ < 3 else off['r'] + segn['r'] / 30 - 0.03))

ins = '-i q/basev.mp4 -loop 1 -framerate 30 -i q/ov.png '; fc = '[0:v][1:v]overlay=0:0:shortest=1[o0];'; last = 'o0'; items = []
for k, (txt, a, b, keys, size, y) in enumerate(caps):
    h = cap(f'c{k}', txt, keys, size); items.append((f'c{k}', (1540 - h) if y is None else y, a, b))
items += extra
for k, (png, y, a, b) in enumerate(items):
    ins += f'-loop 1 -framerate 5 -i q/{png}.png '
    fc += f"[{last}][{2+k}:v]overlay=0:{y}:enable='between(t,{a:.2f},{b:.2f})'[o{k+1}];"; last = f'o{k+1}'
caps_n = len(items)
n = 2 + caps_n; MEND = off['r'] + 0.4
ins += f'-i q/basea.wav -stream_loop 2 -i {MUSIC} '
fc += (f"[{n}:a]asplit[vx][sc];[{n+1}:a]aresample={SR},{ST},volume=-13dB,afade=t=in:d=0.6,atrim=0:{MEND:.2f},afade=t=out:st={MEND-0.6:.2f}:d=0.6,apad=whole_dur={TOTAL:.3f}[mu];"
       f"[mu][sc]sidechaincompress=threshold=0.04:ratio=3:attack=20:release=500[md];[vx][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=11,aresample={SR}[a]")
open('q/fc.txt', 'w').write(fc)
_run(f'ffmpeg -v error -y {ins}-filter_complex_script q/fc.txt -map "[{last}]" -map "[a]" -frames:v {t} -t {TOTAL:.3f} -r 30 -c:v libx264 -preset veryfast -crf 25 -pix_fmt yuv420p -c:a aac -b:a 192k -ar {SR} MAYDAY-Day-25-v3.mp4')
json.dump({'off': off, 'total': TOTAL, 'caps': [(c[0], round(c[1], 2), round(c[2], 2)) for c in caps]}, open('q/meta.json', 'w'), indent=1)
print(_run('ffprobe -v error -show_entries format=duration,size -of csv=p=0 MAYDAY-Day-25-v3.mp4'))
