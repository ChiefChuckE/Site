import subprocess, json, math, os, numpy as np, wave
from PIL import Image, ImageDraw, ImageFont, ImageFilter
def run(c): subprocess.run(c,shell=True,check=True)
D17='../d17g'
for f in ['burst.png','u2netp.onnx','matte.py','thump.wav','pop.wav','whoosh.wav','boing.wav','punch.wav','dod_hit.wav','crash.wav']:
    if not os.path.exists(f): run(f'cp {D17}/{f} .')
F='/usr/share/fonts/opentype/inter/Inter-Black.otf'; EM='/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
# reversed helper sources
if not os.path.exists('R.mp4'): run('ffmpeg -v error -y -ss 29.67 -i S.mov -t 1.24 -an -vf "scale=1080:1920,fps=30,reverse" -c:v libx264 -crf 14 R.mp4')
if not os.path.exists('MR.mp4'): run('ffmpeg -v error -y -i M.mov -t 1.66 -an -vf "scale=1080:1920,fps=30,reverse" -c:v libx264 -crf 14 MR.mp4')
if not os.path.exists('MR2.mp4'): run('ffmpeg -v error -y -t 1.0 -i M.mov -an -vf "scale=1080:1920,fps=30,reverse,tpad=stop_mode=clone:stop_duration=1.6" -c:v libx264 -crf 14 MR2.mp4')
if not os.path.exists('H0.mp4'):
    assert os.path.exists('k0.mp4')
    run('ffmpeg -v error -y -sseof -0.1 -i k0.mp4 -update 1 -frames:v 1 hl.png'); hl=Image.open('hl.png').convert('RGB'); os.makedirs('nf',exist_ok=True)
    for q in range(27):
        z=[1.3,1.8,2.5][q//9]*(1+0.01*(q%9)); w=1080/z; h=1920/z; x=min(max(400-w/2,0),1080-w); y=min(max(640-h*0.42,0),1920-h)
        hl.crop((int(x),int(y),int(x+w),int(y+h))).resize((1080,1920),Image.LANCZOS).save(f'nf/{q:03d}.png')
    run('ffmpeg -v error -y -framerate 30 -i nf/%03d.png -c:v libx264 -crf 14 -pix_fmt yuv420p N.mp4')
    open('h0.txt','w').write("file k0.mp4\nfile N.mp4\n"); run('ffmpeg -v error -y -f concat -i h0.txt -vf fps=30 -c:v libx264 -crf 14 -pix_fmt yuv420p H0.mp4')
SRC={"H0":"H0.mp4","G2":"G2.mov","M2":"MR2.mp4","T":"T1.mov","S":"S.mov","P":"P.mov","G":"G.mov","Z":"Z.mov","I":"I.mov","R":"R.mp4","M":"MR.mp4"}
run('ffmpeg -v error -y -i T1.mov -map 0:a:0 -ac 2 -ar 48000 -af "highpass=f=80,loudnorm=I=-16:TP=-2:LRA=11" wT.wav')
FL="hflip,"; ICE="crop=800:1422:280:150,"; PC="crop=900:1600:90:0,"; MC="crop=960:1706:60:214,"; CW="crop=760:1351:130:120,"; COLD="colorbalance=bs=0.25:bm=0.2:bh=0.1,"
# (vsrc, vstart, dur, astart, alen, vf)   audio always from T
SEG=[("H0",0,3.2,1.04,2.3,""),
("T",4.20,2.14,4.20,2.14,FL),
("R",0,1.24,6.36,1.24,""),
("T",8.26,0.94,8.26,0.94,FL),
("T",12.20,0.76,12.20,0.76,FL),("T",13.64,0.94,13.64,0.94,FL),("T",15.02,1.16,15.02,1.16,FL),
("S",14.64,1.05,18.20,1.05,""),("S",15.69,1.45,19.45,1.45,""),
("P",10.3,0.9,22.60,0.9,PC),("P",26.0,1.4,24.02,1.4,CW),("P",28.5,0.9,29.0,0.9,CW),
("G2",0,1.94,26.46,1.94,""),("G2",1.94,2.0,29.6,2.0,""),
("Z",9.6,1.0,32.08,1.0,COLD),("Z",4.6,1.1,30.5,1.1,COLD),
("T",33.70,1.0,33.70,1.0,FL),
("S",12.30,1.1,41.30,1.1,""),
("T",45.74,1.88,45.74,1.88,FL),
("T",48.14,1.66,48.14,1.66,FL),
("T",50.10,1.02,50.10,1.02,FL),
("T",53.72,1.7,53.72,1.6,FL),
("M2",0,2.3,56.5,2.3,MC),("I",13.5,1.7,57.0,1.7,ICE)]
iP,iC,iC2,iG,iG2,iZ,iZ2,iSY,iON,iFINE,iDAY,iMD,iUN,iSM,iRX=9,10,11,12,13,14,15,16,17,18,19,20,21,22,23
VOL={11:"volume=0.04,",13:"volume=0.04,",15:"volume=0.04,",22:"volume=0.04,",23:"volume=0.04,"}
Wd=[(2.14,"Day"),(2.42,"18,"),(2.8,"numb."),(4.28,"The"),(4.44,"job"),(4.72,"taught"),(5.08,"you"),(5.74,"to"),(5.92,"shut"),(6.18,"your"),(6.42,"feelings"),(7.14,"off"),
(8.34,"so"),(8.46,"you"),(8.56,"could"),(8.78,"work."),(12.26,"Problem"),(12.64,"is,"),(13.7,"there's"),(13.96,"no"),(14.18,"switch"),(15.08,"just"),(15.26,"for"),(15.38,"the"),(15.5,"bad"),(15.82,"ones."),
(18.28,"Shut"),(18.5,"off"),(18.66,"the"),(18.84,"fear,"),(19.52,"and"),(19.62,"the"),(19.8,"joy"),(20.06,"goes"),(20.36,"with"),(20.58,"it."),
(22.66,"You're"),(22.78,"at"),(22.88,"the"),(23.04,"party,"),(24.08,"and"),(24.24,"everyone's"),(24.88,"laughing,"),(26.52,"and"),(26.64,"you're"),(26.88,"watching"),(27.38,"through"),(27.7,"glass."),
(32.14,"That's"),(32.32,"not"),(32.58,"cold."),(33.76,"That's"),(33.94,"a"),(34.08,"symptom."),(41.36,"It"),(41.48,"can"),(41.68,"come"),(41.88,"back."),
(45.8,"but"),(46.02,"only"),(46.22,"if"),(46.32,"you"),(46.44,"stop"),(46.7,"calling"),(46.94,"it"),(47.1,"fine."),
(48.2,"This"),(48.38,"is"),(48.54,"day"),(48.82,"18"),(49.0,"of"),(49.28,"61."),(50.16,"Call"),(50.38,"your"),(50.56,"mayday."),
(53.74,"Send"),(53.9,"it"),(54.0,"to"),(54.04,"someone"),(54.3,"who"),(54.4,"wore"),(54.56,"the"),(54.7,"uniform.")]
vl=open('v.txt','w'); al=open('a.txt','w'); t=0; log=[]
for i,(vs,va,dur,aa,alen,vf) in enumerate(SEG):
    n=round(dur*30); d=n/30; alen=min(alen,d)
    run(f'ffmpeg -v error -y -ss {va:.3f} -i {SRC[vs]} -map 0:v:0 -an -vf "{vf}scale=1080:1920,fps=30,format=yuv420p" -frames:v {n} -c:v libx264 -preset veryfast -crf 16 s{i}.mp4')
    vol=VOL.get(i,"")
    run(f'ffmpeg -v error -y -i wT.wav -af "atrim={aa:.4f}:{aa+alen:.4f},asetpts=PTS-STARTPTS,{vol}afade=t=in:d=0.015,afade=t=out:st={alen-0.03:.4f}:d=0.03,apad,atrim=0:{d:.4f}" -c:a pcm_s16le s{i}.wav')
    vl.write(f"file s{i}.mp4\n"); al.write(f"file s{i}.wav\n"); log.append((aa,aa+alen,t,d)); t+=d
vl.close(); al.close(); TOT=t
run('ffmpeg -v error -y -f concat -i v.txt -c copy vcat.mp4'); run('ffmpeg -v error -y -f concat -i a.txt -c copy acat.wav')
def tl(s):
    for a,b,tt,d in log:
        if a<=s<b: return tt+s-a
def T0(i): return log[i][2]
W=[(w,tl(s)) for s,w in Wd if tl(s) is not None]
ch=[]; cur=[]
for w,s in W:
    cur.append((w,s))
    if w[-1] in ',.:?' or len(cur)==3: ch.append(cur); cur=[]
if cur: ch.append(cur)
CUES=[]
for i,c in enumerate(ch):
    a=c[0][1]; b=ch[i+1][0][1] if i+1<len(ch) else TOT-0.05
    CUES.append((" ".join(w for w,_ in c).upper(),a,min(b,a+2.0)))
CUES[-1]=(CUES[-1][0],CUES[-1][1],T0(iSM)-0.02)
for q_,c_ in enumerate(CUES):
    if c_[0]=='NUMB.': CUES[q_]=(c_[0],c_[1],2.28)
    if c_[0]=="THAT'S NOT COLD.": CUES[q_]=(c_[0],c_[1],T0(iZ2)-0.02)
KEYS={"NUMB.","FEELINGS","OFF","SWITCH","FEAR,","JOY","PARTY,","LAUGHING,","GLASS.","COLD.","SYMPTOM.","BACK.","FINE.","MAYDAY.","UNIFORM.","18","18,","BAD","WORK."}
font=ImageFont.truetype(F,108)
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
def banner(name,lines,box,fs=62):
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im); f=ImageFont.truetype(F,fs)
    d.rectangle(box,fill=(0,0,0,215)); y=box[1]+22
    for txt,col in lines:
        d.text(((1080-d.textlength(txt,font=f))/2,y),txt,font=f,fill=col); y+=fs+26
    im.save(name)
banner('hook.png',[("FIREFIGHTERS, COPS, MEDICS:",(255,255,255)),("FEEL NOTHING? WATCH THIS.",(255,214,0))],[0,330,1080,540])
tag=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(tag)
f1=ImageFont.truetype(F,52); f2=ImageFont.truetype(F,30)
d.rounded_rectangle([50,130,480,242],radius=14,fill=(200,16,46)); d.text((76,138),"MAYDAY",font=f1,fill='white'); d.text((78,202),"DAY 18 OF 61 · NUMB",font=f2,fill='white'); tag.save('tag.png')
st=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(st)
d.rectangle([0,1590,1080,1790],fill=(200,16,46,240))
fa=ImageFont.truetype(F,64); fb=ImageFont.truetype(F,34)
s1="STRUGGLING? CALL OR TEXT 988"; d.text(((1080-d.textlength(s1,font=fa))/2,1612),s1,font=fa,fill='white')
s2="Veterans: 988, press 1  ·  Responders: Safe Call Now 206-459-3020"; d.text(((1080-d.textlength(s2,font=fb))/2,1712),s2,font=fb,fill='white'); st.save('strip.png')
def label(name,items):
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im)
    for txt,cx,cy,fs,bg,fg,ay in items:
        f=ImageFont.truetype(F,fs); w=d.textlength(txt,font=f)
        d.rounded_rectangle([cx-w/2-28,cy-fs/2-18,cx+w/2+28,cy+fs/2+26],radius=22,fill=bg,outline=(0,0,0,255),width=7)
        d.text((cx-w/2,cy-fs/2-6),txt,font=f,fill=fg)
        if ay: d.polygon([(cx-34,cy+fs/2+26),(cx+34,cy+fs/2+26),(cx,ay)],fill=bg,outline=(0,0,0,255))
    im.save(name)
Y=(255,214,0,255); R=(200,16,46,255); K=(0,0,0); Wt=(255,255,255); G=(70,70,70,255)
label('l_feel.png',[("FEELINGS",540,330,120,Y,K,470)])
label('l_off.png',[("OFF",540,330,150,R,Wt,0)])
label('l_fj.png',[("FEAR",290,500,96,R,Wt,640),("JOY",690,500,96,Y,K,640)])
label('l_fj2.png',[("FEAR",290,500,96,G,(150,150,150),640),("JOY",690,500,96,Y,K,640)])
label('l_fj3.png',[("FEAR",290,500,96,G,(150,150,150),640),("JOY",690,500,96,G,(150,150,150),640)])
label('l_both.png',[("BOTH OFF.",540,820,130,R,Wt,0)])
label('l_n1.png',[('ICE.',540,1250,170,Y,K,0)]); label('l_n2.png',[('WATER.',540,1250,170,Y,K,0)]); label('l_n3.png',[('NOTHING.',540,1250,170,R,Wt,0)])
label('l_still.png',[('STILL NOTHING.',540,330,96,R,Wt,0)]); label('l_feel2.png',[('OK. NOW I FEEL IT.',540,1250,100,Y,K,0)])
label('l_ha1.png',[('HA!',200,1000,100,(255,255,255,255),K,0)]); label('l_ha2.png',[('HA HA!',800,820,90,(255,255,255,255),K,0)]); label('l_ha3.png',[('HAHA!',330,640,90,(255,255,255,255),K,0)])
label('l_on.png',[("FEELINGS: ON",540,330,104,Y,K,0)])
label('l_reen.png',[("ME AT EVERY PARTY",540,300,74,Y,K,0)])
label('l_glass.png',[("*SQUEAK*",760,520,64,(255,255,255,255),K,0)])
# I'M FINE stamp
im=Image.new('RGBA',(700,300),(0,0,0,0)); d=ImageDraw.Draw(im); f=ImageFont.truetype(F,130)
d.rounded_rectangle([10,10,690,290],radius=30,outline=(230,20,40,255),width=18); d.text(((700-d.textlength('"FINE"',font=f))/2,70),'"FINE"',font=f,fill=(230,20,40,255))
d.line([40,260,660,40],fill=(230,20,40,255),width=22)
im=im.rotate(-10,expand=True,resample=Image.BICUBIC); c=Image.new('RGBA',(1080,1920),(0,0,0,0)); c.paste(im,(190,330),im); c.save('l_fine.png')
# emoji stickers
def emoji(ch,name):
    f=ImageFont.truetype(EM,109); im=Image.new('RGBA',(160,160),(0,0,0,0)); ImageDraw.Draw(im).text((12,16),ch,font=f,embedded_color=True)
    a=im.split()[3]; out=Image.new('RGBA',(160,160),(0,0,0,0)); edge=a.filter(ImageFilter.MaxFilter(9)); out.paste((255,255,255,255),(0,0),edge); out.paste(im,(0,0),im); out.resize((380,380),Image.LANCZOS).save(f'e_{name}.png')
for ch_,nm in [("\U0001F9CA","ice"),("\U0001F389","party"),("\U0001F602","laugh"),("\U0001F923","rofl"),("❄️","snow"),("\U0001F4A1","bulb"),("\U0001F976","cold"),("\U0001F636","blank")]: emoji(ch_,nm)
# (name, start, x, y, dur)
POPS=[("ice",0.75,60,560,1.3),("blank",T0(0)+1.25,640,600,1.0),("party",T0(9)+0.1,40,520,1.1),("laugh",T0(10)+0.15,20,560,1.2),("rofl",T0(10)+0.4,620,460,1.0),("laugh",T0(10)+0.7,560,900,0.7),
("snow",T0(iZ)+0.1,40,500,0.9),("cold",T0(iZ)+0.3,620,540,0.7),("bulb",tl(41.88),560,460,0.7)]
for j,(name,st0,x,y,dur) in enumerate(POPS):
    nf=int(dur*30); src=Image.open(f'e_{name}.png'); os.makedirs(f'pf{j}',exist_ok=True)
    for q in range(nf):
        tt=q/30
        sc=0.3+0.9*tt/0.15 if tt<0.15 else (1.2-0.2*(tt-0.15)/0.1 if tt<0.25 else 1.0)
        al_=1.0 if tt<dur-0.2 else max(0,(dur-tt)/0.2)
        fr=Image.new('RGBA',(520,520),(0,0,0,0)); im=src.resize((max(1,int(src.width*sc)),max(1,int(src.height*sc))))
        rot=im.rotate(-8+16*math.sin(tt*6+j),resample=Image.BICUBIC,expand=True)
        if al_<1: rot.putalpha(rot.split()[3].point(lambda p:int(p*al_)))
        fr.paste(rot,((520-rot.width)//2,(520-rot.height)//2),rot); fr.save(f'pf{j}/{q:03d}.png')
    run(f'ffmpeg -v error -y -framerate 30 -i pf{j}/%03d.png -c:v qtrle p{j}.mov')
# sounds
def wsave(n,x,sr=48000):
    x=np.clip(x,-1,1); w=wave.open(n,'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((x*32767).astype(np.int16).tobytes()); w.close()
sr=48000; rng=np.random.default_rng(3)
tt=np.arange(int(sr*1.4))/sr; nz=rng.standard_normal(len(tt)); k=np.ones(12)/12; nz=np.convolve(nz,k,'same')*3
wsave('splash.wav',nz*np.minimum(tt/0.05,1)*np.exp(-tt*2.6)*0.8)
tt=np.arange(int(sr*0.09))/sr; wsave('click.wav',(rng.standard_normal(len(tt))*np.exp(-tt*120)+np.sin(2*np.pi*1800*tt)*np.exp(-tt*90))*0.8)
tt=np.arange(int(sr*1.8))/sr; fr=1900-900*tt/1.8+120*np.sin(2*np.pi*14*tt); ph=2*np.pi*np.cumsum(fr)/sr
wsave('squeak.wav',(np.sin(ph)+0.4*np.sin(2*ph))*np.minimum(tt/0.05,1)*np.minimum((1.8-tt)/0.1,1)*0.35)
tt=np.arange(int(sr*1.2))/sr; wsave('ding.wav',(np.sin(2*np.pi*1318*tt)+0.6*np.sin(2*np.pi*1976*tt)+0.3*np.sin(2*np.pi*2637*tt))*np.exp(-tt*3.5)*0.4)
tt=np.arange(int(sr*1.3))/sr; lg=np.zeros(len(tt))
for q in range(7):
    s0=0.05+q*0.17; m=(tt>=s0)&(tt<s0+0.13); u=tt[m]-s0; f0=520-q*18; lg[m]+=(np.sin(2*np.pi*f0*u)+0.5*np.sin(2*np.pi*2*f0*u)+0.3*np.sin(2*np.pi*3*f0*u))*np.sin(np.pi*u/0.13)
wsave('haha.wav',lg*0.3)
tt=np.arange(int(sr*0.5))/sr; wsave('powerdown.wav',np.sin(2*np.pi*np.cumsum(420*np.exp(-tt*5))/sr)*np.exp(-tt*4)*0.6)
stripT=T0(iDAY); HOOK_END=T0(1)
ON=T0(iON)+0.58; SMILE=T0(iSM)+1.0
BEATS=[ON+k*0.7 for k in range(40) if ON+k*0.7<TOT-0.9]
banner('tagline.png',[("TAG SOMEONE",(255,255,255)),("WHO WENT NUMB.",(255,214,0))],[0,330,1080,540],70)
for pct,nm in [(0,'m0'),(25,'m25'),(50,'m50'),(75,'m75'),(100,'m100'),(1000,'m1000')]:
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([510,130,1040,242],radius=14,fill=(0,0,0,225),outline=(255,255,255,255),width=4)
    d.text((530,140),"FEELINGS",font=ImageFont.truetype(F,34),fill='white')
    col=(230,20,40) if pct==0 else (60,210,90)
    t_=f"{pct}%"; fp=ImageFont.truetype(F,52 if pct<1000 else 44); d.text((1024-d.textlength(t_,font=fp),176),t_,font=fp,fill=col)
    d.rounded_rectangle([530,190,860,226],radius=10,fill=(60,60,60,255))
    if pct: d.rounded_rectangle([530,190,530+int(330*min(pct,100)/100),226],radius=10,fill=col+(255,))
    im.save(nm+'.png')
# EKG animation
E0=T0(iP); nfe=int((TOT-E0)*30); os.makedirs('ekf',exist_ok=True); EW,EH=600,100; SP=260.0
def ekv(tm):
    if tm<ON: return 0.0
    u=(tm-ON)%0.7
    if u<0.04: return -0.25*u/0.04
    if u<0.08: return -0.25+1.25*(u-0.04)/0.04
    if u<0.13: return 1.0-1.5*(u-0.08)/0.05
    if u<0.17: return -0.5+0.5*(u-0.13)/0.04
    if 0.28<u<0.42: return 0.18*math.sin(math.pi*(u-0.28)/0.14)
    return 0.0
for q in range(nfe):
    tm=E0+q/30; im=Image.new('RGBA',(EW,EH),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([0,0,EW-1,EH-1],radius=16,fill=(0,0,0,170))
    pts=[(x,EH*0.62-ekv(tm-(EW-20-x)/SP)*EH*0.5) for x in range(14,EW-18,3)]
    c=(60,255,110,255) if tm>=ON else (255,60,60,255)
    d.line(pts,fill=c,width=6,joint='curve'); x,y=pts[-1]; d.ellipse([x-9,y-9,x+9,y+9],fill=(255,255,255,255))
    im.save(f'ekf/{q:04d}.png')
run('ffmpeg -v error -y -framerate 30 -i ekf/%04d.png -c:v qtrle ekg.mov')
# confetti over party
C0=T0(iP); nfc=int((T0(iG)-C0)*30); os.makedirs('cff',exist_ok=True); rg_=np.random.default_rng(7)
PT=[(rg_.uniform(0,1080),rg_.uniform(-1900,0),rg_.uniform(700,1300),rg_.uniform(0,6.28),[(255,60,90),(255,214,0),(60,200,255),(120,230,90),(255,140,30),(200,90,255)][i%6]) for i in range(150)]
for q in range(nfc):
    tm=q/30; im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im)
    for x0,y0,vy,ph,c in PT:
        y=y0+vy*tm; x=x0+40*math.sin(tm*5+ph)
        if -30<y<1950:
            w=10+8*abs(math.sin(tm*9+ph)); d.polygon([(x-w,y-7),(x+w,y-12),(x+w,y+7),(x-w,y+12)],fill=c+(235,))
    im.save(f'cff/{q:04d}.png')
run('ffmpeg -v error -y -framerate 30 -i cff/%04d.png -c:v qtrle confetti.mov')
tt=np.arange(int(sr*0.75))/sr; f0=330+40*np.minimum(tt/0.1,1); ph=2*np.pi*np.cumsum(f0)/sr
wsave('horn.wav',(2*((ph/(2*np.pi))%1)-1)*0.5*np.minimum(tt/0.03,1)*np.minimum((0.75-tt)/0.08,1)*0.5)
fl=max(0.3,ON-T0(iG)); tt=np.arange(int(sr*fl))/sr; wsave('flat.wav',np.sin(2*np.pi*1000*tt)*np.minimum(tt/0.05,1)*np.minimum((fl-tt)/0.02,1)*0.7)
tt=np.arange(int(sr*1.1))/sr; f0=500+900*np.sin(np.pi*tt/1.1)**0.6+25*np.sin(2*np.pi*9*tt); ph=2*np.pi*np.cumsum(f0)/sr; wsave('yeow.wav',(np.sin(ph)+0.5*np.sin(2*ph)+0.25*np.sin(3*ph))*np.minimum(tt/0.04,1)*np.minimum((1.1-tt)/0.15,1)*0.35)
tt=np.arange(int(sr*0.1))/sr; wsave('blip.wav',np.sin(2*np.pi*1000*tt)*np.minimum(tt/0.005,1)*np.minimum((0.1-tt)/0.01,1)*0.8)
OFF1=T0(2)+0.78; OFF2=T0(8)+0.95; FEAR=tl(18.84); FINE=tl(47.10)
fc=[f"[0:v]drawbox=c=black@0.6:t=fill:enable='between(t,{OFF1:.3f},{T0(3)-0.01:.3f})+between(t,{OFF2:.3f},{T0(9)-0.01:.3f})+between(t,{T0(iON):.3f},{ON-0.01:.3f})'[d0]",
 f"[d0]scale=1160:2062,crop=1080:1920:'40+if(between(t,0.55,1.0),30*sin(t*95),0)':'71+if(between(t,0.55,1.0),30*cos(t*80),0)'[v1s]",
 "[v1s][1:v]overlay[v3]", f"[v3][2:v]overlay=enable='lt(t,{HOOK_END:.3f})'[v4]",
 f"[v4]drawbox=x=0:y=0:w='iw*t/{TOT:.3f}':h=14:color=0xFFD600@1:t=fill[v5]"]
cur='[v5]'; idx=3; extra=[]
def ov(png,a,b):
    global cur,idx
    extra.append(f'-loop 1 -i {png}'); fc.append(f"{cur}[{idx}:v]overlay=enable='between(t,{a:.3f},{b:.3f})'[o{idx}]"); cur=f'[o{idx}]'; idx+=1
ov('l_feel.png',T0(2),OFF1-0.01); ov('l_off.png',OFF1,T0(3)-0.02)
ov('l_fj.png',T0(7),FEAR-0.01); ov('l_fj2.png',FEAR,OFF2-0.01); ov('l_fj3.png',OFF2,T0(9)-0.02); ov('l_both.png',OFF2+0.05,T0(9)-0.02)
ov('l_reen.png',T0(9),T0(iG)-0.02); ov('l_glass.png',T0(iG2)+0.1,T0(iZ)-0.05); ov('l_on.png',ON,T0(iFINE)-0.02); ov('l_fine.png',FINE,T0(iDAY)-0.02); ov('tagline.png',T0(iSM),TOT)
ov('m0.png',0,SMILE-0.01)
for q,nm in enumerate(['m25','m50','m75']): ov(nm+'.png',SMILE+q*0.07,SMILE+(q+1)*0.07-0.005)
ov('m100.png',SMILE+0.21,T0(iRX)-0.005); ov('m1000.png',T0(iRX),TOT)
ov('l_n1.png',2.3,2.59); ov('l_n2.png',2.6,2.89); ov('l_n3.png',2.9,3.19)
ov('l_still.png',T0(iZ2)+0.45,T0(iSY)-0.02); ov('l_feel2.png',T0(iRX)+0.1,TOT)
for q,nm in enumerate(['l_ha1','l_ha2','l_ha3']): ov(nm+'.png',T0(iC)+0.25+q*0.3,T0(iC2)-0.02)
extra.append('-i ekg.mov'); fc.append(f"[{idx}:v]setpts=PTS+{T0(iP):.3f}/TB[ek];{cur}[ek]overlay=30:1470:eof_action=pass[vek]"); cur='[vek]'; idx+=1
extra.append('-i confetti.mov'); fc.append(f"[{idx}:v]setpts=PTS+{T0(iP):.3f}/TB[cf];{cur}[cf]overlay=0:0:eof_action=pass[vcf]"); cur='[vcf]'; idx+=1
PIPS=[0,2,7,8,9,10,11,12,13,14,17]
PC_={0:(.65,.52),2:(.60,.50),7:(.55,.45),8:(.50,.42),9:(.40,.45),10:(.50,.48),11:(.60,.40),12:(.55,.42),13:(.60,.40),14:(.72,.55),17:(.80,.72)}
mk=Image.new('L',(400,400),0); ImageDraw.Draw(mk).ellipse([0,0,399,399],fill=255); mk.save('mask.png')
rg=Image.new('RGBA',(424,424),(0,0,0,0)); ImageDraw.Draw(rg).ellipse([2,2,421,421],outline=(255,255,255,255),width=12); rg.save('ring.png')
for j,si in enumerate(PIPS):
    aa=SEG[si][3]; d_=min(log[si][3],2.3) if si==0 else log[si][3]; t0=T0(si)
    run(f'ffmpeg -v error -y -ss {aa:.3f} -i T1.mov -an -t {d_:.3f} -vf "hflip,crop=560:560:{min(520,max(0,int(PC_[si][0]*1080-280)))}:{min(1360,max(0,int(PC_[si][1]*1920-300)))},scale=400:400,fps=30,format=yuv420p" -c:v libx264 -crf 16 pipsrc{j}.mp4')
    extra.append(f'-i pipsrc{j}.mp4 -loop 1 -i mask.png -loop 1 -i ring.png')
    fc.append(f"[{idx}:v]format=rgba[pc{j}];[{idx+1}:v]format=gray[mk{j}];[pc{j}][mk{j}]alphamerge=shortest=1,setpts=PTS+{t0:.3f}/TB[pm{j}];{cur}[pm{j}]overlay=650:1460:eof_action=pass[pq{j}];[pq{j}][{idx+2}:v]overlay=638:1448:enable='between(t,{t0:.3f},{t0+d_-0.03:.3f})'[pr{j}]"); cur=f'[pr{j}]'; idx+=3
for j,(name,st0,x,y,dur) in enumerate(POPS):
    extra.append(f'-i p{j}.mov'); fc.append(f"[{idx}:v]setpts=PTS+{st0:.3f}/TB[pp{j}];{cur}[pp{j}]overlay={x}:{y}:eof_action=pass[pv{j}]"); cur=f'[pv{j}]'; idx+=1
extra.append('-loop 1 -i strip.png'); fc.append(f"{cur}[{idx}:v]overlay=enable='gte(t,{stripT:.3f})'[vs]"); cur='[vs]'; idx+=1
for i,(t_,a,b) in enumerate(CUES):
    extra.append(f'-i cap{i}.png'); fc.append(f"{cur}[{idx}:v]overlay=enable='between(t,{a:.3f},{b:.3f})'[x{i}]"); cur=f'[x{i}]'; idx+=1
open('fc.txt','w').write(";".join(fc))
run(f'ffmpeg -v error -y -i vcat.mp4 -i tag.png -loop 1 -i hook.png '+' '.join(extra)+f' -filter_complex_script fc.txt -map "{cur}" -t {TOT:.3f} -c:v libx264 -crf 17 -preset medium vcap.mp4')
ev=[("splash",0.5,2),("thump",0.55,-3),("click",OFF1-0.03,4),("powerdown",OFF1,-4),("thump",FEAR,-5),("click",OFF2-0.03,4),("powerdown",OFF2,-4),
("pop",T0(9)+0.1,-4),("haha",T0(10)+0.1,-9),("haha",T0(10)+0.55,-11),("horn",T0(iC2)+0.05,-6),("thump",T0(iG)+0.05,-3),("squeak",T0(iG2)+0.1,-3),("whoosh",T0(iZ)-0.12,-6),("thump",T0(iZ)+0.05,-5),("crash",T0(iZ2)+0.45,-8),("thump",T0(iZ2)+0.45,0),("thump",2.3,-1),("thump",2.6,0),("punch",2.9,0),("boing",T0(iRX)+0.15,-2),("boing",T0(iRX)+0.75,-3),("yeow",T0(iRX)+0.05,-5),("flat",T0(iG),-25),
("click",ON-0.03,4),("ding",ON,-3),("punch",FINE,-3),("ding",SMILE,-2),("pop",SMILE,-3),("dod_hit",TOT-0.75,6)]+[("pop",p[1],-9) for p in POPS]+[("blip",bt,-15) for bt in BEATS]
ins=" ".join(f"-i {n}.wav" for n,_,_ in ev); parts=[]; labs=[]
for j,(n,s0,g) in enumerate(ev):
    D=max(0,int(s0*1000)); parts.append(f"[{j+1}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={D}|{D},volume={g}dB[e{j}]"); labs.append(f"[e{j}]")
fa_="; ".join(parts)+f";[0:a]{''.join(labs)}amix=inputs={len(ev)+1}:duration=first:normalize=0[a]"
run(f'ffmpeg -v error -y -i acat.wav {ins} -filter_complex "{fa_}" -map "[a]" amix.wav')
run('ffmpeg -v error -y -i vcap.mp4 -i amix.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le body.mov')
# finish: two-pass loudnorm
import re
r=subprocess.run('ffmpeg -hide_banner -i body.mov -af loudnorm=I=-15.5:TP=-1.5:LRA=11:print_format=json -f null -',shell=True,capture_output=True,text=True).stderr
m=json.loads(re.search(r'\{[^{}]*"input_i"[^{}]*\}',r).group(0))
run(f'ffmpeg -v error -y -i body.mov -af "loudnorm=I=-15.5:TP=-1.5:LRA=11:measured_I={m["input_i"]}:measured_TP={m["input_tp"]}:measured_LRA={m["input_lra"]}:measured_thresh={m["input_thresh"]}:offset={m["target_offset"]}:linear=true" -c:v libx264 -crf 21 -preset medium -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart MAYDAY-Day-18-NUMB.mp4')
json.dump({"log":log,"cues":CUES,"strip":stripT},open('plan.json','w'),indent=0)
print("TOT",TOT,"cues",len(CUES)); print(" | ".join(c for c,_,_ in CUES))
for i in range(len(SEG)): print(i,round(T0(i),2),SEG[i][0])
