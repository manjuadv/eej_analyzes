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
                import calendar as calendar

                fileList = []
                print('Generating file list for month ' + year + '-' + month + '. No extra file append needed (since UTC).')
                daysCountForMonth = calendar.monthrange(int(year), int(month))[1]
                for d in range(1, (daysCountForMonth + 1)):
                    fileList.append(filePath + getDayFileName(stationCode, datetime(int(year), int(month), d)))
                return fileList
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
                import calendar as calendar

                print('Generating file list for year ' + year + '. Extra file append needed.')
                
                if timeZoneOffeset[0]=='+':
                    # append previous day
                    print('Generating file list for year ' + year + '. Previous day file appending.')
                    firstDayOfYear = datetime(int(year), 1, 1)
                    previousDayOf1st = firstDayOfYear - timedelta(days=1)                    
                    previousDayOfFirstDayFile= filePath + getDayFileName(stationCode, previousDayOf1st)
                    fileList = [previousDayOfFirstDayFile]
                    for m in range(1, 13):                
                        daysCountForMonth = calendar.monthrange(int(year), m)[1]
                        for d in range(1, (daysCountForMonth + 1)):
                            fileList.append(filePath + getDayFileName(stationCode, datetime(int(year), m, d)))
                    return fileList
                elif timeZoneOffeset[0]=='-':
                    # append next day
                    print('Generating file list for year ' + year + '. Next day file appending.')
                    daysCountForMonth = calendar.monthrange(int(year), int(month))[1]
                    lastDayOfMonth = datetime(int(year), int(month), daysCountForMonth)
                    nextDayOfLast = lastDayOfMonth + timedelta(days=1)                    
                    nextDayOfLastFile= filePath + getDayFileName(stationCode, nextDayOfLast)
                    fileList = [nextDayOfLastFile]                    
                    for d in range(1, (daysCountForMonth + 1)):
                        fileList.append(filePath + getDayFileName(stationCode, datetime(int(year), int(month), d)))
                    return fileList
            elif (len(month)>0) and not day:
                # file list for month
                import calendar as calendar                
                
                if timeZoneOffeset[0]=='+':
                    # append previous day
                    print('Generating file list for month ' + year + '-' + month + '. Previous day file appending.')
                    firstDayOfMonth = datetime(int(year), int(month), 1)
                    previousDayOf1st = firstDayOfMonth - timedelta(days=1)                    
                    previousDayOfFirstDayFile= filePath + getDayFileName(stationCode, previousDayOf1st)
                    fileList = [previousDayOfFirstDayFile]
                    daysCountForMonth = calendar.monthrange(int(year), int(month))[1]
                    for d in range(1, (daysCountForMonth + 1)):
                        fileList.append(filePath + getDayFileName(stationCode, datetime(int(year), int(month), d)))
                    return fileList
                elif timeZoneOffeset[0]=='-':
                    # append next day
                    print('Generating file list for month ' + year + '-' + month + '. Next day file appending.')
                    daysCountForMonth = calendar.monthrange(int(year), int(month))[1]
                    lastDayOfMonth = datetime(int(year), int(month), daysCountForMonth)
                    nextDayOfLast = lastDayOfMonth + timedelta(days=1)                    
                    nextDayOfLastFile= filePath + getDayFileName(stationCode, nextDayOfLast)
                    fileList = [nextDayOfLastFile]                    
                    for d in range(1, (daysCountForMonth + 1)):
                        fileList.append(filePath + getDayFileName(stationCode, datetime(int(year), int(month), d)))
                    return fileList
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

def getEEIndexFileNameList(stationList, stationCode, minOrSecDB, year=None, targetTimeZone=pytz.UTC):
    stationDBPath = getStationDBPath(stationList, stationCode, minOrSecDB)
    if not stationDBPath:
        return []
    else:
        print('Data is reading for the station [' + stationCode + ']' + ' from path "' + stationDBPath + '"')
        filePath = stationList[stationCode] + '\\' + minOrSecDB + '\\' + year + '\\'
        timeZoneOffeset = targetTimeZone.localize(datetime.now()).tzname()
        if targetTimeZone == pytz.UTC :
            print('Requested time zone = ' + timeZoneOffeset + ' (default)')
            if year :
                # file list for year
                print('Generating file list for year ' + year + '. No extra file append needed (since UTC).')
                pass
            else :
                print('Generating file list from all data files.')
                pass
        else:
            print('Requested time zone = ' + timeZoneOffeset)
            if year :
                # file list for year
                import calendar as calendar

                print('Generating file list for year ' + year + '. Extra file append needed.')
                
                if timeZoneOffeset[0]=='+':
                    # append previous day
                    print('Generating file list for year ' + year + '. Previous day file appending.')
                    firstDayOfYear = datetime(int(year), 1, 1)
                    previousDayOf1st = firstDayOfYear - timedelta(days=1)                    
                    previousDayOfFirstDayFile= filePath + getDayFileName(stationCode, previousDayOf1st)
                    fileList = [previousDayOfFirstDayFile]
                    for m in range(1, 13):                
                        daysCountForMonth = calendar.monthrange(int(year), m)[1]
                        for d in range(1, (daysCountForMonth + 1)):
                            fileList.append(filePath + getDayFileName(stationCode, datetime(int(year), m, d)))
                    return fileList
                elif timeZoneOffeset[0]=='-':
                    # append next day
                    print('Generating file list for year ' + year + '. Next day file appending.')
                    lastDayOfYear = datetime(int(year), 12, 31)
                    nextDayOf31st = lastDayOfYear + timedelta(days=1)                    
                    for m in range(1, 13):                
                        daysCountForMonth = calendar.monthrange(int(year), m)[1]
                        for d in range(1, (daysCountForMonth + 1)):
                            fileList.append(filePath + getDayFileName(stationCode, datetime(int(year), m, d)))
                    fileList.append(filePath + getDayFileName(stationCode, nextDayOf31st))
                    return fileList
            else:
                print('Generating file list from all data files.')
                pass

def getDayFileName(stationCode, day):
    dayFileName =  '{0}{1}pmin.min'.format(stationCode, day.strftime('%Y%m%d'))
    return dayFileName
def getEEIndexDayFileName(stationCode, day):
    dayFileName = 'EEindex{0}p{1}.{2}'.format(day.strftime('%Y%m%d'),'min', stationCode)
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

def truncateAdditionalData(dataFrame, startTime, endTime):
    print('Truncating to select data only within ' + startTime.strftime('%Y-%m-%d %H:%M') + ' - ' + endTime.strftime('%Y-%m-%d %H:%M'))
    #truncatedDataFrame = dataFrame[startTime.strftime('%Y-%m-%d'):endTime.strftime('%Y-%m-%d')].between_time(startTime.strftime('%H:%M'),startTime.strftime('%H:%M'))
    result = dataFrame.loc[(dataFrame['Date_Time'] >= startTime) & (dataFrame['Date_Time'] <= endTime)]
    print('Truncation done')
    return result

def convertToTimezone(dataFrame, timezone):
    dataFrame['Date_Time'] = [x.astimezone(timezone) for x in dataFrame['Date_Time']]    
    return dataFrame
