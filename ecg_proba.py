#библиотеки

from ecg_edf_read import ecg_read
from tkinter import filedialog #работа с файлами

import numpy as np 
import matplotlib.pyplot as plt 
import scipy.signal #import iirfilter, freqs, bilinear, freqz
from scipy.signal import iirfilter, freqs, bilinear, freqz
import math

#диалог открытия файла
fid = filedialog.askopenfilename()

[ns,samples,duration,data_s,units,label,startdate,starttime,patientID]= ecg_read(fid)

#задание диапазона индексов  для всей записи
xt = samples[0];
#построение обзорного графика
x=[]
for ii in range (xt):
    x.append(ii)

#построение графика 1-го сигнала
#plt.plot(x, data_s[0],'b-', linewidth = 0.5,markersize=2)
#plt.plot(x, data_s[1],'r-', linewidth = 0.5,markersize=2)
#plt.plot(x, data_s[2],'m-', linewidth = 0.5,markersize=2)
#plt.xlabel('индексы') #Подпись для оси х
#plt.ylabel(units[0]) #Подпись для оси y
#plt.title(label[0]) #Название
#plt.grid(True)
#plt.legend(label)
#plt.show()

#синтез фильтра
#порядок фильтра
Nf=7
#частота дискретизации из edf файла
f_s=samples[0]/duration
print(' частота дискретизации= ',f_s)
#w_s=2*np.pi*f_s
#частота среза
fsr=1
#синтез аналогового прототипа фильтра Чебышева 2го типа
wsr=2*np.pi*fsr
b,a=iirfilter(Nf,[wsr],rs=40,
              btype='highpass',analog=True,ftype='cheby2')
print(' a= ',a)
print(' b= ',b)
#билинейное преобразование
fsb=f_s
bz,az=bilinear(b,a,fsb)#,f_s)
print(' az= ',az)
print(' bz= ',bz)
#w,h = freqs(b,a)
#wz,hz = freqz(bz,az,worN=2**13,fs=fsb)
#фильтрация
#прогон сначала до конца
data_lfilter = scipy.signal.lfilter(bz, az, data_s[0])
#прогон с реверсом начало-конец-начало, исправляет фазовые сдвиги
data_ff = scipy.signal.filtfilt(bz, az, data_s[0])
#построение графика фильтрованного 1-го сигнала
f=plt.figure()#чтобы сохранить график в нужном разрешении
plt.plot(x, data_s[0],'c-.', linewidth = 0.5,label='data')
plt.plot(x, data_lfilter,'b--', linewidth = 0.5,label='beg-end')
plt.plot(x, data_ff,'r-', linewidth = 0.5,label='beg-end-beg')
#plt.plot(x, data_s[1],'r-', linewidth = 0.5,markersize=2)
#plt.plot(x, data_s[2],'m-', linewidth = 0.5,markersize=2)
plt.xlabel('индексы') #Подпись для оси х
plt.ylabel(units[0]) #Подпись для оси y
plt.title(label[0]) #Название
plt.grid(True)
plt.legend(loc='best')
plt.show()

f.savefig('fig1',dpi=300.0)#сохранение графика с dpi 300s

f=plt.figure()#чтобы сохранить график в нужном разрешении
plt.plot(x, data_s[0],'c--', linewidth = 0.5,label='data')
plt.plot(x, data_s[0]-data_ff,'r-', linewidth = 0.5,label='corr.data')
#plt.plot(x, data_s[1],'r-', linewidth = 0.5,markersize=2)
#plt.plot(x, data_s[2],'m-', linewidth = 0.5,markersize=2)
plt.xlabel('индексы') #Подпись для оси х
plt.ylabel(units[0]) #Подпись для оси y
plt.title(label[0]) #Название
plt.grid(True)
plt.legend(loc='best')
plt.show()

f.savefig('fig2',dpi=300.0)#сохранение графика с dpi 300s

f=plt.figure()#чтобы сохранить график в нужном разрешении
plt.plot(x, data_s[0],'c--', linewidth = 0.5,label='data')
plt.plot(x, data_ff,'r-', linewidth = 0.5,label='corr.data')
#plt.plot(x, data_s[1],'r-', linewidth = 0.5,markersize=2)
#plt.plot(x, data_s[2],'m-', linewidth = 0.5,markersize=2)
plt.xlabel('индексы') #Подпись для оси х
plt.ylabel(units[0]) #Подпись для оси y
plt.title(label[0]) #Название
plt.grid(True)
plt.legend(loc='best')
plt.show()

f.savefig('fig3',dpi=300.0)#сохранение графика с dpi 300s



