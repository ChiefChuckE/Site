import os, subprocess, wave, json, numpy as np
from PIL import Image, ImageDraw, ImageFont
os.chdir('/tmp/claude-0/d27/w')
os.makedirs('q', exist_ok=True)
SR, FPS = 48000, 30
B2 = '/mnt/user-data/uploads/Movies/d27/rs_B2.mp4'
IMG = '/tmp/claude-0/d27/img/'
VENC = '-c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p -r 30'
def run(c): subprocess.run(c, shell=True, check=True)
def fr(s): return int(round(s * FPS))
FI = '/tmp/claude-0/fonts/gf/ofl/montserrat/Montserrat-Italic[wght].ttf'
def MB(sz, v='Black Italic'):
    f = ImageFont.truetype(FI, sz); f.set_variation_by_name(v); return f

def rdw(f):
    w = wave.open(f); x = np.frombuffer(w.readframes(w.getnframes()), np.int16)
    x = x.reshape(-1, w.getnchannels()).astype(np.float32)
    if x.shape[1] == 1: x = np.repeat(x, 2, 1)
    return x
def towav(src, out, ss=None, t=None, af=''):
    a = (f'-ss {ss} ' if ss is not None else '') + f'-i "{src}" ' + (f'-t {t} ' if t is not None else '')
    run(f'ffmpeg -v error -y {a}-vn ' + (f'-af "{af}" ' if af else '') + f'-ar {SR} -ac 2 {out}')
def fit(x, n):
    want = n * SR // FPS
    return x[:want] if len(x) >= want else np.vstack([x, np.zeros((want - len(x), 2), np.float32)])

# ---------- captions
def cap_png(name, text, size=60):
    im = Image.new('RGBA', (1080, 400), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = MB(size); words = text.split(); lines = []; cur = ''
    for w_ in words:
        t = (cur + ' ' + w_).strip()
        if d.textlength(t, font=f) > 940 and cur: lines.append(cur); cur = w_
        else: cur = t
    lines.append(cur)
    h = len(lines) * (size + 14) + 24
    y0 = 400 - h
    d.rounded_rectangle([40, y0, 1040, 400], 22, fill=(0, 0, 0, 170))
    y = y0 + 12
    for l in lines:
        w = d.textlength(l, font=f); d.text(((1080 - w) / 2, y), l, font=f, fill=(255, 255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0, 255)); y += size + 14
    im.save(f'q/{name}.png')

# ---------- segment builders. each returns (name, nframes) and writes q/name.mp4 + audio array
SEGS = []
AUD = {}
def bg_zoom(img, n, z0=1.0, z1=1.06):
    return (f'-loop 1 -framerate 30 -i {img}', f"[0:v]scale=1188:2112,zoompan=z='{z0}+({z1}-{z0})*on/{max(1,n-1)}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,setsar=1[bg]")

def overlays(chain, ins, items, base_idx):
    # items: (png, x, y, t0, t1)
    last = chain
    fc = ''
    for k, (png, x, y, t0, t1) in enumerate(items):
        ins += f' -loop 1 -framerate 30 -i {png}'
        i = base_idx + k
        fc += f";[{i}:v]format=rgba,fade=t=in:st={t0}:d=0.15:alpha=1[p{k}];[{last}][p{k}]overlay={x}:{y}:enable='between(t,{t0},{t1})'[o{k}]"
        last = f'o{k}'
    return ins, fc, last

ANIM = {'s1_open': ('d1', 0.0), 's2_brakes': ('d2', 5.85), 's3_rotate': ('d3', 12.75), 's4_tape': ('d4', 18.5), 's5_calipers': ('d5', 22.9), 's6_shelf': ('d6', 29.0), 's7_pedestal': ('d7', 35.0), 's8_thumbs': ('d8', 40.8)}
def dan(name, scene, a, b, items=(), cap=None, z=(1.0, 1.05), movs=(), pad=0.15, hold=0.0):
    n = fr(b - a + pad + hold)
    clip = ANIM.get(scene)
    if clip and os.path.exists(f'/tmp/claude-0/d27/dan/{clip[0]}.mp4'):
        i0 = f'-ss {max(0, a - clip[1]):.3f} -i /tmp/claude-0/d27/dan/{clip[0]}.mp4'
        fc = '[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=5[bg]'
    else:
        i0, fc = bg_zoom(IMG + scene + '.jpg', n, *z)
    its = list(items)
    if cap: cap_png('cap_' + name, cap); its.append((f'q/cap_{name}.png', 0, 1400, 0, 99))
    ins = i0; last = 'bg'; fcm = ''
    for k, (mv, mx, my, t0) in enumerate(movs):
        ins += f' -i {mv}'
        fcm += f";[{1 + k}:v]setpts=PTS-STARTPTS+{t0}/TB[m{k}];[{last}][m{k}]overlay={mx}:{my}:eof_action=pass[n{k}]"; last = f'n{k}'
    ins, fc2, last = overlays(last, ins, its, 1 + len(movs))
    run(f'ffmpeg -v error -y {ins} -filter_complex "{fc}{fcm}{fc2}" -map "[{last}]" -frames:v {n} {VENC} q/{name}.mp4')
    AUD[name] = fit(DAN[int(a * SR):int(b * SR) + int(pad * SR)], n)
    SEGS.append((name, n))

REL = {'ad': 0.721, 'brakes': 0.792, 'brain': 0.760, 'dizzy': 0.70, 'good': 0.475, 'tissue': 0.512, 'y1999': 0.499}
def head_rel(name):
    d = f'cut/{name}_fx'; fs = sorted(os.listdir(d))[::8]; r = []
    for f in fs:
        a = np.asarray(Image.open(f'{d}/{f}'))[:, :, 3]
        ys, xs = np.where(a > 150)
        if len(ys) == 0: continue
        sel = ys < ys.min() + 120; r.append(np.median(xs[sel]) / a.shape[1])
    return float(np.median(r))
def chuck(name, scene, cap=None, x_center=760, h=1650, bottom=1915, items=(), skip=0.0, dur=None, bgvid=None, capy=1400, aud=None, preaud=None, bgclip=None, slide=False):
    mov = f'cut/{name}.mov'; wav = f'cut/{name}.wav'
    if name not in REL: REL[name] = head_rel(name)
    w0 = int(subprocess.run(f'ffprobe -v error -select_streams v -show_entries stream=width -of csv=p=0 {mov}', shell=True, capture_output=True, text=True).stdout)
    n = int(subprocess.run(f'ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames -of csv=p=0 {mov}', shell=True, capture_output=True, text=True).stdout)
    n -= fr(skip)
    if dur: n = min(n, fr(dur))
    sw = int(w0 * h / 1080) // 2 * 2
    if bgclip:
        i0 = f'-ss {bgclip[1]} -i {bgclip[0]}'; fc = '[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=5[bg]'
    elif bgvid:
        i0 = f'-stream_loop 3 -i {bgvid}'; fc = '[0:v]setsar=1,fps=30[bg]'
    else:
        i0, fc = bg_zoom(IMG + scene + '.jpg', n, 1.03, 1.06)
    ins = i0 + f' -framerate 30 -start_number {fr(skip) + 1} -i cut/{name}_fx/%05d.png'
    fc += f";[1:v]setpts=PTS-STARTPTS,scale={sw}:{h},eq=brightness=0.03:saturation=1.05[ck];[bg][ck]overlay=x='{int(x_center - REL[name] * sw)}{"+1400*pow(max(0,1-t/0.22),2)+1400*pow(max(0,(t-" + str(round(n / FPS - 0.22, 3)) + ")/0.22),2)" if slide else ""}':y={bottom - h}[c0]"
    its = list(items)
    if cap: cap_png('cap_' + name, cap); its.append((f'q/cap_{name}.png', 0, capy, 0, 99))
    ins, fc2, last = overlays('c0', ins, its, 2)
    run(f'ffmpeg -v error -y {ins} -filter_complex "{fc}{fc2}" -map "[{last}]" -frames:v {n} {VENC} q/{name}.mp4')
    x = rdw(wav); x = x[int(skip * SR):]
    if preaud is not None: x = x.copy(); x[:len(preaud)] += preaud
    AUD[name] = fit(x * 1.0, n) if aud is None else fit(aud, n)
    SEGS.append((name, n))

def real(name, ss, dur, cx=None, cap=None, items=(), dark=False, out_wh=(1080, 1920), zoom=1.0):
    n = fr(dur)
    W, H = out_wh
    cw = int(1080 * W / H / zoom) // 2 * 2; ch = int(1080 / zoom) // 2 * 2
    if cx is None: cx = 960
    L = int(max(0, min(1920 - cw, cx - cw / 2)))
    T = int((1080 - ch) / 2) if zoom > 1 else 0
    vf = f"crop={cw}:{ch}:{L}:{T},scale={W}:{H},setsar=1,fps=30" + (",eq=brightness=-0.06:contrast=1.15:saturation=0.75" if dark else ",eq=brightness=0.02")
    its = list(items)
    if cap: cap_png('cap_' + name, cap); its.append((f'q/cap_{name}.png', 0, 1400, 0, 99))
    ins = f'-ss {ss} -i {B2}'
    fc = f"[0:v]{vf}[r0]"
    ins, fc2, last = overlays('r0', ins, its, 1)
    run(f'ffmpeg -v error -y {ins} -filter_complex "{fc}{fc2}" -map "[{last}]" -frames:v {n} {VENC} q/{name}.mp4')
    towav(B2, f'q/{name}.wav', ss, dur + 0.2)
    AUD[name] = fit(rdw(f'q/{name}.wav'), n)
    SEGS.append((name, n))

def person_x(ss):
    from rembg import new_session, remove
    run(f'ffmpeg -v error -y -ss {ss} -i {B2} -frames:v 1 q/px.png')
    im = Image.open('q/px.png').convert('RGB')
    m = np.asarray(remove(im.resize((640, 360)), session=new_session('u2net_human_seg'), only_mask=True))
    ys, xs = np.where(m > 200); return float(np.median(xs)) * 3

def fitclip(name, src, ss, dur, audio=True, items=()):
    n = fr(dur)
    ins = f'-ss {ss} -i {src}'
    fc = ("[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:3,eq=brightness=-0.15[bb];"
          "[b]scale=1080:-2[fg];[bb][fg]overlay=0:(H-h)/2,setsar=1,fps=30[r0]")
    ins, fc2, last = overlays('r0', ins, list(items), 1)
    run(f'ffmpeg -v error -y {ins} -filter_complex "{fc}{fc2}" -map "[{last}]" -frames:v {n} {VENC} q/{name}.mp4')
    towav(src, f'q/{name}.wav', ss, dur + 0.2)
    AUD[name] = fit(rdw(f'q/{name}.wav'), n)
    SEGS.append((name, n))

def static(name, dur):
    n = fr(dur)
    run(f'ffmpeg -v error -y -f lavfi -i "nullsrc=s=270x480:r=30" -vf "geq=lum=\'random(1)*255\':cb=128:cr=128,scale=1080:1920:flags=neighbor" -frames:v {n} {VENC} q/{name}.mp4')
    t = np.random.default_rng(1).uniform(-1, 1, (n * SR // FPS, 2)).astype(np.float32) * 6000
    AUD[name] = t; SEGS.append((name, n))

# ---------- sources
towav('/mnt/user-data/uploads/Movies/d27/dan_vo.mp3', 'q/dan.wav', af='loudnorm=I=-15:TP=-1.5')
DAN = rdw('q/dan.wav')
# chuck audio cleanup: normalize each cutout wav
for c in ['ad3', 'brakes2', 'y1999b', 'y1999c', 'talk', 'talk3', 'yell', 'bib']:
    if os.path.exists(f'cut/{c}.wav') and not os.path.exists(f'cut/{c}.normed'):
        run(f'ffmpeg -v error -y -i cut/{c}.wav -af "highpass=f=90,acompressor=threshold=-24dB:ratio=3,volume=6dB" -ar {SR} -ac 2 cut/{c}_n.wav')
        os.replace(f'cut/{c}_n.wav', f'cut/{c}.wav'); open(f'cut/{c}.normed', 'w').close()

STEAL_N = 21
# ---------- timeline (v4: Chuck's 2:07 PM notes)
dan('d1', 's1_open', 0.0, 5.15, items=[('g/logo.png', 0, 1380, 0.4, 99)])
chuck('ad3', 's1_open', cap="Uh... I saw the ad?", slide=True, x_center=905, h=1500, bottom=1880, bgclip=('/tmp/claude-0/d27/dan/i1.mp4', 0.3), skip=0.03, preaud=DAN[int(5.3 * SR):int(5.65 * SR)])
dan('d2a', 's2_brakes', 5.85, 7.78, cap="Brakes slipping? Snapping at the kids?")
chuck('brakes2', 's2_brakes', slide=True, bgclip=('/tmp/claude-0/d27/dan/i2.mp4', 0.0), cap="My brakes are a little squeaky.", skip=0.2)
dan('d2b', 's2_brakes', 7.9, 12.68, items=[('g/b_1999.png', 500, 330, 1.5, 99)], cap="BRAIN BRAKE JOB: new pads for your short fuse!", movs=[('g/feet.mov', 470, 820, 2.35)])
chuck('y1999c', 's2_brakes', bgclip=('/tmp/claude-0/d27/dan/i2.mp4', 2.7), cap="Nineteen ninety-nine? Sign me up!", items=[('g/b_1999s.png', 610, 120, 0, 99)], skip=0.12, dur=2.3)
run('python3 jackpot.py'); SEGS.append(('jackpot', 30)); AUD['jackpot'] = np.zeros((30 * SR // FPS, 2), np.float32)
dan('d3', 's3_rotate', 12.75, 18.3, items=[('g/b_rotate.png', 500, 300, 0.4, 99)], cap="FREE mind rotation with every visit!", movs=[('g/spin.mov', 330, 860, 0.3)])
dan('d4', 's4_tape', 18.5, 22.7, items=[('g/b_tape.png', 520, 1100, 2.6, 99)], cap="Check engine light on for 20 years? Tape. FREE!")
real('good', 340.48, 0.75, cx=900, zoom=1.0, cap="Good as new.")
dan('d5a', 's5_calipers', 22.9, 25.95, items=[('g/deals.png', 0, 1060, 0.3, 99)])
tw = rdw('cut/tissue.wav'); dd = DAN[int(25.95 * SR):int(28.95 * SR)]
mixa = dd + tw[:len(dd)] * 0.45
chuck('tissue', 's5_calipers', bgclip=('/tmp/claude-0/d27/dan/i5.mp4', 0.5), items=[('g/deals.png', 0, 1060, 0, 99)], dur=3.0, aud=mixa)
dan('d6', 's6_shelf', 29.0, 34.8, items=[('g/b_sleep.png', 480, 120, 3.9, 99)], cap="Full synthetic SLEEP change! ...Out of stock.", movs=[('g/tank.mov', 660, 520, 0.2)])
dan('d7a', 's7_pedestal', 35.0, 37.8, cap="And today only... a BRAND NEW BRAIN!")
chuck('brain', 's7_pedestal', bgclip=('/tmp/claude-0/d27/dan/i7.mp4', 0.3), cap="I'll take the new brain!", skip=1.08, dur=1.35)
TOW_N = 24; run(f"python3 tow.py {REL['brain']} {fr(1.08) + fr(1.35)} {TOW_N}"); SEGS.append(('tow', TOW_N)); AUD['tow'] = np.zeros((TOW_N * SR // FPS, 2), np.float32)
dan('d7b', 's7_pedestal', 38.2, 40.4, items=[('g/b_sold.png', 500, 330, 0.05, 99)], cap="Sold out. Sold out every year.")
dan('d8', 's8_thumbs', 40.8, 44.1, items=[('g/tag.png', 0, 1380, 0.3, 99), ('g/receipt.png', 440, 300, 0.3, 99)], hold=0.0)
cap_png('cap_talk2', "No doorbuster for this one. But the check-up's free, any day. Call or text 988.")
chuck('talk3', None, bgvid='g/spiral.mp4', x_center=540, h=3000, bottom=2663, items=[('q/cap_talk2.png', 0, 1280, 0, 99), ('g/foot.png', 0, 1700, 0, 99)])
run('ffmpeg -v error -y -ss 44.1 -i q/dan.wav -t 4.6 -af "asetrate=48000*1.65,aresample=48000" q/fine_fast.wav')
n9 = fr(2.95)
run(f'ffmpeg -v error -y -loop 1 -framerate 30 -i {IMG}s8_thumbs.jpg -loop 1 -framerate 30 -i g/fine.png -filter_complex "[0:v]scale=1080:1920,eq=brightness=-0.35,setsar=1[a];[a][1:v]overlay=0:820" -frames:v {n9} {VENC} q/d9.mp4')
AUD['d9'] = fit(rdw('q/fine_fast.wav'), n9); SEGS.append(('d9', n9))
real('blp', 465.97, 1.36, cx=person_x(466.3), zoom=1.2, items=[('q/blooper_tag.png', 0, 170, 0, 99)], cap="$20 for a new brain...")
run('python3 steal.py'); SEGS.append(('steal', STEAL_N)); AUD['steal'] = fit(rdw('q/blp.wav')[int(1.36 * SR):int(1.36 * SR) + STEAL_N * SR // FPS] * 0.6, STEAL_N)
fitclip('bob', '/tmp/claude-0/d27/src/b2211.mov', 0.0, 4.6, items=[('q/chucking_s.png', 220, 560, 2.72, 3.9)])
fitclip('lip', '/tmp/claude-0/d27/src/lipsync.mp4', 0.0, 3.56)
# bobblehead, punched in, with Chuck's real yell
ny = fr(3.73)
cap_png('cap_yell', "FIRST RESPONDER PTSD!")
run(f'ffmpeg -v error -y -ss 0.4 -i /tmp/claude-0/d27/src/b2211.mov -loop 1 -framerate 30 -i q/cap_yell.png -filter_complex '
    f'"[0:v]crop=880:1564:208:60,scale=1080:1920,setsar=1,fps=30,eq=contrast=1.12:saturation=1.2[a];[a][1:v]overlay=0:1380[b]" -map "[b]" -frames:v {ny} {VENC} q/yell.mp4')
AUD['yell'] = fit(rdw('cut/yell.wav')[int(0.32 * SR):], ny); SEGS.append(('yell', ny))
# biblical: jail cartoon on top, Chuck close-up over scary sky on bottom; ends right on "biblical"
BIB_SKIP = 0.1; BIB_T = 433.0 - 429.8 - BIB_SKIP
cap_png('disc', "REENACTMENT. Chief Chuck was never actually in handcuffs.", 34)
cap_png('cap_bib', "I'm just getting started... It's gonna be... BIBLICAL.", 62)
nb = fr(3.5)
bw = int(subprocess.run('ffprobe -v error -select_streams v -show_entries stream=width -of csv=p=0 cut/bib.mov', shell=True, capture_output=True, text=True).stdout)
REL['bib'] = head_rel('bib')
bh = 1500; bsw = int(bw * bh / 1080) // 2 * 2; bx = int(540 - REL['bib'] * bsw); by = -int(0.22 * bh)
run(f'ffmpeg -v error -y -loop 1 -framerate 30 -i {IMG}jail.jpg -loop 1 -framerate 30 -i {IMG}scary.png -i cut/bib.mov -loop 1 -framerate 30 -i q/cap_bib.png -loop 1 -framerate 30 -i q/disc.png -filter_complex '
    f'"[0:v]scale=1188:1188,zoompan=z=\'1+0.08*on/{nb}\':d=1:x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':s=1080x960:fps=30,setsar=1[top];'
    f'[1:v]scale=-2:1056,crop=1188:1056,zoompan=z=\'1+0.12*on/{nb}\':d=1:x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':s=1080x960:fps=30,setsar=1[sky];'
    f'[2:v]trim=start_frame={fr(BIB_SKIP)},setpts=PTS-STARTPTS,scale={bsw}:{bh},eq=brightness=-0.02:contrast=1.15:saturation=0.8[ck];[sky][ck]overlay={bx}:{by}:shortest=0[bot];'
    f'[top][bot]vstack[v0];[v0]drawbox=y=956:w=1080:h=8:color=black@1:t=fill[v1a];[v1a][4:v]overlay=0:540[v1];[v1]split[c0][c1];[c1][3:v]overlay=0:1480:enable=\'between(t,0.1,99)\'[v2];[c0]trim=start_frame={nb - 1}:end_frame={nb},setpts=PTS-STARTPTS[last];'
    f'[v2]trim=end_frame={nb}[v3]" -map "[v3]" -frames:v {nb} {VENC} q/bib.mp4 -map "[last]" -frames:v 1 q/bib_last.png')
AUD['bib'] = fit(rdw('cut/bib.wav')[int(BIB_SKIP * SR):], nb); SEGS.append(('bib', nb))
# freeze on face with the 988 footer, then old-TV switch-off
nf = fr(1.25)
run(f'python3 tvoff.py {nf}'); run(f'ffmpeg -v error -y -framerate 30 -i q/tv/%04d.png -frames:v {nf} {VENC} q/tvoff.mp4')
_t = rdw('cut/bib.wav')[int((BIB_SKIP + 3.5) * SR):int((BIB_SKIP + 3.85) * SR)]; _t = _t * np.linspace(1, 0, len(_t))[:, None]; AUD['tvoff'] = fit(_t, nf); SEGS.append(('tvoff', nf))


# ---------- cold-open hook: the $20 steal teaser before Dan starts
cap_png('cap_hook', "WAIT FOR IT...", 70)
nh0 = fr(0.5)
run(f'ffmpeg -v error -y -sseof -0.5 -i q/blp.mp4 -i q/steal.mp4 -loop 1 -framerate 30 -i q/cap_hook.png -filter_complex "[0:v]setpts=PTS-STARTPTS,fps=30[a];[a][1:v]concat=n=2:v=1:a=0[c];[c][2:v]overlay=0:1130[o]" -map "[o]" -frames:v {nh0 + STEAL_N} {VENC} q/hook.mp4')
nhk = nh0 + STEAL_N
hk = np.zeros((nhk * SR // FPS, 2), np.float32)
SEGS.insert(0, ('hook', nhk)); AUD['hook'] = hk

# ---------- assemble
open('q/v.txt', 'w').write(''.join(f"file '{s}.mp4'\n" for s, _ in SEGS))
run('ffmpeg -v error -y -f concat -safe 0 -i q/v.txt -c copy q/basev.mp4')
off = {}; t = 0
for s, n in SEGS: off[s] = t / FPS; t += n
TOTAL = t / FPS
allx = np.vstack([AUD[s] for s, _ in SEGS])
def mix(x, at, g=1.0):
    o = int(at * SR); x = x[:max(0, len(allx) - o)] * g; allx[o:o + len(x)] += x
# bleep the F-word in the bobblehead clip
a0 = int((off['bob'] + 2.79) * SR); a1 = int((off['bob'] + 3.10) * SR); fd = int(0.012 * SR)
i0_, i1_ = int((off['bob'] + 3.10) * SR), int((off['bob'] + 3.34) * SR); allx[i0_:i1_] *= 2.0
env_ = np.ones(a1 - a0 + 2 * fd); env_[fd:-fd] = 0; env_[:fd] = np.linspace(1, 0, fd); env_[-fd:] = np.linspace(0, 1, fd)
allx[a0 - fd:a1 + fd] *= env_[:, None]
# whoosh when the hand yanks the $20
tw_ = np.arange(int(0.4 * SR)) / SR
wh = np.random.default_rng(5).normal(0, 1, len(tw_)) * np.sin(np.pi * tw_ / 0.4) ** 2 * 5000
wh = np.convolve(wh, np.ones(30) / 30, mode='same') * 4
mix(wh[:, None].repeat(2, 1), off['steal'] + 0.22); mix(wh[:, None].repeat(2, 1) * 1.3, off['hook'] + 0.5 + 0.22)
# boom on "biblical"
tb = np.arange(int(2.2 * SR)) / SR
boom = (np.sin(2 * np.pi * (55 - 15 * tb) * tb) * np.exp(-tb * 1.8) * 22000 + np.random.default_rng(2).normal(0, 1, len(tb)) * np.exp(-tb * 12) * 6000)
mix(boom[:, None].repeat(2, 1), off['bib'] + BIB_T)
# record scratch before "sold out"
ts = np.arange(int(0.45 * SR)) / SR
scr = (np.sin(2 * np.pi * (1200 * np.exp(-ts * 6)) * ts) * 7000 * np.exp(-ts * 3) + np.random.default_rng(3).normal(0, 1, len(ts)) * 3000 * np.exp(-ts * 5))
mix(scr[:, None].repeat(2, 1), off['d7b']); mix(scr[:, None].repeat(2, 1), off['d1'] - 0.08)
tz = np.arange(int(0.35 * SR)) / SR
zap = np.sin(2 * np.pi * (2400 * np.exp(-tz * 9)) * tz) * 6000 * np.exp(-tz * 7)
mix(zap[:, None].repeat(2, 1), off['tvoff'] + 0.68)

# ---- cartoon sound effects
def tone(f0, f1, dur, amp, decay=4.0, vib=0.0):
    t_ = np.arange(int(dur * SR)) / SR; fq = f0 + (f1 - f0) * t_ / dur + vib * np.sin(2 * np.pi * 9 * t_) * f0 * 0.06
    ph = 2 * np.pi * np.cumsum(fq) / SR; return np.sin(ph) * amp * np.exp(-t_ * decay)
def st(x): return x[:, None].repeat(2, 1)

def jackpot_sfx():
    r = np.random.default_rng(11); out = np.zeros(int(1.6 * SR))
    # glass smash: bright noise burst
    n = int(0.5 * SR); g = r.normal(0, 1, n) * np.exp(-np.arange(n) / SR * 9) * 9000
    g = g - np.convolve(g, np.ones(8) / 8, mode='same'); out[:n] += g
    # jackpot bells arpeggio
    for k, f0 in enumerate([1568, 1976, 2349, 3136, 2349, 3136, 3951]):
        t0 = int((0.12 + k * 0.08) * SR); b = tone(f0, f0, 0.5, 4200, 6) + tone(f0 * 2.01, f0 * 2.01, 0.5, 1500, 8)
        out[t0:t0 + len(b)] += b[:len(out) - t0]
    # coins clinking
    for k in range(40):
        t0 = int(r.uniform(0.15, 1.4) * SR); f0 = r.uniform(3500, 7000); c = tone(f0, f0, 0.06, r.uniform(1200, 2800), 60)
        out[t0:t0 + len(c)] += c[:len(out) - t0]
    return out

def sfx(n, g=1.0):
    towav('/tmp/claude-0/d27/dan/sfx_' + n + '.mp3', 'q/sfx_' + n + '.wav'); return rdw('q/sfx_' + n + '.wav') * g
if os.path.exists('/tmp/claude-0/d27/dan/sfx_violin.mp3'):
    vio = sfx('violin'); L_ = min(len(vio), int((off['d9'] - off['talk3']) * SR)); vio = vio[:L_].copy()
    e_ = np.ones(L_); f1 = int(0.6 * SR); f2 = int(1.0 * SR); e_[:f1] = np.linspace(0, 1, f1); e_[-f2:] = np.linspace(1, 0, f2)
    mix(vio * e_[:, None] * 0.28, off['talk3'])
if os.path.exists('/tmp/claude-0/d27/dan/sfx_jack.mp3'): mix(sfx('jack', 1.0), off['jackpot'] + 0.1)
mix(sfx('cha', 0.9), off['d2b'] + 1.45); mix(sfx('cha', 2.2), off['jackpot'] + 0.02); mix(st(jackpot_sfx()), off['jackpot'] + 0.08)
mix(sfx('boi', 0.9), off['d3'] + 0.75)
cr_ = sfx('cri', 0.8); mix(cr_, off['d6'] + 4.75)
mix(sfx('sli', 0.8)[:int(1.2 * SR)] * np.linspace(1, 0, int(1.2 * SR))[:, None] if len(sfx('sli')) >= int(1.2 * SR) else sfx('sli', 0.8), off['tow'] + 0.25)
mix(sfx('who', 0.8), off['brakes2']); mix(sfx('who', 0.8), off['d2b'] - 0.25); mix(sfx('who', 1.0), off['steal'] + 0.25); mix(sfx('who', 1.0), off['hook'] + 0.5 + 0.25)
allx = np.clip(allx, -32767, 32767).astype(np.int16)
w = wave.open('q/basea.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(allx.tobytes()); w.close()
MEND = off['talk3']
fc = (f"[1:a]asplit[vx][sc];[2:a]aresample={SR},volume=-15dB,atrim=0:{MEND + 0.6:.2f},afade=t=out:st={MEND - 0.4:.2f}:d=1.0,apad=whole_dur={TOTAL:.3f}[mu];"
      f"[mu][sc]sidechaincompress=threshold=0.03:ratio=4:attack=15:release=400[md];[vx][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=11,aresample={SR}[a];"
      f"[0:v][3:v]overlay=0:0:enable='lt(t,{off['talk3']:.2f})+between(t,{off['d9']:.2f},{off['blp']:.2f})'[v]")
run(f'ffmpeg -v error -y -i q/basev.mp4 -i q/basea.wav -stream_loop 2 -i /mnt/user-data/uploads/Movies/d27/music.mp3 -loop 1 -framerate 30 -i g/ov.png -filter_complex "{fc}" -map "[v]" -map "[a]" -frames:v {t} -t {TOTAL:.3f} -c:v libx264 -preset veryfast -crf 22 -pix_fmt yuv420p -c:a aac -b:a 192k -ar {SR} MAYDAY-Day-27.mp4')
json.dump({'off': off, 'total': TOTAL}, open('q/meta.json', 'w'), indent=1)
print('TOTAL', round(TOTAL, 2), {k: round(v, 2) for k, v in off.items()})
