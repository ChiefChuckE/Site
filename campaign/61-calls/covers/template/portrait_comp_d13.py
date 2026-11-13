from PIL import Image, ImageFilter
src=Image.open('/tmp/claude-0/cov/d13/r2qr.png').convert('RGB')
W,H=1080,1920
# background: smoky region stretched + blurred
bg=src.crop((0,0,640,400)).resize((W,H)).filter(ImageFilter.GaussianBlur(6))
# bed scene bottom
bed=src.crop((0,400,600,720)); s=W/600; bed=bed.resize((W,int(320*s)))
by=H-bed.height
m=Image.linear_gradient('L').resize(bed.size)  # 0 top ->255 bottom
m=m.point(lambda v: min(255,int(v*3.5)))
bg.paste(bed,(0,by),m)
# Chuck
ch=src.crop((620,0,1280,720)); sc=1.4; ch=ch.resize((int(660*sc),int(720*sc)))
cx=540-int((945-620)*sc); cy=470
mk=Image.new('L',ch.size,255)
from PIL import ImageDraw
d=ImageDraw.Draw(mk)
fade=90
for i in range(fade):  # bottom fade
    d.line([(0,ch.height-1-i),(ch.width,ch.height-1-i)],fill=int(255*i/fade))
# side fades
side=Image.linear_gradient('L').rotate(90,expand=True).resize((70,ch.height))  # left->right?
for x in range(70):
    a=int(255*x/70)
    for y in range(0,ch.height,1): pass
L=Image.new('L',ch.size,255); ld=ImageDraw.Draw(L)
for x in range(70):
    ld.line([(x,0),(x,ch.height)],fill=int(255*x/70)); ld.line([(ch.width-1-x,0),(ch.width-1-x,ch.height)],fill=int(255*x/70))
from PIL import ImageChops
mk=ImageChops.multiply(mk,L)
T=Image.new('L',ch.size,255); td=ImageDraw.Draw(T)
for i in range(80): td.line([(0,i),(ch.width,i)],fill=int(255*i/80))
mk=ImageChops.multiply(mk,T)
bg.paste(ch,(cx,cy),mk)
print('chuck',cx,cy,ch.size,'qr bottom',cy+int(655*sc),'bed top',by,'detector y',by+int((490-400)*s))
bg.save('base_p.png')
