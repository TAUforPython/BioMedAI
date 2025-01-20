#библиотеки

#from tkinter import *
#from tkinter import filedialog #работа с файлами
#from tkinter import simpledialog #для ввода
#from tkinter.messagebox import showinfo #сообщения
#это для графиков
import matplotlib.pyplot as plt
from math import pi as pi
import math

#проба генерации образов положительной синус-полуволны

#задание диапазона индексов для полуволны, для симметрии нечётное число точек
x_len = 11
#генерация точек
y_sin=[]
x_sin=[]
for ii in range (x_len):
    x_sin.append(ii)
    y_sin.append(math.sin(pi*ii/(x_len-1)))

#вычисление площади полуволны
sq_w = 0
for ii in range(len(y_sin)-1):
    sq_w = sq_w + (y_sin[ii]+y_sin[ii+1])/2
#амплитуда минус-выбросов, каждый шириной 2 и площадью sq_w/2
a_neg = sq_w/2
#построение вейвлета
x_PT=[]
for ii in range (len(y_sin)+4):
    x_PT.append(ii+13)#13 задаёт смещение от 0 по Х
wavPT=[]
wavPT.append(0)
wavPT.append(-a_neg)
for ii in range (len(y_sin)):
    wavPT.append(y_sin[ii])
wavPT.append(-a_neg)
wavPT.append(0)
#график вейвлета
plt.plot(x_PT, wavPT,'b-', linewidth = 0.5,markersize=2)
plt.xlabel('индексы') #Подпись для оси х
plt.ylabel('вейвлет') #Подпись для оси y
plt.title('вейвлет РТ') #Название
plt.grid(True)
plt.show()

#моделирование с изолированной полуволной
y_mod_len = 7
#генерация точек
y_mod_sin=[]
for ii in range (y_mod_len):
    y_mod_sin.append(1.5*math.sin(pi*ii/(y_mod_len-1)))


y_mod=[]
for ii in range (len(wavPT)):
    y_mod.append(0.0)
for ii in range (len(y_mod_sin)):
    y_mod.append(y_mod_sin[ii])
for ii in range (len(wavPT)+5):
    y_mod.append(0.0)
x_mod=[]
for ii in range (len(y_mod)):
    x_mod.append(ii)

#генерация свёртки
range_beg=0
range_end=len(y_mod)
xs=[]
xsc=[]
for ii in range (range_beg,range_end-len(wavPT)):
    xs.append(ii)
    xsc.append(ii+math.floor(len(wavPT)/2))#смещение образа в индексах
#для совпадения максимумов
ws=[]
for kk in range (range_beg,range_end-len(wavPT)):
    integr=0
    for ii in range (len(wavPT)):#размер wavPT
        integr=integr+y_mod[kk+ii]*wavPT[ii]
    ws.append(integr)

#графики свёртки и исходного сигнала
plt.plot(x_PT, wavPT,'c-',xs,y_mod[range_beg:range_end-len(wavPT)],'b.-',xsc, ws,'r-*',linewidth = 0.5,markersize=2)
plt.grid(True)
plt.xlabel('индексы') #Подпись для оси х
plt.ylabel('отсчёты') #Подпись для оси y
plt.title('вейвлет-образ') #Название
plt.legend(['вейвлет','сигнал','вейвлет-образ'])
plt.show()

