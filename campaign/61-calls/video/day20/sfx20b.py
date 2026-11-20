import numpy as np, wave
sr=48000
def save(n,x):
    x=np.clip(x/ (np.abs(x).max()+1e-9)*0.95,-1,1); w=wave.open(n,'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((x*32767).astype(np.int16).tobytes()); w.close()
rng=np.random.default_rng(7)
# tire screech: noisy squeal gliding down, abrupt start, short tail
n=int(1.05*sr); t=np.arange(n)/sr
f=3200-1700*(t/1.05)**0.7+90*np.sin(2*np.pi*23*t)
ph=2*np.pi*np.cumsum(f)/sr
sq=np.sin(ph)+0.5*np.sin(2*ph)+0.3*np.sin(3*ph)
nz=rng.standard_normal(n); 
from numpy.fft import rfft,irfft
S=rfft(nz); fr=np.fft.rfftfreq(n,1/sr); S*=np.exp(-((fr-2400)/1400)**2); nz=irfft(S,n)
env=np.minimum(1,t/0.01)*np.exp(-np.maximum(0,t-0.75)*9)
x=(0.7*sq+0.9*nz/np.abs(nz).max())*env
save('screech.wav',x)
# rewind: tape whirr sweeping up with flutter + accelerating clock ticks, abrupt stop
n=int(1.5*sr); t=np.arange(n)/sr
f=250+2600*(t/1.5)**1.6
ph=2*np.pi*np.cumsum(f)/sr
w=np.sign(np.sin(ph))*0.5+np.sin(ph)*0.5
w*=0.6+0.4*np.sin(2*np.pi*(14+30*t/1.5)*t)
nz=rng.standard_normal(n); S=rfft(nz); fr=np.fft.rfftfreq(n,1/sr); S*=(fr>1500)*(fr<7000); nz=irfft(S,n); nz*=0.25*(t/1.5)
x=w*0.5*np.minimum(1,t/0.05)+nz
# ticks
tk=np.zeros(n); pos=0.0; rate=9.0
while pos<1.45:
    i=int(pos*sr); L=int(0.012*sr); tick=np.sin(2*np.pi*1900*np.arange(L)/sr)*np.exp(-np.arange(L)/(0.003*sr)); tk[i:i+L]+=tick[:max(0,min(L,n-i))]
    rate=9+31*(pos/1.5)**1.3; pos+=1/rate
x=x+0.6*tk/np.abs(tk).max()
x*=np.where(t>1.46,0,1)
save('rewind.wav',x)
print('ok')
