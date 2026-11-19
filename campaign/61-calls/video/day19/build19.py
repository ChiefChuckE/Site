import subprocess, json, math, os, re, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
def run(c): subprocess.run(c,shell=True,check=True)
for f in ['thump.wav','pop.wav','whoosh.wav','boing.wav','punch.wav','dod_hit.wav','click.wav','ding.wav','powerdown.wav','yeow.wav']:
    if not os.path.exists(f): run(f'cp ../d18g/{f} .')
F='/usr/share/fonts/opentype/inter/Inter-Black.otf'; EM='/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
SRC={"T":"T.mov","K":"c16.mov","C":"c14.mov","N":"c13.mov","L":"c12.mov","U":"c15.mov","R":"c17.mov"}
run('ffmpeg -v error -y -i T.mov -map 0:a:0 -ac 2 -ar 48000 -af "highpass=f=80,loudnorm=I=-16:TP=-2:LRA=11" wT.wav')
FL="hflip,"; CH="crop=720:1280:0:600,"; LK="crop=810:1440:135:300,"; CO="crop=600:1067:240:700,"
Q=0.04
SEG=[("K",6.4,1.7,6.0,1.7,"",1),("T",0.30,1.75,0.30,1.75,FL,1),("C",0.9,2.2,3.50,2.2,CH,1),("N",0,2.02,8.68,2.02,"",1),("N",2.1,0.8,6.2,0.8,"",1),
("T",16.66,2.3,16.66,2.3,FL,1),("L",3.0,1.2,6.0,1.2,LK,1),("L",8.8,1.3,6.3,1.3,LK,1),("L",14.5,0.9,6.9,0.9,"",1),
("K",4.4,2.3,24.26,2.3,"",1),("K",7.2,0.8,6.0,0.8,"",1),("T",27.28,1.38,27.28,1.38,FL,1),("T",29.80,2.16,29.80,2.16,FL,1),
("U",0.8,2.2,34.16,2.2,CO,1),("T",38.26,1.24,38.26,1.24,FL,1),("R",6.5,2.06,40.04,2.06,"",1),("R",8.6,1.1,6.0,1.1,"",1),
("T",44.92,2.08,44.92,2.08,FL,1),("T",47.05,1.2,47.05,1.2,FL,1),("T",48.45,2.1,48.45,2.1,FL,1),("R",12.4,2.6,52.9,1.25,"",1)]
QUIET={0,4,6,7,8,10,16}
OFF=0.717   # transcript times are raw audio-stream times; T.mov audio is delayed by this much
RT={0:12.0,4:12.2,6:12.0,7:12.3,8:12.0,10:12.0,16:12.0}
SEG=[(vs,(va+OFF if vs=="T" else va),dur,(RT[i] if i in QUIET else aa+OFF),alen,vf,vol) for i,(vs,va,dur,aa,alen,vf,vol) in enumerate(SEG)]
Wd=[(0.48,"We"),(0.56,"don't"),(0.78,"say"),(0.98,"we're"),(1.22,"scared."),(3.68,"We"),(3.84,"just"),(4.1,"sit"),(4.56,"facing"),(4.9,"the"),(5.06,"door."),
(8.84,"I"),(8.96,"count"),(9.18,"the"),(9.36,"exits"),(9.72,"at"),(9.9,"parties."),(16.84,"I"),(16.98,"watch"),(17.26,"hands"),(17.54,"at"),(17.64,"the"),(17.76,"grocery"),(18.22,"store."),
(24.42,"The"),(24.6,"toaster"),(24.96,"pops,"),(25.34,"I'm"),(25.48,"ready"),(25.64,"to"),(25.88,"fight."),(27.46,"It's"),(27.54,"not"),(27.72,"a"),(27.9,"quirk."),
(29.98,"That's"),(30.18,"a"),(30.34,"body"),(30.74,"still"),(31.0,"on"),(31.22,"duty."),(34.34,"Nobody"),(34.72,"told"),(34.94,"it"),(35.06,"the"),(35.2,"shift"),(35.46,"was"),(35.7,"over."),
(38.44,"You're"),(38.7,"home."),(40.22,"You're"),(40.38,"allowed"),(40.76,"to"),(40.94,"stand"),(41.32,"down."),(45.08,"This"),(45.24,"is"),(45.36,"day"),(45.56,"19"),(45.96,"of"),(46.24,"61."),
(47.18,"Call"),(47.44,"your"),(47.64,"mayday."),(48.52,"Send"),(48.7,"this"),(48.86,"to"),(49.04,"someone"),(49.32,"who"),(49.42,"wore"),(49.6,"the"),(49.7,"uniform."),
(53.0,"I'm"),(53.06,"ready"),(53.22,"to"),(53.48,"fight!")]
Wd=[(t_+OFF,w_) for t_,w_ in Wd]
vl=open('v.txt','w'); al=open('a.txt','w'); t=0; log=[]
for i,(vs,va,dur,aa,alen,vf,vol) in enumerate(SEG):
    n=round(dur*30); d=n/30; alen=min(alen,d)
    run(f'ffmpeg -v error -y -ss {va:.3f} -i {SRC[vs]} -map 0:v:0 -an -vf "{vf}scale=1080:1920:flags=lanczos,fps=30,format=yuv420p" -frames:v {n} -c:v libx264 -preset veryfast -crf 16 s{i}.mp4')
    run(f'ffmpeg -v error -y -i wT.wav -af "atrim={aa:.4f}:{aa+alen:.4f},asetpts=PTS-STARTPTS,volume={vol},afade=t=in:d=0.04,afade=t=out:st={alen-0.09:.4f}:d=0.09,apad,atrim=0:{d:.4f}" -c:a pcm_s16le s{i}.wav')
    vl.write(f"file s{i}.mp4\n"); al.write(f"file s{i}.wav\n"); log.append((aa,aa+alen,t,d,0 if i in QUIET else 1)); t+=d
vl.close(); al.close(); TOT=t
run('ffmpeg -v error -y -f concat -i v.txt -c copy vcat.mp4'); run('ffmpeg -v error -y -f concat -i a.txt -c copy acat.wav')
def tl(s):
    for a,b,tt,d,vol in log:
        if vol==1 and a<=s<b: return tt+s-a
def T0(i): return log[i][2]
W=[(w,tl(s)) for s,w in Wd if tl(s) is not None]
ch=[]; cur=[]
for w,s in W:
    cur.append((w,s))
    if w[-1] in ',.:?!' or len(cur)==3: ch.append(cur); cur=[]
if cur: ch.append(cur)
CUES=[]
for i,c in enumerate(ch):
    a=c[0][1]; b=ch[i+1][0][1] if i+1<len(ch) else TOT-0.05
    e=min(b,a+1.6)
    for k in range(len(SEG)):   # do not run into silent gag segments
        if log[k][4]!=1 and a<T0(k)<e: e=T0(k)-0.02
    CUES.append((" ".join(w for w,_ in c).upper(),a,e))
CUES[-1]=(CUES[-1][0],CUES[-1][1],T0(20)+1.05)
KEYS={"SCARED.","DOOR.","EXITS","HANDS","TOASTER","FIGHT.","FIGHT!","QUIRK.","DUTY.","OVER.","HOME.","DOWN.","MAYDAY.","UNIFORM.","19"}
font=ImageFont.truetype(F,108)
for i,(txt,a,b) in enumerate(CUES):
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im); lines=[]; cu=''
    for w in txt.split():
        tt=(cu+' '+w).strip()
        if d.textlength(tt,font=font)>920 and cu: lines.append(cu); cu=w
        else: cu=tt
    lines.append(cu); y=1300-len(lines)*60
    for L in lines:
        x=(1080-d.textlength(L,font=font))/2
        for w in L.split():
            col=(255,214,0) if w in KEYS else (255,255,255)
            d.text((x,y+8),w,font=font,fill=(0,0,0,180)); d.text((x,y),w,font=font,fill=col,stroke_width=6,stroke_fill=(0,0,0)); x+=d.textlength(w+' ',font=font)
        y+=120
    im.save(f'cap{i}.png')
def banner(name,lines,box,fs=62):
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im); f=ImageFont.truetype(F,fs); d.rectangle(box,fill=(0,0,0,215)); y=box[1]+22
    for txt,col in lines: d.text(((1080-d.textlength(txt,font=f))/2,y),txt,font=f,fill=col); y+=fs+26
    im.save(name)
banner('hook.png',[("INTERNATIONAL MEN'S DAY",(255,214,0)),("WE DON'T SAY WE'RE SCARED.",(255,255,255))],[0,330,1080,540])
tag=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(tag); f1=ImageFont.truetype(F,52); f2=ImageFont.truetype(F,28)
d.rounded_rectangle([50,130,480,242],radius=14,fill=(200,16,46)); d.text((76,138),"MAYDAY",font=f1,fill='white'); d.text((78,202),"DAY 19 OF 61 · THE SCAN",font=f2,fill='white'); tag.save('tag.png')
st=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(st); d.rectangle([0,1590,1080,1790],fill=(200,16,46,240)); fa=ImageFont.truetype(F,64); fb=ImageFont.truetype(F,34)
s1="STRUGGLING? CALL OR TEXT 988"; d.text(((1080-d.textlength(s1,font=fa))/2,1612),s1,font=fa,fill='white')
s2="Veterans: 988, press 1  ·  Responders: Safe Call Now 206-459-3020"; d.text(((1080-d.textlength(s2,font=fb))/2,1712),s2,font=fb,fill='white'); st.save('strip.png')
def label(name,items):
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im)
    for txt,cx,cy,fs,bg,fg in items:
        f=ImageFont.truetype(F,fs); w=d.textlength(txt,font=f)
        d.rounded_rectangle([cx-w/2-28,cy-fs/2-18,cx+w/2+28,cy+fs/2+26],radius=22,fill=bg,outline=(0,0,0,255),width=7); d.text((cx-w/2,cy-fs/2-6),txt,font=f,fill=fg)
    im.save(name)
Y=(255,214,0,255); R=(200,16,46,255); K=(0,0,0); Wt=(255,255,255)
label('l_what.png',[("WHAT WAS THAT?!",540,1250,96,Y,K)]); label('l_lock1.png',[("LOCKED.",540,1250,130,Y,K)]); label('l_lock2.png',[("CHECK AGAIN.",540,1250,110,Y,K)]); label('l_lock3.png',[("ONE MORE TIME.",540,1250,100,R,Wt)])
label('l_toast.png',[("IT'S TOAST.",540,1250,130,R,Wt)]); label('l_down.png',[("STANDING DOWN...",540,1250,96,Y,K)]); label('l_end.png',[("TOASTER.",540,1180,150,R,Wt)]); label('l_follow.png',[("FOLLOW FOR DAY 20",540,1400,72,Y,K)])
for pct,nm,col in [(100,'m100',(230,20,40)),(0,'m0',(60,210,90)),(1000,'m1000',(230,20,40))]:
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im); d.rounded_rectangle([510,130,1040,242],radius=14,fill=(0,0,0,225),outline=(255,255,255,255),width=4)
    d.text((530,140),"THREAT LEVEL",font=ImageFont.truetype(F,32),fill='white'); t_=f"{pct}%"; fp=ImageFont.truetype(F,52 if pct<1000 else 44); d.text((1024-d.textlength(t_,font=fp),176),t_,font=fp,fill=col)
    d.rounded_rectangle([530,190,860,226],radius=10,fill=(60,60,60,255))
    if pct: d.rounded_rectangle([530,190,860,226],radius=10,fill=col+(255,))
    im.save(nm+'.png')
def emoji(ch_,name):
    f=ImageFont.truetype(EM,109); im=Image.new('RGBA',(160,160),(0,0,0,0)); ImageDraw.Draw(im).text((12,16),ch_,font=f,embedded_color=True)
    a=im.split()[3]; out=Image.new('RGBA',(160,160),(0,0,0,0)); out.paste((255,255,255,255),(0,0),a.filter(ImageFilter.MaxFilter(9))); out.paste(im,(0,0),im); out.resize((380,380),Image.LANCZOS).save(f'e_{name}.png')
for c_,nm in [("\U0001F35E","bread"),("\U0001F6AA","door"),("\U0001F440","eyes"),("\U0001F6D2","cart"),("\U0001F512","lock"),("\U0001F60C","relief")]: emoji(c_,nm)
POPS=[("bread",0.25,60,560,1.2),("door",tl(5.06+OFF),60,520,0.8),("eyes",tl(17.26+OFF),60,520,0.9),("cart",tl(17.76+OFF),640,560,0.8),("lock",T0(6)+0.1,60,560,0.9),("bread",tl(24.6+OFF),640,520,0.9),("relief",T0(16)+0.2,60,560,0.8)]
for j,(name,st0,x,y,dur) in enumerate(POPS):
    nf=int(dur*30); src=Image.open(f'e_{name}.png'); os.makedirs(f'pf{j}',exist_ok=True)
    for q in range(nf):
        tt=q/30; sc=0.3+0.9*tt/0.15 if tt<0.15 else (1.2-0.2*(tt-0.15)/0.1 if tt<0.25 else 1.0); al_=1.0 if tt<dur-0.2 else max(0,(dur-tt)/0.2)
        fr=Image.new('RGBA',(520,520),(0,0,0,0)); im=src.resize((max(1,int(src.width*sc)),max(1,int(src.height*sc)))); rot=im.rotate(-8+16*math.sin(tt*6+j),resample=Image.BICUBIC,expand=True)
        if al_<1: rot.putalpha(rot.split()[3].point(lambda p:int(p*al_)))
        fr.paste(rot,((520-rot.width)//2,(520-rot.height)//2),rot); fr.save(f'pf{j}/{q:03d}.png')
    run(f'ffmpeg -v error -y -framerate 30 -i pf{j}/%03d.png -c:v qtrle p{j}.mov')
stripT=T0(17); HOOK_END=T0(2); DOWN=T0(16)+0.2; END=T0(20)
fc=[f"[0:v]scale=1160:2062,crop=1080:1920:'40+if(between(t,0.3,0.9)+between(t,{END+0.3:.2f},{END+0.9:.2f}),30*sin(t*95),0)':'71+if(between(t,0.3,0.9)+between(t,{END+0.3:.2f},{END+0.9:.2f}),30*cos(t*80),0)'[v1s]","[v1s][1:v]overlay[v3]",f"[v3][2:v]overlay=enable='lt(t,{HOOK_END:.3f})'[v4]",f"[v4]drawbox=x=0:y=0:w='iw*t/{TOT:.3f}':h=14:color=0xFFD600@1:t=fill[v5]"]
cur='[v5]'; idx=3; extra=[]
def ov(png,a,b):
    global cur,idx
    extra.append(f'-loop 1 -i {png}'); fc.append(f"{cur}[{idx}:v]overlay=enable='between(t,{a:.3f},{b:.3f})'[o{idx}]"); cur=f'[o{idx}]'; idx+=1
ov('m100.png',0,DOWN-0.01); ov('m0.png',DOWN,END-0.01); ov('m1000.png',END,TOT)
ov('l_what.png',T0(4),T0(5)-0.02); ov('l_lock1.png',T0(6)+0.3,T0(7)-0.02); ov('l_lock2.png',T0(7)+0.2,T0(8)-0.02); ov('l_lock3.png',T0(8),T0(9)-0.02); ov('l_toast.png',T0(10),T0(11)-0.02)
ov('l_down.png',T0(16),T0(17)-0.02); ov('l_end.png',END+1.1,TOT); ov('l_follow.png',TOT-2.0,TOT)
PIPS=[2,3,9,13,15]
mk=Image.new('L',(400,400),0); ImageDraw.Draw(mk).ellipse([0,0,399,399],fill=255); mk.save('mask.png')
rg=Image.new('RGBA',(424,424),(0,0,0,0)); ImageDraw.Draw(rg).ellipse([2,2,421,421],outline=(255,255,255,255),width=12); rg.save('ring.png')
for j,si in enumerate(PIPS):
    aa=SEG[si][3]; d_=log[si][3]; t0=T0(si)
    run(f'ffmpeg -v error -y -ss {aa:.3f} -i T.mov -an -t {d_:.3f} -vf "hflip,scale=1080:1920:flags=lanczos,crop=560:560:260:200,scale=400:400,fps=30,format=yuv420p" -c:v libx264 -crf 16 pipsrc{j}.mp4')
    extra.append(f'-i pipsrc{j}.mp4 -loop 1 -i mask.png -loop 1 -i ring.png')
    fc.append(f"[{idx}:v]format=rgba[pc{j}];[{idx+1}:v]format=gray[mk{j}];[pc{j}][mk{j}]alphamerge=shortest=1,setpts=PTS+{t0:.3f}/TB[pm{j}];{cur}[pm{j}]overlay=650:1460:eof_action=pass[pq{j}];[pq{j}][{idx+2}:v]overlay=638:1448:enable='between(t,{t0:.3f},{t0+d_-0.03:.3f})'[pr{j}]"); cur=f'[pr{j}]'; idx+=3
for j,(name,st0,x,y,dur) in enumerate(POPS):
    extra.append(f'-i p{j}.mov'); fc.append(f"[{idx}:v]setpts=PTS+{st0:.3f}/TB[pp{j}];{cur}[pp{j}]overlay={x}:{y}:eof_action=pass[pv{j}]"); cur=f'[pv{j}]'; idx+=1
extra.append('-loop 1 -i strip.png'); fc.append(f"{cur}[{idx}:v]overlay=enable='between(t,{stripT:.3f},{END-0.01:.3f})'[vs]"); cur='[vs]'; idx+=1
for i,(t_,a,b) in enumerate(CUES):
    extra.append(f'-i cap{i}.png'); fc.append(f"{cur}[{idx}:v]overlay=enable='between(t,{a:.3f},{b:.3f})'[x{i}]"); cur=f'[x{i}]'; idx+=1
open('fc.txt','w').write(";".join(fc))
run(f'ffmpeg -v error -y -i vcat.mp4 -i tag.png -loop 1 -i hook.png '+' '.join(extra)+f' -filter_complex_script fc.txt -map "{cur}" -t {TOT:.3f} -c:v libx264 -crf 17 -preset veryfast vcap.mp4')
ev=[("boing",0.15,0),("yeow",0.45,-4),("thump",0.5,-3),("thump",T0(4)+0.15,0),("click",T0(6)+0.3,5),("click",T0(7)+0.6,5),("thump",T0(8),-2),("boing",T0(9)+1.7,-2),("punch",T0(10),0),("yeow",T0(10)+0.05,-6),
("powerdown",DOWN,-3),("ding",DOWN+0.3,-4),("boing",END+0.2,0),("yeow",END+1.2,-5),("punch",END+1.9,-2),("dod_hit",TOT-0.75,6)]+[("pop",p[1],-9) for p in POPS]
ins=" ".join(f"-i {n}.wav" for n,_,_ in ev); parts=[]; labs=[]
for j,(n,s0,g) in enumerate(ev):
    D=max(0,int(s0*1000)); parts.append(f"[{j+1}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={D}|{D},volume={g}dB[e{j}]"); labs.append(f"[e{j}]")
fa_="; ".join(parts)+f";[0:a]{''.join(labs)}amix=inputs={len(ev)+1}:duration=first:normalize=0[a]"
run(f'ffmpeg -v error -y -i acat.wav {ins} -filter_complex "{fa_}" -map "[a]" amix.wav')
run('ffmpeg -v error -y -i vcap.mp4 -i amix.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le body.mov')
r=subprocess.run('ffmpeg -hide_banner -i body.mov -af loudnorm=I=-15.5:TP=-1.5:LRA=11:print_format=json -f null -',shell=True,capture_output=True,text=True).stderr
m=json.loads(re.search(r'\{[^{}]*"input_i"[^{}]*\}',r).group(0))
run(f'ffmpeg -v error -y -i body.mov -af "loudnorm=I=-15.5:TP=-1.5:LRA=11:measured_I={m["input_i"]}:measured_TP={m["input_tp"]}:measured_LRA={m["input_lra"]}:measured_thresh={m["input_thresh"]}:offset={m["target_offset"]}:linear=true" -c:v libx264 -crf 21 -preset fast -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart MAYDAY-Day-19-THE-SCAN.mp4')
print("TOT",TOT); print(" | ".join(c for c,_,_ in CUES)); print([round(T0(i),2) for i in range(len(SEG))])
