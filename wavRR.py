#библиотеки

from tkinter import *
from tkinter import filedialog #работа с файлами
from tkinter import simpledialog #для ввода
from tkinter.messagebox import showinfo #сообщения
#это для графиков
import matplotlib.pyplot as plt
from math import pi as pi
import math

#root = Tk()
#диалог открытия файла
fid = filedialog.askopenfilename()
with open(fid,'rb') as f:
    #HEADER
    vers = float(f.read(8))#номер версии файла
    patientID = f.read(80).decode('utf-8')#ID пациента
    patientID = patientID.strip()#обрезание пробелов в начале и конце
    recordID = f.read(80).decode('utf-8')#ID записи
    recordID = recordID.strip()#обрезание пробелов в начале и конце
    startdate = f.read(8).decode('utf-8')#дата начала записи (dd.mm.yy)
    startdate = startdate.strip()#обрезание пробелов в начале и конце
    starttime = f.read(8).decode('utf-8')#время начала записи (hh.mm.ss)
    starttime = starttime.strip()#обрезание пробелов в начале и конце
    numBytes = int(f.read(8))#число байт
    reserved = f.read(44).decode('utf-8')#зарезервировано
    reserved = reserved.strip()#обрезание пробелов в начале и конце
    numRec = int(f.read(8))#число записей
    duration = float(f.read(8))#длительность записи
    ns = int(f.read(4))#число сигналов
    #создаётся пустой список меток
    label = []
    for ii in range(ns):#чтение меток = ответвлений
        label.append(f.read(16).decode('utf-8'))#добавление в список
        label[ii] = label[ii].strip()#обрезание пробелов в начале и конце
    #создаётся пустой список преобразователей? что это?
    transducer = []
    for ii in range(ns):#чтение преобразователей
        transducer.append(f.read(80).decode('utf-8'))#добавление в список
    #единицы измерения (мВ, мкВ, любые другие)
    units = []
    for ii in range(ns):#чтение
        units.append(f.read(8).decode('utf-8'))#добавление в список
        units[ii] = units[ii].strip()#обрезание пробелов в начале и конце
    #минимальное значение
    physicalMin = []
    for ii in range(ns):#чтение
        physicalMin.append(float(f.read(8)))#добавление в список    
    #максимальное значение
    physicalMax = []
    for ii in range(ns):#чтение
        physicalMax.append(float(f.read(8)))#добавление в список 
    #минимальное значение в дискретах
    digitalMin = []
    for ii in range(ns):#чтение
        digitalMin.append(float(f.read(8)))#добавление в список    
    #максимальное значение в дискретах
    digitalMax = []
    for ii in range(ns):#чтение
        digitalMax.append(float(f.read(8)))#добавление в список
    #префильтр
    prefilter = []
    for ii in range(ns):#чтение
        prefilter.append(f.read(80).decode('utf-8'))#добавление в список
        prefilter[ii] = prefilter[ii].strip()#обрезание пробелов в начале и конце
    #отсчёты
    samples = []
    for ii in range(ns):#чтение
        samples.append(int(f.read(8)))#добавление в список
    #резервы сигналов
    reserv_ns = []
    for ii in range(ns):#чтение
        reserv_ns.append(f.read(32).decode('utf-8'))#добавление в список
        reserv_ns[ii] = reserv_ns[ii].strip()#обрезание пробелов в начале и конце
    #вычисление масштабного множителя для перевода дискрет в mV
    scalefac = []
    for ii in range(ns):
        sc_tmp = (physicalMax[ii] - physicalMin[ii])/(digitalMax[ii] - digitalMin[ii])
        scalefac.append(sc_tmp) 
    #постоянная составляющая - корректор нуля
    dc = []
    for ii in range(ns):
        dc_tmp = physicalMax[ii] - scalefac[ii]*digitalMax[ii]
        dc.append(dc_tmp) 
    #чтение данных:одно значение "целое со знаком" записано в 2 байта в порядке little
    #это когда последний байт знаковый. Соответственно этому задаются параметры метода
    #int.from_bytes - чтение 2 байт, byteorder='little',signed=True
    #ТУТ НУЖНО СДЕЛАТЬ ЦИКЛ ДЛЯ ВСЕХ СИГНАЛОВ    
    data_s = []
    for ii in range (samples[0]):
        data_tmp =  int.from_bytes(f.read(2),byteorder='little',signed=True)
        data_s.append(data_tmp*scalefac[0]+dc[0])
#ТУТ НУЖНО СДЕЛАТЬ ЦИКЛ ДЛЯ ВСЕХ СИГНАЛОВ

#задание диапазона индексов  для всей записи
xt = samples[0];
#построение обзорного графика
x=[]
for ii in range (xt):
    x.append(ii)

#построение графика 1-го сигнала
plt.plot(x, data_s,'b-', linewidth = 0.5,markersize=2)
plt.xlabel('индексы') #Подпись для оси х
plt.ylabel('экг') #Подпись для оси y
plt.title('экг') #Название
plt.grid(True)
plt.show()

#список диапазона индексов
#range_ind=[0,0]
#
root = Tk()
root.withdraw()
showinfo(title='цикл ввода диапазона индексов',
         message='ввод [нач.,кон.], выхода из цикла [0,0]')

#цикл ввода индексов
while True:
    root = Tk()
    root.withdraw()
    tmp_beg = int(simpledialog.askstring(title='',
                                  prompt='начальный индекс'))
    root = Tk()
    root.withdraw()
    tmp_end = int(simpledialog.askstring(title='',
                                  prompt='конечный индекс'))

    if tmp_beg >= tmp_end:
         break
    range_beg = tmp_beg
    range_end = tmp_end
    #построение обзорного графика
    x=[]
    for ii in range (range_beg,range_end):
        x.append(ii)
    
    #построение обзорного графика сигнала
    plt.plot(x, data_s[range_beg:range_end],'b-', linewidth = 0.5,markersize=2)
    plt.xlabel('индексы') #Подпись для оси х
    plt.ylabel('экг') #Подпись для оси y
    plt.title('экг') #Название
    plt.grid(True)
    plt.show()

#часть 2 - выделение QRS комплексов
#вейвлет
wav1=(0,-1,-2,0,6,0,-2,-1,0)#шляпа
wav2=(0,1,2,1,0,-1,-2,-1,0)#пила
wav3=(0,1.4,2,1.4,0,-1.4,-2,-1.4,0)#синус

x_wav=[]
for ii in range (9):
    x_wav.append(ii)

#применённые вейвлеты
plt.plot(x_wav, wav1,'b-', linewidth = 0.5,markersize=2)
plt.xlabel('индексы') #Подпись для оси х
plt.ylabel('w') #Подпись для оси y
plt.title('мексиканская шляпа') #Название
plt.grid(True)
plt.show()

plt.plot(x_wav, wav2,'b-', linewidth = 0.5,markersize=2)
plt.xlabel('индексы') #Подпись для оси х
plt.ylabel('w') #Подпись для оси y
plt.title('пила') #Название
plt.grid(True)
plt.show()

plt.plot(x_wav, wav3,'b-', linewidth = 0.5,markersize=2)
plt.xlabel('индексы') #Подпись для оси х
plt.ylabel('w') #Подпись для оси y
plt.title('синус') #Название
plt.grid(True)
plt.show()

#генерация свёрток и построение графиков
#пила
xs=[]
for ii in range (range_beg,range_end-len(wav2)):
    xs.append(ii)

ws=[]
for kk in range (range_beg,range_end-len(wav2)):
    integr=0
    for ii in range (len(wav2)):#размер wav2
        integr=integr+data_s[kk+ii]*wav2[ii]
    ws.append(integr)

#построение вейвлет-образа с пилой
plt.plot(xs, ws,'r.-',xs,data_s[range_beg:range_end-len(wav2)],'b.-',linewidth = 0.5,markersize=2)
plt.xlabel('индексы') #Подпись для оси х
plt.ylabel('F(t,tau)') #Подпись для оси y
plt.title('свёртка с пилой') #Название
plt.grid(True)
plt.show()

#шляпа
xs=[]
for ii in range (range_beg,range_end-len(wav1)):
    xs.append(ii)

ws=[]
for kk in range (range_beg,range_end-len(wav1)):
    integr=0
    for ii in range (len(wav3)):#размер wav1
        integr=integr+data_s[kk+ii]*wav1[ii]
    ws.append(integr)

#построение вейвлет-образа с шляпой
plt.plot(xs, ws,'r.-',xs,data_s[range_beg:range_end-len(wav1)],'b.-',linewidth = 0.5,markersize=2)
plt.xlabel('индексы') #Подпись для оси х
plt.ylabel('F(t,tau)') #Подпись для оси y
plt.title('свёртка с мексиканской шляпой') #Название
plt.grid(True)
plt.show()

#синус
xs=[]
for ii in range (range_beg,range_end-len(wav3)):
    xs.append(ii)

ws=[]
for kk in range (range_beg,range_end-len(wav3)):
    integr=0
    for ii in range (len(wav3)):#размер wav3
        integr=integr+data_s[kk+ii]*wav3[ii]
    ws.append(integr)

#построение вейвлет-образа
plt.plot(xs, ws,'r.-',xs,data_s[range_beg:range_end-len(wav3)],'b.-',linewidth = 0.5,markersize=2)
plt.xlabel('индексы') #Подпись для оси х
plt.ylabel('F(t,tau)') #Подпись для оси y
plt.title('свёртка с синусом') #Название
plt.grid(True)
plt.show()


#коррекция вейвлет-образа - обнуление всего что меньше порога
porog = 6
for ii in range (len(ws)):
    if ws[ii]-porog < 0 : ws[ii]=0
    else : ws[ii]=ws[ii]-porog

#графики свёртки и исходного сигнала
plt.plot(xs, ws,'r-',xs,data_s[range_beg:range_end-len(wav3)],'b.-',linewidth = 0.5,markersize=2)
plt.xlabel('индексы') #Подпись для оси х
plt.ylabel('y,F(t,tau)') #Подпись для оси y
plt.title('экг и свёртка с коррекцией') #Название
plt.grid(True)
plt.show()

#вычисление индексов R зубцов в отдельный список
indR=[]
yR=[]
kk=0 #счётчик indR
ii=1 #счётчик ws
tmp_max=0
flag=False

while ii <= len(ws)-1:
    if ws[ii]>tmp_max:#путь к максимуму
        tmp_max=ws[ii]
        flag=True
    else:#здесь начало падения, фиксация R
        if flag:
            indR.append(range_beg+ii) #коррекция вершины
            yR.append(0.6)#ординаты отображаемых точек R
            tmp_max=ws[ii]
            flag=False
            kk=kk+1
        else:tmp_max=ws[ii]#это путь к нулю
    ii=ii+1
#график исходного сигнала с отметками R зубцов
plt.plot(indR,yR,'+r',xs,data_s[range_beg:range_end-len(wav3)],'b-',linewidth = 0.5,markersize=5)
plt.xlabel('индексы') #Подпись для оси х
plt.ylabel('y,R-marker') #Подпись для оси y
plt.title('экг и R-маркеры') #Название
plt.grid(True)
plt.show()

#график изменения периода сердечных сокращений
deltaR=[]
xR=[]
ii=0;
while ii < len(indR)-1:
    deltaR.append(indR[ii+1]-indR[ii])
    xR.append(ii)
    ii=ii+1
plt.plot(xR,deltaR,'b-',linewidth = 0.5,markersize=3)
plt.xlabel('период №') #Подпись для оси х
plt.ylabel('длительность в отсчётах') #Подпись для оси y
plt.title('вариация периода сердцебиения') #Название
plt.grid(True)
plt.show()

