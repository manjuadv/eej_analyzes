import matplotlib.pyplot as plt

def daily_graph(dataFrame, componentName, outliers=None):

    if dataFrame.empty:
        print('No data is available to plot')
        return

    from astroplan import Observer
    import astropy.units as u
    from astropy.time import Time
    import pytz
    import datetime
    import helper_astro as astro
    import matplotlib.dates as mdates

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
    if componentName=='D':
        ax.axhline(y=0, c='purple')
    hours = mdates.HourLocator(interval = 1)
    h_fmt = mdates.DateFormatter('%d %H:%M:%S', localTZ)
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(h_fmt)
    
    if outliers is not None:
        y_min, y_max = ax.get_ylim()
        outliers[componentName] = y_min
        kw = dict(marker='o', linestyle='none', color='r', alpha=0.3)
        ax.plot(outliers[componentName] , label= componentName + '-outlier', **kw)

    moon_phase = astro.moon_get_moon_phase(dataFrame['Date_Time'][0])
    t = ax.text(0.03, 0.9,'Lunar phase {:3.0f}%'.format(moon_phase * 100), horizontalalignment='left'
    , verticalalignment='center',transform=ax.transAxes)
    t.set_bbox(dict(facecolor='red', alpha=0.5, edgecolor='red'))

    minValueIndex = dataFrame[componentName].idxmin() 
    maxValueIndex = dataFrame[componentName].idxmax()
    #print(dataFrame.loc[maxValueIndex])

    print('Max value : ' + str(dataFrame.loc[maxValueIndex][componentName]) + ', at : '
    + dataFrame.loc[maxValueIndex]['Date_Time'].strftime('%Y-%m-%d %H:%M:%S %z'))
    print('Min value : ' + str(dataFrame.loc[minValueIndex][componentName]) + ', at : '
    + dataFrame.loc[minValueIndex]['Date_Time'].strftime('%Y-%m-%d %H:%M:%S %z'))

    yAxisMiddle = dataFrame.loc[minValueIndex][componentName] + ((dataFrame.loc[maxValueIndex][componentName] 
    - dataFrame.loc[minValueIndex][componentName]) / 2)

    noonTimeRow = dataFrame[(dataFrame['Date_Time'] == noonTimeLocal.replace(second=0, microsecond=0))]
    if not noonTimeRow.empty:
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

    plt.xlabel('Time (hours)')
    plt.xticks( rotation= 90 )
    plt.ylabel(componentName + ' Component (nT)')
    plt.legend()
    plt.title('Daily variation : Component ' + componentName + ' - ' + noonTimeLocal.strftime('%Y %B %d'))
    plt.show()

def monthly_graph(dataFrame, componentName, outliers=None):

    if dataFrame.empty:
        print('No data is available to plot')
        return

    print('Monthly graph is being generated.')
    #from astroplan import Observer
    #import astropy.units as u
    #from astropy.time import Time
    import pytz
    import datetime
    import matplotlib.dates as mdates
    import helper_astro as astro
    from datetime import datetime

    dayDateTimeObj = dataFrame['Date_Time'][0] # just get one of elements from 'Date_Time' list. Will be used to for certian calculations
    localTZ = dayDateTimeObj.tzinfo

    fig, ax = plt.subplots()
    ax.plot(dataFrame['Date_Time'], dataFrame[componentName], label= componentName + ' Comp')
    days = mdates.DayLocator(interval = 1)
    h_fmt = mdates.DateFormatter('%Y-%m-%d', localTZ)
    hours = mdates.HourLocator(interval = 4)
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(h_fmt)
    ax.xaxis.set_minor_locator(hours)
    #from matplotlib import ticker
    #ax.xaxis.set_minor_formatter(ticker.FuncFormatter(ticks_format))
    
    y_min, y_max = ax.get_ylim()
    
    if outliers is not None:
        outliers[componentName] = y_min
        kw = dict(marker='o', linestyle='none', color='r', alpha=0.3)
        ax.plot(outliers[componentName] , label= componentName + '-outlier', **kw)


    start_date = datetime(year=dataFrame['Date_Time'][0].year, month=dataFrame['Date_Time'][0].month, day=dataFrame['Date_Time'][0].day, tzinfo=localTZ)
    end_date_obj = dataFrame['Date_Time'][len(dataFrame['Date_Time']) - 1]
    end_date = datetime(year=end_date_obj.year, month=end_date_obj.month, day=end_date_obj.day, tzinfo=localTZ)
    moon_phases = astro.moon_get_moon_phase_range(start_date, end_date)
    moon_phases_data = []
    for index, row in dataFrame.iterrows():
        day_offset_from_start_date = (row['Date_Time'] - start_date).days
        phase = y_min + moon_phases[day_offset_from_start_date] * ((y_max - y_min) / 4)
        moon_phases_data.append(phase)
    ax.plot(dataFrame['Date_Time'], moon_phases_data, label= 'Moon phase')

    plt.xlabel('Time (days)')
    plt.xticks( rotation= 90 )
    plt.ylabel(componentName + ' Component (nT)')
    plt.legend()
    plt.title('Monthly variation : Component ' + componentName + ' - ' + dayDateTimeObj.strftime('%Y %B'))
    plt.show()

def ticks_format(value, index):
    import matplotlib.dates as mdates
    return (mdates.num2date(value).strftime('%H'))
def yearly_graph(dataFrame, componentName, outliers=None):

    import helper_astro as astro
    import pytz
    from datetime import datetime
    import matplotlib.dates as mdates

    if dataFrame.empty:
        print('No data is available to plot')
        return

    print('Yearly graph is being generated.')

    dayDateTimeObj = dataFrame['Date_Time'][0] # just get one of elements from 'Date_Time' list. Will be used to for certian calculations
    localTZ = dayDateTimeObj.tzinfo

    fig, ax = plt.subplots()
    ax.plot(dataFrame['Date_Time'], dataFrame[componentName], label= componentName + ' Comp')
    days = mdates.WeekdayLocator(interval = 1)
    h_fmt = mdates.DateFormatter('%Y-%m-%d', localTZ)
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(h_fmt)
    
    if outliers is not None:
        y_min, y_max = ax.get_ylim()
        outliers[componentName] = y_min
        kw = dict(marker='o', linestyle='none', color='r', alpha=0.3)
        ax.plot(outliers[componentName] , label= componentName + '-outlier', **kw)

    start_date = datetime(year=dataFrame['Date_Time'][0].year, month=dataFrame['Date_Time'][0].month, day=dataFrame['Date_Time'][0].day, tzinfo=localTZ)
    end_date_obj = dataFrame['Date_Time'][- 1]
    end_date = datetime(year=end_date_obj.year, month=end_date_obj.month, day=end_date_obj.day, tzinfo=localTZ)
    moon_phases = astro.moon_get_moon_phase_range_data_frame(start_date, end_date)
    # print(moon_phases)
    # moon_phases_data = []
    # for index, row in dataFrame.iterrows():
    #     day_offset_from_start_date = (row['Date_Time'] - start_date).days
    #     phase = y_min + (moon_phases[day_offset_from_start_date] * ((y_max - y_min) / 4))
    #     moon_phases_data.append(phase)
    moon_phases['Plot_val'] = y_min + (moon_phases['Phase'] * ((y_max - y_min) / 4))
    ax.plot(moon_phases.index.values, moon_phases['Plot_val'], label= 'Moon phase')

    plt.xlabel('Time (days)')
    plt.xticks( rotation= 90 )
    plt.ylabel(componentName + ' Component (nT)')
    plt.legend()
    plt.title('Yearly variation : Component ' + componentName + ' - ' + dayDateTimeObj.strftime('%Y'))
    plt.show()

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




