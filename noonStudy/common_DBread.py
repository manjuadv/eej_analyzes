import common_Magnetic as mag
from os import path

def getData(fileList):
    import pandas as pd
    import numpy as np
    import pytz as pytz
    filesFailed = []
    dataSet = {'Date_Time' : [],
            'H' : [], 'D' : [], 'Z' : [], 'F' : []}
    for fileName in fileList:
        if path.exists(fileName):  
            ReadObj = mag.IAGA2002()
            ReadObj.read(fileName)

            dataSet['Date_Time'] = np.append(dataSet['Date_Time'],[pytz.UTC.localize(x) for x in ReadObj.get(ReadObj.datetime_index)])
            dataSet['H'] = np.append(dataSet['H'],ReadObj.get('h'))
            dataSet['D'] = np.append(dataSet['D'],ReadObj.get('d'))
            dataSet['Z'] = np.append(dataSet['Z'],ReadObj.get('z'))
            dataSet['F'] = np.append(dataSet['F'],ReadObj.get('f'))
            #print(fileName + ' completed')
        else:
            filesFailed.append(fileName)
    
    if len(filesFailed) > 0:
        print ('Error : Following ' + str(len(filesFailed)) + ' file(s) expected to read, but not found.')
        for f in filesFailed:
            print('Error : data file "' + f + '" was not found')

    # Construct pandas.DataFrame object from file data
    # In the pandas.DataFrame object, index always will be UTC time. 
    # This index (UTC time value) will used in all the complex operations like 'search items, find time which has minimum value'
    # If the data is converted to local time zone, 'Date_Time' column will have the local time (still index is in UTC)
    dataFrame = pd.DataFrame(data=dataSet, index=dataSet['Date_Time'], columns=['Date_Time','H','D','Z','F'])
    dataFrame = fillMissingEntries(dataFrame)
    dataFrame.sort_index(inplace=True)
    return dataFrame

def fillMissingEntries(dataFrame):
    # This method supposed to fill missing entries (according to continues time flow)
    # This will help to identify if any data missing and will prevent generating incorrect graphs

    #TODO
    
    return dataFrame