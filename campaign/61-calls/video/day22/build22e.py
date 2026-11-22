import subprocess, os, random, math
from PIL import Image, ImageDraw, ImageFont
def run(c): subprocess.run(c, shell=True, check=True)
os.chdir('/tmp/claude-0/d22w')
SD = '/tmp/claude-0/d20g/'
FI = '/tmp/claude-0/fonts/gf/ofl/montserrat/Montserrat-Italic[wght].ttf'
def MB(sz, var='Black Italic'):
    f = ImageFont.truetype(FI, sz); f.set_variation_by_name(var); return f
def off(c):
    o = subprocess.check_output(f'ffprobe -v error -select_streams a:0 -show_entries stream=start_time -of csv=p=0 {c}.MOV', shell=True).decode().strip()
    return float(o or 0)
Y = (255, 214, 0, 255)
# audio masters
for c, extra in (('c1B68', ''), ('cEA66', 'afftdn=nf=-28,')):
    if not os.path.exists(f'w/n{c}.wav'):
        run(f'ffmpeg -v error -y -i {c}.MOV -map 0:a:0 -ac 2 -ar 48000 -af "highpass=f=100,{extra}loudnorm=I=-17:TP=-2:LRA=9" w/n{c}.wav')
O1 = off('c1B68'); OE = off('cEA66'); print('offs', O1, OE)
FPS = 30
SAD = ',eq=saturation=0.3:brightness=-0.06:contrast=1.0,vignette=PI/3.2'
pieces = []  # (file, dur)
caps = []    # (txt, t0, t1, size, keys)
T = 0.0
def enc(name, clip, ss, dur, extra='', grade=False, zoomramp=None, plate=None, nostack=False):
    global T
    n = round(dur * FPS); d = n / FPS
    zr = f",scale=w='trunc(1080*({zoomramp[0]}+{zoomramp[1]}*t)/2)*2':h=-2:eval=frame,crop=1080:1920" if zoomramp else ''
    pl = ''
    if plate:
        px, py, pw, ph = plate
        pl = f',split[a][b];[b]crop={pw}:{ph}:{px}:{py},scale={pw//20}:{ph//20}:flags=area,scale={pw}:{ph}:flags=neighbor[p];[a][p]overlay={px}:{py}'
    vf = f'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920{pl}{extra}{zr},fps=30{SAD if grade else ""},format=yuv420p'
    run(f'ffmpeg -v error -y -ss {ss:.3f} -i {clip}.MOV -map 0:v:0 -an -vf "{vf}" -frames:v {n} -c:v libx264 -preset veryfast -crf 18 w/{name}.mp4')
    if not nostack: pieces.append((f'w/{name}.mp4', d))
    t0 = T; T += d; return t0, d
def encV(name, path, ss, dur):
    global T
    n = round(dur * FPS); d = n / FPS
    run(f'ffmpeg -v error -y -ss {ss:.3f} -i {path} -an -vf "scale=1080:1920:flags=lanczos,fps=30,format=yuv420p" -frames:v {n} -c:v libx264 -preset veryfast -crf 17 w/{name}.mp4')
    pieces.append((f'w/{name}.mp4', d)); t0 = T; T += d; return t0, d
def addcaps(base, lst):
    for (txt, a, b, keys) in lst: caps.append((txt, base + a, base + b, keys))
TS = {}
# S1 split
n = round(3.9 * FPS); d = n / FPS
run(f'ffmpeg -v error -y -ss 1.30 -t 4.0 -i c1B68.MOV -ss 1.35 -t 4.0 -i cF5AA.MOV -filter_complex "[0:v]crop=720:640:0:330,scale=1080:960[a];[1:v]crop=720:640:0:330,scale=1080:960[b];[a][b]vstack,fps=30,format=yuv420p[o]" -map "[o]" -an -frames:v {n} -c:v libx264 -preset veryfast -crf 18 w/s1.mp4')
pieces.append(('w/s1.mp4', d)); TS['s1'] = T; T += d
# S2
t0, d = encV('s2a', 'w/d22_veo_kick.mp4', 1.2, 2.3); TS['s2'] = t0; encV('s2b', 'w/d22_veo_head.mp4', 1.1, 2.3)
addcaps(t0, [("KICKOFF IS AT 5:20.", 0.1, 2.2, {"5:20."}), ("MY BRAIN KICKED OFF AT 3 A.M.", 2.3, 4.6, {"3"})])
# S3
t0, d = enc('s3a', 'c1B68', 11.45, 2.85); TS['s3'] = t0
enc('s3b', 'c3003n', 0.55, 2.15); enc('s3c', 'c3003', 41.3, 1.55); enc('s3d', 'c3003', 38.6, 1.30)
addcaps(t0, [("EVERYBODY'S GOT A PLAYBOOK.", 0.1, 1.8, {"PLAYBOOK."}), ("MINE IS:", 1.8, 2.8, set()), ("CHECK THE EXITS.", 2.8, 4.9, {"EXITS."}), ("CHECK THE ROOF.", 5.0, 6.5, {"ROOF."}), ("CHECK THE CROWD.", 6.5, 7.85, {"CROWD."})])
# S4
t0, d = enc('s4a', 'c1B68', 19.85, 2.2); TS['s4'] = t0
enc('s4b', 'c3007n', 0.0, 3.5, extra=',minterpolate=fps=120:mi_mode=mci:mc_mode=aobmc:vsbmc=1,setpts=4*PTS')
addcaps(t0, [("FANS SCREAM AT A TOUCHDOWN.", 0.1, 2.2, {"TOUCHDOWN."}), ("I FLINCH AT A CAR DOOR.", 2.2, 5.6, {"DOOR."})])
# S5 v4: talk -> flag flies in on "flag" -> stays over face -> ref pops up, Chuck in corner circle
TS['s5'] = T
VS = 3.85; REFD = 8.7; S5D = VS + REFD
run('ffmpeg -v error -y -ss 24.65 -t 3.85 -i c1B68.MOV -framerate 30 -i w/fk/f%03d.png -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p[b];[1:v]scale=1080:1920,format=rgba,setpts=PTS+1.0/TB[f];[b][f]overlay=0:0:eof_action=repeat,format=yuv420p[o]" -map "[o]" -frames:v 116 -c:v libx264 -preset veryfast -crf 17 w/s5a.mp4')
# circle mask + ring
cm = Image.new('L', (340, 340), 0); ImageDraw.Draw(cm).ellipse([0, 0, 339, 339], fill=255); cm.save('w/cmask.png')
rg = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); dr = ImageDraw.Draw(rg)
dr.ellipse([700 + 6, 300 + 10, 1040 + 6, 640 + 10], fill=(0, 0, 0, 170)); dr.ellipse([700 - 8, 300 - 8, 1040 + 8, 640 + 8], outline=(255, 255, 255, 255), width=9); rg.save('w/ring.png')
run('ffmpeg -v error -y -ss 0 -i w/refclip.mp4 -ss 3.4 -i w/flag2.mp4 -i w/cmask.png -i w/ring.png -filter_complex "[0:v]scale=1080:1920:flags=lanczos,setpts=1.0875*PTS,fps=30,tpad=stop_mode=clone:stop_duration=1,format=yuv420p[bg];[1:v]crop=640:640:0:400,scale=340:340,fps=30,tpad=stop_mode=clone:stop_duration=6,format=rgba[c0];[c0][2:v]alphamerge[c];[bg][c]overlay=700:300:shortest=0[o1];[o1][3:v]overlay=0:0,format=yuv420p[o]" -map "[o]" -t %.3f -c:v libx264 -preset veryfast -crf 17 w/s5c.mp4' % REFD)
run('ffmpeg -v error -y -i w/s5a.mp4 -i w/s5c.mp4 -filter_complex "[0][1]concat=n=2:v=1:a=0,format=yuv420p" -c:v libx264 -preset veryfast -crf 17 w/s5.mp4')
V0 = VS
addcaps(T, [("REFEREES THROW A FLAG.", 0.1, 2.0, {"FLAG."}), ("MY BRAIN THROWS A FLASHBACK.", 2.0, 3.8, {"FLASHBACK."}), ("FLAG ON THE PLAY!", V0 + 0.0, V0 + 1.1, {"FLAG"}), ("UNNECESSARY LOUDNESS.", V0 + 1.3, V0 + 3.3, {"LOUDNESS."}), ("FIGHTING FOR FIRST RESPONDER PTSD.", V0 + 3.5, V0 + 6.2, {"PTSD."}), ("15-YARD PENALTY.", V0 + 6.35, V0 + 7.6, {"15-YARD"}), ("CHIEF CHUCK.", V0 + 7.85, S5D - 0.3, {"CHUCK."})])
Tsave = T
enc('s6', 'c2993', 0.5, 1.6, grade=True, plate=(680, 1335, 250, 125), nostack=True)
run(f'ffmpeg -v error -y -i w/s5.mp4 -i w/s6.mp4 -filter_complex "[0][1]xfade=transition=dissolve:duration=0.4:offset={S5D-0.4},format=yuv420p" -c:v libx264 -preset veryfast -crf 18 w/s56.mp4')
pieces.append(('w/s56.mp4', S5D + 1.2)); TS['s6'] = Tsave + S5D - 0.4; T = Tsave + S5D + 1.2
# S7 closing
t0, d = enc('s7', 'cEA66', 1.70, 33.25, grade=True, zoomramp=(1.02, 0.0022)); TS['s7'] = t0; S7D = d
cl = [("HERE'S THE PART NOBODY PLAYS ON THE HIGHLIGHT REEL.", 0.22, {"HIGHLIGHT"}), ("IT'S AFTER THE CALL.", 3.64, {"CALL."}), ("THERE'S NO HALFTIME. NO TIMEOUT.", 5.40, {"HALFTIME.", "TIMEOUT."}), ("IT'S PTSD.", 8.66, {"PTSD."}), ("AN INJURY FROM THE JOB. NOT WEAKNESS.", 10.33, {"WEAKNESS."}), ("WHOEVER YOU ROOT FOR, HERE'S WHAT WINS:", 14.26, {"WINS:"}), ("SAY IT OUT LOUD TO SOMEBODY WHO GETS IT.", 17.5, {"LOUD", "GETS"}), ("DAY 22 OF 61.", 20.54, {"22"}), ("CALL YOUR MAYDAY.", 22.87, {"MAYDAY."}), ("SEND THIS TO SOMEONE WHO WORE THE UNIFORM.", 24.28, {"UNIFORM."}), ("AND YES, A SPORTS JERSEY IS A UNIFORM TOO.", 26.58, {"JERSEY", "UNIFORM"}), ("DIFFERENT FIRE, SAME FIGHT.", 30.68, {"FIRE,", "FIGHT."})]
for i, (txt, a, keys) in enumerate(cl):
    b = cl[i + 1][1] - 0.05 if i + 1 < len(cl) else S7D
    caps.append((txt, t0 + a, t0 + b, keys))
# S8 rapid-fire shirts
TS['s8'] = T
BASE = (16.0, 64.4, 90.0)
for k in range(12):
    ss = BASE[k % 3] + (k // 3) * 0.267
    run(f'ffmpeg -v error -y -ss {ss:.3f} -i c2998.MOV -an -vf "split[a][b];[b]crop=120:70:625:1170,scale=6:3:flags=area,scale=120:70:flags=neighbor[p];[a][p]overlay=625:1170,crop=600:1067:170:700,scale=1080:1920,fps=30,format=yuv420p" -frames:v 8 -c:v libx264 -preset veryfast -crf 18 w/r{k}.mp4')
    pieces.append((f'w/r{k}.mp4', 8 / 30)); T += 8 / 30
TS['end'] = T
TOT = T; print('TOTAL', TOT, TS)
open('w/vl.txt', 'w').write('\n'.join(f"file '{os.path.basename(p)}'" for p, _ in pieces))
run('cd w && ffmpeg -v error -y -f concat -safe 0 -i vl.txt -c copy vcat.mp4')
# ---------- overlays ----------
def mbtext(im, xy, txt, font, stroke=11, sh=(9, 11), col=(255, 255, 255, 255)):
    x, y = xy; d = ImageDraw.Draw(im)
    d.text((x + sh[0], y + sh[1]), txt, font=font, fill=(0, 0, 0, 255), stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    d.text((x, y), txt, font=font, fill=col, stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
def brush(d, box, col=(214, 18, 36, 255), seed=1):
    rnd = random.Random(seed); x0, y0, x1, y1 = box
    pts = [(x, y0 + rnd.uniform(-9, 9)) for x in range(int(x0), int(x1), 26)] + [(x1 + rnd.uniform(-4, 26), y) for y in range(int(y0), int(y1), 22)] + [(x, y1 + rnd.uniform(-9, 9)) for x in range(int(x1), int(x0), -26)] + [(x0 - rnd.uniform(-4, 26), y) for y in range(int(y1), int(y0), -22)]
    d.polygon([(px + 8, py + 10) for px, py in pts], fill=(0, 0, 0, 235)); d.polygon(pts, fill=col)
ovs = []
for i, (txt, a, b, keys) in enumerate(caps):
    sz = 125 if len(txt) <= 18 else 105 if len(txt) <= 30 else 92
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
# split labels
for j, (txt, cy, col) in enumerate((("RED CAR", 905, (214, 18, 36, 255)), ("PURPLE CAR", 1865, (110, 40, 190, 255)))):
    im = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); dd = ImageDraw.Draw(im); f = MB(70); w = dd.textlength(txt, font=f)
    if j == 1: dd.rectangle([0, 1800, 1080, 1920], fill=(20, 8, 40, 255))
    else: dd.rectangle([0, 850, 1080, 960], fill=(30, 4, 8, 255))
    brush(dd, [540 - w / 2 - 30, cy - 50, 540 + w / 2 + 30, cy + 40], col=col, seed=j + 4); mbtext(im, (540 - w / 2, cy - 48), txt, f, stroke=5, sh=(5, 6))
    im.save(f'w/lab{j}.png'); ovs.append((f'w/lab{j}.png', TS['s1'], TS['s2']))
# seam line
im = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); ImageDraw.Draw(im).rectangle([0, 954, 1080, 966], fill=(255, 255, 255, 255)); im.save('w/seam.png'); ovs.append(('w/seam.png', TS['s1'], TS['s2']))
# tag / badge / strip / follow
tag = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); dd = ImageDraw.Draw(tag); brush(dd, [48, 128, 470, 196], seed=3); mbtext(tag, (64, 126), "MAYDAY", MB(60), stroke=5, sh=(5, 6)); mbtext(tag, (60, 204), "DAY 22 OF 61", MB(40), stroke=7, sh=(5, 6), col=Y)
bd = Image.open('/home/claude/site/campaign/61-calls/covers/template/logo_badge.png').convert('RGBA'); bd = bd.resize((92, int(92 * bd.height / bd.width)))
tag.alpha_composite(bd, (940, 126)); tag.save('w/tag.png')
st = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); dd = ImageDraw.Draw(st); brush(dd, [40, 1590, 1040, 1700], seed=5); f = MB(60); s1 = "STRUGGLING? CALL OR TEXT 988"; mbtext(st, ((1080 - dd.textlength(s1, font=f)) / 2, 1602), s1, f, stroke=5, sh=(5, 6))
f = MB(33)
for s_, yy in (("VETERANS: 988, PRESS 1", 1716), ("RESPONDERS: SAFE CALL NOW 206-459-3020", 1762)): mbtext(st, ((1080 - dd.textlength(s_, font=f)) / 2, yy), s_, f, stroke=6, sh=(4, 5), col=Y)
st.save('w/strip.png')
fo = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); dd = ImageDraw.Draw(fo); f = MB(70); s_ = "FOLLOW FOR DAY 23"; w = dd.textlength(s_, font=f)
big = Image.open('/home/claude/site/campaign/61-calls/covers/template/logo_badge.png').convert('RGBA'); big = big.resize((330, int(330 * big.height / big.width))); brush(dd, [60, 1090, 1020, 1210], seed=9)
mbtext(fo, ((1080 - w) / 2, 1108), s_, f, stroke=8, sh=(5, 6), col=Y); fo.save('w/follow.png')
# flag icon
fl_ = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); dd = ImageDraw.Draw(fl_)
dd.line([(780, 880), (780, 560)], fill=(0, 0, 0, 255), width=22); dd.line([(780, 880), (780, 560)], fill=(235, 235, 235, 255), width=10)
poly = [(790, 562), (960, 590), (930, 640), (965, 700), (790, 676)]
dd.polygon([(x + 8, y + 8) for x, y in poly], fill=(0, 0, 0, 220)); dd.polygon(poly, fill=Y, outline=(0, 0, 0, 255), width=6); fl_.save('w/flag.png')
for k, al in enumerate((255, 190)): Image.new('RGBA', (1080, 1920), (255, 255, 255, al)).save(f'w/fl{k}.png')
S5 = TS['s5']; S6 = TS['s6']
ovs += [('w/tag.png', TS['s2'], TOT), ('w/strip.png', S6, TOT), ('w/follow.png', TS['s8'], TOT), ]
S2s = TS['s2']
seqs = []
inputs = ' '.join(f'-framerate 30 -i {q}' for q, _, _ in seqs) + ' ' + ' '.join(f'-i {p}' for p, _, _ in ovs)
fc = ''; last = '0:v'
for k, (q, st, nfr) in enumerate(seqs):
    fc += f"[{k+1}:v]setpts=PTS+{st:.3f}/TB[q{k}];[{last}][q{k}]overlay=0:0:enable='between(t,{st:.3f},{st + nfr/30:.3f})'[s{k}];"; last = f's{k}'
for k, (p, a, b) in enumerate(ovs):
    fc += f"[{last}][{k+1+len(seqs)}:v]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'[o{k}];"; last = f'o{k}'
fc = fc.rstrip(';').rsplit('[', 1)[0] + '[fin]'
run(f'ffmpeg -v error -y -i w/vcat.mp4 {inputs} -filter_complex "{fc}" -map "[fin]" -c:v libx264 -preset veryfast -crf 21 -pix_fmt yuv420p w/vid.mp4')
# ---------- audio ----------
ins = ''; fl = ''; mix = []; n = 0
def add(src, ss, dur, at, gain=0, fade=True):
    global ins, fl, n
    ins += f' -ss {ss:.3f} -t {dur:.3f} -i {src}'; ms = int(at * 1000)
    fl += f'[{n}:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,volume={gain}dB,afade=t=in:d=0.012,afade=t=out:st={dur-0.012:.3f}:d=0.012,adelay={ms}|{ms},apad=whole_dur={TOT:.2f}[x{n}];'; mix.append(f'[x{n}]'); n += 1
add('w/nc1B68.wav', 1.30 - O1, 3.9, TS['s1']); add('w/nc1B68.wav', 5.75 - O1, 4.6, TS['s2']); add('w/nc1B68.wav', 11.45 - O1, 7.85, TS['s3'])
add('w/nc1B68.wav', 19.85 - O1, 4.0, TS['s4']); add('w/nc1B68.wav', 24.65 - O1, 3.85, S5)
add('w/ncEA66.wav', 1.70 - OE, 33.25, TS['s7'], 3)
ins += ' -i w/door1.mp3'; dm = int((TS['s4'] + 2.2 + 0.8) * 1000); fl += f'[{n}:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,volume=2dB,atrim=0:2.5,afade=t=out:st=2.0:d=0.5,adelay={dm}|{dm},apad=whole_dur={TOT:.2f}[x{n}];'; mix.append(f'[x{n}]'); n += 1
def sfx(name, at, gain):
    global ins, fl, n
    ins += f' -i {SD}{name}.wav'; ms = int(max(0, at) * 1000)
    fl += f'[{n}:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,volume={gain}dB,adelay={ms}|{ms},apad=whole_dur={TOT:.2f}[x{n}];'; mix.append(f'[x{n}]'); n += 1
ins += ' -ss 0.15 -t 0.9 -i w/wh1.mp3'; fl += f'[{n}:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,volume=3dB,afade=t=in:d=0.01,afade=t=out:st=0.8:d=0.1,apad=whole_dur={TOT:.2f}[x{n}];'; mix.append(f'[x{n}]'); n += 1
# kick (Veo): legs enter ~+0.3, ball hits lens ~+1.5
sfx('whoosh', S2s + 0.25, -4); sfx('punch', S2s + 1.5, 2); sfx('thump', S2s + 1.5, 0)
# head open / brain / football (Veo)
sfx('boing', S2s + 2.3 + 0.15, -6); sfx('whoosh', S2s + 2.3 + 0.85, -8); sfx('slap', S2s + 2.3 + 1.85, -4)
pass; sfx('whoosh', TS['s3'] + 2.85, -12)
# flag falls / hits
sfx('whoosh', S5 + 1.35, -3); sfx('punch', S5 + 3.5, -3); sfx('thump', S5 + 3.5, -2); sfx('whoosh', S5 + VS - 0.1, -6)
# ref VO (gruff, sped 1.2x, tail trimmed)
ins += ' -i w/refvo.wav'; ms = int((S5 + VS) * 1000)
fl += f'[{n}:a]atrim=0:10.1,asetpts=PTS-STARTPTS,atempo=1.2,highpass=f=120,acompressor=threshold=-18dB:ratio=3,volume=3dB,adelay={ms}|{ms},apad=whole_dur={TOT:.2f}[x{n}];'; mix.append(f'[x{n}]'); n += 1
# rapid fire shirts
sfx('whoosh', TS['s8'], -6)
for k in range(0, 12, 3): sfx('slap', TS['s8'] + k * 8 / 30, -10)
ins += ' -i w/hn1.mp3'; hs = TS['s8'] + 0.15
fl += f'[{n}:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,atrim=0.35:3.2,asetpts=PTS-STARTPTS,volume=0dB,afade=t=out:st=2.0:d=0.8,adelay={int(hs*1000)}|{int(hs*1000)},apad=whole_dur={TOT:.2f}[x{n}];'; mix.append(f'[x{n}]'); n += 1
# music: hard bed under the sports part, soft pad under the car
ins += f' -stream_loop -1 -i {SD}hard1.wav'; hd = TS['s7'] + 0.6
fl += f'[{n}:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,volume=-25dB,atrim=0:{hd:.2f},afade=t=in:d=0.4,afade=t=out:st={hd-1.6:.2f}:d=1.6,apad=whole_dur={TOT:.2f}[x{n}];'; mix.append(f'[x{n}]'); n += 1
ps = TS['s7'] - 0.4; CT = TS['s7'] + 19.0; pl = CT + 1.0 - ps; ms = int(ps * 1000)
ins += ' -i /home/claude/site/campaign/61-calls/sounds/church_pad.wav'
fl += f'[{n}:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,volume=-21dB,atrim=0:{pl:.2f},afade=t=in:d=1.8,afade=t=out:st={pl-1.5:.2f}:d=1.5,adelay={ms}|{ms},apad=whole_dur={TOT:.2f}[x{n}];'; mix.append(f'[x{n}]'); n += 1
ins += ' -stream_loop -1 -i w/crowd_low.mp3'; cl_ = TOT - CT; cms = int(CT * 1000)
fl += f'[{n}:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,volume=-12dB,atrim=0:{cl_:.2f},asetpts=PTS-STARTPTS,afade=t=in:d=1.5,afade=t=out:st={cl_-1.5:.2f}:d=1.5,adelay={cms}|{cms},apad=whole_dur={TOT:.2f}[x{n}];'; mix.append(f'[x{n}]'); n += 1
fl += ''.join(mix) + f'amix=inputs={len(mix)}:normalize=0:duration=longest,alimiter=limit=0.95,loudnorm=I=-15.5:TP=-1.5:LRA=11[m]'
run(f'ffmpeg -v error -y {ins} -filter_complex "{fl}" -map "[m]" -t {TOT:.3f} -ar 48000 w/mix.wav')
run('ffmpeg -v error -y -i w/vid.mp4 -i w/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -shortest MAYDAY-Day-22-GAME-DAY-v5.mp4')
print('DONE', TOT)
