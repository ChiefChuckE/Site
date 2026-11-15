import subprocess,json
def run(c): subprocess.run(c,shell=True,check=True)
# loudness-match each source's audio first
SRC={"O":"raw15out.mp4","I":"raw15.mp4"}
VOFF={"O":0.091995,"I":0.688005}  # audio stream start_time: video media time = wav/ASR time + offset
SEG=[("O",4.78,6.52),("O",6.70,7.40),("O",8.10,8.84),("O",10.54,11.68),("O",11.92,12.84),("O",13.76,14.78),("O",15.68,17.22),("O",17.88,19.24),("O",19.78,21.28),("O",21.56,22.78),("O",23.06,24.28),("O",24.66,26.14),
("I",27.88,29.02),("I",29.74,32.20),("I",32.70,34.18),("I",34.32,35.76),
("O",38.52,43.70),
("I",39.84,41.80),("I",42.62,43.86),("I",44.08,45.14),("I",48.16,50.02),("I",50.10,51.76),("I",52.36,55.70),("I",56.82,59.20)]
vl=open("v.txt","w");al=open("a.txt","w");t=0;log=[]
for i,(k,a,b) in enumerate(SEG):
    d=b-a;n=round(d*30);d=n/30
    vf="hflip,"+("scale=1166:2074,crop=1080:1920:43:40," if i%2 else "")
    run(f'ffmpeg -v error -y -ss {a+VOFF[k]:.3f} -i {SRC[k]} -an -vf "{vf}fps=30,format=yuv420p" -frames:v {n} -c:v libx264 -preset veryfast -crf 16 s{i}.mp4')
    run(f'ffmpeg -v error -y -i a_{k}.wav -af "atrim={a:.4f}:{a+d:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={d-0.03:.4f}:d=0.03,apad,atrim=0:{d:.4f}" -c:a pcm_s16le s{i}.wav')
    vl.write(f"file s{i}.mp4\n");al.write(f"file s{i}.wav\n");log.append((k,a,b,t));t+=d
L=len(SEG)-1
run(f'ffmpeg -v error -y -sseof -0.04 -i s{L}.mp4 -frames:v 1 last.png')
run('ffmpeg -v error -y -loop 1 -i last.png -vf "scale=1080:1920,fps=30,format=yuv420p" -frames:v 30 -c:v libx264 -preset veryfast -crf 16 pad.mp4')
run('ffmpeg -v error -y -f lavfi -i anullsrc=r=48000:cl=stereo -t 1 -c:a pcm_s16le pad.wav')
vl.write("file pad.mp4\n");al.write("file pad.wav\n");vl.close();al.close()
run('ffmpeg -v error -y -f concat -i v.txt -c copy vcat.mp4')
run('ffmpeg -v error -y -f concat -i a.txt -c copy acat.wav')
json.dump(log,open("seglog.json","w"));print(t)
for x in log: print(x[0],x[1],x[2],round(x[3],3))
