import subprocess, json
from PIL import Image, ImageDraw, ImageFont
def run(c): subprocess.run(c,shell=True,check=True)
SRC="../d16/sync16.mov"
run(f'ffmpeg -v error -y -i {SRC} -vn -ac 2 -ar 48000 -af "highpass=f=80" w.wav')
SEG=[(12.50,14.36),(14.88,17.46),(18.20,19.02),(19.14,20.10),(20.74,21.52),(22.24,23.58),(25.38,26.46),(28.32,29.80),(30.50,32.30),
(36.32,37.60),(38.66,40.64),(41.40,43.20),(45.28,46.78),(47.06,48.70),(49.80,50.98),(52.24,53.14),(53.32,54.36),(55.00,58.40),
(62.30,64.30),(64.42,65.46),(65.70,70.45)]
words=json.load(open("../d16/w16.json"))
vl=open('v.txt','w'); al=open('a.txt','w'); t=0; log=[]
for i,(a,b) in enumerate(SEG):
    n=round((b-a)*30); d=n/30
    vf="scale=1210:2150,crop=1080:1920:65:70," if i%2 else ""
    run(f'ffmpeg -v error -y -ss {a:.3f} -i {SRC} -an -vf "{vf}fps=30,format=yuv420p" -frames:v {n} -c:v libx264 -preset veryfast -crf 16 s{i}.mp4')
    run(f'ffmpeg -v error -y -i w.wav -af "atrim={a:.4f}:{a+d:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st={d-0.03:.4f}:d=0.03,apad,atrim=0:{d:.4f}" -c:a pcm_s16le s{i}.wav')
    vl.write(f"file s{i}.mp4\n"); al.write(f"file s{i}.wav\n"); log.append((a,b,t)); t+=d
vl.close(); al.close(); TOT=t
run('ffmpeg -v error -y -f concat -i v.txt -c copy vcat.mp4'); run('ffmpeg -v error -y -f concat -i a.txt -c copy acat.wav')
W=[]
for s,e,w in words:
    for a,b,tt in log:
        if a<=s<b: W.append((w.replace('"',''),tt+s-a)); break
W.sort(key=lambda x:x[1])
ch=[]; cur=[]
for w,s in W:
    cur.append((w,s))
    if w[-1] in ',.:' or len(cur)==3 or w.lower() in ('out','looks'): ch.append(cur); cur=[]
if cur: ch.append(cur)
CUES=[]
for i,c in enumerate(ch):
    a=c[0][1]; b=ch[i+1][0][1] if i+1<len(ch) else TOT-0.1
    CUES.append((" ".join(w for w,_ in c).upper(),a,min(b,a+2.2)))
KEYS={"LOVE.","SHORT","FUSE.","CALM,","STEADY.","HOME,","MILK,","BLOW","UP.","NOT","BRAIN","ALERT","SMOKE,","FIRE'S","UNDERNEATH.","FLARES,","WALK","OUT","10","MINUTES,","WASN'T","YOU.","MAYDAY.","SUBSCRIBE","SHARE,","UNIFORM."}
F='/usr/share/fonts/opentype/inter/Inter-Black.otf'; font=ImageFont.truetype(F,104)
ins=[]
for i,(txt,a,b) in enumerate(CUES):
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im)
    ws=txt.split(); lines=[]; cu=''
    for w in ws:
        tt=(cu+' '+w).strip()
        if d.textlength(tt,font=font)>880 and cu: lines.append(cu); cu=w
        else: cu=tt
    lines.append(cu); y=1400-len(lines)*58
    for L in lines:
        x=(1080-d.textlength(L,font=font))/2
        for w in L.split():
            col=(255,45,61) if w in KEYS else (255,255,255)
            d.text((x,y+6),w,font=font,fill=(0,0,0,160)); d.text((x,y),w,font=font,fill=col,stroke_width=3,stroke_fill=(0,0,0))
            x+=d.textlength(w+' ',font=font)
        y+=116
    im.save(f'cap{i}.png'); ins.append(f'-i cap{i}.png')
tag=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(tag)
f2=ImageFont.truetype(F,44); sub="DAY 16 · THE SHORT FUSE"; wbox=max(709,int(d.textlength(sub,font=f2))+88)
d.rectangle([83,205,83+wbox,205+190],fill=(200,16,46)); d.text((127,227),"MAYDAY",font=ImageFont.truetype(F,100),fill='white'); d.text((127,335),sub,font=f2,fill='white'); tag.save('tag.png')
fc='[0:v][1:v]overlay[v1];'; cur='[v1]'
for i,(t_,a,b) in enumerate(CUES):
    fc+=f"{cur}[{i+2}:v]overlay=enable='between(t,{a:.3f},{b:.3f})'[x{i}];"; cur=f'[x{i}]'
open('fc.txt','w').write(fc.rstrip(';'))
run('ffmpeg -v error -y -i vcat.mp4 -i tag.png '+' '.join(ins)+f' -filter_complex_script fc.txt -map "{cur}" -c:v libx264 -crf 17 -preset medium vcap.mp4')
run('ffmpeg -v error -y -i vcap.mp4 -i acat.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -movflags +faststart body.mp4')
json.dump({"log":log,"cues":CUES},open('plan.json','w'),indent=0)
print(TOT,len(CUES)); [print(f"{a:6.2f} {c}") for c,a,b in CUES]
