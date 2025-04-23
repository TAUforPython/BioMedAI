#эта функция читает edf файл с именем file_path
#и возвращает следующую структуру в виде списка
#[ns, samples, duration, data_s,units, label, startdate, starttime, patientID]
#ns - число сигналов, samples - список чисел отсчетов в каждом сигнале,
#duration - продолжительность записи в секундах
#data_s - матрица размером ns x samples,в которой записаны отсчёты сигналов
#units - список ns строк с названиями единиц измерения отсчётов, например 'mV'
#label - список ns строк с названиями сигналов, например 'ECG V2-Ref'
#startdate - дата начала записи (dd.mm.yy)
#starttime - время начала записи (hh.mm.ss) 
#patientID - строка идентификатор пациента.
def ecg_read(file_path):

    with open(file_path,'rb') as f:
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

    #ЦИКЛ ДЛЯ ВСЕХ СИГНАЛОВ
        data_s=[]
        for ii in range(ns):
            data_s.append([])    
        for jj in range(ns):
            data_s[jj] = []
            for ii in range (samples[jj]):
                data_tmp =  int.from_bytes(f.read(2),byteorder='little',signed=True)
                data_s[jj].append(data_tmp*scalefac[jj]+dc[jj])
    #КОНЕЦ ЦИКЛА ДЛЯ ВСЕХ СИГНАЛОВ
    return([ns,samples,duration,data_s,units,label,startdate,starttime,patientID])


