import subprocess, json, math, os, re, random, glob, sys, numpy as np, wave
from PIL import Image, ImageDraw, ImageFont, ImageFilter
def run(c): subprocess.run(c,shell=True,check=True)
os.chdir('/tmp/claude-0/d20g')
FI='/tmp/claude-0/fonts/gf/ofl/montserrat/Montserrat-Italic[wght].ttf'; EM='/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
def MB(sz,var='Black Italic'):
    f=ImageFont.truetype(FI,sz); f.set_variation_by_name(var); return f
OFFB=0.0; OFFA=0.1; OFF={'tB':OFFB,'tA':OFFA}
KEEP=os.environ.get('KEEP','0')=='1'
# ---- master audio (aligned) -------------------------------------------------
if not os.path.exists('wTB.wav'): run('ffmpeg -v error -y -i tB.mov -map 0:a:0 -ac 2 -ar 48000 -af "highpass=f=80,loudnorm=I=-16:TP=-2:LRA=11" wTB.wav')
if not os.path.exists('wTA.wav'): run('ffmpeg -v error -y -i tA.mov -map 0:a:0 -ac 2 -ar 48000 -af "adelay=100|100,highpass=f=80,loudnorm=I=-20:TP=-2:LRA=11" wTA.wav')
WAV={'tB':'wTB.wav','tA':'wTA.wav'}
# ---- segment table ------------------------------------------------------------
# dict: name, src, vs (video start s), dur, speed, look (hot|sad), aud=(clip,rawstart,rawlen,gain_db) , matte key, pip=(clip,rawstart), crop, zoom, freeze, black
def seg(name,src=None,vs=0,dur=1.0,speed=1.0,look='hot',aud=None,matte=None,pip=None,crop='',zoom=False,freeze=False,black=False,mo=0.0,grp=None,zs=0.20,rew=False,pre=0.0,flip=False):
    return dict(name=name,src=src,vs=vs,dur=dur,speed=speed,look=look,aud=aud,matte=matte,pip=pip,crop=crop,zoom=zoom,freeze=freeze,black=black,mo=mo,grp=grp or name,zs=zs,rew=rew,pre=pre,flip=flip)
PRE=2.4
S=[
 seg('hook','c28',1.00,2.60,aud=('tB',1.56,2.60,0),pip=('tB',1.56)),
 seg('catchA',matte='mk_tB_6.500_197.mp4',mo=0.0,dur=6.0,aud=('tB',6.50,6.0,0),grp='catch'),
 seg('fz1',freeze=True,dur=1.0,zs=0.05,grp='catch'),
 seg('catchB',matte='mk_tB_6.500_197.mp4',mo=6.0,dur=197/30-6.0,aud=('tB',12.50,197/30-6.0,0),grp='catch'),
 seg('wt',matte='mk_tB_13.400_22.mp4',dur=22/30,aud=('tB',13.40,0.64,0)),
 seg('ptsdA',matte='mk_tB_14.600_84.mp4',mo=0.0,dur=2.4,aud=('tB',14.60,2.4,0),grp='ptsd'),
 seg('fz2',freeze=True,dur=1.0,zs=0.05,grp='ptsd'),
 seg('ptsdB',matte='mk_tB_14.600_84.mp4',mo=2.4,dur=0.4,aud=('tB',17.0,0.4,0),grp='ptsd'),
 seg('fuse','c36',0.0,72/30,aud=('tB',23.55,1.40,0),pip=('tB',23.55)),
 seg('laugha','c35',1.90,31/30,aud=('tB',26.70,1.03,0),pip=('tB',26.70)),
 seg('laughb','c37',1.50,24/30,aud=('tB',27.70,0.80,0),pip=('tB',27.70)),
 seg('chaira','c37',0.0,42/30,aud=('tB',30.65,1.40,0),pip=('tB',30.65)),
 seg('chairb','c37',2.40,51/30,aud=('tB',32.05,1.70,0),pip=('tB',32.05)),
 seg('lasta','c31',6.00,51/30,aud=('tB',38.65,1.60,0),pip=('tB',38.65)),
 seg('lastb','c31',7.70,51/30,pip=('tB',40.30)),
 seg('signa','c38',0.40,66/30,aud=('tB',43.10,2.20,0),pip=('tB',43.10)),
 seg('reveal','c38',2.60,48/30,pip=('tB',46.00)),
 seg('walk','c38',4.20,48/30,pip=('tB',47.20)),
 seg('freeze',dur=1.0,freeze=True),
 seg('gap0',dur=0.6,black=True,look='sad'),
 seg('s1','tA',2.70+OFFA,68/30+PRE,look='sad',aud=('tA',2.70,2.0,0),zoom=True,matte='dk_tA_2.800_68.mp4',pre=PRE,flip=True),
 seg('s2','tA',4.95+OFFA,62/30,look='sad',aud=('tA',4.95,2.0,0),zoom=True,matte='dk_tA_5.050_62.mp4',flip=True),
 seg('s3','c36',0.0,1.2,speed=0.5,look='sad'),
 seg('s4','c37',2.20,2.35,speed=0.5,look='sad',aud=('tA',8.30,2.30,0)),
 seg('s5','c31',9.0,1.4,speed=0.5,look='sad'),
 seg('s6','tA',11.10+OFFA,2.0+PRE,look='sad',aud=('tA',11.10,1.9,0),zoom=True,matte='dk_tA_11.200_60.mp4',pre=PRE,flip=True),
 seg('s7','c38',10.0,1.0,speed=0.5,look='sad'),
 seg('s8','c31',10.4,1.80,speed=0.5,look='sad',aud=('tA',15.10,1.75,0),crop='crop=iw*0.5:ih*0.5:iw*0.45:ih*0.40,'),
 seg('s9','tA',19.95+OFFA,3.8+PRE,look='sad',aud=('tA',19.95,2.8,0),zoom=True,matte='dk_tA_20.050_114.mp4',pre=PRE,flip=True),
 seg('rew',dur=1.5,look='sad',rew=True),
 seg('e1',flip=True,matte='mk_tA_23.900_111.mp4',dur=111/30,aud=('tA',23.80,111/30,4)),
 seg('e2','c38',4.70,57/30,aud=('tA',27.85,1.95,4),pip=('tA',27.85)),
 seg('e3','c38',6.60,33/30),
 seg('e4',freeze=True,dur=1.4),
]
for q,sg in enumerate(S): sg['i']=q
IX={sg['name']:q for q,sg in enumerate(S)}
# round durations to frames
t=0.0
for sg in S:
    sg['n']=max(1,round(sg['dur']*30)); sg['d']=sg['n']/30; sg['t0']=t; t+=sg['d']
TOT=t
def T0(n): return S[IX[n]]['t0'] if isinstance(n,str) else S[n]['t0']
def TE(n): s_=S[IX[n]] if isinstance(n,str) else S[n]; return s_['t0']+s_['d']
def tl(clip,raw):
    for sg in S:
        a=sg['aud']
        if a and a[0]==clip and a[1]<=raw<a[1]+a[2]: return sg['t0']+raw-a[1]+sg['pre']
    return None
SADA=T0('gap0'); SADB=T0('e1'); SADE=T0('rew'); F1=T0('fz1'); F2=T0('fz2')
# ---- render segments ---------------------------------------------------------
vl=open('v.txt','w'); al=open('a.txt','w')
for sg in S:
    i=sg['i']; n=sg['n']; d=sg['d']; look=sg['look']
    sadf=",eq=saturation=0.10:brightness=-0.06:contrast=0.97,vignette=PI/3.2,gblur=sigma=0.7" if look=='sad' else ""
    if not (KEEP and os.path.exists(f's{i}.mp4')):
        if sg['black']:
            run(f'ffmpeg -v error -y -f lavfi -i color=c=black:s=1080x1920:r=30 -t {d:.4f} -pix_fmt yuv420p -c:v libx264 -crf 16 s{i}.mp4')
        elif sg['freeze']:
            run(f'ffmpeg -v error -y -sseof -0.05 -i s{i-1}.mp4 -frames:v 1 -update 1 frz{i}.png'); im=Image.open(f'frz{i}.png').convert('RGB'); os.makedirs(f'zf{i}',exist_ok=True)
            for q in range(n):
                z=(1.0+sg['zs']*min(1,q/4))*(1+0.0014*q); w=1080/z; h=1920/z; x=(1080-w)*0.5; y=(1920-h)*0.40
                im.crop((int(x),int(y),int(x+w),int(y+h))).resize((1080,1920),Image.LANCZOS).save(f'zf{i}/{q:03d}.png')
            run(f'ffmpeg -v error -y -framerate 30 -i zf{i}/%03d.png -c:v libx264 -crf 14 -pix_fmt yuv420p s{i}.mp4')
        elif sg['rew']:
            run(f'ffmpeg -v error -y -sseof -3.0 -i s{i-1}.mp4 -an -vf "reverse,setpts=PTS/2.0,fps=30,noise=alls=26:allf=t,rgbashift=rh=22:bh=-22:enable=\'lt(mod(t,0.34),0.12)\',eq=brightness=0.04:contrast=1.15,format=yuv420p" -frames:v {n} -c:v libx264 -preset veryfast -crf 16 s{i}.mp4')
        elif sg['matte']:
            sadm=(",vignette=PI/3.2" if sg['matte'].startswith('dk_') else ",eq=saturation=0.10:brightness=-0.06:contrast=0.97,vignette=PI/3.2") if look=='sad' else ""
            pre_=f",tpad=start_mode=clone:start_duration={sg['pre']:.3f}" if sg['pre']>0 else ""
            fi_=",fade=t=in:st=0:d=0.5" if sg['pre']>0 else ""
            fl_="hflip," if sg['flip'] else ""
            zmm=f",scale=w='trunc(1080*(1+0.05*t/{d:.3f})/2)*2':h='trunc(1920*(1+0.05*t/{d:.3f})/2)*2':eval=frame:flags=bicubic,crop=1080:1920" if sg['zoom'] else ""
            run(f'ffmpeg -v error -y -ss {sg["mo"]:.4f} -i {sg["matte"]} -an -vf "{fl_}fps=30{pre_},format=yuv420p{fi_}{sadm}{zmm},format=yuv420p" -frames:v {n} -c:v libx264 -preset veryfast -crf 14 s{i}.mp4')
        else:
            srcd=d*sg['speed']; spd=f'setpts={1/sg["speed"]:.3f}*PTS,framerate=fps=30:interp_start=0:interp_end=255:scene=100,' if sg['speed']!=1.0 else ''
            zm=f',scale=w=\'trunc(1080*(1+0.05*t/{d:.3f})/2)*2\':h=\'trunc(1920*(1+0.05*t/{d:.3f})/2)*2\':eval=frame:flags=bicubic,crop=1080:1920' if sg['zoom'] else ''
            run(f'ffmpeg -v error -y -ss {sg["vs"]:.3f} -t {srcd+0.1:.3f} -i {sg["src"]}.mov -map 0:v:0 -an -vf "{sg["crop"]}scale=1080:1920:flags=lanczos,fps=30,{spd}fps=30,format=yuv420p{sadf}{zm},format=yuv420p" -frames:v {n} -c:v libx264 -preset veryfast -crf 16 s{i}.mp4')
    a=sg['aud']
    if a is None: run(f'ffmpeg -v error -y -f lavfi -i anullsrc=r=48000:cl=stereo -t {d:.4f} -c:a pcm_s16le s{i}.wav')
    else:
        clip,rs,rl,g=a; aa=rs+OFF[clip]; rl=min(rl,d-sg['pre']); pdl=int(sg['pre']*1000)
        run(f'ffmpeg -v error -y -i {WAV[clip]} -af "atrim={aa:.4f}:{aa+rl:.4f},asetpts=PTS-STARTPTS,volume={g}dB,afade=t=in:d=0.03,afade=t=out:st={max(0,rl-0.06):.4f}:d=0.06,adelay={pdl}|{pdl},apad=whole_dur={d:.4f}" -c:a pcm_s16le s{i}.wav')
    vl.write(f"file s{i}.mp4\n"); al.write(f"file s{i}.wav\n")
vl.close(); al.close()
run('ffmpeg -v error -y -f concat -i v.txt -c copy vcat.mp4'); run('ffmpeg -v error -y -f concat -i a.txt -c copy acat.wav')
print('TOT',round(TOT,2),[(s_['name'],round(s_['t0'],2)) for s_ in S])

# ---- halo over the solo shots ---------------------------------------------------------
HALO=[]; HV={}
def sprite(w,h,thick,glow):
    im=Image.new('RGBA',(w+120,h+120),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.ellipse([60,60,60+w,60+h],outline=(255,205,70,255),width=thick)
    g=im.filter(ImageFilter.GaussianBlur(glow)); core=Image.new('RGBA',im.size,(0,0,0,0)); d2=ImageDraw.Draw(core)
    d2.ellipse([60+thick//2,60+thick//2,60+w-thick//2,60+h-thick//2],outline=(255,250,215,255),width=max(3,thick//2))
    out=Image.alpha_composite(g,g); out=Image.alpha_composite(out,im); out=Image.alpha_composite(out,core.filter(ImageFilter.GaussianBlur(1.2)))
    return out
SPR=sprite(300,80,16,14)
for nm in HALO:
    sg=S[IX[nm]]; i=sg['i']; n=sg['n']
    raw=subprocess.run(f'ffmpeg -v error -i s{i}.mp4 -vf scale=270:480,format=gray -f rawvideo -',shell=True,capture_output=True).stdout
    fr=np.frombuffer(raw,dtype=np.uint8).reshape(-1,480,270)[:n]
    tops=[];cxs=[]
    for f in fr:
        rows=np.where((f>75).sum(axis=1)>=10)[0]; rows=rows[rows>60]
        if len(rows)==0: tops.append(tops[-1] if tops else 120); cxs.append(cxs[-1] if cxs else 135); continue
        tp=rows[0]; band=f[tp:tp+22]; ys,xs=np.where(band>75); tops.append(tp); cxs.append(xs.mean() if len(xs) else 135)
    k=9; pad=lambda a: np.convolve(np.pad(a,(k//2,k//2),mode='edge'),np.ones(k)/k,mode='valid')
    tops=pad(np.array(tops,float))*4; cxs=pad(np.array(cxs,float))*4
    os.makedirs(f'hl{i}',exist_ok=True)
    for q in range(n):
        tt=q/30; a=min(1,tt/0.35)*(0.88+0.12*math.sin(tt*5)); sc=0.7+0.3*min(1,tt/0.35)
        sp=SPR.resize((int(SPR.width*sc),int(SPR.height*sc)),Image.LANCZOS); sp=sp.rotate(-6,resample=Image.BICUBIC,expand=True)
        sp.putalpha(sp.split()[3].point(lambda p:int(p*a)))
        cv=Image.new('RGBA',(1080,1920),(0,0,0,0)); cv.paste(sp,(int(cxs[q]-sp.width/2),int(tops[q]-sp.height/2-52+8*math.sin(tt*2.4))),sp); cv.save(f'hl{i}/{q:03d}.png')
    run(f'ffmpeg -v error -y -framerate 30 -i hl{i}/%03d.png -c:v qtrle halo{i}.mov'); HV[nm]=i
# ---- text helpers -------------------------------------------------------------
GR=Image.new('RGB',(4,256))
for yy in range(256):
    k=yy/255; GR.paste((255,int(236-110*k*k),int(20*(1-k))),(0,yy,4,yy+1))
def mbtext(im,xy,txt,font,key=False,stroke=11,sh=(9,11),col=(255,255,255,255)):
    x,y=xy; d=ImageDraw.Draw(im)
    d.text((x+sh[0],y+sh[1]),txt,font=font,fill=(0,0,0,255),stroke_width=stroke,stroke_fill=(0,0,0,255))
    d.text((x,y),txt,font=font,fill=col,stroke_width=stroke,stroke_fill=(0,0,0,255))
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
def label(name,txt,cy,fs,style="red",cx=540,rot=-4):
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im); f=MB(fs); w=d.textlength(txt,font=f)
    if style=="red":
        brush(d,[cx-w/2-34,cy-fs*0.62,cx+w/2+34,cy+fs*0.72],seed=len(txt)); mbtext(im,(cx-w/2,cy-fs*0.55),txt,f,stroke=6,sh=(6,7))
    else: mbtext(im,(cx-w/2,cy-fs*0.55),txt,f,key=True,stroke=12)
    im=im.rotate(rot,resample=Image.BICUBIC,center=(cx,cy)); im.save(name)
# ---- captions -----------------------------------------------------------------
HOT=[ # text, clip, raw a, raw b, size, keywords
 ("YOUR FAMILY SAW IT",'tB',1.66,2.64,118,set()),("WAY BEFORE YOU DID.",'tB',2.68,3.9,118,{"DID."}),
 ("NOBODY LISTENED,",'tB',6.74,8.2,124,{"LISTENED,"}),("SO I'M GONNA GET",'tB',8.24,9.38,112,set()),("LOUDER,",'tB',9.40,10.40,150,{"LOUDER,"}),("AND LOUDER,",'tB',10.44,11.60,176,{"LOUDER,"}),("AND LOUDER.",'tB',11.64,13.05,206,{"LOUDER."}),
 ("WE'RE TALKING",'tB',13.46,14.06,120,set()),("PTSD.",'tB',14.62,15.24,170,{"PTSD."}),("PTSD.",'tB',15.26,15.84,200,{"PTSD."}),("PTSD.",'tB',15.86,16.44,232,{"PTSD."}),("PTSD!",'tB',16.46,17.40,262,{"PTSD!"}),
 ("THEY SAW THE SHORT",'tB',23.64,24.44,112,set()),("FUSE.",'tB',24.46,25.5,160,{"FUSE."}),
 ("THEY SAW YOU STOP",'tB',26.74,27.68,112,set()),("LAUGHING.",'tB',27.70,28.6,150,{"LAUGHING."}),
 ("THEY SAW YOU LEAVE",'tB',30.72,31.46,106,set()),("THE ROOM",'tB',31.48,32.20,124,{"ROOM"}),("WITHOUT EVEN LEAVING",'tB',32.22,33.12,100,set()),("YOUR CHAIR.",'tB',33.14,34.1,140,{"CHAIR."}),
 ("AND YOU WERE THE",'tB',38.74,39.26,112,set()),("LAST ONE TO KNOW.",'tB',39.28,40.5,112,{"KNOW."}),
 ("YOU CAN'T EVEN READ",'tB',43.14,43.82,104,set()),("THE SIGN ON YOUR",'tB',43.84,44.5,104,set()),("OWN BACK.",'tB',44.52,45.6,152,{"BACK."}),
 ("THIS IS DAY 20",'tA',23.96,24.8,112,{"20"}),("OF 61.",'tA',24.8,25.8,170,{"61."}),("CALL YOUR MAYDAY,",'tA',26.52,27.5,120,{"MAYDAY,"}),
 ("AND THEN SEND THIS",'tA',27.94,28.54,104,set()),("TO SOMEONE WHO WORE",'tA',28.54,29.30,104,set()),("THE UNIFORM.",'tA',29.30,30.3,128,{"UNIFORM."}),
]
SOFT=[("So when the ones that love you",'tA',2.9,4.95),("tell you something's off,",'tA',4.96,7.0),("please don't fight them.",'tA',8.38,10.3),("Believe them.",'tA',11.24,12.7),("They're not attacking you.",'tA',15.18,16.9),("They're calling your mayday for you.",'tA',20.04,22.7)]
CUES=[]
for i,(txt,clip,ra,rb,sz,keys) in enumerate(HOT):
    a=tl(clip,ra+0.0001); b=tl(clip,rb-0.0001)
    if a is None: print('NO MAP',txt); continue
    if b is None: # clamp to the end of the segment
        sg=[s_ for s_ in S if s_['aud'] and s_['aud'][0]==clip and s_['aud'][1]<=ra<s_['aud'][1]+s_['aud'][2]][0]; b=TE(sg['i'])
    # do not run past the owning segment
    own=[s_ for s_ in S if s_['t0']<=a<s_['t0']+s_['d']][0]; gend=max(s_['t0']+s_['d'] for s_ in S if s_['grp']==own['grp']); b=min(b,gend-0.02)
    if b-a<0.25: b=min(a+0.3,gend-0.02)
    CUES.append((txt,a,b,sz,keys,i))
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im); font=MB(sz); lines=[]; cu=''
    for w in txt.split():
        tt=(cu+' '+w).strip()
        if d.textlength(tt,font=font)>960 and cu: lines.append(cu); cu=w
        else: cu=tt
    lines.append(cu); lh=int(sz*1.14); y=1290-len(lines)*int(lh/2)
    for L in lines:
        x=(1080-d.textlength(L,font=font))/2
        for w in L.split():
            mbtext(im,(x,y),w,font,key=(w in keys),stroke=max(8,sz//10),sh=(max(6,sz//12),max(7,sz//10))); x+=d.textlength(w+' ',font=font)
        y+=lh
    im.save(f'cap{i}.png')
SC=[]
for j,(txt,clip,ra,rb) in enumerate(SOFT):
    a=tl(clip,ra+0.0001); own=[s_ for s_ in S if s_['t0']<=a<s_['t0']+s_['d']][0]; b=own['t0']+own['d']-0.05
    b=max(b,a+1.4) if False else b
    SC.append((a,b)); im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im); font=MB(80,'SemiBold Italic'); lines=[]; cu=''
    for w in txt.split():
        tt=(cu+' '+w).strip()
        if d.textlength(tt,font=font)>900 and cu: lines.append(cu); cu=w
        else: cu=tt
    lines.append(cu); y=1380-len(lines)*46
    for L in lines: mbtext(im,((1080-d.textlength(L,font=font))/2,y),L,font,stroke=7,sh=(4,5)); y+=96
    im.save(f'soft{j}.png')
# ---- overlays art ---------------------------------------------------------------
tag=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(tag); brush(d,[48,128,470,196],seed=3); mbtext(tag,(64,126),"MAYDAY",MB(60),stroke=5,sh=(5,6)); mbtext(tag,(60,204),"DAY 20 OF 61",MB(40),key=True,stroke=7,sh=(5,6)); tag.save('tag.png')
st=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(st); brush(d,[40,1590,1040,1700],seed=5); f=MB(60); s1="STRUGGLING? CALL OR TEXT 988"; mbtext(st,((1080-d.textlength(s1,font=f))/2,1602),s1,f,stroke=5,sh=(5,6))
f=MB(33); s2="VETERANS: 988, PRESS 1"; mbtext(st,((1080-d.textlength(s2,font=f))/2,1716),s2,f,key=True,stroke=6,sh=(4,5)); s3="RESPONDERS: SAFE CALL NOW 206-459-3020"; mbtext(st,((1080-d.textlength(s3,font=f))/2,1762),s3,f,key=True,stroke=6,sh=(4,5)); st.save('strip.png')
label('l_fuse.png',"SHORT FUSE.",1180,120); label('l_laugh.png',"STOPPED LAUGHING.",1180,90); label('l_notes.png',"THEY LEFT NOTES.",1180,100)
label('l_oh.png',"...OH.",1180,150,"yel"); label('l_see.png',"THIS IS WHAT THEY SEE.",1180,78); label('l_notok.png',"NOT OK.",960,250,"yel",rot=-6)
label('l_follow.png',"FOLLOW FOR DAY 21",1400,70,"yel",rot=0)
def emoji(ch_,name,sz=380):
    f=ImageFont.truetype(EM,109); im=Image.new('RGBA',(160,160),(0,0,0,0)); ImageDraw.Draw(im).text((12,16),ch_,font=f,embedded_color=True)
    a=im.split()[3]; out=Image.new('RGBA',(160,160),(0,0,0,0)); out.paste((255,255,255,255),(0,0),a.filter(ImageFilter.MaxFilter(9))); out.paste(im,(0,0),im); out.resize((sz,sz),Image.LANCZOS).save(f'e_{name}.png')
for c_,nm in [("\U0001F9E8","fuse"),("\U0001F602","lol"),("\U0001F610","flat"),("\U0001F6AA","door"),("\U0001FA91","chair"),("\U0001F4DD","memo")]: emoji(c_,nm)
POPS=[("fuse",tl('tB',24.46),60,520,0.9),("lol",T0('laugha')+0.05,60,520,0.8),("flat",T0('laughb')+0.02,60,520,0.8),("door",tl('tB',31.64),60,520,0.8),("chair",tl('tB',33.14),640,560,0.9),("memo",T0('lastb')+0.15,60,520,0.8),("memo",T0('lastb')+0.75,640,560,0.8)]
for j,(name,st0,x,y,dur) in enumerate(POPS):
    nf=int(dur*30); src=Image.open(f'e_{name}.png'); os.makedirs(f'pf{j}',exist_ok=True)
    for q in range(nf):
        tt=q/30; sc=0.3+0.9*tt/0.15 if tt<0.15 else (1.2-0.2*(tt-0.15)/0.1 if tt<0.25 else 1.0); al_=1.0 if tt<dur-0.2 else max(0,(dur-tt)/0.2)
        fr=Image.new('RGBA',(520,520),(0,0,0,0)); im=src.resize((max(1,int(src.width*sc)),max(1,int(src.height*sc)))); rot=im.rotate(-8+16*math.sin(tt*6+j),resample=Image.BICUBIC,expand=True)
        if al_<1: rot.putalpha(rot.split()[3].point(lambda p:int(p*al_)))
        fr.paste(rot,((520-rot.width)//2,(520-rot.height)//2),rot); fr.save(f'pf{j}/{q:03d}.png')
    run(f'ffmpeg -v error -y -framerate 30 -i pf{j}/%03d.png -c:v qtrle p{j}.mov')
mk=Image.new('L',(400,400),0); ImageDraw.Draw(mk).ellipse([0,0,399,399],fill=255); mk.save('mask.png')
rg=Image.new('RGBA',(424,424),(0,0,0,0)); ImageDraw.Draw(rg).ellipse([2,2,421,421],outline=(255,255,255,255),width=12); rg.save('ring.png')

# ---- rewind clock ----------------------------------------------------------------
NC=int(1.5*30); os.makedirs('ck',exist_ok=True)
for q in range(NC):
    im=Image.new('RGBA',(800,800),(0,0,0,0)); d=ImageDraw.Draw(im); cx=cy=400; tt=q/30
    sc=0.55+0.45*min(1,tt/0.18)
    d.ellipse([20,20,780,780],fill=(10,10,12,215),outline=(255,255,255,255),width=18)
    d.ellipse([40,40,760,760],outline=(214,18,36,255),width=8)
    for k in range(12):
        a=math.radians(k*30); r0=300 if k%3 else 270
        d.line([(cx+r0*math.sin(a),cy-r0*math.cos(a)),(cx+345*math.sin(a),cy-345*math.cos(a))],fill=(255,255,255,255),width=14 if k%3==0 else 8)
    ma=-(tt/1.5)*360*4+215; ha=ma/12+30; sa=-(tt/1.5)*360*14
    def hand(a,L,w,col):
        r=math.radians(a); d.line([(cx,cy),(cx+L*math.sin(r),cy-L*math.cos(r))],fill=col,width=w)
    hand(ha,190,26,(255,255,255,255)); hand(ma,290,18,(255,255,255,255)); hand(sa,320,8,(255,214,0,255))
    d.ellipse([cx-24,cy-24,cx+24,cy+24],fill=(214,18,36,255))
    # rewind chevrons
    for k,xx in enumerate((300,400)):
        d.polygon([(xx+60,610),(xx+60,690),(xx,650)],fill=(255,214,0,255),outline=(0,0,0,255))
    al=1.0 if tt<1.3 else max(0,(1.5-tt)/0.2)
    im=im.resize((int(800*sc),int(800*sc)),Image.LANCZOS)
    if al<1: im.putalpha(im.split()[3].point(lambda p:int(p*al)))
    fr=Image.new('RGBA',(800,800),(0,0,0,0)); fr.paste(im,((800-im.width)//2,(800-im.height)//2),im); fr.save(f'ck/{q:03d}.png')
run('ffmpeg -v error -y -framerate 30 -i ck/%03d.png -c:v qtrle clock.mov')

# ---- coffee pot sign (intro) -------------------------------------------------------
os.makedirs('cs',exist_ok=True)
base=Image.new('RGBA',(520,440),(0,0,0,0)); d=ImageDraw.Draw(base)
d.rectangle([30,36,490,406],fill=(0,0,0,140))
d.rectangle([20,26,480,396],fill=(252,250,238,255),outline=(30,30,30,255),width=5)
fa=MB(78,'Black Italic')
for ln,yy,col in (("PLEASE TALK",72,(200,16,32,255)),("TO",160,(20,20,20,255)),("SOMEONE.",235,(200,16,32,255))):
    w=d.textlength(ln,font=fa); d.text((250-w/2,yy),ln,font=fa,fill=col)
fs=MB(40,'Bold Italic'); t2="- WE LOVE YOU"; d.text((250-d.textlength(t2,font=fs)/2,335),t2,font=fs,fill=(20,20,20,255))
d.rectangle([180,8,320,48],fill=(235,215,150,230)); d.rectangle([180,372,320,412],fill=(235,215,150,230))
for q in range(int(1.4*30)):
    tt=q/30; sc=0.25+1.05*tt/0.16 if tt<0.16 else (1.3-0.3*(tt-0.16)/0.12 if tt<0.28 else 1.0)
    im=base.resize((int(520*sc),int(440*sc)),Image.LANCZOS).rotate(-5+(10*(1-min(1,tt/0.3)) if tt<0.3 else 0),resample=Image.BICUBIC,expand=True)
    fr=Image.new('RGBA',(620,540),(0,0,0,0)); fr.paste(im,((620-im.width)//2,(540-im.height)//2),im); fr.save(f'cs/{q:03d}.png')
run('ffmpeg -v error -y -framerate 30 -i cs/%03d.png -c:v qtrle coffeesign.mov')
# ---- base: zoom + shake ------------------------------------------------------------
L1=tl('tB',9.40); L2=tl('tB',10.74); L3=tl('tB',12.04); CE=TE('catchB')
B1=tl('tB',14.65); B2=tl('tB',15.25); B3=tl('tB',15.85); B4=tl('tB',16.45); PE=TE('ptsdB')
ZZ=f"(1+0.06*between(t,{L1:.2f},{CE:.2f})+0.06*between(t,{L2:.2f},{CE:.2f})+0.10*between(t,{L3:.2f},{CE:.2f})+0.04*between(t,{B2:.2f},{PE:.2f})+0.04*between(t,{B3:.2f},{PE:.2f})+0.06*between(t,{B4:.2f},{PE:.2f}))"
CH=T0('fuse')+1.45; FZ=T0('freeze'); SL=T0('e3')
SHK=[(L1,L1+0.25,14),(L2,L2+0.3,22),(L3,L3+0.6,34),(B1,B1+0.25,16),(B2,B2+0.25,22),(B3,B3+0.25,28),(B4,B4+0.7,40),(CH,CH+0.2,12),(CH+0.45,CH+0.65,12),(FZ,FZ+0.35,30),(SL,SL+0.3,30),(T0('e1'),T0('e1')+0.35,34),(F1,F1+0.15,26),(F2,F2+0.15,26)]
sh=lambda f: "+".join(f"if(between(t,{a:.2f},{b:.2f}),{amp}*{f}(t*90),0)" for a,b,amp in SHK)
hotmask=f"if(between(t,{SADA:.3f},{SADB:.3f}),1.0,1.08)"
fc=[f"[0:v]scale=w='trunc(1080*{hotmask}*{ZZ}/2)*2':h='trunc(1920*{hotmask}*{ZZ}/2)*2':eval=frame:flags=bicubic,crop=1080:1920:'(iw-1080)/2+{sh('sin')}':'(ih-1920)/2+{sh('cos')}'[v1]",
    f"[v1]drawbox=c=white@0.85:t=fill:enable='between(t,{FZ:.3f},{FZ+0.07:.3f})+between(t,{SL:.3f},{SL+0.06:.3f})+between(t,{B4:.3f},{B4+0.05:.3f})+between(t,{F1:.3f},{F1+0.05:.3f})+between(t,{F2:.3f},{F2+0.05:.3f})+between(t,{SADB:.3f},{SADB+0.07:.3f})',drawbox=x=0:y=0:w='iw*t/{TOT:.3f}':h=14:color=0xFFD600@1:t=fill:enable='lt(t,{SADA:.3f})+gt(t,{SADB:.3f})'[v5]"]
cur='[v5]'; idx=2; extra=[]
def ov(png,a,b):
    global cur,idx
    extra.append(f'-loop 1 -i {png}'); fc.append(f"{cur}[{idx}:v]overlay=enable='between(t,{a:.3f},{b:.3f})'[o{idx}]"); cur=f'[o{idx}]'; idx+=1
def ovfade(png,a,b,fd=0.3):
    global cur,idx
    extra.append(f'-loop 1 -i {png}'); fc.append(f"[{idx}:v]format=rgba,fade=t=in:st={a:.3f}:d={fd}:alpha=1,fade=t=out:st={b-fd:.3f}:d={fd}:alpha=1[sf{idx}];{cur}[sf{idx}]overlay=enable='between(t,{a:.3f},{b:.3f})'[o{idx}]"); cur=f'[o{idx}]'; idx+=1
# tag (hot parts)
ov('tag.png',0,SADA); ov('tag.png',SADB,TOT)
# labels
ov('l_fuse.png',T0('fuse')+0.5,TE('fuse')-0.02); ov('l_laugh.png',T0('laughb')+0.02,TE('laughb')-0.02); ov('l_notes.png',T0('lastb')+0.15,TE('lastb')-0.02)
ov('l_oh.png',T0('reveal')+0.55,TE('reveal')-0.02); ov('l_see.png',T0('walk')+0.15,TE('walk')-0.02); ov('l_notok.png',FZ+0.12,TE('freeze')-0.02)
for k,(a,b) in enumerate(SC): ovfade(f'soft{k}.png',a,b,0.35)
# pips: contiguous groups
groups=[]; cg=[]
for sg in S:
    if sg['pip']: cg.append(sg)
    else:
        if cg: groups.append(cg); cg=[]
if cg: groups.append(cg)
for gi,gp in enumerate(groups):
    pcs=[]
    for sg in gp:
        clip,rs=sg['pip']; aa=rs+OFF[clip]; pcs.append(f'pq{gi}_{sg["i"]}.mp4')
        run(f'ffmpeg -v error -y -ss {aa:.3f} -t {sg["d"]:.4f} -i pip_{clip}.mp4 -an -vf "fps=30,format=yuv420p" -frames:v {sg["n"]} -c:v libx264 -crf 16 {pcs[-1]}')
    open(f'pl{gi}.txt','w').write("".join(f"file {p}\n" for p in pcs)); run(f'ffmpeg -v error -y -f concat -i pl{gi}.txt -c copy pipg{gi}.mp4')
    t0=gp[0]['t0']; t1=gp[-1]['t0']+gp[-1]['d']
    extra.append(f'-i pipg{gi}.mp4 -loop 1 -i mask.png -loop 1 -i ring.png')
    fc.append(f"[{idx}:v]format=rgba[pc{gi}];[{idx+1}:v]format=gray[mk{gi}];[pc{gi}][mk{gi}]alphamerge=shortest=1,setpts=PTS+{t0:.3f}/TB[pm{gi}];{cur}[pm{gi}]overlay=650:1460:eof_action=pass[pq{gi}];[pq{gi}][{idx+2}:v]overlay=638:1448:enable='between(t,{t0:.3f},{t1-0.03:.3f})'[pr{gi}]"); cur=f'[pr{gi}]'; idx+=3
for j,(name,st0,x,y,dur) in enumerate(POPS):
    extra.append(f'-i p{j}.mov'); fc.append(f"[{idx}:v]setpts=PTS+{st0:.3f}/TB[pp{j}];{cur}[pp{j}]overlay={x}:{y}:eof_action=pass[pv{j}]"); cur=f'[pv{j}]'; idx+=1
for nm in HALO:
    extra.append(f'-i halo{HV[nm]}.mov'); fc.append(f"[{idx}:v]setpts=PTS+{T0(nm):.3f}/TB[hh{idx}];{cur}[hh{idx}]overlay=0:0:eof_action=pass[hv{idx}]"); cur=f'[hv{idx}]'; idx+=1
extra.append('-i clock.mov'); fc.append(f"[{idx}:v]setpts=PTS+{SADE:.3f}/TB[ckk];{cur}[ckk]overlay=140:560:eof_action=pass[ckv]"); cur='[ckv]'; idx+=1
stripT=T0('e3'); ov('strip.png',stripT,TOT)
for (txt,a,b,sz,keys,i) in CUES:
    ov(f'cap{i}.png',a,b)
ov('l_follow.png',T0('e4')+0.1,TOT)
open('fc.txt','w').write(";".join(fc))
run(f'ffmpeg -v error -y -i vcat.mp4 -i tag.png '+' '.join(extra)+f' -filter_complex_script fc.txt -map "{cur}" -t {TOT:.3f} -c:v libx264 -crf 17 -preset veryfast vcap.mp4')
# ---- audio --------------------------------------------------------------------------
LD=tl('tB',9.40); LD2=tl('tB',10.74); LD3=tl('tB',12.04)
ev=[("whoosh",0.0,-4),("thump",0.08,3),
    ("thump",LD,0),("thump",LD2,3),("riser",LD3-1.2,-6),("punch",LD3,3),("bomb",LD3,-3),
    ("thump",B1,1),("thump",B2,3),("thump",B3,5),("punch",B4,5),("bomb",B4,0),
    ("whoosh",T0('fuse')-0.05,-3),("sizzle",tl('tB',24.0),-3),("chirp",CH,-1),
    ("pop",T0('laugha')+0.05,0),("thump",T0('laughb'),-2),("pop",T0('laughb')+0.02,-1),
    ("pop",tl('tB',31.64),-2),("pop",tl('tB',33.14),-2),
    ("whoosh",T0('lasta')-0.05,-4),("pop",T0('lastb')+0.15,-1),("pop",T0('lastb')+0.75,-1),
    ("whoosh",T0('signa')-0.05,-4),("pop",T0('reveal')+0.7,0),("ding",T0('reveal')+0.9,-6),("heart",T0('walk'),0),("heart",T0('walk')+0.75,0),
    ("drop",FZ,0),("punch",FZ,4),
    ("scratch",T0('e1')-0.05,-4),("rewind",SADE,0),("choir",T0('s1'),-2),("choir",T0('s6'),-3),("choir",T0('s9'),-3),("punch",SADB,5),("bomb",SADB,-1),("screech",F1,2),("screech",F2,2),("thump",F1+1.0,2),("thump",F2+1.0,2),("whoosh",T0('e2')-0.05,-3),("slap",SL+0.02,4),("boing",SL+0.1,-2),("dod_hit",TOT-0.75,6)]
ins=" ".join(f"-i {n}.wav" for n,_,_ in ev); parts=[]; labs=[]
for j,(n,s0,g) in enumerate(ev):
    D=max(0,int(s0*1000)); parts.append(f"[{j+1}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={D}|{D},volume={g}dB[e{j}]"); labs.append(f"[e{j}]")
nin=len(ev)+1
MG=float(os.environ.get('MG','-22')); SG=float(os.environ.get('SG','-24.5'))
silhot="+".join(f"between(t,{s_['t0']:.2f},{s_['t0']+s_['d']:.2f})" for s_ in S if s_['look']=='hot' and not s_['aud'] and not s_['matte'] and not s_['freeze'])
ins+=" -i hard1.wav -i sad.wav -i hard2.wav"
parts.append(f"[{nin}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{FZ+0.03:.3f},volume='{10**(MG/20):.4f}*(1+0.9*({silhot}))*(1-between(t,{F1:.3f},{F1+1.0:.3f}))*(1-between(t,{F2:.3f},{F2+1.0:.3f}))':eval=frame,afade=t=in:d=0.2,afade=t=out:st={FZ-0.02:.3f}:d=0.05[m1]"); labs.append("[m1]"); nin+=1
sd=TOT-(T0('s1')-0.2);
parts.append(f"[{nin}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{SADE-T0('s1')+0.2:.3f},afade=t=in:d=0.6,afade=t=out:st={SADE-T0('s1')+0.2-0.5:.3f}:d=0.5,volume={10**(SG/20):.4f},adelay={int((T0('s1')-0.2)*1000)}|{int((T0('s1')-0.2)*1000)}[m2]"); labs.append("[m2]"); nin+=1
parts.append(f"[{nin}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{TOT-SADB:.3f},volume={10**(MG/20):.4f}*1.2,afade=t=out:st={TOT-SADB-0.9:.3f}:d=0.9,adelay={int(SADB*1000)}|{int(SADB*1000)}[m3]"); labs.append("[m3]"); nin+=1
fa_="; ".join(parts)+f";[0:a]{''.join(labs)}amix=inputs={nin}:duration=first:normalize=0[a]"
run(f'ffmpeg -v error -y -i acat.wav {ins} -filter_complex "{fa_}" -map "[a]" amix.wav')
run('ffmpeg -v error -y -i vcap.mp4 -i amix.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le body.mov')
r=subprocess.run('ffmpeg -hide_banner -i body.mov -af loudnorm=I=-15.5:TP=-1.5:LRA=11:print_format=json -f null -',shell=True,capture_output=True,text=True).stderr
m=json.loads(re.search(r'\{[^{}]*"input_i"[^{}]*\}',r).group(0))
run(f'ffmpeg -v error -y -i body.mov -af "loudnorm=I=-15.5:TP=-1.5:LRA=11:measured_I={m["input_i"]}:measured_TP={m["input_tp"]}:measured_LRA={m["input_lra"]}:measured_thresh={m["input_thresh"]}:offset={m["target_offset"]}:linear=true" -c:v libx264 -crf 21 -preset fast -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart -shortest MAYDAY-Day-20-THEY-SAW-IT-FIRST.mp4')
print('DONE TOT',TOT)
