from os import path
import pytz
from datetime import datetime, timedelta

def printStationList():
    print('List of stations feeded in to DB')
    print('---------------------------------')
    for s in stationList:
        print(s + '\t : ' + stationList[s])

def getFileListForYear(stationCode, year, targetTimeZone=pytz.UTC):
    expectedFileList = getExpectedFileNameList(stationCode, targetTimeZone, year)
    return expectedFileList

def getFileListForMonth(stationCode, year, month, targetTimeZone=pytz.UTC):
    expectedFileList = getExpectedFileNameList(stationCode, targetTimeZone, year, month=month)
    return expectedFileList

def getFileListForDay(stationCode, year, month, day, targetTimeZone=pytz.UTC):
    expectedFileList = getExpectedFileNameList(stationCode, targetTimeZone, year, month=month, day=day)
    return expectedFileList

def getExpectedFileNameList(stationCode, targetTimeZone, year, month=None, day=None):
    stationDBPath = getStationDBPath(stationCode)
    if not stationDBPath:
        return []
    else:
        print('Data is reading for the station [' + stationCode + ']' + ' from path "' + stationDBPath + '"')
        filePath = stationList[stationCode] + '\\' + minOrSecDB + '\\' + year + '\\'
        timeZoneOffeset = targetTimeZone.localize(datetime.now()).tzname()
        if targetTimeZone == pytz.UTC :
            print('Requested time zone = ' + timeZoneOffeset + ' (default)')
            if not month and not day :
                # file list for year
                print('Generating file list for year ' + year + '. No extra file append needed (since UTC).')
                pass
            elif (len(month)>0) and not day:
                # file list for month
                print('Generating file list for month ' + year + '-' + month + '. No extra file append needed (since UTC).')
                pass
            else:
                # file list for day
                targetDay = datetime(int(year), int(month), int(day))
                targetDayFile = filePath + getDayFileName(stationCode, targetDay)
                fileList = [targetDayFile]
                return fileList
        else:
            print('Requested time zone = ' + timeZoneOffeset)
            if not month and not day :
                # file list for year
                print('Generating file list for month ' + year + '. Extra file append needed.')
                pass
            elif (len(month)>0) and not day:
                # file list for month
                print('Generating file list for month ' + year + '-' + month + '. Extra file append needed')
                pass
            else:
                # file list for day
                if timeZoneOffeset[0]=='+':
                    # append previous day
                    print('Generating file list for month ' + year + '-' + month + '-' + day +'. Previous day file appending.')
                    targetDay = datetime(int(year), int(month), int(day))
                    targetDayFile = filePath + getDayFileName(stationCode, targetDay)
                    previousDay = targetDay - timedelta(days=1)
                    targetPreviousDayFile = filePath + getDayFileName(stationCode, previousDay)
                    fileList = [targetPreviousDayFile, targetDayFile]
                    return fileList
                elif timeZoneOffeset[0]=='-':
                    # append next day
                    print('Generating file list for month ' + year + '-' + month + '-' + day +'. Next day file appending.')
                    targetDay = datetime(int(year), int(month), int(day))
                    targetDayFile = filePath + getDayFileName(stationCode, targetDay)
                    nextDay = targetDay + timedelta(days=1)
                    targetNextDayFile = filePath + getDayFileName(stationCode, nextDay)
                    fileList = [targetDayFile, targetNextDayFile]
                    return fileList

def getDayFileName(stationCode, day):
    dayFileName = stationCode + day.strftime('%Y%m%d') + 'pmin.min'
    return dayFileName

def getStationDBPath(stationCode):
    try:
        stationFilePath = stationList[stationCode] + '\\' + minOrSecDB + '\\'
    except :
        print('Requested stations are not in the system. Following station are only feeded.')
        printStationList()
        return ''

    if not stationCode:
        print('Please provide a valid station code')
        return ''
    elif not stationCode in stationList:
        print('Requested stations are not in the system. Following station are only feeded.')
        printStationList()
        return ''
    elif not path.exists(stationFilePath):
        print('Data files are not in the expected path "' + stationFilePath + '"')
        return ''
    return stationFilePath

# For any station to be used with this python program, it should be listed below with the path to the base folder of station's file list
stationList = {'CMB' : 'C:\\Data\\Study\\Post Grad\\MAGDAS\\MAGDAS data\\CMB_MAGDAS_IAGA_1s_1m\\CMB',
'DAV' : 'C:\\Data\\Study\\Post Grad\\MAGDAS\\MAGDAS data\\DAV_MAGDAS_IAGA_1s_1m\\DAV'}
minOrSecDB = 'Min' # 'Sec' (For one second resolution DB)