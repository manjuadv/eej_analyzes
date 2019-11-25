def component_compare_daily_all(dataFrame, outliers=None):

    #componentName = 'H'
    if dataFrame.empty:
        print('No data is available to plot')
        return

    import pytz
    import datetime
    import matplotlib.dates as mdates
    import helper_astro as astro
    from astroplan import Observer
    from datetime import datetime
    from astropy.time import Time
    import astropy.units as u
    import matplotlib.pyplot as plt

    print('Daily comparison graph is being generated.')

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

    h_comp_min = dataFrame['H'].min()
    h_comp_max = dataFrame['H'].max()
    h_comp_magnitude = h_comp_max - h_comp_min
    d_comp_min = dataFrame['D'].min()
    d_comp_max = dataFrame['D'].max()
    d_comp_magnitude = d_comp_max - d_comp_min
    z_comp_min = dataFrame['Z'].min()
    z_comp_max = dataFrame['Z'].max()
    z_comp_magnitude = z_comp_max - z_comp_min
    #h_comp_magnitude = dataFrame['H'].max() - dataFrame['H'].min()
    
    h_comp_first_val = dataFrame['H'][0]
    d_comp_first_val = dataFrame['D'][0]
    z_comp_first_val = dataFrame['Z'][0]
    #dataFrame['D'] = dataFrame['D'].mul(h_comp_magnitude/d_comp_magnitude)
    dataFrame['D'] = dataFrame['D'].add(h_comp_first_val - d_comp_first_val)
    #dataFrame['Z'] = dataFrame['Z'].mul(h_comp_magnitude/z_comp_magnitude)
    dataFrame['Z'] = dataFrame['Z'].add(h_comp_first_val - z_comp_first_val)
    d_comp_zero_level = h_comp_first_val - d_comp_first_val

    fig, ax = plt.subplots()
    ax.plot(dataFrame['Date_Time'], dataFrame['H'], label= 'H component')
    ax.plot(dataFrame['Date_Time'], dataFrame['D'], label= 'D comp pattern')
    ax.plot(dataFrame['Date_Time'], dataFrame['Z'], label= 'Z comp pattern')
    ax.axhline(y=d_comp_zero_level, c='purple')
    hours = mdates.HourLocator(interval = 1)
    h_fmt = mdates.DateFormatter('%d %H:%M:%S', localTZ)
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(h_fmt)
    
    H_comp_name = 'H'

    if outliers is not None:
        y_min, y_max = ax.get_ylim()
        outliers[H_comp_name] = y_min
        kw = dict(marker='o', linestyle='none', color='r', alpha=0.3)
        ax.plot(outliers[H_comp_name] , label= 'Outliers', **kw)

    moon_phase = astro.moon_get_moon_phase(dataFrame['Date_Time'][0])
    t = ax.text(0.03, 0.9,'Lunar phase {:3.0f}%'.format(moon_phase * 100), horizontalalignment='left'
    , verticalalignment='center',transform=ax.transAxes)
    t.set_bbox(dict(facecolor='red', alpha=0.5, edgecolor='red'))

    minValueIndex = dataFrame[H_comp_name].idxmin() 
    maxValueIndex = dataFrame[H_comp_name].idxmax()

    print('Max value : ' + str(dataFrame.loc[maxValueIndex][H_comp_name]) + ', at : '
    + dataFrame.loc[maxValueIndex]['Date_Time'].strftime('%Y-%m-%d %H:%M:%S %z'))
    print('Min value : ' + str(dataFrame.loc[minValueIndex][H_comp_name]) + ', at : '
    + dataFrame.loc[minValueIndex]['Date_Time'].strftime('%Y-%m-%d %H:%M:%S %z'))

    yAxisMiddle = dataFrame.loc[minValueIndex][H_comp_name] + ((dataFrame.loc[maxValueIndex][H_comp_name] 
    - dataFrame.loc[minValueIndex][H_comp_name]) / 2)

    noonTimeRow = dataFrame[(dataFrame['Date_Time'] == noonTimeLocal.replace(second=0, microsecond=0))]
    print('Noon time value of ' + H_comp_name + '-Component {:6.3f}'.format(noonTimeRow[H_comp_name][0]))
    ax.axvline(x=noonTimeRow['Date_Time'][0], ls='--', c='orange')
    ax.text(noonTimeRow['Date_Time'][0], yAxisMiddle, 'Local noon', rotation=90, ha='left', va='center')
    ax.axvline(x=sunRiseTimeLocal, ls='--', c='gray')
    ax.axvline(x=sunRiseTimeLocalTwilight, ls='--', c='gray')
    ax.text(sunRiseTimeLocal, dataFrame.loc[minValueIndex][H_comp_name], 'Sun rise', rotation=90, ha='left', va='bottom')
    ax.axvline(x=sunSetTimeLocal, ls='--', c='gray')    
    ax.text(sunSetTimeLocal, dataFrame.loc[minValueIndex][H_comp_name], 'Sun set', rotation=90, ha='left', va='bottom')

    ax.axvline(x=dataFrame.loc[maxValueIndex]['Date_Time'], ls='--', c='green')
    ax.text(dataFrame.loc[maxValueIndex]['Date_Time'], yAxisMiddle, 'Max value', rotation=90, ha='left', va='center')

    plt.xlabel('Time (hours)')
    plt.xticks( rotation= 90 )
    plt.ylabel('Scalled component value')
    plt.legend()
    plt.show()
