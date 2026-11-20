import sys, subprocess, numpy as np, onnxruntime as ort
from PIL import Image, ImageFilter
src,vs,n,dst=sys.argv[1],float(sys.argv[2]),int(sys.argv[3]),sys.argv[4]
W,H=1080,1920
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
r=np.sqrt(((xx-W/2)/(W*0.75))**2+((yy-H*0.45)/(H*0.55))**2)
g=np.clip(26-22*r,4,26)
BG=np.stack([g,g,g*1.15],-1).astype(np.float32)
so=ort.SessionOptions(); so.intra_op_num_threads=2
s=ort.InferenceSession('u2netp.onnx',so,providers=['CPUExecutionProvider']); name=s.get_inputs()[0].name
mean=np.array([.485,.456,.406],dtype=np.float32); std=np.array([.229,.224,.225],dtype=np.float32)
rd=subprocess.Popen(f'ffmpeg -v error -ss {vs} -i {src}.mov -map 0:v:0 -an -vf scale={W}:{H}:flags=lanczos,fps=30 -frames:v {n} -f rawvideo -pix_fmt rgb24 -',shell=True,stdout=subprocess.PIPE)
wr=subprocess.Popen(f'ffmpeg -v error -y -f rawvideo -pix_fmt rgb24 -s {W}x{H} -r 30 -i - -c:v libx264 -preset veryfast -crf 14 -pix_fmt yuv420p {dst}',shell=True,stdin=subprocess.PIPE)
prev=None; k=0
while True:
    b=rd.stdout.read(W*H*3)
    if len(b)<W*H*3: break
    fr=np.frombuffer(b,dtype=np.uint8).reshape(H,W,3)
    x=np.asarray(Image.fromarray(fr).resize((320,320),Image.BILINEAR),dtype=np.float32)/255.0; x=((x-mean)/std).transpose(2,0,1)[None]
    o=s.run(None,{name:x})[0][0,0]; o=(o-o.min())/(o.max()-o.min()+1e-6)
    if prev is not None: o=0.6*o+0.4*prev
    prev=o
    m=Image.fromarray((np.clip((o-0.35)/0.3,0,1)*255).astype(np.uint8)).resize((W,H),Image.BILINEAR).filter(ImageFilter.GaussianBlur(3))
    a=(np.asarray(m,dtype=np.float32)/255.0)[...,None]
    out=(fr.astype(np.float32)*a+BG*(1-a)).astype(np.uint8)
    wr.stdin.write(out.tobytes()); k+=1
wr.stdin.close(); wr.wait(); print('done',dst,k)
