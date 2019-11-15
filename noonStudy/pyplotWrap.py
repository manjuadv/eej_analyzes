import matplotlib.pyplot as plt

def dialyCompMaxAndNoon(timeSet, dataSet, componentName):
    from astroplan import Observer
    import astropy.units as u
    from astropy.time import Time
    import pytz
    import datetime
    import matplotlib.dates as mdates

    localTZ = pytz.timezone('Asia/Colombo')
    localTimeSet = [pytz.UTC.localize(x) for x in timeSet]
    timesInLocalTZ = [x.astimezone(localTZ) for x in localTimeSet]
    lastRecordIndex = len(timeSet) - 1

    subaru = Observer(longitude=80.07*u.deg, latitude=6.97*u.deg, elevation=0*u.m, name="Subaru", 
    timezone="Asia/Colombo")
    noonTimeInTimeObj = subaru.noon(Time(timeSet[lastRecordIndex]), which='previous')

    noonTimeUTC = noonTimeInTimeObj.to_datetime(timezone = pytz.timezone('UTC'))
    print('Local noon time (utc) : ' + noonTimeUTC.strftime('%Y-%m-%d %H:%M:%S %z'))
    noonTime = noonTimeUTC.astimezone(localTZ)
    print('Local noon time (local time zone) : ' + noonTime.strftime('%Y-%m-%d %H:%M:%S %z'))
    sunRiseTime = subaru.sun_rise_time(noonTimeInTimeObj, which="previous").to_datetime(localTZ)
    sunSetTime = subaru.sun_set_time(noonTimeInTimeObj, which='next').to_datetime(localTZ)
    noonTimeIndex, sunRiseIndex, sunSetIndex = getSunEventTimeIndexes(timesInLocalTZ, noonTime, sunRiseTime, sunSetTime)
    print('Sun rise time (local time zone) : ' + sunRiseTime.strftime('%Y-%m-%d %H:%M:%S %z'))
    print('Sun set time (local time zone) : ' + sunSetTime.strftime('%Y-%m-%d %H:%M:%S %z'))

    maxInx,minInx = getLocalMaxIndex(dataSet)
    print('max value : ' + str(dataSet[maxInx]) + ', at : '+ timesInLocalTZ[maxInx].strftime('%Y-%m-%d %H:%M:%S %z'))

    yAxisMiddle = dataSet[minInx] + ((dataSet[maxInx] - dataSet[minInx]) / 2)

    fig, ax = plt.subplots()
    ax.plot(timesInLocalTZ, dataSet, label= componentName + ' Comp')
    ax.axvline(x=noonTime, ls='--', c='orange')
    yAxesMin, yAxesMax = ax.get_ylim()
    ax.axvline(x=sunRiseTime, ymax= ((dataSet[sunRiseIndex] - yAxesMin) / (yAxesMax - yAxesMin)), ls='--', c='gray')
    ax.axvline(x=sunSetTime, ymax= ((dataSet[sunSetIndex] - yAxesMin) / (yAxesMax - yAxesMin)), ls='--', c='gray')
    ax.text(noonTime, yAxisMiddle, 'Local noon', rotation=90, ha='left', va='center')
    ax.text(sunRiseTime, yAxesMin + ((dataSet[sunRiseIndex] - yAxesMin) / 2) , 'Sun rise', rotation=90, ha='left', va='center')
    ax.text(sunSetTime, yAxesMin + ((dataSet[sunSetIndex] - yAxesMin) / 2) , 'Sun set', rotation=90, ha='left', va='center')
    hours = mdates.HourLocator(interval = 1)
    h_fmt = mdates.DateFormatter('%d %H:%M:%S', localTZ)
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(h_fmt)

    limMin = noonTime.replace(hour=0, minute=0, second=0, microsecond=0).astimezone(localTZ)
    limMax = noonTime.replace(hour=23, minute=59, second=0, microsecond=0).astimezone(localTZ)
    ax.axvline(x=timesInLocalTZ[maxInx], ls='--', c='green')
    ax.text(timesInLocalTZ[maxInx], yAxisMiddle, 'Max value', rotation=90, ha='left', va='center')

    timeMinutesBetWeenPeakAndNoon = (noonTime - timesInLocalTZ[maxInx]).total_seconds()/60
    print('Noon and peak time diff in minutes (HH:MM) : {:3.0f}'.format(timeMinutesBetWeenPeakAndNoon) + ' minutes ({:1.0f}'.format(timeMinutesBetWeenPeakAndNoon//60) + ':{:.0f}'.format(timeMinutesBetWeenPeakAndNoon%60) + ')')
    
    ax.annotate('', xy=(timesInLocalTZ[maxInx], dataSet[maxInx]), xytext=(noonTime, dataSet[maxInx]), 
    xycoords='data', textcoords='data', arrowprops={'arrowstyle': '<->'})
    ax.annotate('{:1.0f}mins'.format(timeMinutesBetWeenPeakAndNoon), xy=((timesInLocalTZ[maxInx] + datetime.timedelta(minutes=(timeMinutesBetWeenPeakAndNoon/2))), dataSet[maxInx]), ha='center', va='bottom')

    peakAndNoonDiff = dataSet[maxInx] - dataSet[noonTimeIndex]
    ax.annotate('', xy=(timesInLocalTZ[noonTimeIndex + 10], dataSet[maxInx]), xytext=(timesInLocalTZ[noonTimeIndex + 10], dataSet[noonTimeIndex]), 
    xycoords='data', textcoords='data', arrowprops={'arrowstyle': '<->'})
    ax.annotate('{:1.0f} nT'.format(peakAndNoonDiff), xy=(timesInLocalTZ[noonTimeIndex + 15], dataSet[maxInx] - peakAndNoonDiff/2), ha='left', va='center', rotation=90)
    print('Difference between peak and noon time value : {:1.0f}'.format(peakAndNoonDiff))

    plt.xlabel('Time (hours)')
    plt.xticks( rotation= 90 )
    plt.ylabel(componentName + ' Component (nT)')
    plt.xlim(limMin, limMax)
    plt.legend()
    plt.show()

def getLocalMaxIndex(valueSet):
    maxInx = -1
    minInx = -1
    maxVal = -9999999
    minVal = 9999999
    for i, x in enumerate(valueSet):
        if x > maxVal:
            maxInx = i
            maxVal = x
        if x < minVal:
            minInx = i
            minVal = x
    return maxInx, minInx

def getSunEventTimeIndexes(timeSet, noonTime, sunRise, sunSet): 
    noonIndex = -1
    sunRiseIndex = -1
    sunSetIndex = -1
    for i, x in enumerate(timeSet):
        if x.day == noonTime.day and x.hour == noonTime.hour and x.minute == noonTime.minute:
            noonIndex = i
        if x > noonTime:
            sunRiseIndex = i
        if x > noonTime:
            sunSetIndex = i
    return noonIndex, sunRiseIndex, sunSetIndex