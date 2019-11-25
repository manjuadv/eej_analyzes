import matplotlib.pyplot as plt

def dailyVariationAnalyzes(dataFrame, componentName, outliers):
    from astroplan import Observer
    import astropy.units as u
    from astropy.time import Time
    import pytz
    import datetime
    import matplotlib.dates as mdates
    import numpy as np
    import math

    dayDateTimeObj = dataFrame['Date_Time'][0] # just get one of elements from 'Date_Time' list. Will be used to for certian calculations
    localTZ = dayDateTimeObj.tzinfo
    subaru = Observer(longitude=80.07*u.deg, latitude=6.97*u.deg, elevation=0*u.m, name="Subaru", 
    timezone=localTZ)

    noonTimeUTC = subaru.noon(Time(dayDateTimeObj), which='next').to_datetime(pytz.timezone('UTC'))
    print('Local noon time (utc) : ' + noonTimeUTC.strftime('%Y-%m-%d %H:%M:%S %z'))
    noonTimeLocal = subaru.noon(Time(dayDateTimeObj), which='next').to_datetime(localTZ)
    print('Local noon time (local time zone) : ' + noonTimeLocal.strftime('%Y-%m-%d %H:%M:%S %z'))
    sunRiseTimeLocal = subaru.sun_rise_time(Time(dayDateTimeObj), which="next").to_datetime(localTZ)
    sunRiseTimeLocalTwilight = subaru.sun_rise_time(Time(dayDateTimeObj), which="next", horizon=-6*u.deg).to_datetime(localTZ)
    sunSetTimeLocal = subaru.sun_set_time(Time(dayDateTimeObj), which='next').to_datetime(localTZ)    
    print('Sun rise time (local time zone) : ' + sunRiseTimeLocal.strftime('%Y-%m-%d %H:%M:%S %z'))
    print('Sun set time (local time zone) : ' + sunSetTimeLocal.strftime('%Y-%m-%d %H:%M:%S %z'))


    fig, ax = plt.subplots()
    ax.plot(dataFrame['Date_Time'], dataFrame[componentName], label= componentName + ' Comp')
    hours = mdates.HourLocator(interval = 1)
    h_fmt = mdates.DateFormatter('%d %H:%M:%S', localTZ)
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(h_fmt)
    
    y_min, y_max = ax.get_ylim()
    outliers[componentName] = y_min
    kw = dict(marker='o', linestyle='none', color='r', alpha=0.3)
    #ax.plot(outliers[componentName] , label= 'Outlier values', **kw)

    minValueIndex = dataFrame[componentName].idxmin() 
    maxValueIndex = dataFrame[componentName].idxmax()
    print('Max value : ' + str(dataFrame.loc[maxValueIndex][componentName]) + ', at : '
    + dataFrame.loc[maxValueIndex]['Date_Time'].strftime('%Y-%m-%d %H:%M:%S %z'))
    print('Min value : ' + str(dataFrame.loc[minValueIndex][componentName]) + ', at : '
    + dataFrame.loc[minValueIndex]['Date_Time'].strftime('%Y-%m-%d %H:%M:%S %z'))

    yAxisMiddle = dataFrame.loc[minValueIndex][componentName] + ((dataFrame.loc[maxValueIndex][componentName] 
    - dataFrame.loc[minValueIndex][componentName]) / 2)

    noonTimeRow = dataFrame[(dataFrame['Date_Time'] == noonTimeLocal.replace(second=0, microsecond=0))]
    print('Noon time value of ' + componentName + '-Component {:6.3f}'.format(noonTimeRow[componentName][0]))
    ax.axvline(x=noonTimeRow['Date_Time'][0], ls='--', c='orange')
    ax.text(noonTimeRow['Date_Time'][0], yAxisMiddle, 'Local noon', rotation=90, ha='left', va='center')
    ax.axvline(x=sunRiseTimeLocal, ls='--', c='gray')
    ax.axvline(x=sunRiseTimeLocalTwilight, ls='--', c='gray')
    ax.text(sunRiseTimeLocal, dataFrame.loc[minValueIndex][componentName], 'Sun rise', rotation=90, ha='left', va='bottom')
    ax.axvline(x=sunSetTimeLocal, ls='--', c='gray')    
    ax.text(sunSetTimeLocal, dataFrame.loc[minValueIndex][componentName], 'Sun set', rotation=90, ha='left', va='bottom')

    ax.axvline(x=dataFrame.loc[maxValueIndex]['Date_Time'], ls='--', c='green')
    ax.text(dataFrame.loc[maxValueIndex]['Date_Time'], yAxisMiddle, 'Max value', rotation=90, ha='left', va='center')

    timeMinutesBetWeenPeakAndNoon = (noonTimeRow['Date_Time'][0] - dataFrame.loc[maxValueIndex]['Date_Time']).total_seconds()/60
    print('Noon and peak time diff in minutes (HH:MM) : {:3.0f}'.format(timeMinutesBetWeenPeakAndNoon) 
    + ' minutes ({:1.0f}'.format(timeMinutesBetWeenPeakAndNoon//60) + ':{:.0f}'.format(timeMinutesBetWeenPeakAndNoon%60) + ')')
    ax.annotate('', xy=(dataFrame.loc[maxValueIndex]['Date_Time'], dataFrame.loc[maxValueIndex][componentName]), 
    xytext=(noonTimeRow['Date_Time'][0], dataFrame.loc[maxValueIndex][componentName]), 
    xycoords='data', textcoords='data', arrowprops={'arrowstyle': '<->'})
    ax.annotate('{:1.0f}mins'.format(timeMinutesBetWeenPeakAndNoon), xy=((dataFrame.loc[maxValueIndex]['Date_Time'] 
    + datetime.timedelta(minutes=(timeMinutesBetWeenPeakAndNoon/2))), dataFrame.loc[maxValueIndex][componentName]), ha='center', va='bottom')

    peakAndNoonDiff = dataFrame.loc[maxValueIndex][componentName] - noonTimeRow[componentName][0]
    print(peakAndNoonDiff)
    if peakAndNoonDiff > 0:
        print('Difference between peak and noon time value : {:1.0f}'.format(peakAndNoonDiff))
        ax.annotate('', xy=(noonTimeRow['Date_Time'][0] + datetime.timedelta(minutes=15), dataFrame.loc[maxValueIndex][componentName]),
        xytext=(noonTimeRow['Date_Time'][0] + datetime.timedelta(minutes=15), noonTimeRow[componentName][0]),
        xycoords='data', textcoords='data', arrowprops={'arrowstyle': '<->'})
        ax.annotate('{:1.0f} nT'.format(peakAndNoonDiff), xy=(noonTimeRow['Date_Time'][0] + datetime.timedelta(minutes=20), 
        dataFrame.loc[maxValueIndex][componentName] - peakAndNoonDiff/2), ha='left', va='center', rotation=90)

    sunRiseTimeRow = dataFrame[(dataFrame['Date_Time'] == sunRiseTimeLocal.replace(second=0, microsecond=0))]
    timeMinutesBetWeenPeakAndSunRise = (dataFrame.loc[maxValueIndex]['Date_Time'] - sunRiseTimeRow['Date_Time'][0]).total_seconds()/60
    print('Sun rise and peak time diff in minutes (HH:MM) : {:3.0f}'.format(timeMinutesBetWeenPeakAndSunRise) 
    + ' minutes ({:1.0f}'.format(timeMinutesBetWeenPeakAndSunRise//60) + ':{:.0f}'.format(timeMinutesBetWeenPeakAndSunRise%60) + ')')
    ax.annotate('', xy=(dataFrame.loc[maxValueIndex]['Date_Time'], dataFrame.loc[minValueIndex][componentName]), 
    xytext=(sunRiseTimeRow['Date_Time'][0], dataFrame.loc[minValueIndex][componentName]), 
    xycoords='data', textcoords='data', arrowprops={'arrowstyle': '<->'})
    ax.annotate('{:1.0f}mins'.format(timeMinutesBetWeenPeakAndSunRise), xy=((dataFrame.loc[maxValueIndex]['Date_Time'] 
    - datetime.timedelta(minutes=(timeMinutesBetWeenPeakAndSunRise/2))), dataFrame.loc[minValueIndex][componentName]), ha='center', va='bottom')

    sunRiseToPeakDiff = dataFrame.loc[maxValueIndex][componentName] - sunRiseTimeRow[componentName][0]
    print(sunRiseToPeakDiff)
    if not math.isnan(sunRiseToPeakDiff):
        print('Difference between sun rise value to peak : {:1.0f}'.format(sunRiseToPeakDiff))
        ax.annotate('', xy=(sunRiseTimeRow['Date_Time'][0] + datetime.timedelta(minutes=15), dataFrame.loc[maxValueIndex][componentName]), 
        xytext=(sunRiseTimeRow['Date_Time'][0] + datetime.timedelta(minutes=15), sunRiseTimeRow[componentName][0]), 
        xycoords='data', textcoords='data', arrowprops={'arrowstyle': '<->'})
        ax.annotate('{:1.0f} nT'.format(sunRiseToPeakDiff), xy=(sunRiseTimeRow['Date_Time'][0] + datetime.timedelta(minutes=20), 
        dataFrame.loc[maxValueIndex][componentName] - sunRiseToPeakDiff/2), ha='left', va='center', rotation=90)

    plt.xlabel('Time (hours)')
    plt.title('Geomagnetic field ' + componentName + '-component daily variation of ' + noonTimeLocal.strftime('%Y-%m-%d'),loc='center')
    plt.xticks( rotation= 90 )
    plt.ylabel(componentName + ' Component (nT)')
    plt.legend()
    plt.show()

def montly_peak_noon_gap_variatoin(data_frame, comp_name, outliers):

    from astroplan import Observer
    import astropy.units as u
    from astropy.time import Time
    import pytz
    from datetime import timedelta, date

    start_date = data_frame['Date_Time'][0].replace(minute=0, second=0)
    end_date = data_frame['Date_Time'][len(data_frame.index) - 1].replace(minute=0, second=0)

    localTZ = data_frame['Date_Time'][0].tzinfo
    subaru = Observer(longitude=80.07*u.deg, latitude=6.97*u.deg, elevation=0*u.m, name="Subaru", timezone=localTZ)

    for single_date in daterange(start_date, end_date):
        noonTimeUTC = subaru.noon(Time(single_date), which='next').to_datetime(pytz.timezone('UTC'))
        print('Local noon time (utc) : ' + noonTimeUTC.strftime('%Y-%m-%d %H:%M:%S %z'))
        noonTimeLocal = subaru.noon(Time(single_date), which='next').to_datetime(localTZ)
        print('Local noon time (local time zone) : ' + noonTimeLocal.strftime('%Y-%m-%d %H:%M:%S %z'))

        noonTimeRow = data_frame[(data_frame['Date_Time'] == noonTimeLocal.replace(second=0, microsecond=0))]
        #df.loc[(df['column_name'] >= A) & (df['column_name'] <= B)]
        maxValueIndex = get_max_value_index_in_range(data_frame, comp_name, single_date.replace(hour=0, minute=0,second=0), single_date.replace(hour=23, minute=59,second=0))#data_frame.loc[(data_frame['Date_Time']>single_date.replace(hour=0, minute=0,second=0)) & (data_frame['Date_Time']<single_date.replace(hour=23, minute=59,second=0))].max()
        print(maxValueIndex)
        print(data_frame.loc[maxValueIndex])
        print('Max value : ' + str(data_frame.loc[maxValueIndex][comp_name]) + ', at : '
        + data_frame.loc[maxValueIndex]['Date_Time'].strftime('%Y-%m-%d %H:%M:%S %z'))
        peakAndNoonDiff = data_frame.loc[maxValueIndex][comp_name] - noonTimeRow[comp_name][0]
        print('Difference between peak and noon time value : {:1.0f}'.format(peakAndNoonDiff))

def get_max_value_index_in_range(data_frame, comp, time_r_begin, time_r_end):
    max = -100000
    max_index = None
    range_started = False
    for index, row in data_frame.iterrows():
        if row['Date_Time'] > time_r_begin:
            range_started = True
        elif range_started and row['Date_Time'] > time_r_end:
            range_started = False
            return max_index
        
        if range_started and row[comp]>max:
            max_index = index
        
    return max_index
            

def daterange(start_date, end_date):
    from datetime import timedelta
    for n in range(int ((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)

def getMinMaxIndex(valueSet):
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




