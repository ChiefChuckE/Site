import subprocess, json, re
from PIL import Image, ImageDraw, ImageFont
def run(c): subprocess.run(c,shell=True,check=True)
SRC={"B":("../d15b/raw2.mp4",0.661),"A":("../d15b/raw.mp4",0.088)}
for k,(f,o) in SRC.items(): run(f'ffmpeg -v error -y -i {f} -vn -ac 2 -ar 48000 -af "highpass=f=80" w{k}.wav')
SEG=[("B",3.00,4.62),("B",5.00,5.48),("B",6.22,6.80),("B",7.60,9.50),("B",11.60,12.45),("B",13.76,15.75),("B",16.26,17.40),("B",17.90,19.05),("B",19.86,20.70),("B",21.14,22.00),("B",22.20,23.30),("B",23.74,25.10),("B",25.34,26.30),("B",27.14,30.05),("B",32.40,33.65),("B",33.98,35.20),("B",35.82,37.00),("B",37.32,38.70),("B",40.56,42.35),("B",42.80,44.00),("A",1.85,11.75)]
WORDS={"B":"""14 3120|days 3560|of 3800|hard 3880|stuff. 4180|Today, 5100|none. 6320|Day 7700|15, 7940|off 8780|duty. 9020|Here's 11700|your 11900|order. 12040|Do 13860|one 14140|thing 14440|you 15080|like. 15300|Not 16360|something 16560|useful, 16940|something 18000|you 18420|like. 18560|The 19960|game, 20140|a 21240|ride, 21400|a 22300|car 22440|show, 22820|a 23840|nap 23960|in 24220|the 24320|chair. 24500|Do 25440|nothing. 25680|If 27240|guilt 27400|shows 27640|up, 28020|that's 28560|the 28800|injury 28980|talking. 29420|Rest 32500|is 32759|not 32880|quitting. 33140|Rest 34080|is 34360|maintenance. 34540|You 35920|service 36060|the 36400|engine. 36500|You 37420|service 37560|your 37880|pistol. 38080|It's 40660|time 40840|to 41020|take 41160|care 41360|of 41520|yourself. 41620|You're 42900|allowed 43120|to. 43620""",
"A":"""This 1980|is 2100|day 2200|15 2380|of 2740|61. 3000|Subscribe 4220|to 4600|the 4680|channel, 4780|like, 5180|share, 5500|call 6540|your 6760|mayday, 6920|and 7640|send 7780|this 7960|to 8080|someone 8160|who 8400|wore 8520|the 8700|uniform, 8820|and 9900|please 10060|have 10320|a 10480|blessed 10560|Sunday. 10860"""}
vl=open('v.txt','w'); al=open('a.txt','w'); t=0; log=[]
for i,(k,a,b) in enumerate(SEG):
    f,o=SRC[k]; n=round((b-a)*30); d=n/30
    vf="scale=1210:2150,crop=1080:1920:65:70," if (i%2 and k=="B") else ""
    run(f'ffmpeg -v error -y -ss {a+o:.3f} -i {f} -an -vf "{vf}fps=30,format=yuv420p" -frames:v {n} -c:v libx264 -preset veryfast -crf 16 s{i}.mp4')
    run(f'ffmpeg -v error -y -i w{k}.wav -af "atrim={a:.4f}:{a+d:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st={d-0.03:.4f}:d=0.03,apad,atrim=0:{d:.4f}" -c:a pcm_s16le s{i}.wav')
    vl.write(f"file s{i}.mp4\n"); al.write(f"file s{i}.wav\n"); log.append((k,a,b,t)); t+=d
vl.close(); al.close(); TOT=t
run('ffmpeg -v error -y -f concat -i v.txt -c copy vcat.mp4'); run('ffmpeg -v error -y -f concat -i a.txt -c copy acat.wav')
# words on cut timeline
W=[]
for k,raw in WORDS.items():
    toks=[(x.rsplit(' ',1)[0],int(x.rsplit(' ',1)[1])/1000) for x in raw.split('|')]
    for j,(w,s) in enumerate(toks):
        for kk,a,b,tt in log:
            if kk==k and a<=s<b: W.append((w,tt+s-a)); break
W.sort(key=lambda x:x[1])
# chunks: max 3 words, break after punctuation
ch=[]; cur=[]
for w,s in W:
    cur.append((w,s))
    if w[-1] in ',.:' or len(cur)==3: ch.append(cur); cur=[]
if cur: ch.append(cur)
CUES=[]
for i,c in enumerate(ch):
    a=c[0][1]; b=ch[i+1][0][1] if i+1<len(ch) else TOT-0.1
    CUES.append((" ".join(w for w,_ in c).upper(),a,min(b,a+2.2)))
KEYS={"HARD","NONE.","OFF","ORDER.","LIKE.","USEFUL,","GAME,","RIDE,","CAR","SHOW,","NAP","NOTHING.","GUILT","INJURY","QUITTING.","MAINTENANCE.","ENGINE.","PISTOL.","YOURSELF.","ALLOWED","SUBSCRIBE","SHARE,","MAYDAY,","UNIFORM,","BLESSED","SUNDAY."}
F='/usr/share/fonts/opentype/inter/Inter-Black.otf'; font=ImageFont.truetype(F,104)
ins=[]
for i,(txt,a,b) in enumerate(CUES):
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im)
    words=txt.split(); lines=[]; cu=''
    for w in words:
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
d.rectangle([83,205,83+709,205+190],fill=(200,16,46)); d.text((127,227),"MAYDAY",font=ImageFont.truetype(F,100),fill='white'); d.text((127,335),"DAY 15 · OFF DUTY",font=ImageFont.truetype(F,44),fill='white'); tag.save('tag.png')
# B-roll: car show photo on "a car show, a nap in the chair. Do nothing." (segments 10-12)
bs=log[10][3]; be=log[13][3]; bd=be-bs
ph=Image.open('../d15b/carshow.jpg').convert('RGB'); ph.crop((218,0,1343,2000)).resize((1080,1920),Image.LANCZOS).save('photo.png')
nf=int(bd*30)
run(f'ffmpeg -v error -y -loop 1 -i photo.png -vf "zoompan=z=\'1+0.0010*on\':x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':d={nf}:s=1080x1920:fps=30,format=yuva420p,fade=t=in:st=0:d=0.2:alpha=1,fade=t=out:st={bd-0.25:.2f}:d=0.25:alpha=1" -frames:v {nf} -c:v qtrle broll.mov')
fc=f'[1:v]setpts=PTS+{bs:.3f}/TB[br];[0:v][br]overlay=eof_action=pass[v0];[v0][2:v]overlay[v1];'; cur='[v1]'
for i,(t_,a,b) in enumerate(CUES):
    fc+=f"{cur}[{i+3}:v]overlay=enable='between(t,{a:.3f},{b:.3f})'[x{i}];"; cur=f'[x{i}]'
open('fc.txt','w').write(fc.rstrip(';'))
run('ffmpeg -v error -y -i vcat.mp4 -i broll.mov -i tag.png '+' '.join(ins)+f' -filter_complex_script fc.txt -map "{cur}" -c:v libx264 -crf 17 -preset medium vcap.mp4')
run(f'ffmpeg -v error -y -i vcap.mp4 -i acat.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -movflags +faststart body.mp4')
json.dump({"log":log,"cues":CUES,"broll":[bs,be]},open('plan.json','w'),indent=0)
print(TOT, bs, be, len(CUES))
