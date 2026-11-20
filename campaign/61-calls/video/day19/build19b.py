import subprocess, json, math, os, re, random, numpy as np, wave
from PIL import Image, ImageDraw, ImageFont, ImageFilter
def run(c): subprocess.run(c,shell=True,check=True)
for f in ['thump.wav','pop.wav','whoosh.wav','boing.wav','punch.wav','dod_hit.wav','click.wav','ding.wav','powerdown.wav','yeow.wav']:
    if not os.path.exists(f): run(f'cp ../d18g/{f} .')
FI='/tmp/claude-0/fonts/gf/ofl/montserrat/Montserrat-Italic[wght].ttf'; F='/usr/share/fonts/opentype/inter/Inter-Black.otf'; EM='/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
def MB(sz):
    f=ImageFont.truetype(FI,sz); f.set_variation_by_name('Black Italic'); return f
OFF=0.717
SRC={"T":"T.mov","K":"c16.mov","C":"c14.mov","N":"c13.mov","L":"c12.mov","U":"c15.mov","R":"c17.mov","Z":"FRZ.mp4","B":"BOOM.mp4"}
if not os.path.exists("BOOM.mp4"): run('ffmpeg -v error -y -ss 2.55 -i c13.mov -frames:v 1 -update 1 boomf.png'); run('ffmpeg -v error -y -loop 1 -framerate 30 -i boomf.png -t 2 -vf "scale=1080:1920,format=yuv420p" -c:v libx264 -crf 14 BOOM.mp4')
if not os.path.exists('wT.wav'): run('ffmpeg -v error -y -i T.mov -map 0:a:0 -ac 2 -ar 48000 -af "highpass=f=80,loudnorm=I=-16:TP=-2:LRA=11" wT.wav')
FL="hflip,"; CH="crop=720:1280:0:600,"; LK="crop=810:1440:135:300,"; CO="crop=600:1067:240:700,"
# (vsrc, vstart, dur, araw or None, vf, name)   T video start given as RAW (offset added below); araw None = room tone
S=[("K",4.9,3.2,None,"","hook"),
("T",0.30,1.95,0.30,FL,""),
("C",0.9,2.45,3.50,CH,""),
("N",0,2.05,8.68,"",""),
("N",2.1,0.45,None,"","flinch"),("B",0,1.4,None,"","boom"),
("T",16.66,2.5,16.66,FL,""),
("L",3.0,1.6,None,LK,"lock1"),("L",8.6,2.0,None,LK,"lock2"),("L",14.6,1.1,None,"","lock3"),("L",23.8,1.6,None,LK,"lock4"),
("K",5.45,1.05,24.26,"","pops"),
("T",52.90,1.08,52.90,FL,"punch1"),("Z",0,1.2,None,"","frz"),
("T",27.28,1.5,27.28,FL,""),("T",29.80,2.3,29.80,FL,""),
("U",0.8,2.3,34.16,CO,""),
("T",38.26,1.4,38.26,FL,""),
("R",6.0,2.2,40.04,"",""),("R",8.2,2.0,None,"","hold"),
("T",44.92,2.1,44.92,FL,""),("T",47.05,1.25,47.05,FL,""),("T",48.45,2.2,48.45,FL,""),
("R",12.2,3.2,None,"","end")]
IX={nm:i for i,s in enumerate(S) if (nm:=s[5])}
RTB=12.0
IXR=[i for i,sg in enumerate(S) if sg[0]=='R'][0]
IXU=[i for i,sg in enumerate(S) if sg[0]=='U'][0]
Wd=[(0.48,"We"),(0.56,"don't"),(0.78,"say"),(0.98,"we're"),(1.22,"scared."),(3.68,"We"),(3.84,"just"),(4.1,"sit"),(4.56,"facing"),(4.9,"the"),(5.06,"door."),
(8.84,"I"),(8.96,"count"),(9.18,"the"),(9.36,"exits"),(9.72,"at"),(9.9,"parties."),(16.84,"I"),(16.98,"watch"),(17.26,"hands"),(17.54,"at"),(17.64,"the"),(17.76,"grocery"),(18.22,"store."),
(24.42,"The"),(24.6,"toaster"),(24.96,"pops,"),(27.46,"It's"),(27.54,"not"),(27.72,"a"),(27.9,"quirk."),
(29.98,"That's"),(30.18,"a"),(30.34,"body"),(30.74,"still"),(31.0,"on"),(31.22,"duty."),(34.34,"Nobody"),(34.72,"told"),(34.94,"it"),(35.06,"the"),(35.2,"shift"),(35.46,"was"),(35.7,"over."),
(38.44,"You're"),(38.7,"home."),(40.22,"You're"),(40.38,"allowed"),(40.76,"to"),(40.94,"stand"),(41.32,"down."),(45.08,"This"),(45.24,"is"),(45.36,"day"),(45.56,"19"),(45.96,"of"),(46.24,"61."),
(47.18,"Call"),(47.44,"your"),(47.64,"mayday."),(48.52,"Send"),(48.7,"this"),(48.86,"to"),(49.04,"someone"),(49.32,"who"),(49.42,"wore"),(49.6,"the"),(49.7,"uniform."),
(53.0,"I'm"),(53.06,"ready"),(53.22,"to"),(53.48,"fight!")]
vl=open('v.txt','w'); al=open('a.txt','w'); t=0; log=[]
for i,(vs,va,dur,ar,vf,nm) in enumerate(S):
    n=round(dur*30); d=n/30; vss=va+OFF if vs=="T" else va
    if vs=="Z":   # freeze on the last frame of the (already cut out) punch shot, snap zoom
        run(f'ffmpeg -v error -y -sseof -0.05 -i s{i-1}.mp4 -frames:v 1 -update 1 frz.png'); im=Image.open('frz.png').convert('RGB'); os.makedirs('zf',exist_ok=True)
        for q in range(n):
            z=(1.0+0.22*min(1,q/4))*(1+0.0012*q); w=1080/z; h=1920/z; x=(1080-w)*0.45; y=(1920-h)*0.42
            im.crop((int(x),int(y),int(x+w),int(y+h))).resize((1080,1920),Image.LANCZOS).save(f'zf/{q:03d}.png')
        run('ffmpeg -v error -y -framerate 30 -i zf/%03d.png -c:v libx264 -crf 14 -pix_fmt yuv420p FRZ.mp4')
    run(f'ffmpeg -v error -y -ss {vss:.3f} -i {SRC[vs]} -map 0:v:0 -an -vf "{vf}scale=1080:1920:flags=lanczos,fps=30,format=yuv420p" -frames:v {n} -c:v libx264 -preset veryfast -crf 16 s{i}.mp4')
    if vs=="T":
        import glob
        hit=glob.glob(f"mk_{va:.3f}_{n}_*.mp4"); key=hit[0] if hit else f"mk_{va:.3f}_{n}_0.mp4"
        if not hit: run(f'python3 matte2.py s{i}.mp4 {key} 0')
        run(f'cp {key} s{i}.mp4')
    aa=0 if ar is None else ar+OFF; vol=1.0
    if ar is None: run(f'ffmpeg -v error -y -f lavfi -i anullsrc=r=48000:cl=stereo -t {d:.4f} -c:a pcm_s16le s{i}.wav')
    else: run(f'ffmpeg -v error -y -i wT.wav -af "atrim={aa:.4f}:{aa+d:.4f},asetpts=PTS-STARTPTS,volume={vol},afade=t=in:d=0.04,afade=t=out:st={d-0.09:.4f}:d=0.09,apad,atrim=0:{d:.4f}" -c:a pcm_s16le s{i}.wav')
    vl.write(f"file s{i}.mp4\n"); al.write(f"file s{i}.wav\n"); log.append((ar,d,t)); t+=d
vl.close(); al.close(); TOT=t
run('ffmpeg -v error -y -f concat -i v.txt -c copy vcat.mp4'); run('ffmpeg -v error -y -f concat -i a.txt -c copy acat.wav')
def T0(i): return log[i][2] if isinstance(i,int) else log[IX[i]][2]
def TE(i): i=i if isinstance(i,int) else IX[i]; return log[i][2]+log[i][1]
def tl(s):
    for ar,d,tt in log:
        if ar is not None and ar<=s<ar+d: return tt+s-ar
W=[(w,tl(s)) for s,w in Wd if tl(s) is not None]
ch=[]; cur=[]
for w,s in W:
    cur.append((w,s))
    if w[-1] in ',.:?!' or len(cur)==3: ch.append(cur); cur=[]
if cur: ch.append(cur)
CUES=[]
for i,c in enumerate(ch):
    a=c[0][1]; b=ch[i+1][0][1] if i+1<len(ch) else TOT; e=min(b,a+1.8)
    for k in range(len(S)):
        if T0(k)<=a<TE(k): e=min(e,TE(k)-0.02)
    CUES.append((" ".join(w for w,_ in c).upper(),a,e))
KEYS={"SCARED.","DOOR.","EXITS","HANDS","TOASTER","POPS,","FIGHT!","QUIRK.","DUTY.","OVER.","HOME.","DOWN.","MAYDAY.","UNIFORM.","19"}
GR=Image.new('RGB',(4,256)); 
for yy in range(256):
    k=yy/255; GR.paste((255,int(236-110*k*k),int(20*(1-k))),(0,yy,4,yy+1))
def mbtext(im,xy,txt,font,key=False,stroke=11,sh=(9,11)):
    x,y=xy; d=ImageDraw.Draw(im)
    d.text((x+sh[0],y+sh[1]),txt,font=font,fill=(0,0,0,255),stroke_width=stroke,stroke_fill=(0,0,0,255))
    d.text((x,y),txt,font=font,fill=(255,255,255,255),stroke_width=stroke,stroke_fill=(0,0,0,255))
    if key:
        bb=d.textbbox((x,y),txt,font=font); m=Image.new('L',im.size,0); ImageDraw.Draw(m).text((x,y),txt,font=font,fill=255)
        g=GR.resize((im.size[0],max(1,int(bb[3]-bb[1])))); layer=Image.new("RGB",im.size,(255,214,0)); layer.paste(g,(0,int(bb[1]))); im.paste(layer,(0,0),m)
def brush(d,box,col=(214,18,36,255),seed=1):
    rnd=random.Random(seed); x0,y0,x1,y1=box; pts=[]
    for x in range(int(x0),int(x1),26): pts.append((x,y0+rnd.uniform(-9,9)))
    for y in range(int(y0),int(y1),22): pts.append((x1+rnd.uniform(-4,26),y))
    for x in range(int(x1),int(x0),-26): pts.append((x,y1+rnd.uniform(-9,9)))
    for y in range(int(y1),int(y0),-22): pts.append((x0-rnd.uniform(-4,26),y))
    d.polygon([(px+8,py+10) for px,py in pts],fill=(0,0,0,235)); d.polygon(pts,fill=col)
    for k in range(5):
        yy=rnd.uniform(y0+8,y1-8); d.rectangle([x1+10,yy,x1+rnd.uniform(30,70),yy+rnd.uniform(4,9)],fill=col); yy=rnd.uniform(y0+8,y1-8); d.rectangle([x0-rnd.uniform(30,70),yy,x0-10,yy+rnd.uniform(4,9)],fill=col)
font=MB(112)
for i,(txt,a,b) in enumerate(CUES):
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im); lines=[]; cu=''
    for w in txt.split():
        tt=(cu+' '+w).strip()
        if d.textlength(tt,font=font)>940 and cu: lines.append(cu); cu=w
        else: cu=tt
    lines.append(cu); y=1290-len(lines)*64
    for L in lines:
        x=(1080-d.textlength(L,font=font))/2
        for w in L.split():
            mbtext(im,(x,y),w,font,key=(w in KEYS)); x+=d.textlength(w+' ',font=font)
        y+=128
    im.save(f'cap{i}.png')
def label(name,txt,cy,fs,style="red",cx=540,rot=-4):
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im); f=MB(fs); w=d.textlength(txt,font=f)
    if style=="red":
        brush(d,[cx-w/2-34,cy-fs*0.62,cx+w/2+34,cy+fs*0.72],seed=len(txt)); mbtext(im,(cx-w/2,cy-fs*0.55),txt,f,stroke=6,sh=(6,7))
    else: mbtext(im,(cx-w/2,cy-fs*0.55),txt,f,key=True,stroke=12)
    im=im.rotate(rot,resample=Image.BICUBIC,center=(cx,cy)); im.save(name)
# hook banner
hk=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(hk); f=MB(62); t1="INTERNATIONAL MEN'S DAY"; w=d.textlength(t1,font=f)
brush(d,[540-w/2-30,318,540+w/2+30,410],seed=7); mbtext(hk,(540-w/2,326),t1,f,stroke=5,sh=(5,6))
f=MB(86)
for li,t2 in enumerate(["WE DON'T SAY","WE'RE SCARED."]):
    w=d.textlength(t2,font=f); mbtext(hk,(540-w/2,440+li*104),t2,f,key=True,stroke=11)
hk=hk.rotate(-3,resample=Image.BICUBIC,center=(540,480)); hk.save('hook.png')
tag=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(tag); brush(d,[48,128,470,196],seed=3); mbtext(tag,(64,126),"MAYDAY",MB(60),stroke=5,sh=(5,6)); mbtext(tag,(60,204),"DAY 19 OF 61",MB(40),key=True,stroke=7,sh=(5,6)); tag.save('tag.png')
st=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(st); brush(d,[40,1590,1040,1700],seed=5); f=MB(60); s1="STRUGGLING? CALL OR TEXT 988"; mbtext(st,((1080-d.textlength(s1,font=f))/2,1602),s1,f,stroke=5,sh=(5,6))
f=MB(33); s2="VETERANS: 988, PRESS 1"; mbtext(st,((1080-d.textlength(s2,font=f))/2,1716),s2,f,key=True,stroke=6,sh=(4,5)); s3="RESPONDERS: SAFE CALL NOW 206-459-3020"; mbtext(st,((1080-d.textlength(s3,font=f))/2,1762),s3,f,key=True,stroke=6,sh=(4,5)); st.save('strip.png')
label('l_pop.png',"*POP!*",760,120,"yel",cx=330,rot=-10)
label('l_what.png',"WHAT WAS THAT?!",1250,92); label('l_boom.png',"BOOM!",1300,170,"yel"); label('l_lock1.png',"LOCKED.",1250,130); label('l_lock2.png',"CHECK AGAIN.",1250,104); label('l_lock3.png',"...ARE YOU SURE?",1250,96); label('l_lock4.png',"ONE MORE TIME.",1250,100)
label('l_frz.png',"READY TO FIGHT!",1330,104); label('l_frz2.png',"VS. A TOASTER",1500,84,"yel")
label('l_down.png',"STANDING DOWN...",1250,92); label('l_end.png',"TOASTER.",1150,150); label('l_follow.png',"FOLLOW FOR DAY 20",1400,70,"yel",rot=0)
for pct,nm,col in [(100,'m100',(230,20,40)),(0,'m0',(60,210,90)),(1000,'m1000',(230,20,40))]:
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im); d.rounded_rectangle([520,128,1044,250],radius=16,fill=(0,0,0,230),outline=(255,255,255,255),width=5)
    mbtext(im,(536,134),"THREAT LEVEL",MB(34),stroke=3,sh=(3,4)); t_=f"{pct}%"; fp=MB(54 if pct<1000 else 46); mbtext(im,(1030-d.textlength(t_,font=fp),182),t_,fp,key=True,stroke=5,sh=(4,5))
    d.rounded_rectangle([536,196,850,236],radius=10,fill=(70,70,70,255),outline=(0,0,0,255),width=3)
    if pct: d.rounded_rectangle([536,196,850,236],radius=10,fill=col+(255,),outline=(0,0,0,255),width=3)
    im.save(nm+'.png')
def emoji(ch_,name,sz=380):
    f=ImageFont.truetype(EM,109); im=Image.new('RGBA',(160,160),(0,0,0,0)); ImageDraw.Draw(im).text((12,16),ch_,font=f,embedded_color=True)
    a=im.split()[3]; out=Image.new('RGBA',(160,160),(0,0,0,0)); out.paste((255,255,255,255),(0,0),a.filter(ImageFilter.MaxFilter(9))); out.paste(im,(0,0),im); out.resize((sz,sz),Image.LANCZOS).save(f'e_{name}.png')
for c_,nm in [("\U0001F35E","bread"),("\U0001F6AA","door"),("\U0001F440","eyes"),("\U0001F6D2","cart"),("\U0001F512","lock"),("\U0001F60C","relief"),("\U0001F94A","glove"),("\U0001F514","bell")]: emoji(c_,nm)
# toast launch animation (two slices from the toaster slots)
br=Image.open('e_bread.png').resize((230,230),Image.LANCZOS); os.makedirs('tf',exist_ok=True); NT=60
for q in range(NT):
    tm=q/30; fr=Image.new('RGBA',(520,900),(0,0,0,0))
    for k,(bx,ph) in enumerate([(40,0.0),(230,0.06)]):
        u=max(0,tm-ph); y=-1500*u+2300*u*u if u<0.62 else -46-18*math.exp(-(u-0.62)*6)*abs(math.sin((u-0.62)*14))   # up fast, fall, settle popped
        y=min(y,0) if u<0.62 else y
        rot=(u*520 if u<0.62 else 0)*(1 if k else -1); im=br.rotate(rot,resample=Image.BICUBIC,expand=True)
        fr.paste(im,(int(bx+115-im.width/2),int(650+y-im.height/2+115)),im)
    fr.save(f'tf/{q:03d}.png')
run('ffmpeg -v error -y -framerate 30 -i tf/%03d.png -c:v qtrle toast.mov')
POPS=[("door",tl(5.06),60,520,0.8),("eyes",tl(17.26),60,520,0.9),("cart",tl(17.76),640,560,0.8),("lock",T0("lock1")+0.2,60,560,1.0),("glove",T0("frz"),40,480,1.3),("bell",T0("frz")+0.1,660,470,1.2),("relief",T0("hold")+0.4,620,620,1.0)]
for j,(name,st0,x,y,dur) in enumerate(POPS):
    nf=int(dur*30); src=Image.open(f'e_{name}.png'); os.makedirs(f'pf{j}',exist_ok=True)
    for q in range(nf):
        tt=q/30; sc=0.3+0.9*tt/0.15 if tt<0.15 else (1.2-0.2*(tt-0.15)/0.1 if tt<0.25 else 1.0); al_=1.0 if tt<dur-0.2 else max(0,(dur-tt)/0.2)
        fr=Image.new('RGBA',(520,520),(0,0,0,0)); im=src.resize((max(1,int(src.width*sc)),max(1,int(src.height*sc)))); rot=im.rotate(-8+16*math.sin(tt*6+j),resample=Image.BICUBIC,expand=True)
        if al_<1: rot.putalpha(rot.split()[3].point(lambda p:int(p*al_)))
        fr.paste(rot,((520-rot.width)//2,(520-rot.height)//2),rot); fr.save(f'pf{j}/{q:03d}.png')
    run(f'ffmpeg -v error -y -framerate 30 -i pf{j}/%03d.png -c:v qtrle p{j}.mov')
def wsave(n,x,sr=48000):
    x=np.clip(x,-1,1); w=wave.open(n,'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((x*32767).astype(np.int16).tobytes()); w.close()
sr=48000; tt=np.arange(int(sr*2.6))/sr; bell=np.zeros(len(tt))
for s0 in (0.0,0.26,0.52):
    u=np.clip(tt-s0,0,None); m=(tt>=s0)
    for fr_,am,dc in [(742,1.0,2.2),(1486,0.7,2.8),(2231,0.5,3.4),(3105,0.35,4.5),(4212,0.2,6)]: bell+=m*am*np.sin(2*np.pi*fr_*u)*np.exp(-u*dc)
    bell+=m*0.5*np.random.default_rng(1).standard_normal(len(tt))*np.exp(-u*120)
wsave('bell.wav',bell*0.16)
emoji("\U0001F4A5","boom",900); bm=Image.open('e_boom.png'); os.makedirs('bf',exist_ok=True); rb=random.Random(4)
PART=[(rb.uniform(0,6.28),rb.uniform(500,1500),rb.uniform(14,38),[(255,214,0),(255,140,0),(230,40,20),(60,60,60)][k%4]) for k in range(70)]
for q in range(34):
    tm=q/30; fr=Image.new('RGBA',(1080,1080),(0,0,0,0)); d=ImageDraw.Draw(fr)
    rr=60+900*tm; al=int(max(0,170*(1-tm/0.9))); d.ellipse([540-rr,540-rr,540+rr,540+rr],outline=(90,90,90,al),width=int(46*(1-min(1,tm))+4))
    for an,v,sz_,c in PART:
        dist=v*tm*(1-0.35*tm); x=540+math.cos(an)*dist; y=540+math.sin(an)*dist+500*tm*tm; a_=int(255*max(0,1-tm/1.05)); d.ellipse([x-sz_,y-sz_,x+sz_,y+sz_],fill=c+(a_,))
    sc=(0.12+0.95*tm/0.12) if tm<0.12 else (1.0+0.25*math.exp(-(tm-0.12)*5))
    a_=1.0 if tm<0.7 else max(0,1-(tm-0.7)/0.4); im=bm.resize((max(2,int(900*sc)),max(2,int(900*sc)))).rotate(12*math.sin(tm*20),resample=Image.BICUBIC)
    if a_<1: im.putalpha(im.split()[3].point(lambda p:int(p*a_)))
    fr.paste(im,(540-im.width//2,540-im.height//2),im); fr.save(f'bf/{q:03d}.png')
run('ffmpeg -v error -y -framerate 30 -i bf/%03d.png -c:v qtrle boom.mov')
rg2=np.random.default_rng(9); tt=np.arange(int(sr*2.0))/sr; lp=np.convolve(rg2.standard_normal(len(tt)),np.ones(60)/60,'same')*8
bomb=np.sin(2*np.pi*np.cumsum(35+75*np.exp(-tt*5))/sr)*np.exp(-tt*2.2)*1.0+lp*np.exp(-tt*3.2)*0.9+rg2.standard_normal(len(tt))*np.exp(-tt*28)*0.8
wsave('bomb.wav',np.tanh(bomb*1.6)*0.9)
tt=np.arange(int(sr*2.5))/sr; fq=260+520*(tt/2.5)**1.6+60*np.sin(2*np.pi*3.1*tt)+25*rg2.standard_normal(len(tt)).cumsum()/200; ph=2*np.pi*np.cumsum(fq)/sr
grit=np.clip(np.convolve((rg2.random(len(tt))<0.004).astype(float),np.hanning(900),'same'),0,1)
cr=((2*((ph/(2*np.pi))%1)-1)*0.6+np.sin(3.01*ph)*0.3+np.sin(5.03*ph)*0.2)*(0.35+0.65*grit)*np.minimum(tt/0.08,1)*np.minimum((2.5-tt)/0.05,1)
ck=np.zeros(len(tt)); k0=int(sr*2.32); u=tt[:len(tt)-k0]; ck[k0:]=(np.sin(2*np.pi*140*u)*np.exp(-u*30)+rg2.standard_normal(len(u))*np.exp(-u*90)*0.7)*1.4
wsave('creak.wav',np.tanh(cr*1.3)*0.5+ck*0.6)
tt=np.arange(int(sr*1.3))/sr; fq=190+150*np.exp(-tt*2.2)*np.sin(2*np.pi*11*tt)+260*np.exp(-tt*3); ph=2*np.pi*np.cumsum(fq)/sr
wsave('spring.wav',(np.sin(ph)+0.5*np.sin(2*ph)+0.3*np.sin(3.02*ph))*np.exp(-tt*2.4)*np.minimum(tt/0.004,1)*0.55)
tt=np.arange(int(sr*0.25))/sr; n_=rg2.standard_normal(len(tt)); hp=n_-np.convolve(n_,np.ones(12)/12,'same')
wsave('snap.wav',(hp*np.exp(-tt*160)*1.2+np.sin(2*np.pi*2400*tt)*np.exp(-tt*120)*0.6+np.roll(hp*np.exp(-tt*160),int(sr*0.045))*0.25)*0.8)
# --- v7 sounds and the sleeping Zs
rg3=np.random.default_rng(21)
def clickat(buf,t0,amp=1.0,f=2600,dec=220):
    k=int(sr*t0); u=np.arange(min(len(buf)-k,int(sr*0.08)))/sr; buf[k:k+len(u)]+=amp*(rg3.standard_normal(len(u))*np.exp(-u*dec)*0.8+np.sin(2*np.pi*f*u)*np.exp(-u*dec*0.7)*0.6)
kl=np.zeros(int(sr*2.2)); tt=np.arange(len(kl))/sr
for t0 in (0.02,0.07,0.13,0.2,0.26): clickat(kl,t0,0.35,5200,300)          # keys jingle
m=(tt>0.36)&(tt<0.72); kl[m]+=rg3.standard_normal(m.sum())*0.22*np.sin(np.pi*(tt[m]-0.36)/0.36)*(0.5+0.5*np.sign(np.sin(2*np.pi*55*tt[m])))   # key sliding in
for j in range(9): clickat(kl,0.86+j*0.055,0.5,3100,260)                    # pins as the key turns
k0=int(sr*1.42); u=tt[:len(tt)-k0]; kl[k0:]+=(np.sin(2*np.pi*120*u)*np.exp(-u*24)*1.3+rg3.standard_normal(len(u))*np.exp(-u*70)*0.8)   # bolt thunk
clickat(kl,1.42,1.0,1800,150)
wsave('keylock.wav',np.tanh(kl*1.5)*0.8)
nk=np.zeros(int(sr*1.1)); tt=np.arange(len(nk))/sr
for t0,a_ in [(0.0,1.0),(0.07,0.7),(0.15,1.0),(0.21,0.6),(0.3,0.9),(0.36,0.5),(0.47,1.0),(0.52,0.6)]:
    k=int(sr*t0); u=np.arange(int(sr*0.09))/sr; nk[k:k+len(u)]+=a_*(rg3.standard_normal(len(u))*np.exp(-u*90)*0.9+np.sin(2*np.pi*(330+rg3.uniform(-60,90))*u)*np.exp(-u*60)*0.9+np.sin(2*np.pi*95*u)*np.exp(-u*40)*0.7)
wsave('neck.wav',np.tanh(nk*1.8)*0.9)
def snore(L=1.9):
    tt=np.arange(int(sr*L))/sr; n_=np.convolve(rg3.standard_normal(len(tt)),np.ones(40)/40,'same')*6
    inh=(tt<1.05); x=np.zeros(len(tt)); rattle=0.5+0.5*np.sign(np.sin(2*np.pi*27*tt))*0.9
    x[inh]=(n_[inh]*rattle[inh]+0.6*np.sin(2*np.pi*88*tt[inh])*rattle[inh])*np.sin(np.pi*tt[inh]/1.05)**0.7
    ex=(tt>=1.15)&(tt<L); u=tt[ex]-1.15; x[ex]=(np.sin(2*np.pi*np.cumsum(900-380*u/(L-1.15))/sr)*0.25+rg3.standard_normal(ex.sum())*0.12)*np.sin(np.pi*u/(L-1.15))
    return np.tanh(x*1.4)*0.8
wsave('snore.wav',snore())
zf=MB(150); zr=random.Random(8); ZT0=T0(IXR)+0.3; ZD=TE("hold")-0.05-ZT0; ZN=int(ZD*30); os.makedirs('zz',exist_ok=True)
ZS=[(k*0.3,zr.uniform(-40,40),zr.uniform(0.8,1.25),zr.uniform(0,6.28)) for k in range(int(ZD/0.3))]
for q in range(ZN):
    tm=q/30; fr=Image.new('RGBA',(800,780),(0,0,0,0))
    for t0,dx_,sc_,ph_ in ZS:
        u=tm-t0
        if u<0 or u>1.9: continue
        k=u/1.9; size=int((50+150*k)*sc_); f_=MB(size); x=300+dx_+230*k+35*math.sin(u*4+ph_); y=690-620*k
        lay=Image.new('RGBA',(size*2,size*2),(0,0,0,0)); mbtext(lay,(size*0.4,size*0.3),"Z",f_,key=True,stroke=max(4,size//14),sh=(max(3,size//22),max(3,size//18)))
        lay=lay.rotate(-12+18*math.sin(u*3+ph_),resample=Image.BICUBIC); a_=min(1,u/0.15)*(1 if k<0.75 else max(0,(1-k)/0.25))
        if a_<1: lay.putalpha(lay.split()[3].point(lambda p:int(p*a_)))
        fr.paste(lay,(int(x-size),int(y-size)),lay)
    fr.save(f'zz/{q:04d}.png')
run('ffmpeg -v error -y -framerate 30 -i zz/%04d.png -c:v qtrle zzz.mov')
POPT=1.25; BT=T0("boom")+0.3; stripT=T0(len(S)-4); HOOK_END=T0(1); DOWN=T0("hold")+0.5; END=T0("end"); FZ=T0("frz"); POP2=tl(24.96)
sh=f"between(t,{BT:.2f},{BT+0.6:.2f})+between(t,{POPT:.2f},{POPT+0.5:.2f})+between(t,{FZ:.2f},{FZ+0.35:.2f})+between(t,{END+0.35:.2f},{END+0.9:.2f})"
fc=[f"[0:v]scale=1160:2062,crop=1080:1920:'40+if({sh},30*sin(t*95),0)':'71+if({sh},30*cos(t*80),0)'[v1s]","[v1s][1:v]overlay[v3]",f"[v3][2:v]overlay=enable='lt(t,{HOOK_END:.3f})'[v4]",f"[v4]drawbox=c=white@0.85:t=fill:enable='between(t,{FZ:.3f},{FZ+0.07:.3f})+between(t,{BT:.3f},{BT+0.08:.3f})',drawbox=x=0:y=0:w='iw*t/{TOT:.3f}':h=14:color=0xFFD600@1:t=fill[v5]"]
cur='[v5]'; idx=3; extra=[]
def ov(png,a,b):
    global cur,idx
    extra.append(f'-loop 1 -i {png}'); fc.append(f"{cur}[{idx}:v]overlay=enable='between(t,{a:.3f},{b:.3f})'[o{idx}]"); cur=f'[o{idx}]'; idx+=1
for k,(st0,en) in enumerate([(POPT,TE("hook")),(POP2,TE("pops"))]):
    extra.append('-i toast.mov'); fc.append(f"[{idx}:v]trim=0:{en-st0:.3f},setpts=PTS-STARTPTS+{st0:.3f}/TB[ts{k}];{cur}[ts{k}]overlay=20:400:eof_action=pass[tv{k}]"); cur=f'[tv{k}]'; idx+=1
ov('m100.png',0,DOWN-0.01); ov('m0.png',DOWN,END+0.34); ov('m1000.png',END+0.35,TOT)
ov('l_pop.png',POPT,POPT+0.9); ov('l_what.png',T0("flinch")+0.05,BT-0.02); ov('l_boom.png',BT+0.1,TE("boom")-0.02)
extra.append('-i zzz.mov'); fc.append(f"[{idx}:v]setpts=PTS+{ZT0:.3f}/TB[zz];{cur}[zz]overlay=100:0:eof_action=pass[vzz]"); cur='[vzz]'; idx+=1
extra.append('-i boom.mov'); fc.append(f"[{idx}:v]setpts=PTS+{BT:.3f}/TB[bm];{cur}[bm]overlay=340:280:eof_action=pass[vbm]"); cur='[vbm]'; idx+=1; ov('l_lock1.png',T0("lock1")+0.5,TE("lock1")-0.02); ov('l_lock2.png',T0("lock2")+0.6,TE("lock2")-0.02); ov('l_lock3.png',T0("lock3")+0.1,TE("lock3")-0.02); ov('l_lock4.png',T0("lock4")+0.3,TE("lock4")-0.02)
ov('l_frz.png',FZ+0.05,TE("frz")-0.02); ov('l_frz2.png',FZ+0.45,TE("frz")-0.02); ov('l_down.png',T0("hold")+0.3,TE("hold")-0.02); ov('l_end.png',END+1.3,TOT); ov('l_follow.png',TOT-1.8,TOT)
PIPS=[i for i,sg in enumerate(S) if sg[0] not in ("T","Z")]
mk=Image.new('L',(400,400),0); ImageDraw.Draw(mk).ellipse([0,0,399,399],fill=255); mk.save('mask.png')
rg=Image.new('RGBA',(424,424),(0,0,0,0)); ImageDraw.Draw(rg).ellipse([2,2,421,421],outline=(255,255,255,255),width=12); rg.save('ring.png')
for j,si in enumerate(PIPS):
    ar=S[si][3]; d_=log[si][1]; t0=T0(si); aa=43.2 if ar is None else ar+OFF
    lim=f"-t {min(d_,1.3):.3f}" if ar is None else ""; pad=",tpad=stop_mode=clone:stop_duration=5" if ar is None else ""
    run(f'ffmpeg -v error -y -ss {aa:.3f} {lim} -i T.mov -an -t {d_:.3f} -vf "hflip,scale=1080:1920:flags=lanczos,crop=560:560:260:200,scale=400:400,fps=30,format=yuv420p{pad}" -c:v libx264 -crf 16 pipsrc{j}.mp4')
    extra.append(f'-i pipsrc{j}.mp4 -loop 1 -i mask.png -loop 1 -i ring.png')
    fc.append(f"[{idx}:v]format=rgba[pc{j}];[{idx+1}:v]format=gray[mk{j}];[pc{j}][mk{j}]alphamerge=shortest=1,setpts=PTS+{t0:.3f}/TB[pm{j}];{cur}[pm{j}]overlay=650:1460:eof_action=pass[pq{j}];[pq{j}][{idx+2}:v]overlay=638:1448:enable='between(t,{t0:.3f},{t0+d_-0.03:.3f})'[pr{j}]"); cur=f'[pr{j}]'; idx+=3
for j,(name,st0,x,y,dur) in enumerate(POPS):
    extra.append(f'-i p{j}.mov'); fc.append(f"[{idx}:v]setpts=PTS+{st0:.3f}/TB[pp{j}];{cur}[pp{j}]overlay={x}:{y}:eof_action=pass[pv{j}]"); cur=f'[pv{j}]'; idx+=1
extra.append('-loop 1 -i strip.png'); fc.append(f"{cur}[{idx}:v]overlay=enable='between(t,{stripT:.3f},{END-0.01:.3f})'[vs]"); cur='[vs]'; idx+=1
for i,(t_,a,b) in enumerate(CUES):
    extra.append(f'-i cap{i}.png'); fc.append(f"{cur}[{idx}:v]overlay=enable='between(t,{a:.3f},{b:.3f})'[x{i}]"); cur=f'[x{i}]'; idx+=1
open('fc.txt','w').write(";".join(fc))
run(f'ffmpeg -v error -y -i vcat.mp4 -i tag.png -loop 1 -i hook.png '+' '.join(extra)+f' -filter_complex_script fc.txt -map "{cur}" -t {TOT:.3f} -c:v libx264 -crf 17 -preset veryfast vcap.mp4')
ev=[("boing",POPT-0.05,2),("pop",POPT,2),("yeow",POPT+0.75,-4),("thump",POPT+0.8,-3),("thump",T0("flinch")+0.1,0),("bomb",BT,5),("keylock",T0("lock3")-0.67,5),("neck",T0(IXU)+1.08,8),("snore",ZT0+0.1,-2),("snore",T0("hold")+0.05,6),("spring",POP2-0.03,7),("click",T0("lock1")+0.5,5),("click",T0("lock2")+0.8,5),("thump",T0("lock3")+0.1,-2),("click",T0("lock4")+0.5,5),
("pop",POP2,1),("whoosh",FZ-0.22,-2),("punch",FZ-0.02,2),("bell",FZ+0.05,0),
("powerdown",DOWN,-3),("ding",DOWN+0.3,-4),("boing",END+0.3,1),("pop",END+0.35,1),("yeow",END+1.3,-5),("punch",END+2.2,-2),("dod_hit",TOT-0.75,6)]+[("pop",p[1],-10) for p in POPS]
ins=" ".join(f"-i {n}.wav" for n,_,_ in ev); parts=[]; labs=[]
for j,(n,s0,g) in enumerate(ev):
    D=max(0,int(s0*1000)); parts.append(f"[{j+1}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={D}|{D},volume={g}dB[e{j}]"); labs.append(f"[e{j}]")
nin=len(ev)+1; mus=""
if os.path.exists('music.mp3'):
    ins+=" -i music.mp3"; MG=float(os.environ.get('MG','-23'))
    # music: quieter under talking, a little up on the silent gags
    up="+".join(f"between(t,{T0(i):.2f},{TE(i):.2f})" for i,sg in enumerate(S) if sg[3] is None)
    parts.append(f"[{nin}:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-16:TP=-2:LRA=9,atrim=0:{TOT:.3f},volume='{10**(MG/20):.4f}*(1+0.9*({up}))':eval=frame,afade=t=in:d=0.3,afade=t=out:st={TOT-1.2:.3f}:d=1.2[mu]"); labs.append("[mu]"); nin+=1
fa_="; ".join(parts)+f";[0:a]{''.join(labs)}amix=inputs={nin}:duration=first:normalize=0[a]"
run(f'ffmpeg -v error -y -i acat.wav {ins} -filter_complex "{fa_}" -map "[a]" amix.wav')
run('ffmpeg -v error -y -i vcap.mp4 -i amix.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le body.mov')
r=subprocess.run('ffmpeg -hide_banner -i body.mov -af loudnorm=I=-15.5:TP=-1.5:LRA=11:print_format=json -f null -',shell=True,capture_output=True,text=True).stderr
m=json.loads(re.search(r'\{[^{}]*"input_i"[^{}]*\}',r).group(0))
run(f'ffmpeg -v error -y -i body.mov -af "loudnorm=I=-15.5:TP=-1.5:LRA=11:measured_I={m["input_i"]}:measured_TP={m["input_tp"]}:measured_LRA={m["input_lra"]}:measured_thresh={m["input_thresh"]}:offset={m["target_offset"]}:linear=true" -c:v libx264 -crf 21 -preset fast -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart -shortest MAYDAY-Day-19-THE-SCAN.mp4')
print("TOT",TOT,"music",os.path.exists('music.mp3')); print(" | ".join(c for c,_,_ in CUES)); print([(S[i][5] or S[i][0],round(T0(i),2)) for i in range(len(S))])
