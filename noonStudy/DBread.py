import magnetic as mag
from os import path

def getData(fileList):
    import pandas as pd
    import numpy as np
    filesFailed = []
    dataSet = {'Date_Time' : [],
            'H' : [], 'D' : [], 'Z' : [], 'F' : []}
    for fileName in fileList:
        if path.exists(fileName):  
            ReadObj = mag.IAGA2002()
            ReadObj.read(fileName)

            dataSet['Date_Time'] = np.append(dataSet['Date_Time'],ReadObj.get(ReadObj.datetime_index))
            dataSet['H'] = np.append(dataSet['H'],ReadObj.get('h'))
            dataSet['D'] = np.append(dataSet['D'],ReadObj.get('d'))
            dataSet['Z'] = np.append(dataSet['Z'],ReadObj.get('z'))
            dataSet['F'] = np.append(dataSet['F'],ReadObj.get('f'))
            print(fileName)
        else:
            filesFailed.append(fileName)
    
    if len(filesFailed) > 0:
        print ('Error : Following ' + str(len(filesFailed)) + ' file(s) expected to read, but not found.')
        for f in filesFailed:
            print('Error : data file "' + f + '" was not found')
    return pd.DataFrame(data=dataSet, index=dataSet['Date_Time'], columns=['Date_Time','H','D','Z','F'])