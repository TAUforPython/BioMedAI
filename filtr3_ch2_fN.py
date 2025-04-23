# import required modules 
import numpy as np 
import matplotlib.pyplot as plt
import scipy
#from scipy import signal
from scipy.signal import iirfilter, freqs, bilinear, freqz
import math
#порядок фильтра
Nf=7
#частота дискретизации из edf файла
f_s=200
w_s=2*np.pi*f_s
#частота среза
fsr=0.8#синтез аналогового прототипа фильтра Чебышева 2го типа
wsr=2*np.pi*fsr
b,a=iirfilter(Nf,[wsr],rs=40,
              btype='lowpass',analog=True,ftype='cheby2')
print(' a= ',a)
print(' b= ',b)
#билинейное преобразование
fsb=f_s
bz,az=bilinear(b,a,fsb)#,f_s)
print(' az= ',az)
print(' bz= ',bz)
w,h = freqs(b,a)
wz,hz = freqz(bz,az,worN=2**13,fs=fsb)
#результат
f=plt.figure()#чтобы сохранить график в нужном разрешении
plt.semilogx(w/(2*np.pi), 20*np.log10(abs(h)),'b-',label='analog')
plt.semilogx(wz, 20*np.log10(abs(hz)),'r.',label='digital')
plt.xscale('log') 
plt.title('filter frequency response') 
plt.xlabel('Frequency [Hz]') 
plt.ylabel('Amplitude [dB]') 
#plt.margins(0, 0.1) 
plt.grid(which='both', axis='both')
#plt.xlim([0.1,10.0])
#plt.ylim([-90.0,10.0])
plt.legend(loc='best')
plt.show()

f.savefig('fig1',dpi=300.0)#сохранение графика с dpi 300
