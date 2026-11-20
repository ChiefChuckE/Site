import numpy as np, wave
sr=48000; rg=np.random.default_rng(5)
def wsave(n,x):
    x=np.clip(x,-1,1); w=wave.open(n,'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((x*32767).astype(np.int16).tobytes()); w.close()
def lp(x,k): return np.convolve(x,np.ones(k)/k,'same')
def hp(x,k): return x-lp(x,k)
def T(d): return np.arange(int(sr*d))/sr
# --- effects
t=T(0.9); ch=np.zeros(len(t))
for s0 in (0.0,0.45):
    u=np.clip(t-s0,0,None); m=(t>=s0)&(t<s0+0.16)
    ch+=m*(np.sin(2*np.pi*3150*u)+0.5*np.sin(2*np.pi*6300*u))*np.minimum(u/0.003,1)*np.exp(-u*14)
wsave('chirp.wav',ch*0.7)
t=T(0.7); f=2200*np.exp(-t*5.5)*(1+0.6*np.sin(2*np.pi*10*t))+160; ph=2*np.pi*np.cumsum(f)/sr
sc=((2*((ph/(2*np.pi))%1)-1)*0.7+hp(rg.standard_normal(len(t)),8)*0.25)*np.minimum(t/0.01,1)*np.minimum((0.7-t)/0.05,1); wsave('scratch.wav',np.tanh(sc*1.6)*0.7)
t=T(0.5); n=rg.standard_normal(len(t)); sl=hp(lp(n,3),40)*np.exp(-t*60)*1.6+np.sin(2*np.pi*95*t)*np.exp(-t*22)*1.2+rg.standard_normal(len(t))*np.exp(-t*160)*0.9
wsave('slap.wav',np.tanh(sl*1.6)*0.9)
t=T(1.3); f=180*np.exp(t*2.6); ph=2*np.pi*np.cumsum(f)/sr; ri=(np.sin(ph)*0.35+hp(rg.standard_normal(len(t)),6)*0.5*(t/1.3))*(t/1.3)**1.6*np.minimum((1.3-t)/0.02,1); wsave('riser.wav',ri*0.8)
t=T(1.0); n=hp(rg.standard_normal(len(t)),5); cr=(rg.random(len(t))<0.004).astype(float); cr=lp(cr,30)*40
wsave('sizzle.wav',np.tanh((n*0.35*(0.4+0.6*np.minimum(t/0.1,1))*np.exp(-t*1.6)+cr*np.exp(-t*1.2)))*0.6)
t=T(1.5); hb=np.zeros(len(t))
for s0 in (0.0,0.22,0.75,0.97):
    u=np.clip(t-s0,0,None); hb+=(t>=s0)*np.sin(2*np.pi*(62-20*np.minimum(u,0.1)/0.1)*u)*np.exp(-u*14)*1.2
wsave('heart.wav',np.tanh(hb*1.3)*0.85)
t=T(1.6); dr=np.sin(2*np.pi*np.cumsum(46-10*(t/1.6))/sr)*np.exp(-t*1.5)*1.2+lp(rg.standard_normal(len(t)),60)*np.exp(-t*3)*3; wsave('drop.wav',np.tanh(dr*1.3)*0.9)
# --- music: hardcore beat
def hard(bars,bpm=140,intro_bars=0,seed=3):
    r=np.random.default_rng(seed); st=60/bpm/4; L=int(sr*st*16*bars)+sr; x=np.zeros(L)
    def at(buf,t0,sig,g=1.0):
        k=int(sr*t0); n=min(len(sig),len(buf)-k)
        if n>0: buf[k:k+n]+=sig[:n]*g
    tk=T(0.3); kick=np.sin(2*np.pi*np.cumsum(45+120*np.exp(-tk*30))/sr)*np.exp(-tk*11)*1.3
    tn=T(0.2); sn=(lp(r.standard_normal(len(tn)),2)*np.exp(-tn*28)*0.9+np.sin(2*np.pi*190*tn)*np.exp(-tn*30)*0.6)
    th=T(0.06); hat=hp(r.standard_normal(len(th)),6)*np.exp(-th*90)*0.45
    tb=T(0.6)
    def bass(f0,d):
        tt=T(d); f=f0*(1+0.25*np.exp(-tt*30)); return np.tanh(np.sin(2*np.pi*np.cumsum(f)/sr)*2.2)*np.minimum(tt/0.004,1)*np.minimum((d-tt)/0.03,1)*0.8
    def stab(f0,d):
        tt=T(d); w=sum(np.sign(np.sin(2*np.pi*f0*(1+dt)*tt))*0.2 for dt in (-0.004,0,0.005)); return lp(w,12)*np.exp(-tt*9)*0.7
    notes=[(0,6,55),(10,4,55),(14,2,65.4)]; riff=[(0,220),(3,261.6),(6,329.6),(8,440),(11,329.6),(14,261.6)]
    for b in range(bars):
        t0=b*st*16; full=b>=intro_bars
        for s_ in (0,6,10):
            if full or s_==0: at(x,t0+s_*st,kick,1.0)
        if full:
            for s_ in (4,12): at(x,t0+s_*st,sn,1.0)
        for s_ in range(0,16,2): at(x,t0+s_*st,hat,0.7 if s_%4 else 1.0)
        for s_,d,f in notes: at(x,t0+s_*st,bass(f,d*st),1.0)
        if full:
            for s_,f in riff: at(x,t0+s_*st,stab(f,0.3),0.8)
    return x
hd=hard(24,intro_bars=1); wsave('hard1.wav',np.tanh(hd*1.1)*0.8)
wsave('hard2.wav',np.tanh(hard(6,intro_bars=0,seed=7)*1.1)*0.8)
# --- music: piano bed
def piano(f0,d,vel=1.0):
    tt=T(d); x=np.zeros(len(tt)); dec=1.6+ (400/f0)*0.35
    for h,a in [(1,1),(2,0.55),(3,0.3),(4,0.18),(5,0.1),(6,0.06)]:
        fr=f0*h*np.sqrt(1+0.0004*h*h); x+=a*np.sin(2*np.pi*fr*tt+rg.uniform(0,6))*np.exp(-tt*dec*(0.8+0.25*h))
    x+=lp(rg.standard_normal(len(tt)),4)*np.exp(-tt*90)*0.15
    return x*np.minimum(tt/0.004,1)*vel*0.5
N={'A2':110,'F2':87.3,'C3':130.8,'G2':98,'E3':164.8,'A3':220,'C4':261.6,'E4':329.6,'F3':174.6,'G3':196,'B3':246.9,'D4':293.7,'G4':392,'D3':146.8,'F4':349.2,'A4':440,'C5':523.3,'E5':659.3}
chords=[['A2','E3','A3','C4','E4'],['F2','C3','F3','A3','C4'],['C3','G3','C4','E4','G4'],['G2','D3','G3','B3','D4']]
L=int(sr*30); pa=np.zeros(L); step=0.62; t0=0.0; q=0
while t0<26.5:
    ch_=chords[(q//5)%4]; nm=ch_[q%5]; sig=piano(N[nm],3.2,0.9+0.15*(q%5==0)); k=int(sr*t0); n=min(len(sig),L-k); pa[k:k+n]+=sig[:n]; t0+=step; q+=1
# pad swell on last chord (Am): from 17 s
tt=T(30)
for fq,a in [(110,0.5),(220,0.5),(261.6,0.35),(329.6,0.35),(440,0.2)]:
    env=np.clip((tt-16.0)/4.0,0,1)*np.clip((28.0-tt)/2.5,0,1); pa+=np.sin(2*np.pi*fq*tt+rg.uniform(0,6))*env*a*0.18
ir=T(2.2); ir=rg.standard_normal(len(ir))*np.exp(-ir*2.2); ir[:int(sr*0.02)]*=0.1; ir/=np.abs(ir).sum()**0.5*4
wet=np.convolve(pa,ir,'full')[:L]; pa=pa*0.75+wet*1.8; pa/=np.abs(pa).max(); wsave('sad.wav',pa*0.9)
print('ok')
