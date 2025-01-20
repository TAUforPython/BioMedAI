#библиотеки

#from tkinter import *
#from tkinter import filedialog #работа с файлами
#from tkinter import simpledialog #для ввода
#from tkinter.messagebox import showinfo #сообщения
#это для графиков
import matplotlib.pyplot as plt
from math import pi as pi
import math

#проба генерации образов синус-вейвлета
#синус-вейвлет
wavsin=(0,1.4,2,1.4,0,-1.4,-2,-1.4,0)
x_sin=(0,1,2,3,4,5,6,7,8)

#график вейвлета
plt.plot(x_sin, wavsin,'b-', linewidth = 0.5,markersize=2)
plt.xlabel('индексы') #Подпись для оси х
plt.ylabel('вейвлет') #Подпись для оси y
plt.title('синус-вейвлет') #Название
plt.grid(True)
plt.show()

#моделирование с изолированным QRS, по здоровой ЭКГ
#T(QRS)<=110 мс, дискретизация 5 мс, T(QRS)=22 интервала
#зубец R равен 6 интервалов, амплитуда R максимально
amR=2.5
#зубец Q равен 2 интервала, его амплитуда в минус
amQ=amR/4*0.5  #максимально R/4, может быть меньше
#зубец S равен 2 интервала, его амплитуда в минус
amS=amR/4*1.5  #максимально, может быть меньше

#генерация точек
y_mod=[]
#левый хвост
for ii in range(len(wavsin)+2):
    y_mod.append(0.0)
#Q
#y_mod.append(-amQ/2)
y_mod.append(-amQ)
#y_mod.append(-amQ/2)
y_mod.append(0.0)
#R
for ii in range (2):
    y_mod.append((ii+1)*amR/2)
for ii in range (2):
    y_mod.append((1-ii)*amR/2)
#S
#y_mod.append(-amS/2)
y_mod.append(-amS)
#y_mod.append(-amS/2)
y_mod.append(0.0)
#правый хвост
for ii in range(len(wavsin)+2):
    y_mod.append(0.0)

x_mod=[]
for ii in range (len(y_mod)):
    x_mod.append(ii)

plt.plot(x_mod, y_mod)
plt.xlabel('индексы') #Подпись для оси х
plt.ylabel('отсчёты') #Подпись для оси y
plt.title('Модель QRS') #Название
plt.grid(True)
plt.show()

#генерация свёртки
range_beg=0
range_end=len(y_mod)
xs=[]
xsc=[]
for ii in range (range_beg,range_end-len(wavsin)):
    xs.append(ii)
    xsc.append(ii+math.floor(len(wavsin)/2)-2)#смещение образа в индексах
#для совпадения максимумов
ws=[]
for kk in range (range_beg,range_end-len(wavsin)):
    integr=0
    for ii in range (len(wavsin)):#размер wavPT
        integr=integr+y_mod[kk+ii]*wavsin[ii]
    ws.append(integr)

#графики свёртки и исходного сигнала
plt.plot(x_sin, wavsin,'c-',xs,y_mod[range_beg:range_end-len(wavsin)],'b.-',xsc, ws,'r-*',linewidth = 0.5,markersize=2)
plt.grid(True)
plt.xlabel('индексы') #Подпись для оси х
plt.ylabel('отсчёты') #Подпись для оси y
plt.title('вейвлет-образ') #Название
plt.legend(['вейвлет','сигнал','вейвлет-образ'])
plt.show()

