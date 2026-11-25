"""MAYDAY Day 24 v3. Sync-safe build: every segment is a whole number of frames,
video and audio are rendered separately at exactly the same length, then joined."""
import subprocess, os, re, json, wave, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
os.chdir('/tmp/claude-0/d24/w'); os.makedirs('q', exist_ok=True)
src = open('build24.py').read()
exec(src[src.index('def run'):src.index('# ---------- segments')].replace("'p/", "'q/").replace("f'p/", "f'q/"))   # run, dur, fonts, cap, capsule, card, overlay
FI = '/tmp/claude-0/fonts/gf/ofl/montserrat/Montserrat-Italic[wght].ttf'
_run = run
def run(c):
    last = c.split()[-1]
    if c.startswith('ffmpeg') and last.startswith('q/') and last.endswith(('.mp4', '.wav')) and os.path.exists(last) and os.path.getsize(last) > 1000: return ''
    return _run(c)
VO = '/mnt/user-data/uploads/Movies/d24/'
INTRO, SIDE, MUSIC, DISC = VO + '138377.mp3', VO + '289678.mp3', VO + '1458322.mp3', VO + 'disc.mp3'
SR = 48000
VENC = '-r 30 -c:v libx264 -preset veryfast -crf 17 -pix_fmt yuv420p -an'
VOFF = {'a13699': 0.0, 'a13697': 0.13, 'u13695': 0.11, 'n3054': 0.0}
VAF = 'highpass=f=90,acompressor=threshold=-24dB:ratio=3:attack=5:release=120,loudnorm=I=-16:TP=-2:LRA=7'
BW = ',hue=s=0,eq=contrast=1.15:brightness=-0.04'

def fr(d): return max(1, round(d * 30))
def vseg(name, srcf, vt, d, extra='', pre=''):
    n = fr(d)
    run(f'ffmpeg -v error -y -ss {vt:.3f} -i {srcf} -vf "{pre}{FIT}{extra}" -frames:v {n} {VENC} q/{name}.mp4'); return n
def wav_exact(name, n, filt_input, filt):
    d = n / 30
    run(f'ffmpeg -v error -y {filt_input} -af "{filt},aresample={SR},aformat=sample_fmts=s16:channel_layouts=stereo,apad,atrim=0:{d:.5f}" -ar {SR} -ac 2 q/{name}.wav')
def silence(name, n):
    run(f'ffmpeg -v error -y -f lavfi -t {n/30:.5f} -i anullsrc=r={SR}:cl=stereo -ar {SR} -ac 2 q/{name}.wav')
def talk(name, clip, a, d, extra='', pre=''):
    """a = start on the WAV clock; video is cut at a + VOFF so lips match."""
    n = vseg(name, clip + '.mov', a + VOFF[clip], d, extra, pre)
    wav_exact(name, n, f'-ss {a:.3f} -t {n/30 + 0.3:.3f} -i {clip}.wav', VAF); return n
def quiet(name, clip, vt, d, extra='', pre=''):
    n = vseg(name, clip + '.mov', vt, d, extra, pre); silence(name, n); return n
def still(name, png, d):
    n = fr(d)
    run(f'ffmpeg -v error -y -loop 1 -framerate 30 -i q/{png}.png -vf "zoompan=z=\'1+0.0005*on\':d=1:x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':s=1080x1920:fps=30,fade=t=in:d=0.25" -frames:v {n} {VENC} q/{name}.mp4'); silence(name, n); return n

segs = []
segs.append(('s1a', quiet('s1a', 'u13681', 1.5, 4.2, BW)))
segs.append(('s1b', quiet('s1b', 'a13693', 12.4, 3.9, BW)))

# ---- s2: pitch, un-mirrored, with the real prescription label blurred around the LEADERSHIP sticker
A2, D2 = 1.75, 8.8
import labelblur
n2 = fr(D2); os.makedirs('q/s2f', exist_ok=True)
for f in glob.glob('q/s2f/*.jpg'): os.remove(f)
run(f'ffmpeg -v error -y -ss {A2:.3f} -i a13699.mov -vf "hflip,{FIT}" -frames:v {n2} -q:v 2 q/s2f/%04d.jpg')
res = {i: labelblur.regions(Image.open(f'q/s2f/{i:04d}.jpg').convert('RGB')) for i in range(1, n2 + 1)}
ex = [i for i in res if res[i][0] == 'exact']
print('label: exact in', len(ex), 'frames', (min(ex), max(ex)) if ex else None)
for i in range(1, n2 + 1):
    kind, bx = res[i]
    if kind == 'full' and not any(abs(i - j) <= 12 for j in ex): continue
    if kind == 'none' and ex and min(ex) < i < max(ex): kind, bx = 'full', [(300, 1050, 1080, 1800)]
    if bx:
        im = Image.open(f'q/s2f/{i:04d}.jpg').convert('RGB'); labelblur.apply(im, bx).save(f'q/s2f/{i:04d}.jpg', quality=95)
run(f'ffmpeg -v error -y -framerate 30 -i q/s2f/%04d.jpg -frames:v {n2} {VENC} q/s2.mp4')
wav_exact('s2', n2, f'-ss {A2:.3f} -t {n2/30 + 0.3:.3f} -i a13699.wav', VAF); segs.append(('s2', n2))

segs.append(('s3', still('s3', 'card1', 2.6)))
A4 = 1.05; segs.append(('s4', talk('s4', 'a13697', A4, 2.65, pre='hflip,')))
side_d = dur(SIDE); TEMPO = 1.12; side_len = side_d / TEMPO; q4 = (side_len + 0.6) / 4
segs.append(('s5a', quiet('s5a', 'u13691', 8.6, q4, pre='setpts=2.0*PTS,')))
segs.append(('s5b', quiet('s5b', 'u13691', 23.0, q4)))
segs.append(('s5c', quiet('s5c', 'a13689', 5.0, q4)))
segs.append(('s5d', quiet('s5d', 'a13689', 12.6, q4)))
A6a, A6b = 1.25, 11.4
segs.append(('s6a', talk('s6a', 'u13695', A6a, 8.75)))
segs.append(('s6b', talk('s6b', 'u13695', A6b, 6.2)))

# ---- s7: end card with scrolling fine print, rapid-fire disclaimer runs the whole time
DT = 1.75; disc_len = dur(DISC) / DT; n7 = fr(disc_len + 0.5)
card('card2', "LEADERSHIP", "(accountability, extended-release)", ["ASK YOUR CHIEF IF IT'S RIGHT", "FOR YOUR DEPARTMENT."])
fine = ("LEADERSHIP is not available in all departments. Results may vary. Do not operate a fire engine while ignoring your crew. "
        "LEADERSHIP may cause eye contact, honest conversations and follow-through. If accountability lasts more than four hours, congratulations. "
        "Not a substitute for actual treatment, which is real, and which works. Void where egos are prohibited. "
        "Consult your chief, your captain, or anyone who actually listens. See your union rep for details. ")
f = MB(30, 'Bold Italic'); d0 = ImageDraw.Draw(Image.new('RGB', (10, 10))); lines = []; cur = ''
for w in (fine * 2).split():
    if d0.textlength(cur + ' ' + w, font=f) > 940: lines.append(cur); cur = w
    else: cur = (cur + ' ' + w).strip()
lines.append(cur); LH = 40; tall = Image.new('RGBA', (1080, LH * len(lines) + 20), (0, 0, 0, 0)); dd = ImageDraw.Draw(tall)
for i, ln in enumerate(lines): dd.text(((1080 - dd.textlength(ln, font=f)) / 2, 10 + i * LH), ln, font=f, fill=(10, 30, 80, 255))
tall.save('q/fine.png'); SP = (tall.height - 240) / (n7 / 30)
run(f'ffmpeg -v error -y -loop 1 -framerate 30 -i q/card2.png -loop 1 -framerate 30 -i q/fine.png -filter_complex "[1:v]crop=1080:240:0:\'min(ih-240,{SP:.2f}*t)\'[fp];[0:v][fp]overlay=0:1290,fade=t=in:d=0.25" -frames:v {n7} {VENC} q/s7.mp4')
silence('s7', n7); segs.append(('s7', n7))

# ---- transition: colour bars + tone
nt = fr(0.9)
run(f'ffmpeg -v error -y -f lavfi -i "smptebars=s=1080x1920:r=30" -frames:v {nt} {VENC} q/tr.mp4')
wav_exact('tr', nt, f'-f lavfi -t 1.2 -i "sine=frequency=1000:sample_rate={SR}"', 'volume=0.18,afade=t=in:d=0.02,afade=t=out:st=0.82:d=0.06'); segs.append(('tr', nt))

# ---- blooper at the very end: the bag
ABL = 0.1; segs.append(('bl1', talk('bl1', 'n3054', ABL, 6.65)))
nb = fr(4.66 * 2 + 0.9)
run(f'ffmpeg -v error -y -ss 6.75 -t 4.66 -i n3054.mov -vf "{FIT},setpts=2.0*PTS,tpad=stop_mode=clone:stop_duration=1.2" -frames:v {nb} {VENC} q/bl2.mp4')
wav_exact('bl2', nb, '-ss 6.75 -t 4.66 -i n3054.wav', f'highpass=f=60,asetrate=16000*0.5,aresample={SR},aecho=0.8:0.6:120:0.25,loudnorm=I=-17:TP=-2:LRA=9'); segs.append(('bl2', nb))

# ---- join: video list and audio list separately (same frame counts), then mux
off = {}; t = 0
for nme, n in segs: off[nme] = t / 30; t += n
TOTAL = t / 30; print({k: round(v, 2) for k, v in off.items()}, 'TOTAL', round(TOTAL, 2))
open('q/v.txt', 'w').write(''.join(f"file '{n}.mp4'\n" for n, _ in segs))
run('ffmpeg -v error -y -f concat -safe 0 -i q/v.txt -c copy q/basev.mp4')
buf = []
for nme, n in segs:
    w = wave.open(f'q/{nme}.wav'); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2); want = n * SR // 30
    x = x[:want] if len(x) >= want else np.vstack([x, np.zeros((want - len(x), 2), np.int16)]); buf.append(x)
allx = np.vstack(buf); w = wave.open('q/basea.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(allx.tobytes()); w.close()
print('video frames', t, 'audio s', round(len(allx) / SR, 4), 'video s', round(TOTAL, 4))

# ---- captions
def sentence_spans(path, k, tempo=1.0):
    p = subprocess.run(f'ffmpeg -hide_banner -i {path} -af silencedetect=noise=-38dB:d=0.12 -f null -', shell=True, capture_output=True, text=True).stderr
    st = [float(v) for v in re.findall(r'silence_start: ([\d.]+)', p)]; en = [float(v) for v in re.findall(r'silence_end: ([\d.]+)', p)]
    D = dur(path); sil = [(a, b) for a, b in zip(st, en) if a > 0.15 and b < D - 0.15]
    cuts = sorted(sorted(sil, key=lambda s: s[0] - s[1])[:k - 1]); spans = []; a = 0.0
    for s, e in cuts: spans.append((a, s)); a = e
    spans.append((a, D))
    while len(spans) < k: spans.append(spans[-1])
    return [(x / tempo, y / tempo) for x, y in spans]
caps = []
def add(txt, a, b, keys=(), size=70, y=None): caps.append((txt, a, b, keys, size, y))
def spread(chunks, a, b, keys=(), size=70):
    tot = sum(len(c[1]) for c in chunks); t0 = a
    for shown, spoken in chunks:
        t1 = t0 + (b - a) * len(spoken) / tot; add(shown, t0, t1 - 0.03, keys, size); t0 = t1
i0 = off['s1a'] + 0.25; sp = sentence_spans(INTRO, 4)
add("IS YOUR DEPARTMENT SUFFERING FROM UNTREATED PTSD?", i0 + sp[0][0], i0 + sp[0][1] + 0.1, ("PTSD",))
add("SHORT TEMPERS. EMPTY BUNKS.", i0 + sp[1][0], i0 + sp[2][1] + 0.1); add("GOOD PEOPLE LEAVING EARLY.", i0 + sp[3][0], i0 + sp[3][1] + 0.2, ("LEAVING",))
o = off['s2'] - A2
add("I'M CHIEF CHUCK.", o + 1.9, o + 2.8); add("FOR YEARS I LOOKED FOR A CURE FOR PTSD.", o + 3.03, o + 5.4, ("CURE", "PTSD"))
add("TURNS OUT IT COMES IN A CAPSULE.", o + 5.7, o + 7.4, ("CAPSULE",)); add("IT'S CALLED LEADERSHIP.", o + 7.63, o + 9.75, ("LEADERSHIP",), 64, 330)
o = off['s4'] - A4; add("ONE CAPSULE. TAKEN DAILY. BY THE PEOPLE IN CHARGE.", o + 1.2, o + 3.6, ("CHARGE",))
s0 = off['s5a'] + 0.3; sp = sentence_spans(SIDE, 4, TEMPO); K5 = ("TRUST", "HAPPY", "ACCOUNTABILITY", "REAL", "INJURY")
spread([("SIDE EFFECTS MAY INCLUDE:", "Side effects of Leadership may include"), ("CREWS WHO TALK TO EACH OTHER,", "crews who talk to each other,"), ("CHIEFS WHO ASK \"HOW ARE YOU, REALLY?\"", "chiefs who ask how are you, really?"),
        ("FEWER SICK DAYS,", "fewer sick days,"), ("SUDDEN OUTBREAKS OF TRUST,", "sudden outbreaks of trust,"), ("AND PEOPLE ACTUALLY RETIRING HAPPY.", "and people actually retiring happy.")], s0 + sp[0][0], s0 + sp[0][1], K5, 58)
add("DO NOT TAKE LEADERSHIP IF YOU ARE ALLERGIC TO ACCOUNTABILITY.", s0 + sp[1][0], s0 + sp[1][1], K5, 58)
add("LEADERSHIP IS NOT A REAL DRUG.", s0 + sp[2][0], s0 + sp[2][1], K5, 58); add("PTSD IS A REAL INJURY.", s0 + sp[3][0], s0 + sp[3][1] + 0.2, K5, 58)
o = off['s6a'] - A6a
add("THERE'S NO PILL THAT PREVENTS PTSD.", o + 1.37, o + 3.3, ("PILL",)); add("BUT LEADERSHIP DOES.", o + 3.54, o + 4.8, ("LEADERSHIP",))
add("CHIEFS, IT'S TIME TO CHECK ON YOUR PEOPLE", o + 5.1, o + 7.4, ("CHECK",)); add("BEFORE THE BAD CALL, NOT AFTER.", o + 7.7, o + 9.9, ("BEFORE",))
o = off['s6b'] - A6b; add("LEADERSHIP. ASK YOUR CHIEF IF IT'S RIGHT FOR YOUR DEPARTMENT.", o + 11.55, o + 17.45, ("CHIEF",), 64)
o = off['bl1'] - ABL; add("COME ON.", o + 0.35, o + 2.1); add("DID YOU REALLY THINK THERE WAS A PILL THAT CURED PTSD?", o + 2.33, o + 4.7, ("PILL", "CURED"))
o = off['bl2']; add("THERE IS NO PILL. THERE IS LEADERSHIP.", o + 9.0, o + nb / 30, ("LEADERSHIP.",), 64)

ins = '-i q/basev.mp4 -loop 1 -framerate 30 -i q/ov.png '; fc = '[0:v][1:v]overlay=0:0:shortest=1[o0];'; last = 'o0'
for k, (txt, a, b, keys, size, y) in enumerate(caps):
    h = cap(f'c{k}', txt, keys, size); ins += f'-loop 1 -framerate 30 -i q/c{k}.png '
    fc += f"[{last}][{2+k}:v]overlay=0:{(1540-h) if y is None else y}:enable='between(t,{a:.2f},{b:.2f})'[o{k+1}];"; last = f'o{k+1}'
n = 2 + len(caps)
ins += f'-i q/basea.wav -i {INTRO} -i {SIDE} -i {DISC} -stream_loop 1 -i {MUSIC} '
di, ds, dc = int(i0 * 1000), int(s0 * 1000), int((off['s7'] + 0.25) * 1000); MEND = off['tr']
fc += (f"[{n+1}:a]aresample={SR},volume=1.5,{ST},adelay={di}|{di}[vi];[{n+2}:a]aresample={SR},atempo={TEMPO},volume=1.5,{ST},adelay={ds}|{ds}[vs];"
       f"[{n+3}:a]aresample={SR},atempo={DT},volume=1.5,{ST},adelay={dc}|{dc}[vd];"
       f"[{n}:a][vi][vs][vd]amix=inputs=4:duration=first:normalize=0,asplit[vx][sc];"
       f"[{n+4}:a]aresample={SR},{ST},volume=-11dB,afade=t=in:d=0.6,atrim=0:{MEND:.2f},afade=t=out:st={MEND-0.5:.2f}:d=0.5,apad=whole_dur={TOTAL:.3f}[mu];[mu][sc]sidechaincompress=threshold=0.04:ratio=3:attack=20:release=500[md];"
       f"[vx][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=11,aresample={SR}[a]")
open('q/fc.txt', 'w').write(fc)
run(f'ffmpeg -v error -y {ins}-filter_complex_script q/fc.txt -map "[{last}]" -map "[a]" -frames:v {t} -t {TOTAL:.3f} -r 30 -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 192k -ar {SR} MAYDAY-Day-24-v3.mp4')
json.dump({'off': off, 'total': TOTAL, 'caps': [(c[0], round(c[1], 2), round(c[2], 2)) for c in caps]}, open('q/meta.json', 'w'), indent=1)
print(run('ffprobe -v error -show_entries format=duration,size -of csv=p=0 MAYDAY-Day-24-v3.mp4'))
