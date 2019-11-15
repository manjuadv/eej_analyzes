from os import path
import pytz
from datetime import datetime, timedelta

def getExpectedFileNameList(stationList, stationCode, minOrSecDB, year, month=None, day=None, targetTimeZone=pytz.UTC):
    stationDBPath = getStationDBPath(stationList, stationCode, minOrSecDB)
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

def getStationDBPath(stationList, stationCode, minOrSecDB):
    try:
        stationFilePath = stationList[stationCode] + '\\' + minOrSecDB + '\\'
    except Exception as e:
        print('Requested stations are not in the system. Following station are only feeded.')
        print(e)
        printStationList(stationList)
        return ''

    if not stationCode:
        print('Please provide a valid station code')
        return ''
    elif not stationCode in stationList:
        print('Requested stations are not in the system. Following station are only feeded.')
        printStationList(stationList)
        return ''
    elif not path.exists(stationFilePath):
        print('Data files are not in the expected path "' + stationFilePath + '"')
        return ''
    return stationFilePath

def printStationList(stationList):
    print('List of stations feeded in to DB')
    print('---------------------------------')
    for s in stationList:
        print(s + '\t : ' + stationList[s])

def truncateAdditionalData(dataFrame, targetStartTime, targetEndTime):
    print('Truncating to select data only within ' + targetStartTime.strftime('%Y-%m-%d %H:%M') + '-' + targetEndTime.strftime('%Y-%m-%d %H:%M'))
    truncatedDataFrame = dataFrame#['2016-03-06':'2016-03-07'].between_time('00:00','19:00')
    return truncatedDataFrame
