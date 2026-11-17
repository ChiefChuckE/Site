import subprocess, json, math, os
from PIL import Image, ImageDraw, ImageFont
def run(c): subprocess.run(c,shell=True,check=True)
SRC={"B":"../d17/sync2.mov","N":"../d17/sync1.mov","H":"../d17h/b.mov","A":"../d17h/a.mov"}
for k,f in SRC.items(): run(f'ffmpeg -v error -y -i {f} -map 0:a:0 -ac 2 -ar 48000 -af "highpass=f=80,loudnorm=I=-16:TP=-2:LRA=11" w{k}.wav')
BZ="crop=864:1536:168:400,scale=1080:1920,"; NA="crop=675:1200:262:480,scale=1080:1920,"; NB="crop=560:996:320:560,scale=1080:1920,"
WALL="crop=760:1351:160:330,scale=1080:1920,"; SHW="crop=760:1351:160:300,scale=1080:1920,"
NIGHT="eq=brightness=-0.14:saturation=0.55,colorbalance=bs=0.35:bm=0.25:bh=0.1,"
# (vsrc, vstart, dur, asrc, astart, alen, vf)
SEG=[("H",0.70,2.80,"B",30.62,1.36,""),
("B",32.64,1.22,"B",32.64,1.22,"crop=600:1067:200:300,scale=1080:1920,"),
("B",35.34,1.26,"B",35.34,1.26,"crop=675:1200:262:600,scale=1080:1920,"),
("H",42.30,1.00,"H",42.30,1.00,WALL),("H",46.60,1.00,"H",46.60,1.00,WALL),("H",50.10,1.00,"H",50.10,1.00,WALL),
("A",22.60,2.00,"A",22.60,2.00,SHW),("A",26.80,2.00,"A",26.80,2.00,SHW),("A",38.10,1.10,"A",38.10,1.10,SHW),
("B",19.84,1.06,"B",19.84,1.06,""),("B",21.56,1.44,"B",21.56,1.44,""),("B",23.36,1.14,"B",23.36,1.14,""),
("B",39.52,2.63,"B",39.52,2.63,BZ),("B",43.34,1.28,"B",43.34,1.28,""),("B",44.82,1.66,"B",44.82,1.66,BZ),
("H",16.00,2.38,"B",46.60,2.38,NIGHT),
("N",2.06,0.99,"N",2.06,0.99,NB),("H",52.90,1.20,"N",4.00,1.20,WALL),("N",6.28,1.12,"N",6.28,1.12,NB),("N",8.22,1.83,"N",8.22,1.83,NA),
("N",12.34,1.96,"N",12.34,1.96,NB),("N",14.78,1.07,"N",14.78,1.07,NA),("N",20.36,2.45,"N",20.36,1.99,NB)]
SPLIT=[9,10,11]
words={"B":json.load(open("../d17/b_words.json")),"N":json.load(open("../d17/n_words.json")),
"H":[(42.58,42.7,"One"),(42.78,43.0,"beer."),(46.86,47.0,"Two"),(47.1,47.4,"beers."),(50.38,50.5,"All"),(50.5,50.6,"of"),(50.62,50.8,"them.")],
"A":[(22.80,23,"Before"),(23.0,23.1,"you"),(23.15,23.2,"know"),(23.25,23.3,"it,"),(23.56,23.6,"you"),(23.68,23.8,"drink"),(23.82,23.9,"the"),(23.9,24.0,"whole"),(24.04,24.4,"bottle."),(38.30,38.4,"It"),(38.45,38.5,"has"),(38.6,38.7,"to"),(38.72,38.9,"stop.")]}
vl=open('v.txt','w'); al=open('a.txt','w'); t=0; log=[]
for i,(vs,va,dur,as_,aa,alen,vf) in enumerate(SEG):
    n=round(dur*30); d=n/30; alen=min(alen,d)
    run(f'ffmpeg -v error -y -ss {va:.3f} -i {SRC[vs]} -map 0:v:0 -an -vf "{vf}scale=1080:1920,fps=30,format=yuv420p" -frames:v {n} -c:v libx264 -preset veryfast -crf 16 s{i}.mp4')
    BGM={0:'burst.png',6:'burst.png',7:'burst.png',8:'burst.png'}
    if i==15: run('ffmpeg -v error -y -i s15.mp4 -i night_band.png -filter_complex overlay -c:v libx264 -preset veryfast -crf 16 -pix_fmt yuv420p s15b.mp4 && mv s15b.mp4 s15.mp4')
    if i in BGM:
        if os.path.exists(f'k{i}.mp4'): run(f'cp k{i}.mp4 s{i}.mp4')
        else: run(f'python3 matte.py s{i}.mp4 k{i}.mp4 {BGM[i]} && cp k{i}.mp4 s{i}.mp4')
    if i in (13,14):
        off=0 if i==13 else round(SEG[13][2]*30)
        run(f'ffmpeg -v error -y -i loop.mp4 -vf "select=gte(n\\,{off}),setpts=N/30/TB" -frames:v {n} -c:v libx264 -preset veryfast -crf 16 -pix_fmt yuv420p s{i}.mp4')
    vol={6:"volume=5dB,",7:"volume=0.8,",8:"volume=17dB,alimiter=limit=0.9,"}.get(i,"")
    run(f'ffmpeg -v error -y -i w{as_}.wav -af "atrim={aa:.4f}:{aa+alen:.4f},asetpts=PTS-STARTPTS,{vol}afade=t=in:d=0.015,afade=t=out:st={alen-0.03:.4f}:d=0.03,apad,atrim=0:{d:.4f}" -c:a pcm_s16le s{i}.wav')
    vl.write(f"file s{i}.mp4\n"); al.write(f"file s{i}.wav\n"); log.append((as_,aa,aa+alen,t,d)); t+=d
vl.close(); al.close(); TOT=t
run('ffmpeg -v error -y -f concat -i v.txt -c copy vcat.mp4'); run('ffmpeg -v error -y -f concat -i a.txt -c copy acat.wav')
def tl(k,s):
    for kk,a,b,tt,d in log:
        if kk==k and a<=s<b: return tt+s-a
W=[]
for k in words:
    for s,e,w in words[k]:
        x=tl(k,s)
        if x is not None: W.append((w,x))
W.sort(key=lambda x:x[1])
ch=[]; cur=[]
for w,s in W:
    cur.append((w,s))
    if w[-1] in ',.:?' or len(cur)==3: ch.append(cur); cur=[]
if cur: ch.append(cur)
CUES=[]
for i,c in enumerate(ch):
    a=c[0][1]; b=ch[i+1][0][1] if i+1<len(ch) else TOT-0.05
    CUES.append((" ".join(w for w,_ in c).upper(),a,min(b,a+2.0)))
KEYS={"SLEEP,","RELAXING,","MEDICATING.","BEER.","BEERS.","THEM.","BOTTLE.","STOP.","JOKE","CHOIR","PRACTICE,","COLD","ONE.","ALCOHOL","ALARM","LOUDER","LOUDER,","3:00","MORNING.","TEST.","WEEK.","SCARES","ANSWER","MAYDAY.","SUBSCRIBE","UNIFORM.","17","NOT","WHOLE"}
F='/usr/share/fonts/opentype/inter/Inter-Black.otf'; font=ImageFont.truetype(F,108)
for i,(txt,a,b) in enumerate(CUES):
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im)
    lines=[]; cu=''
    for w in txt.split():
        tt=(cu+' '+w).strip()
        if d.textlength(tt,font=font)>920 and cu: lines.append(cu); cu=w
        else: cu=tt
    lines.append(cu); y=1300-len(lines)*60
    for L in lines:
        x=(1080-d.textlength(L,font=font))/2
        for w in L.split():
            col=(255,214,0) if w in KEYS else (255,255,255)
            d.text((x,y+8),w,font=font,fill=(0,0,0,180)); d.text((x,y),w,font=font,fill=col,stroke_width=6,stroke_fill=(0,0,0))
            x+=d.textlength(w+' ',font=font)
        y+=120
    im.save(f'cap{i}.png')
hk=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(hk)
fh=ImageFont.truetype(F,62); t1="FIREFIGHTERS, COPS, MEDICS:"; t2="THIS ISN'T \"RELAXING.\""
d.rectangle([0,330,1080,540],fill=(0,0,0,215))
d.text(((1080-d.textlength(t1,font=fh))/2,352),t1,font=fh,fill=(255,255,255)); d.text(((1080-d.textlength(t2,font=fh))/2,440),t2,font=fh,fill=(255,45,61))
hk.save('hook.png'); HOOK_END=log[3][3]
tag=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(tag)
f1=ImageFont.truetype(F,52); f2=ImageFont.truetype(F,30)
d.rounded_rectangle([50,130,550,242],radius=14,fill=(200,16,46)); d.text((76,138),"MAYDAY",font=f1,fill='white'); d.text((78,202),"DAY 17 OF 61 · THE DRINK",font=f2,fill='white'); tag.save('tag.png')
st=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(st)
d.rectangle([0,1590,1080,1790],fill=(200,16,46,240))
fa=ImageFont.truetype(F,64); fb=ImageFont.truetype(F,34)
s1="STRUGGLING? CALL OR TEXT 988"; d.text(((1080-d.textlength(s1,font=fa))/2,1612),s1,font=fa,fill='white')
s2="Veterans: 988, press 1  ·  Responders: Safe Call Now 206-459-3020"; d.text(((1080-d.textlength(s2,font=fb))/2,1712),s2,font=fb,fill='white'); st.save('strip.png')
LAND=1.35
POPS=[("sleep",LAND+0.25),("pill",tl("B",35.60)),("beer",tl("H",42.58)),("beers",tl("H",46.86)),("clock",log[15][3]+0.1),("calendar",tl("N",4.68)),("fear",tl("N",6.72))]
for name,st0 in POPS:
    dur=1.3 if name!="beer" and name!="beers" else 0.85; nf=int(dur*30)
    src=Image.open(f'pop/{name}.png').convert('RGBA'); src=src.resize((380,int(380*src.height/src.width)),Image.LANCZOS)
    os.makedirs(f'pf_{name}',exist_ok=True)
    for j in range(nf):
        tt=j/30
        sc=0.3+0.9*tt/0.15 if tt<0.15 else (1.2-0.2*(tt-0.15)/0.1 if tt<0.25 else 1.0)
        al_=1.0 if tt<dur-0.2 else max(0,(dur-tt)/0.2)
        fr=Image.new('RGBA',(520,520),(0,0,0,0)); im=src.resize((max(1,int(src.width*sc)),max(1,int(src.height*sc))))
        rot=im.rotate(-8+16*math.sin(tt*6),resample=Image.BICUBIC,expand=True)
        if al_<1: rot.putalpha(rot.split()[3].point(lambda p:int(p*al_)))
        fr.paste(rot,((520-rot.width)//2,(520-rot.height)//2),rot); fr.save(f'pf_{name}/{j:03d}.png')
    run(f'ffmpeg -v error -y -framerate 30 -i pf_{name}/%03d.png -c:v qtrle p_{name}.mov')
ss=log[SPLIT[0]][3]; se=log[SPLIT[-1]][3]+log[SPLIT[-1]][4]; sd=se-ss
b1=Image.open('br1.png').convert('RGB'); w,h=b1.size; r=1080/960; cw=int(h*r)
b1.crop(((w-cw)//2,0,(w-cw)//2+cw,h)).resize((1080,960),Image.LANCZOS).save('br1c.png')
nf=int(sd*30)+2
run(f'ffmpeg -v error -y -loop 1 -i br1c.png -vf "zoompan=z=\'1+0.0015*on\':x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':d={nf}:s=1080x960:fps=30" -frames:v {nf} -c:v libx264 -crf 16 -pix_fmt yuv420p brs.mp4')
stripT=TOT-4.2
STP=log[8][3]+0.62-0.5; HIT2=STP+0.5
BUD=tl("N",9.34)
bd=Image.new("RGBA",(1080,1920),(0,0,0,0)); dd=ImageDraw.Draw(bd); fbd=ImageFont.truetype(F,80)
dd.rounded_rectangle([90,268,990,408],radius=40,fill=(255,214,0,255),outline=(0,0,0,255),width=8)
tb="WHERE'S MY BUDDY?"; dd.text(((1080-dd.textlength(tb,font=fbd))/2,290),tb,font=fbd,fill=(0,0,0))
bd.save("buddy.png")
# shake window at landing
fc=[]
fc.append("[0:v]split=2[base][sp]")
fc.append(f"[sp]trim=start={ss:.3f}:end={se:.3f},setpts=PTS-STARTPTS,crop=1080:960:0:760[bot]")
fc.append(f"[1:v][bot]vstack,setpts=PTS+{ss:.3f}/TB[splitd]")
fc.append(f"[base][splitd]overlay=enable='between(t,{ss:.3f},{se-0.02:.3f})':eof_action=pass[v1]")
fc.append(f"[v1]scale=1160:2062,crop=1080:1920:'40+if(between(t,{LAND},{LAND+0.45})+between(t,{HIT2:.3f},{HIT2+0.4:.3f}),38*sin(t*95),0)':'71+if(between(t,{LAND},{LAND+0.45})+between(t,{HIT2:.3f},{HIT2+0.4:.3f}),38*cos(t*80),0)'[v1s]")
fc.append(f"[v1s][2:v]overlay[v3]")
fc.append(f"[v3][3:v]overlay=enable='lt(t,{HOOK_END:.3f})'[v4]")
fc.append(f"[v4]drawbox=x=0:y=0:w='iw*t/{TOT:.3f}':h=14:color=0xFFD600@1:t=fill[v5]")
cur='[v5]'; idx=4; extra=[]

PIPS=[(0,264,560,520),(13,320,1040,520),(14,320,1040,520),(15,320,1040,520),(17,412,700,360)]
mk=Image.new('L',(400,400),0); ImageDraw.Draw(mk).ellipse([0,0,399,399],fill=255); mk.save('mask.png')
rg=Image.new('RGBA',(424,424),(0,0,0,0)); ImageDraw.Draw(rg).ellipse([2,2,421,421],outline=(255,255,255,255),width=12); rg.save('ring.png')
for j,(si,cx,cy,cs) in enumerate(PIPS):
    _,_,_,as_,aa,alen,_=SEG[si]; t0=log[si][3]
    run(f'ffmpeg -v error -y -ss {aa:.3f} -i {SRC[as_]} -an -t {alen:.3f} -vf "crop={cs}:{cs}:{cx}:{cy},scale=400:400,fps=30,format=yuv420p" -c:v libx264 -crf 16 pipsrc{j}.mp4')
    extra.append(f'-i pipsrc{j}.mp4 -loop 1 -i mask.png -loop 1 -i ring.png')
    fc.append(f"[{idx}:v]format=rgba[pc{j}];[{idx+1}:v]format=gray[mk{j}];[pc{j}][mk{j}]alphamerge=shortest=1,setpts=PTS+{t0:.3f}/TB[pm{j}];{cur}[pm{j}]overlay=650:1460:eof_action=pass[pq{j}];[pq{j}][{idx+2}:v]overlay=638:1448:enable='between(t,{t0:.3f},{t0+alen-0.03:.3f})'[pr{j}]"); cur=f'[pr{j}]'; idx+=3
for j,(name,st0) in enumerate(POPS):
    extra.append(f'-i p_{name}.mov')
    fc.append(f"[{idx}:v]setpts=PTS+{st0:.3f}/TB[pp{j}];{cur}[pp{j}]overlay=560:330:eof_action=pass[pv{j}]"); cur=f'[pv{j}]'; idx+=1
SM=tl('B',40.10)
extra.append('-i smash.mov')
fc.append(f"[{idx}:v]setpts=PTS+{SM:.3f}/TB[sm];{cur}[sm]overlay=90:300:eof_action=pass[vsm]"); cur='[vsm]'; idx+=1
RS=log[6][3]; RE=log[8][3]+log[8][4]
extra.append('-loop 1 -i ribbon.png')
fc.append(f"{cur}[{idx}:v]overlay=420:880:enable='between(t,{RS:.3f},{RE-0.02:.3f})'[vr]"); cur='[vr]'; idx+=1
extra.append('-i stopsign.mov')
fc.append(f"[{idx}:v]setpts=PTS+{STP:.3f}/TB[stp];{cur}[stp]overlay=0:0:eof_action=pass[vstp]"); cur='[vstp]'; idx+=1
extra.append('-loop 1 -i jesse_top.png')
fc.append(f"{cur}[{idx}:v]overlay=0:0:enable='between(t,31,33)*lt(mod(t,0.3),0.2)'[vj]"); cur='[vj]'; idx+=1
extra.append('-loop 1 -i buddy.png')
fc.append(f"{cur}[{idx}:v]overlay=enable='between(t,{BUD:.3f},{min(BUD+1.9,30.95):.3f})'[vb]"); cur='[vb]'; idx+=1
extra.append('-loop 1 -i strip.png')
fc.append(f"{cur}[{idx}:v]overlay=enable='gte(t,{stripT:.3f})'[vs]"); cur='[vs]'; idx+=1
for i,(t_,a,b) in enumerate(CUES):
    extra.append(f'-i cap{i}.png')
    fc.append(f"{cur}[{idx}:v]overlay=enable='between(t,{a:.3f},{b:.3f})'[x{i}]"); cur=f'[x{i}]'; idx+=1
open('fc.txt','w').write(";".join(fc))
run(f'ffmpeg -v error -y -i vcat.mp4 -i brs.mp4 -i tag.png -loop 1 -i hook.png '+' '.join(extra)+f' -filter_complex_script fc.txt -map "{cur}" -t {TOT:.3f} -c:v libx264 -crf 17 -preset medium vcap.mp4')
ev=[("fall",LAND-0.5,-8),("crash",LAND,0),("boing",LAND+0.08,-3),("thump",tl("B",35.60),-4),
("thump",log[3][3]+0.25,-3),("thump",log[4][3]+0.25,-2),("thump",log[5][3]+0.25,-1),("thump",log[8][3]+0.15,-2),
("whoosh",ss-0.15,-6),("alarm",log[15][3],-9),("smash",SM+0.55,-1),("brake",HIT2-0.7,-7),("punch",HIT2,2),("dod_hit",TOT-0.75,6),("pop",BUD,-4)]+[("pop",s0,-8) for _,s0 in POPS]
ins=" ".join(f"-i {n}.wav" for n,_,_ in ev); parts=[]; labs=[]
for j,(n,s0,g) in enumerate(ev):
    D=max(0,int(s0*1000)); parts.append(f"[{j+1}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={D}|{D},volume={g}dB[e{j}]"); labs.append(f"[e{j}]")
fa_="; ".join(parts)+f";[0:a]{''.join(labs)}amix=inputs={len(ev)+1}:duration=first:normalize=0[a]"
run(f'ffmpeg -v error -y -i acat.wav {ins} -filter_complex "{fa_}" -map "[a]" amix.wav')
run(f'ffmpeg -v error -y -i vcap.mp4 -i amix.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le body.mov')
json.dump({"log":log,"cues":CUES,"strip":stripT},open('plan.json','w'),indent=0)
print("TOT",TOT,"cues",len(CUES)); print(" | ".join(c for c,_,_ in CUES))
