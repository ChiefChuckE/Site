exec(open('/tmp/claude-0/d26/w/b26head.py').read())
OUT = 'MAYDAY-Day-26-v1.mp4'
ANN = '/mnt/user-data/uploads/Movies/d26/announcer.mp3'
GL = lambda z: ImageFont.truetype('GloriaHallelujah.ttf', z)
PMK = lambda z: ImageFont.truetype('PermanentMarker-Regular.ttf', z)

# ---------- graphics
def blank(): return Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
ov = blank(); d = ImageDraw.Draw(ov)
d.rounded_rectangle([40, 150, 430, 236], 16, fill=RED)
for dx, dy in ((-3, 0), (3, 0), (0, -3), (0, 3), (4, 6)): d.text((62 + dx, 150 + dy), "MAYDAY", font=MB(66), fill=(0, 0, 0, 255))
d.text((62, 150), "MAYDAY", font=MB(66), fill=W_)
for dx, dy in ((-3, 0), (3, 0), (0, -3), (0, 3), (4, 6)): d.text((60 + dx, 244 + dy), "DAY 26 OF 61", font=MB(44), fill=(0, 0, 0, 255))
d.text((60, 244), "DAY 26 OF 61", font=MB(44), fill=Y_)
d.rounded_rectangle([40, 1834, 1040, 1876], 12, fill=(0, 0, 0, 150)); ctext(d, "Comedy with a point. Fake sponsors. PTSD is a real injury.", 1840, MB(25, 'Bold Italic'), W_)
ov.save('q/ov.png')
ft = Image.new('RGBA', (1080, 170), (0, 0, 0, 0)); d = ImageDraw.Draw(ft)
d.rectangle([0, 0, 1080, 86], fill=RED); ctext(d, "STRUGGLING? CALL OR TEXT 988", 10, MB(56), W_, o=4)
d.rectangle([0, 86, 1080, 170], fill=(0, 0, 0, 215))
ctext(d, "VETERANS: 988, PRESS 1", 92, MB(30), Y_); ctext(d, "RESPONDERS: SAFE CALL NOW 206-459-3020", 128, MB(30), Y_)
ft.save('q/foot.png')
# show title over the opening B-roll
ti = blank(); d = ImageDraw.Draw(ti)
d.rounded_rectangle([90, 0, 990, 470], 40, fill=(15, 15, 15, 225), outline=(255, 214, 0, 255), width=8)
ctext(d, "COOKING WITH", 40, PMK(96), Y_); ctext(d, "CHEF CHUCK", 160, PMK(150), W_)
ctext(d, "TODAY: PTSD PIE", 355, MB(52), (255, 120, 60, 255)); ti.save('q/title.png')
# lower third
lt = Image.new('RGBA', (1080, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(lt)
d.rectangle([0, 20, 760, 120], fill=(255, 214, 0, 245)); d.rectangle([0, 120, 640, 180], fill=(15, 15, 15, 235))
d.text((40, 30), "CHEF CHUCK", font=MB(70), fill=(15, 15, 15, 255)); d.text((40, 126), "Executive Chef · Station 1601", font=MB(38, 'Bold Italic'), fill=W_)
lt.save('q/lt.png')
def card(name, big, small, sub=''):
    im = Image.new('RGB', (1080, 1920), (18, 18, 18)); d = ImageDraw.Draw(im)
    for i in range(0, 1080, 90):
        for j in range(0, 1920, 90):
            if (i // 90 + j // 90) % 2 == 0: d.rectangle([i, j, i + 89, j + 89], fill=(190, 30, 30))
            else: d.rectangle([i, j, i + 89, j + 89], fill=(245, 240, 228))
    d.rounded_rectangle([80, 640, 1000, 1240], 40, fill=(18, 18, 18), outline=(255, 214, 0), width=10)
    ctext(d, "COOKING WITH CHEF CHUCK", 690, MB(46), (255, 214, 0))
    y = 790
    for ln in big: ctext(d, ln, y, PMK(110), (255, 255, 255)); y += 140
    ctext(d, small, y + 10, MB(46, 'Bold Italic'), (255, 214, 0))
    if sub: ctext(d, sub, y + 80, MB(36), (220, 220, 220))
    im.save(f'q/{name}.png')
card('bump1', ["A WORD FROM", "OUR SPONSORS"], "Nobody Cares · Paper Tigers")
card('bump2', ["WE'LL BE", "RIGHT BACK"], "Coming up: fresh out of the oven")
im = Image.new('RGB', (1080, 1920), (14, 14, 14)); d = ImageDraw.Draw(im)
d.rounded_rectangle([140, 300, 940, 420], 22, fill=(200, 20, 20)); ctext(d, "MAYDAY · DAY 26 OF 61", 320, MB(60), (255, 255, 255))
ctext(d, "THE REAL RECIPE", 560, PMK(110), (255, 214, 0))
y = 740
for ln in ["Let it breathe.", "One person you trust.", "Sleep. A lot of humor.", "Help. Ask for it."]: ctext(d, ln, y, MB(64), (255, 255, 255)); y += 100
ctext(d, "Serves everyone at your table.", y + 40, MB(50, 'Bold Italic'), (255, 214, 0))
ctext(d, "TOMORROW · DAY 27: CHECKED OUT", 1380, MB(46), (220, 220, 220))
im.save('q/cardend.png')

# ---------- segments (times = each clip's WAV clock)
S = []
MIR = {'c14004','c14008','c14014','c14018','c14020','c14030','c14032','c14042','c14044'}
def T(name, clip, a, d, **k):
    if clip in MIR: k.setdefault('pre', 'hflip,')
    S.append((name, talk(name, clip, a, d, **k), clip, a))
def Q(name, n): S.append((name, n, None, 0))
Q('o1', quiet('o1', 'c3116', 0.0, 5.0))
T('s1', 'c14014', 1.75, 7.5); T('s2', 'c14014', 9.75, 19.75); T('s3', 'c14014', 32.45, 7.45)
T('i1', 'c14008', 0.6, 7.1); T('i2', 'c14008', 12.6, 5.0); T('i3', 'c14008', 24.8, 6.5); T('i4', 'c14008', 34.4, 4.05); T('i5', 'c14008', 42.9, 7.7)
T('w', 'c14042', 0.9, 2.55)
T('ph', 'c14020', 10.3, 6.5)
T('ov1', 'c14018', 8.75, 2.95)
Q('bump2', still('bump2', 'bump2', 2.9, 0.0006))
T('sp', 'c14032', 2.95, 34.6)
T('ov2', 'c14018', 24.3, 9.7)
nt = fr(0.9)
run(f'ffmpeg -v error -y -f lavfi -i "nullsrc=s=270x480:r=30" -vf "geq=lum=\'random(1)*255\':cb=128:cr=128,scale=1080:1920:flags=neighbor,eq=contrast=1.3" -frames:v {nt} {VENC} q/tr.mp4')
wav_exact('tr', nt, f'-f lavfi -t 1.2 -i "anoisesrc=color=white:sample_rate={SR}:amplitude=0.5"', 'highpass=f=300,volume=0.35,afade=t=in:d=0.02,afade=t=out:st=0.84:d=0.05'); Q('tr', nt)
T('b5', 'c14034', 0.5, 18.57)
# tribute: freeze on the Bob cloth
_run('ffmpeg -v error -y -ss 19.05 -i src/c14034.mov -vf "' + FIT + '" -frames:v 1 q/bobfr.png')
Image.open('q/bobfr.png').convert('RGB').save('q/trib.png')
n_ = fr(1.2); VF_ = """zoompan=z='1+0.0012*on':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30"""
run(f'ffmpeg -v error -y -loop 1 -framerate 30 -i q/trib.png -vf "{VF_}" -frames:v {n_} {VENC} q/trib.mp4'); silence('trib', n_); Q('trib', n_)
ph_ = Image.open('q/bob_src.jpg').convert('RGB').crop((0, 0, 554, 458)).resize((1080, 893), Image.LANCZOS)
bm = Image.new('RGB', (1080, 1920), (8, 8, 8)); bm.paste(ph_, (0, 230)); d = ImageDraw.Draw(bm)
d.rectangle([0, 1123, 1080, 1223], fill=(141, 1, 4)); ctext(d, "MARCH 2, 2017", 1138, MB(64), (255, 255, 255))
ctext(d, "For all who had the honor", 1300, MB(54, 'Bold Italic'), (255, 214, 0)); ctext(d, "to work with him,", 1368, MB(54, 'Bold Italic'), (255, 214, 0))
ctext(d, "we are thankful for his leadership.", 1436, MB(48, 'Bold Italic'), (255, 214, 0))
ctext(d, "Rest easy, Chief.", 1560, MB(64), (255, 255, 255))
bm.save('q/bobmem.png')
Q('bobm', still('bobm', 'bobmem', 14.0, 0.0003))

off = {}; A = {}; t = 0
for nme, n, clip, a in S: off[nme] = t / 30; A[nme] = a; t += n
TOTAL = t / 30; print({k: round(v, 2) for k, v in off.items()}, 'TOTAL', round(TOTAL, 2), flush=True)
open('q/v.txt', 'w').write(''.join(f"file '{s[0]}.mp4'\n" for s in S))
_run('ffmpeg -v error -y -f concat -safe 0 -i q/v.txt -c copy q/basev.mp4')
buf = []
for nme, n, _, _ in S:
    w = wave.open(f'q/{nme}.wav'); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2); want = n * SR // 30
    buf.append(x[:want] if len(x) >= want else np.vstack([x, np.zeros((want - len(x), 2), np.int16)]))
allx = np.vstack(buf).astype(np.int32)
def rdw(f):
    w_ = wave.open(f); return np.frombuffer(w_.readframes(w_.getnframes()), dtype=np.int16).reshape(-1, 2).astype(np.int32)
_run(f'ffmpeg -v error -y -i {ANN} -af "loudnorm=I=-15:TP=-2,aresample={SR}" -ar {SR} -ac 2 q/ann.wav')
an = rdw('q/ann.wav')
def mix(x_, at, g=1.0):
    o_ = int(at * SR); x_ = (x_[:max(0, len(allx) - o_)] * g).astype(np.int32); allx[o_:o_ + len(x_)] += x_
for (a_, b_), seg_, dl in (((0.0, 4.5), 'o1', 0.3), ((7.95, 10.37), 'bump2', 0.25)):
    mix(an[int(a_ * SR):int(b_ * SR)], off[seg_] + dl)
tt = np.arange(int(0.35 * SR)) / SR
ding = (np.sin(2 * np.pi * 1568 * tt) * np.exp(-tt * 9) * 7000 + np.sin(2 * np.pi * 2093 * tt) * np.exp(-tt * 11) * 4000).astype(np.int32)
for at in (6.7, 15.8, 23.0): mix(ding[:, None].repeat(2, 1), off['sp'] + at - A['sp'])
tc = np.arange(int(0.12 * SR)) / SR; chirp = (np.sign(np.sin(2 * np.pi * 3100 * tc)) * 2600).astype(np.int32)[:, None].repeat(2, 1)
import os as _os
if _os.path.exists('q/pipes.wav'):
    pp = (rdw('q/pipes.wav')[int(17.0 * SR):] * 1.5).astype(np.int32); pt = off['trib']; L = len(allx) - int(pt * SR); pp = pp[:L]
    fo = np.ones(len(pp)); nf = int(2.5 * SR); fo[-nf:] = np.linspace(1, 0, nf); pp = (pp * fo[:, None]).astype(np.int32)
    mix(pp, pt)
allx = np.clip(allx, -32767, 32767).astype(np.int16); w = wave.open('q/basea.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(allx.tobytes()); w.close()
print('video frames', t, 'audio s', round(len(allx) / SR, 4), 'video s', round(TOTAL, 4), flush=True)

# ---------- captions
caps = []
segn = dict((s[0], s[1]) for s in S)
def add(seg, txt, a, b, keys=(), size=70, y=None):
    if seg not in off: return
    o = off[seg] - A[seg]; s0, s1 = off[seg], off[seg] + segn[seg] / 30
    caps.append((txt, max(s0, o + a), min(s1 - 0.02, o + b), keys, size, y))
def whole(seg, txt, keys=(), size=62, y=None):
    if seg not in off: return
    caps.append((txt, off[seg], off[seg] + segn[seg] / 30 - 0.02, keys, size, y))
add('s1', "WELCOME TO COOKING WITH CHEF CHUCK.", 1.92, 3.8, ("CHEF", "CHUCK.")); add('s1', "NOT CHIEF.", 4.86, 5.7); add('s1', "CHEF.", 6.02, 6.95, (), 90)
add('s1', "DIFFERENT UNIFORM.", 7.1, 8.2); add('s1', "SAME FIGHT.", 8.42, 9.25, ("SAME", "FIGHT."))
add('s2', "TODAY'S RECIPE IS A FIRE STATION CLASSIC.", 9.9, 12.4, ("FIRE", "STATION")); add('s2', "IT'S BEEN PASSED DOWN FOR GENERATIONS...", 13.26, 15.9)
add('s2', "...AND NOBODY TALKS ABOUT IT.", 16.18, 18.2, ("NOBODY",)); add('s2', "IT'S SERVED YEAR-ROUND.", 18.54, 20.2); add('s2', "THAT'S RIGHT, I'M TALKING ABOUT...", 20.46, 22.6)
add('s2', "P... T... S... D...", 22.7, 25.0, ("P...", "T...", "S...", "D..."), 90); add('s2', "PIE.", 25.18, 26.4, ("PIE.",), 110)
add('s2', "AND TODAY I'M SHARING MY RECIPE FOR THE FIRST TIME.", 26.58, 29.45)
add('s3', "THE FAMILY RECIPE.", 32.6, 34.6, ("FAMILY",)); add('s3', "A LITTLE STAINED.", 35.06, 36.5); add('s3', "NOBODY'S EVER CLEANED IT UP.", 36.66, 38.3); add('s3', "THAT'S PART OF THE RECIPE.", 38.5, 39.85)
add('sp', "I'D LIKE TO THANK TODAY'S SPONSORS.", 3.14, 5.6); add('sp', "NOBODY CARES.", 6.84, 8.0, ("NOBODY", "CARES."), 84)
add('sp', "AT NOBODY CARES, THEY PRIDE THEMSELVES ON NOT GIVING A CHUCK ABOUT YOU.", 8.26, 12.5, ("CHUCK",)); add('sp', "NOBODY CARES. ALWAYS ON YOUR SIDE.", 12.92, 15.5)
add('sp', "AND PAPER TIGERS,", 15.92, 17.1, ("PAPER", "TIGERS,"), 84); add('sp', "WHERE YOU'RE ALWAYS NUMBER ONE...", 17.32, 19.0); add('sp', "...ON PAPER.", 19.24, 20.5, ("PAPER.",), 84)
add('sp', "AND UNNORMAL ANTI-STRESS SHOTS.", 23.16, 25.9, ("ANTI-STRESS", "SHOTS.")); add('sp', "NOW AVAILABLE IN TWO SIZES:", 26.42, 28.3)
add('sp', "REGULAR STRESS...", 28.66, 30.0, ("REGULAR",)); add('sp', "...AND SUPER STRESS.", 30.26, 31.6, ("SUPER",)); add('sp', "AND THEY ACTUALLY COME IN A SHOT.", 31.78, 34.5)
add('sp', "BLACK FRIDAY SPECIAL, WHEREVER BAD DECISIONS ARE SOLD.", 34.78, 37.5, ("BAD", "DECISIONS"))
add('i1', "FIRST, WE START WITH A CUP OF I'M FINE.", 0.86, 3.9, ("I'M", "FINE.")); add('i1', "WE ALWAYS USE TOO MUCH.", 4.42, 6.3); add('i1', "EVERYBODY DOES.", 6.66, 7.65)
add('i2', "NEXT, TWO SPOONS OF SHORT FUSE.", 12.84, 15.6, ("SHORT", "FUSE.")); add('i2', "HANDLE HOT.", 16.1, 17.5); add('i2', "KEEP AWAY FROM FAMILY.", 19.02, 20.8, ("FAMILY.",)); add('i2', "TOO LATE.", 21.8, 22.38, (), 84)
add('i3', "AND THEN A SPLASH OF DENIAL.", 25.04, 27.2, ("DENIAL.",)); add('i3', "EXTRA VIRGIN.", 27.38, 28.9); add('i3', "NEVER OPENED. SEE?", 29.5, 31.28)
add('i4', "GUILT.", 34.68, 35.9, ("GUILT.",), 90); add('i4', "PAIRS WELL WITH 3 IN THE MORNING.", 36.12, 38.4, ("3",)); add('i4', "SHAKE WELL.", 39.14, 40.58)
add('i5', "SLEEP.", 43.14, 44.4, ("SLEEP.",), 90); add('i5', "JUST A PINCH.", 44.66, 46.4); add('i5', "TOO BAD WE'VE BEEN OUT OF IT SINCE 2004.", 47.48, 50.6, ("2004.",)); add('i5', "NOT IN THIS KITCHEN ANYMORE.", 51.4, 53.88)
add('w', "NOW YOU'RE GOING TO BEAT IT UNTIL IT STOPS TALKING.", 1.18, 3.35, ("STOPS", "TALKING.")); add('w', "LISTEN... PERFECT.", 3.5, 5.98)
add('ph', "HELLO?", 2.1, 3.4); add('ph', "YEAH, I'M FINE.", 3.7, 5.3, ("I'M", "FINE.")); add('ph', "A LITTLE MORE I'M FINE NEVER HURT ANYBODY.", 6.2, 10.2)
add('ph', "BITTER.", 13.42, 14.25, (), 90); add('ph', "LIKE MY LAST PERFORMANCE REVIEW.", 14.34, 16.75, ("PERFORMANCE", "REVIEW."))
add('st', "STUFF IT ALL DOWN...", 18.5, 21.0, ("STUFF",)); add('st', "...AND BAKE IT UNDER PRESSURE FOR 20 YEARS.", 21.1, 24.9, ("PRESSURE", "20", "YEARS.")); add('st', "SET THE TIMER FOR 20 YEARS.", 25.98, 27.98, ("20", "YEARS."))
add('ov1', "YOU'RE GOING TO WANT TO BAKE IT.", 2.96, 5.0); add('ov1', "I LIKE TO GO HIGH. AS HIGH AS YOU CAN GO.", 5.34, 8.7, ("HIGH",)); add('ov1', "BAKE IT AT 350 FOR 20 MINUTES.", 8.94, 11.68, ("350",))
add('st2', "NOW... HERE'S ONE I MADE EARLIER.", 29.26, 32.28)
add('ov2', "HERE'S ONE FRESH OUT OF THE OVEN.", 24.48, 26.5); add('ov2', "LET'S CHECK IT OUT.", 26.72, 29.0); add('ov2', "LOOK AT THAT PTSD PIE.", 30.04, 33.98, ("PTSD", "PIE."))
add('ov3', "LOOK AT THAT PTSD PIE, FRESH OUT OF THE OVEN.", 39.9, 44.18, ("PTSD", "PIE,"))
add('se', "SERVING SUGGESTION:", 2.82, 4.2); add('se', "SERVE COLD AT THE DINNER TABLE...", 4.44, 6.6); add('se', "...TO THE PEOPLE YOU LOVE.", 6.78, 8.4, ("LOVE.",)); add('se', "AND DON'T SAY A WORD.", 8.64, 9.78)
add('tu', "HERE'S THE PTSD RECIPE FOR PIE.", 19.06, 22.3); add('tu', "AND HERE'S THE REAL RECIPE.", 22.46, 24.7, ("REAL",)); add('tu', "NOW, THAT RECIPE...", 24.88, 29.98)
add('rr1', "HERE'S THE REAL RECIPE.", 3.04, 5.28, ("REAL",)); add('rr2', "HUMOR... AND HELP.", 6.42, 9.6, ("HUMOR...", "HELP."))
add('rr2', "IT'S A NEW RECIPE.", 11.2, 13.1); add('rr2', "LET IT BREATHE.", 13.3, 14.7, ("BREATHE.",)); add('rr2', "ADD ONE PERSON YOU TRUST.", 14.94, 17.6, ("TRUST.",))
add('rr2', "FOLD IN SOME SLEEP.", 17.9, 19.8, ("SLEEP.",)); add('rr2', "A LOT OF HUMOR.", 20.14, 22.9, ("HUMOR.",)); add('rr2', "AND HELP.", 23.28, 24.9, ("HELP.",)); add('rr2', "YOU HAVE TO ASK FOR IT.", 25.08, 26.58, ("ASK",))
add('fin', "SERVES EVERYONE AT YOUR TABLE.", 1.9, 3.6); add('fin', "HAPPY THANKSGIVING!", 3.76, 5.7, ("THANKSGIVING!",)); add('fin', "IF THE OLD RECIPE IS ALL YOU'VE GOT...", 5.98, 8.5); add('fin', "CALL OR TEXT 988.", 8.84, 10.28, ("988.",), 84)
add('b1', "BLOOPER: WAIT A MINUTE...", 1.8, 3.9, ("BLOOPER:",)); add('b1', "THAT'S NOT IT. WHOA!", 4.26, 7.0); add('b1', "THAT'S NOT A RECIPE.", 8.04, 9.48)
add('b2', "SMOKE DETECTOR CHECK.", 8.0, 12.0, ("SMOKE",)); add('b2', "CHEF CHUCK DOES NOT TRUST THE SMOKE DETECTOR.", 16.0, 23.4)
add('b3', "RELAX. I KNOW A GUY.", 6.08, 7.58, ("GUY.",), 80)
whole('b4', "QUALITY CONTROL: OUR PTSD THERAPY DOG.", ("PTSD", "THERAPY", "DOG."))
add('b5', "ARE WE ON?", 2.62, 3.7); add('b5', "YOU GUYS GOTTA TELL ME WHEN WE COME ON!", 3.82, 6.4); add('b5', "DOING THAT TO ME ALL THE TIME.", 6.68, 8.6)
add('b5', "CAN WE GET SOME OTHER CLOTHS IN HERE?", 15.42, 17.4); add('b5', "DO WE REALLY HAVE TO HAVE A BOB CLOTH?", 17.62, 20.0, ("BOB", "CLOTH?"))

# ---------- extra overlays: title, lower third, tribute text panels
extra = []
extra.append(('title', 620, off['o1'] + 0.2, off['s1'] - 0.03))
extra.append(('foot', 1750, off['bobm'] + 3.0, TOTAL)); extra.append(('lt', 1040, off['s1'] + 0.4, off['s1'] + 6.5))
TR1 = ["In the early 1990s, while in Riverside,", "he became active in then CDF Firefighters,", "CAL FIRE Local 2881, first as a rank-and-file", "representative, then as Chapter Director and", "Region VI Director/Vice President."]
TR2 = ["He was elected general vice president of", "the statewide union in 2001, and became", "its president in 2003. When he retired in 2012,", "he was the longest-serving president of the now", "largest firefighter union in North America."]
TR3 = ["For all who had the honor to work with him,", "we are thankful for his leadership.", "", "Rest easy, Bob."]
for k, lines in enumerate((TR1, TR2, TR3)):
    p = Image.new('RGBA', (1080, 520), (0, 0, 0, 0)); d = ImageDraw.Draw(p)
    d.rectangle([0, 0, 1080, 520], fill=(10, 10, 10, 255)); y = 20
    for ln in lines:
        f = MB(44) if k < 2 else MB(50, 'Bold Italic')
        z = 44 if k < 2 else 50
        while d.textlength(max(lines, key=lambda q_: d.textlength(q_, font=f)), font=f) > 1000: z -= 1; f = MB(z) if k < 2 else MB(z, 'Bold Italic')
        d.text(((1080 - d.textlength(ln, font=f)) / 2, y), ln, font=f, fill=(235, 235, 235, 255) if k < 2 else (255, 214, 0, 255)); y += 64 if k < 2 else 78
    p.save(f'q/tr{k}.png')
t0 = off['trib']; segs = []
for k, (a_, b_) in enumerate(segs): extra.append((f'tr{k}', 1425, t0 + a_, t0 + b_ - 0.04))

ins = '-i q/basev.mp4 -loop 1 -framerate 30 -i q/ov.png '; fc = "[0:v][1:v]overlay=0:0:shortest=1:enable='lt(t," + f"{off['trib']:.2f}" + ")'[o0];"; last = 'o0'; items = []
for k, (txt, a, b, keys, size, y) in enumerate(caps):
    h = cap(f'c{k}', txt, keys, size); items.append((f'c{k}', (1800 - h) if y is None else y, a, b))
items += extra
for k, (png, y, a, b) in enumerate(items):
    ins += f'-loop 1 -framerate 5 -i q/{png}.png '
    fc += f"[{last}][{2+k}:v]overlay=0:{y}:enable='between(t,{a:.2f},{b:.2f})'[o{k+1}];"; last = f'o{k+1}'
n = 2 + len(items); MEND = off['tr']
ins += f'-i q/basea.wav -stream_loop 4 -i {MUSIC} '
fc += (f"[{n}:a]asplit[vx][sc];[{n+1}:a]aresample={SR},{ST},volume=-14dB,afade=t=in:d=0.6,atrim=0:{MEND:.2f},afade=t=out:st={MEND-0.8:.2f}:d=0.8,apad=whole_dur={TOTAL:.3f}[mu];"
       f"[mu][sc]sidechaincompress=threshold=0.04:ratio=3:attack=20:release=500[md];[vx][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=11,aresample={SR}[a]")
open('q/fc.txt', 'w').write(fc)
_run(f'ffmpeg -v error -y {ins}-filter_complex_script q/fc.txt -map "[{last}]" -map "[a]" -frames:v {t} -t {TOTAL:.3f} -r 30 -c:v libx264 -preset veryfast -crf 25 -pix_fmt yuv420p -c:a aac -b:a 192k -ar {SR} {OUT}')
json.dump({'off': off, 'total': TOTAL, 'caps': [(c[0], round(c[1], 2), round(c[2], 2)) for c in caps]}, open('q/meta.json', 'w'), indent=1)
print(_run(f'ffprobe -v error -show_entries format=duration,size -of csv=p=0 {OUT}'))
