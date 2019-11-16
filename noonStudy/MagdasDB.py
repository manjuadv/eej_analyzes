import DbUtility as dbUtils
import DBread as dbRead
import pytz
from datetime import datetime

def getMinData(stationCode, year, month, day, targetTimeZone=pytz.UTC):
    targetDay = targetTimeZone.localize(datetime(int(year), int(month), int(day)))
    targetFileList = dbUtils.getExpectedFileNameList(stationData, stationCode, 'Min', year=year, month=month, day=day, targetTimeZone=targetTimeZone)
    dataFrame = dbRead.getData(targetFileList)
    if targetTimeZone == pytz.UTC :
        # Data in UTC times. So no time adjustment  needed. Return original value come from files
        return dataFrame
    else:
        # Target timezone is not UTC. 
        # Convert times in 'dataFrame' to local times based on provided timezone.
        # After this convertion data in dataFrame['Date_Time'] will be local times. But values in 'dataFrame' will be in UTC
        dataFrame = dbUtils.convertToTimezone(dataFrame, targetTimeZone)
        # Data collected from database contains data of previous OR next day (based on given timezone)
        # But local-midnight to local-midnight data should be constructed
        # Based on timezone (UTC+ or UTC-), data should be truncated to select data only within local-midnight to local-midnight
        timeZoneOffset = targetTimeZone.localize(datetime.now()).tzname()
        if timeZoneOffset[0]=='+':
            # Timezone is a UTC+ timezone. All data of previous day is already appended in 'dataFrame' list. 
            # Data before day start time (00:00 time of requested day) and data after day end time (00:00 time of requested day) 
            # should be truncated to select data only within local-midnight to local-midnight            
            dataFrame = dbUtils.truncateAdditionalData(dataFrame, targetDay.replace(hour=0,minute=0), targetDay.replace(hour=23,minute=59))
            return dataFrame
        elif timeZoneOffset[0]=='-':
            # Timezone is a UTC- timezone. All data of next day is already appended in 'dataFrame' list. 
            # Data before day start time (00:00 time of requested day) and data after day end time (00:00 time of requested day) 
            # should be truncated to select data only within local-midnight to local-midnight
            dataFrame = dbUtils.truncateAdditionalData(dataFrame, targetDay.replace(hour=0,minute=0), targetDay.replace(hour=23,minute=59))
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