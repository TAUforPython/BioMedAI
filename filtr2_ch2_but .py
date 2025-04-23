#исследование фильтров Чебышева и Баттерворта
# import required modules 
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.signal import iirfilter, freqs, bilinear, freqz
import math
#порядок фильтра
Nf=7
#частота дискретизации из edf файла
f_s=200
w_s=2*np.pi*f_s
#частота среза
fsr=1
#синтез аналогового прототипа фильтра Чебышева 2го типа
#заданного порядка
b,a=iirfilter(Nf,[2*np.pi*fsr],rs=40,
              btype='lowpass',analog=True,ftype='cheby2')
print(' a= ',a)
print(' b= ',b)
w,h = freqs(b,a)
#синтез фильтра высокого порядка
b1,a1=iirfilter(2*Nf+1,[2*np.pi*fsr],rs=40,
              btype='lowpass',analog=True,ftype='cheby2')
w1,h1 = freqs(b1,a1)
#синтез аналогового прототипа фильтра Батерворта
bb,ab=iirfilter(Nf,[2*np.pi*fsr],rs=40,
              btype='lowpass',analog=True,ftype='butter')
print(' ab= ',ab)
print(' bb= ',bb)
wb,hb = freqs(bb,ab)
#синтез фильтра высокого порядка
bb1,ab1=iirfilter(2*Nf+1,[2*np.pi*fsr],rs=40,
              btype='lowpass',analog=True,ftype='butter')
wb1,hb1 = freqs(bb1,ab1)
f=plt.figure()#чтобы сохранить график в нужном разрешении
plt.semilogx(w/(2*np.pi), 20*np.log10(abs(h)),'b-',label='ch2_'+str(Nf))
plt.semilogx(w1/(2*np.pi), 20*np.log10(abs(h1)),'b--',label='ch2_'+str(2*Nf+1))
plt.semilogx(wb/(2*np.pi), 20*np.log10(abs(hb)),'r-',label='butt_'+str(Nf))
plt.semilogx(wb1/(2*np.pi), 20*np.log10(abs(hb1)),'r--',label='butt_'+str(2*Nf+1))
plt.semilogx(fsr, -40,'bo',label='all ch2')
plt.semilogx(fsr, -3,'ro',label='all butt')
plt.xscale('log') 
plt.title('filter frequency response') 
plt.xlabel('Frequency [Hz]') 
plt.ylabel('Amplitude [dB]') 
plt.margins(0, 0.1) 
plt.grid(which='both', axis='both')
plt.xlim([0.1,10.0])
plt.ylim([-90.0,10.0])
plt.legend(loc='best')#легенду в хорошее место
plt.show()
f.savefig('fig1',dpi=300.0)#сохранение графика с dpi 300)

