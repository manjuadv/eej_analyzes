import magnetic as mag
from os import path

def readDayDataLocalTime(targetFileList, comp):
    import numpy as np
    #dayFiles = glob.glob('*' + (year + month + day) + '*')
    # filePath = stationList[stCode] + '\\' + minOrSecDB + '\\' + year + '\\'
     
    # previousDay = datetime.datetime.strptime(year + '-'  + month + '-' + day, '%Y-%m-%d') - datetime.timedelta(days=1)
    # previousDayStr = previousDay.strftime('%Y%m%d')

    #dayFiles = [path.basename(x) for x in glob.glob(filePath + '*' + (year + month + day) + '*') or glob.glob(filePath + '*' + (previousDayStr) + '*')]
 
    dayFiles = targetFileList
    boolFistFileOK = False
    boolSecondFileOk = False
    if path.exists(dayFiles[0]):
        boolFistFileOK = True
    if path.exists(dayFiles[1]):
        boolSecondFileOk = True
    
    if boolFistFileOK and boolSecondFileOk :
        print("File count : " + str(len(dayFiles)))
    elif boolFistFileOK :
        print("Only file '" + dayFiles[0] + "' exists")
    elif boolSecondFileOk :
        print("Only file '" + dayFiles[1] + "' exists")
    else:
        print("Data files not exist")
        return [[],[]]

    timeSet = []
    dataSet = {"h":[],"d":[],"z":[],"f":[]}
    for fileName in dayFiles :
        print(fileName)
        ReadObj = mag.IAGA2002()
        ReadObj.read(fileName)
        print(ReadObj.get('f'))
        timeSet = np.append(timeSet,ReadObj.get(ReadObj.datetime_index))
        if len(comp) == 1:
            dataSet[comp] = np.append(dataSet[comp],ReadObj.get(comp))
        else:
            for c in comp:
                dataSet[c] = np.append(dataSet[c],ReadObj.get(c))
    return [timeSet, dataSet]