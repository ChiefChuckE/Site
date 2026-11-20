import numpy as np, wave
from numpy.fft import rfft,irfft,rfftfreq
sr=48000; n=int(2.6*sr); t=np.arange(n)/sr
rng=np.random.default_rng(3)
def voice(f0,det):
    ph=2*np.pi*np.cumsum(f0*(1+det)*(1+0.004*np.sin(2*np.pi*5.2*t+rng.uniform(0,6.28)))*np.ones(n))/sr
    return sum(np.sin(k*ph)/k**1.1 for k in range(1,14))
x=np.zeros(n)
for f0 in (261.6,329.6,392.0,523.3,659.3):
    for det in (-0.004,0.0,0.004): x+=voice(f0,det)
S=rfft(x); fr=rfftfreq(n,1/sr)
form=np.exp(-((fr-750)/230)**2)+0.8*np.exp(-((fr-1150)/260)**2)+0.35*np.exp(-((fr-2700)/500)**2)+0.05
x=irfft(S*form,n)
env=np.minimum(1,t/0.55)**1.6*np.exp(-np.maximum(0,t-1.3)*2.6)
x*=env
# shimmer
for i,f in enumerate((1318.5,1568,2093,2637)):
    st=0.25+0.16*i; m=t>st; x+=0.06*np.sin(2*np.pi*f*t)*np.exp(-(t-st)*3.2)*m*np.abs(x).max()*3
# reverb
L=int(1.4*sr); ir=rng.standard_normal(L)*np.exp(-np.arange(L)/(0.4*sr)); ir[0]=0
from numpy.fft import fft,ifft
N=n+L; y=np.real(ifft(fft(x,N)*fft(ir,N)))[:n]; x=x+0.5*y/np.abs(y).max()*np.abs(x).max()
x=x/np.abs(x).max()*0.9
w=wave.open('choir.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((x*32767).astype(np.int16).tobytes()); w.close(); print('ok')
