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

def montly_peak_noon_height_variatoin(data_frame, comp_name, outliers):

    from astroplan import Observer
    import astropy.units as u
    from astropy.time import Time
    import pytz
    from datetime import timedelta, date, datetime
    import pandas as pd
    import matplotlib.dates as mdates
    import numpy as np

    localTZ = data_frame['Date_Time'][0].tzinfo
    subaru = Observer(longitude=80.07*u.deg, latitude=6.97*u.deg, elevation=0*u.m, name="Subaru", timezone=localTZ)

    fig, axs = plt.subplots(3, 1, sharex=True)
    fig.subplots_adjust(hspace=0)
    axs[0].plot(data_frame['Date_Time'], data_frame[comp_name], label= comp_name + ' Comp')
    #axs[0].set_yticks(np.arange(-0.9, 1.0, 0.4))
    #axs[0].set_ylim(-1, 1)
    axs[0].set_ylabel(comp_name + ' Component (nT)')
    days = mdates.DayLocator(interval = 1)
    h_fmt = mdates.DateFormatter('%Y-%m-%d', localTZ)
    axs[0].xaxis.set_major_locator(days)
    axs[0].xaxis.set_major_formatter(h_fmt)

    date_max_values = get_max_of_day(data_frame,comp_name)

    for day, day_data_row in date_max_values.iterrows():
        print('Max time of day ' + day.strftime('%Y-%m-%d %H:%M:%S %z') + ' ' + day_data_row['Max_Time'].strftime('%Y-%m-%d %H:%M:%S %z')
        + ' value : ' + str(day_data_row['Max_Value']))
        noonTimeLocal = subaru.noon(Time(day), which='next').to_datetime(localTZ)
        print('Local noon time (local time zone) : ' + noonTimeLocal.strftime('%Y-%m-%d %H:%M:%S %z'))

        noonTimeRow = data_frame.loc[(data_frame['Date_Time'] == noonTimeLocal.replace(second=0, microsecond=0))]
        axs[0].axvline(x=noonTimeRow['Date_Time'][0], ls='--', c='orange')
        axs[0].axvline(x=day_data_row['Max_Time'], ls='--', c='green')

        date_max_values.loc[day, 'Peak_Height'] = day_data_row['Max_Value'] - noonTimeRow[comp_name][0]

        date_max_values.loc[day, 'Peak_distance'] = (noonTimeRow['Date_Time'][0] - day_data_row['Max_Time']).total_seconds()/60
        
        print('Noon and peak time diff in minutes (HH:MM) : {:3.0f}'.format(date_max_values.loc[day, 'Peak_distance']))
    
    print(date_max_values)


    #date_max_values['Peak_Height'] = date_max_values['Peak_Height']
    axs[1].plot(date_max_values['Peak_Height'], label= comp_name + ' peak-noon height')
    axs[1].set_ylabel(comp_name + ' peak-noon (nT)')
    #axs[1].set_yticks(np.arange(0, 500, 10))
    #axs[1].set_ylim(0, 100)

    axs[2].plot(date_max_values['Peak_distance'], label= comp_name + ' peak-noon distance(mins)')
    axs[2].set_ylabel(comp_name + ' peak distance (mins)')

    plt.xlabel('Time (days)')
    plt.xticks( rotation= 90 )
    plt.legend()
    plt.show()

def montly_sun_rise_peak_variatoin(data_frame, comp_name, outliers):
    
    from astroplan import Observer
    import astropy.units as u
    from astropy.time import Time
    import pytz
    from datetime import timedelta, date, datetime
    import pandas as pd
    import matplotlib.dates as mdates
    import numpy as np

    localTZ = data_frame['Date_Time'][0].tzinfo
    subaru = Observer(longitude=80.07*u.deg, latitude=6.97*u.deg, elevation=0*u.m, name="Subaru", timezone=localTZ)

    fig, axs = plt.subplots(3, 1, sharex=True)
    fig.subplots_adjust(hspace=0)
    axs[0].plot(data_frame['Date_Time'], data_frame[comp_name], label= comp_name + ' Comp')
    axs[0].set_ylabel(comp_name + ' Component (nT)')
    days = mdates.DayLocator(interval = 1)
    h_fmt = mdates.DateFormatter('%Y-%m-%d', localTZ)
    axs[0].xaxis.set_major_locator(days)
    axs[0].xaxis.set_major_formatter(h_fmt)

    date_max_values = get_max_of_day(data_frame,comp_name)
    print(date_max_values)

    for day, day_data_row in date_max_values.iterrows():
        # print('Max time of day ' + day.strftime('%Y-%m-%d %H:%M:%S %z') + ' ' + day_data_row['Max_Time'].strftime('%Y-%m-%d %H:%M:%S %z')
        # + ' value : ' + str(day_data_row['Max_Value']))
        sunRiseTimeLocal = subaru.sun_rise_time(Time(day), which="previous").to_datetime(localTZ)
        # print('Sun rise time (local time zone) : ' + sunRiseTimeLocal.strftime('%Y-%m-%d %H:%M:%S %z'))
        
        axs[0].axvline(x=day_data_row['Max_Time'], ls='--', c='green')

        sunRiseTimeRow = data_frame.loc[(data_frame['Date_Time'] == sunRiseTimeLocal.replace(second=0, microsecond=0))]
        if sunRiseTimeRow.empty:
            print('Sunrise time data is not available for the date {0}'.format(sunRiseTimeLocal.strftime('%Y-%m-%d %z')))
        else:
            axs[0].axvline(x=sunRiseTimeRow['Date_Time'][0], ls='--', c='orange')
            print(day_data_row)
            date_max_values.loc[day, 'Peak_Height'] = day_data_row['Max_Value'] - sunRiseTimeRow[comp_name][0]      
            date_max_values.loc[day, 'Peak_distance'] = (day_data_row['Max_Time'] - sunRiseTimeRow['Date_Time'][0]).total_seconds()/60
            # print('Sun-rise to peak time diff in minutes (HH:MM) : {0:3.0f}, peak height {1:4.0f}'.format(date_max_values.loc[day, 'Peak_distance'], date_max_values.loc[day, 'Peak_Height']))

    print(date_max_values)

    axs[1].plot(date_max_values['Peak_Height'], label= comp_name + ' sunrise-peak height')
    axs[1].set_ylabel(comp_name + ' magnitude (nT)')

    axs[2].plot(date_max_values['Peak_distance'], label= comp_name + ' sunrise-peak distance(mins)')
    axs[2].set_ylabel(comp_name + ' peak distance (mins)')

    plt.xlabel('Time (days)')
    plt.xticks( rotation= 90 )
    plt.legend()
    plt.show()

def get_max_of_day(data_frame, component):

    import numpy as np
    import pandas as pd
    import math

    dataSet = {'Max_Time' : [], 'Max_Value' : []}
    day_list = []
    day_list = np.append(day_list, pd.to_datetime(data_frame['Date_Time'][0], format='%Y-%m-%d %H:%M:%S').replace(hour=12, minute=0))
    dataSet['Max_Time'] = np.append(dataSet['Max_Time'], data_frame['Date_Time'][0])
    dataSet['Max_Value'] = np.append(dataSet['Max_Value'], data_frame[component][0])

    max = data_frame[component][0]
    current_date = data_frame['Date_Time'][0]
    for index, row in data_frame.iterrows():
        if current_date.day != row['Date_Time'].day:
            current_date = row['Date_Time']
            day_list = np.append(day_list, pd.to_datetime(row['Date_Time'], format='%Y-%m-%d %H:%M:%S').replace(hour=12, minute=0))
            dataSet['Max_Value'] = np.append(dataSet['Max_Value'], row[component])
            dataSet['Max_Time'] = np.append(dataSet['Max_Time'], current_date)
            
            if row[component] is not pd.NaT:
                max = row[component]
            else:
                max = -9999999

        if row[component] is not pd.NaT and row[component] > max:
            dataSet['Max_Value'][-1] = row[component]
            dataSet['Max_Time'][-1] = row['Date_Time']
            max = row[component]
    month_data = pd.DataFrame(data=dataSet, index=day_list, columns=['Max_Time','Max_Value'])
    return month_data

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




