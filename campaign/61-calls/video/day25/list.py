from PIL import Image, ImageDraw, ImageFont
import random
random.seed(7)
W,H=2550,3300
im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im)
for y in range(520,H-100,190): d.line([0,y,W,y],fill=(150,190,235),width=5)
d.line([330,0,330,H],fill=(235,120,120),width=6)
G=lambda s:ImageFont.truetype('GloriaHallelujah.ttf',s); M=lambda s:ImageFont.truetype('PermanentMarker-Regular.ttf',s)
INK=(25,35,120)
def put(x,y,t,f,fill=INK,ang=None):
    ang=random.uniform(-1.6,1.6) if ang is None else ang
    w=int(d.textlength(t,font=f))+60; h=f.size*2
    L=Image.new('RGBA',(w,h),(0,0,0,0)); ImageDraw.Draw(L).text((20,h//4),t,font=f,fill=fill)
    L=L.rotate(ang,expand=True,resample=Image.BICUBIC); im.paste(L,(x,y-h//4),L); return w
put(420,130,"PTSD Thanksgiving",M(210),(20,20,20),-2)
d.line([430,420,2150,395],fill=(20,20,20),width=14)
items=["coffee  (the BIG one)","paper towels  (lots)","antacid","earplugs  (uncle)","chicken  (already cooked)","wine","a good night's sleep","my mind ??"]
y=560
for i,t in enumerate(items):
    yy=y+i*190
    d.rectangle([390,yy+20,480,yy+110],outline=INK,width=8)
    w=put(540+random.randint(-10,15),yy-45,t,G(120))
    if t=="wine":
        d.line([520,yy+75,560+w,yy+55],fill=(200,20,20),width=16); d.line([525,yy+95,550+w,yy+78],fill=(200,20,20),width=12)
        put(1050,yy-30,"NOPE. not this year.",M(100),(200,20,20),3)
    if t.startswith("a good"): put(1750,yy+70,"sold out!",M(90),(200,20,20),-6)
    if t.startswith("my mind"): put(1350,yy-20,"check lost + found",M(90),(200,20,20),4)
    if False: d.line([400,yy+60,430,yy+100],fill=(20,20,20),width=12); d.line([430,yy+100,500,yy-10],fill=(20,20,20),width=12)
y0=y+8*190+60
put(420,y0,"the REAL list:",M(130),(20,20,20),-1.5)
for j,t in enumerate(["seat by the door","walk after dinner","text ONE person","ok to leave early"]):
    put(520,y0+185+j*158-45,"*  "+t,G(118))
d.ellipse([560,H-255,2000,H-35],outline=(200,20,20),width=16)
put(700,H-240,"call or text 988",M(125),(200,20,20),-1)
im.save('MAYDAY-Day-25-shopping-list.pdf',resolution=300); im.resize((510,660)).save('lprev.jpg')
