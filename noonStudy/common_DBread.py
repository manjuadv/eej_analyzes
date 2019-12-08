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
    dataFrame.drop_duplicates(inplace=True,keep='first')
    return dataFrame

def getEEIndex(fileList):
    import pandas as pd
    import numpy as np
    import pytz as pytz
    import os
    filesFailed = []
    data_frame_list = []
    for fileName in fileList:
        if path.exists(fileName):  
            # ReadObj = mag.IAGA2002()
            # ReadObj.read(fileName)

            # dataSet['Date_Time'] = np.append(dataSet['Date_Time'],[pytz.UTC.localize(x) for x in ReadObj.get(ReadObj.datetime_index)])
            # dataSet['EDst1h'] = np.append(dataSet['EDst1h'],ReadObj.get('EDst1h'))
            # dataSet['EDst6h'] = np.append(dataSet['EDst6h'],ReadObj.get('EDst6h'))
            # dataSet['ER'] = np.append(dataSet['ER'],ReadObj.get('ER'))
            # dataSet['EUEL'] = np.append(dataSet['EUEL'],ReadObj.get('EUEL'))
            # try:
            #     f = open(fileName, "r")
            #     for x in f:
            #         print(x)
            # except Exception as e:
            #     print('Error : Failed to read the file "{0}"'.format(fileName))
            #     print(e)
            # finally:
            #     f.close()

            ee_index_data_frame = pd.read_csv(fileName, index_col=False, skiprows=12, header=0, delim_whitespace=True, names=['DATE','TIME', 'DOY', 'EDst1h','EDst6h','ER','EUEL','|'])
            ee_index_data_frame.drop(columns='|', inplace=True)
            ee_index_data_frame['Date_Time'] = pd.to_datetime(ee_index_data_frame['DATE'] + ' ' + ee_index_data_frame['TIME'], format='%Y-%m-%d %H:%M:%S')
            ee_index_data_frame.Date_Time = ee_index_data_frame.Date_Time.dt.tz_localize('UTC')
            ee_index_data_frame.set_index('Date_Time', inplace=True)
            data_frame_list.append(ee_index_data_frame)
            #print(fileName + ' completed')
        else:
            filesFailed.append(fileName)
    data_frame_all = pd.concat(data_frame_list, axis=0)
    data_frame_all.sort_index(inplace=True)
    data_frame_all.drop_duplicates(inplace=True,keep='first')
    if len(filesFailed) > 0:
        print ('Error : Following ' + str(len(filesFailed)) + ' file(s) expected to read, but not found.')
        for f in filesFailed:
            print('Error : data file "' + f + '" was not found')

    # Construct pandas.DataFrame object from file data
    # In the pandas.DataFrame object, index always will be UTC time. 
    # This index (UTC time value) will used in all the complex operations like 'search items, find time which has minimum value'
    # If the data is converted to local time zone, 'Date_Time' column will have the local time (still index is in UTC)
    #dataFrame = pd.DataFrame(data=dataSet, index=dataSet['Date_Time'], columns=['Date_Time','EDst1h','EDst6h','ER','EUEL'])
    #dataFrame = fillMissingEntries(dataFrame)
    #dataFrame.sort_index(inplace=True)
    #dataFrame.drop_duplicates(inplace=True,keep='first')
    return data_frame_all
def fillMissingEntries(dataFrame):
    # This method supposed to fill missing entries (according to continues time flow)
    # This will help to identify if any data missing and will prevent generating incorrect graphs

    #TODO
    
    return dataFrame

def dateparse (datetime_str):  
    import datetime
    return datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S %z')