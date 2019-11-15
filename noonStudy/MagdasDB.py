import DbUtility as dbUtils
import DBread as dbRead
import pytz
from datetime import datetime

def getMinData(stationCode, year, month, day, targetTimeZone=pytz.UTC):
    targetFileList = dbUtils.getExpectedFileNameList(stationData, stationCode, 'Min', year=year, month=month, day=day, targetTimeZone=targetTimeZone)
    dataFrame = dbRead.getData(targetFileList)
    dataFrame = dbUtils.truncateAdditionalData(dataFrame, datetime.now(), datetime.now())
    return dataFrame

def getSecData(stationCode, year, month, day, targetTimeZone=pytz.UTC):
    targetFileList = dbUtils.getExpectedFileNameList(stationData, stationCode, 'Min', year=year, month=month, day=day, targetTimeZone=targetTimeZone)
    dataFrame = dbRead.getData(targetFileList)
    return dataFrame

def printStationList():
    dbUtils.printStationList(stationData)

# For any station to be used with this python program, it should be listed below with the path to the base folder of station's file list
stationData = {'CMB' : 'C:\\Data\\Study\\Post Grad\\MAGDAS\\MAGDAS data\\CMB_MAGDAS_IAGA_1s_1m\\CMB',
'DAV' : 'C:\\Data\\Study\\Post Grad\\MAGDAS\\MAGDAS data\\DAV_MAGDAS_IAGA_1s_1m\\DAV'}
minOrSecDB = 'Min' # 'Sec' (For one second resolution DB)