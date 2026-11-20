import sys, subprocess, os, shutil, numpy as np, onnxruntime as ort
from PIL import Image, ImageFilter
src,dst,off=sys.argv[1],sys.argv[2],int(sys.argv[3])
BG=[Image.open(f'sp_{q:02d}.png').convert('RGB') for q in range(30)]
d='mt_'+os.path.basename(src).split('.')[0]; shutil.rmtree(d,ignore_errors=True); os.makedirs(d,exist_ok=True)
subprocess.run(f'ffmpeg -v error -y -i {src} {d}/%04d.png',shell=True,check=True)
so=ort.SessionOptions(); so.intra_op_num_threads=4
s=ort.InferenceSession('u2netp.onnx',so,providers=['CPUExecutionProvider']); name=s.get_inputs()[0].name
mean=np.array([.485,.456,.406],dtype=np.float32); std=np.array([.229,.224,.225],dtype=np.float32); prev=None
for k,f in enumerate(sorted(os.listdir(d))):
    im=Image.open(f'{d}/{f}').convert('RGB')
    x=np.asarray(im.resize((320,320),Image.BILINEAR),dtype=np.float32)/255.0; x=((x-mean)/std).transpose(2,0,1)[None]
    o=s.run(None,{name:x})[0][0,0]; o=(o-o.min())/(o.max()-o.min()+1e-6)
    if prev is not None: o=0.6*o+0.4*prev
    prev=o
    m=Image.fromarray((np.clip((o-0.35)/0.3,0,1)*255).astype(np.uint8)).resize(im.size,Image.BILINEAR).filter(ImageFilter.GaussianBlur(3))
    Image.composite(im,BG[(off+k)%30],m).save(f'{d}/{f}')
subprocess.run(f'ffmpeg -v error -y -framerate 30 -i {d}/%04d.png -c:v libx264 -preset veryfast -crf 16 -pix_fmt yuv420p {dst}',shell=True,check=True)
