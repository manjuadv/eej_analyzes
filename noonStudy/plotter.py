import matplotlib.pyplot as plt

def dailyVariationAnalyzes(dataFrame, componentName, outliers):
    from astroplan import Observer
    import astropy.units as u
    from astropy.time import Time
    import pytz
    import datetime
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
    hours = mdates.HourLocator(interval = 1)
    h_fmt = mdates.DateFormatter('%d %H:%M:%S', localTZ)
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(h_fmt)
    
    y_min, y_max = ax.get_ylim()
    outliers[componentName] = y_min
    kw = dict(marker='o', linestyle='none', color='r', alpha=0.3)
    ax.plot(outliers[componentName] , label= componentName + '-outlier', **kw)

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
    print('Difference between sun rise value to peak : {:1.0f}'.format(sunRiseToPeakDiff))
    ax.annotate('', xy=(sunRiseTimeRow['Date_Time'][0] + datetime.timedelta(minutes=15), dataFrame.loc[maxValueIndex][componentName]), 
    xytext=(sunRiseTimeRow['Date_Time'][0] + datetime.timedelta(minutes=15), sunRiseTimeRow[componentName][0]), 
    xycoords='data', textcoords='data', arrowprops={'arrowstyle': '<->'})
    ax.annotate('{:1.0f} nT'.format(sunRiseToPeakDiff), xy=(sunRiseTimeRow['Date_Time'][0] + datetime.timedelta(minutes=20), 
    dataFrame.loc[maxValueIndex][componentName] - sunRiseToPeakDiff/2), ha='left', va='center', rotation=90)

    plt.xlabel('Time (hours)')
    plt.xticks( rotation= 90 )
    plt.ylabel(componentName + ' Component (nT)')
    plt.legend()
    plt.show()

def generate_guassian_normal_curve():
    
    import numpy as np
    from scipy.stats import norm

    mu = 998.8
    sigma = 73.10
    x1 = 900
    x2 = 1100

    # calculate the z-transform
    z1 = ( x1 - mu ) / sigma
    z2 = ( x2 - mu ) / sigma

    x = np.arange(z1, z2, 0.001) # range of x in spec
    x_all = np.arange(-10, 10, 0.001) # entire range of x, both in and out of spec
    # mean = 0, stddev = 1, since Z-transform was calculated
    y = norm.pdf(x,0,1)
    y2 = norm.pdf(x_all,0,1)

    fig, ax = plt.subplots(figsize=(9,6))
    plt.style.use('fivethirtyeight')
    print(x_all)
    print(y2)
    ax.plot(x_all,y2)
    ax.fill_between(x,y,0, alpha=0.3, color='b')
    ax.fill_between(x_all,y2,0, alpha=0.1)
    #ax.set_xlim([-4,4])
    ax.set_xlabel('# of Standard Deviations Outside the Mean')
    #ax.set_yticklabels([])
    ax.set_title('Normal Gaussian Curve')
    plt.savefig('normal_curve.png', dpi=72, bbox_inches='tight')
    plt.show()

def generate_guassian_fit_curve_for_data(dataFrame, componentName):
    import matplotlib.pyplot as plt
    from numpy import exp, loadtxt, pi, sqrt, arange
    from lmfit import Model
    #data = loadtxt('model1d_gauss.dat')
    x = arange(start=0, stop=len(dataFrame[componentName]), step=1) #dataFrame['Date_Time'].values #data[:, 0]
    print(x)
    y = dataFrame[componentName].values #data[:, 1]
    gmodel = Model(gaussian)
    result = gmodel.fit(y, x=x, amp=5, cen=5, wid=1)
    print(result.fit_report())
    
    plt.plot(x, y, 'bo')
    #plt.plot(x, result.init_fit, 'k--', label='initial fit')
    plt.plot(x, result.best_fit, 'r-', label='best fit')
    plt.legend(loc='best')
    plt.show()

def gaussian(x, amp, cen, wid):
    from numpy import exp, pi, sqrt
    """1-d gaussian: gaussian(x, amp, cen, wid)"""
    return (amp / (sqrt(2*pi) * wid)) * exp(-(x-cen)**2 / (2*wid**2))

def daily_graph(dataFrame, componentName, outliers):
    from astroplan import Observer
    import astropy.units as u
    from astropy.time import Time
    import pytz
    import datetime
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
    hours = mdates.HourLocator(interval = 1)
    h_fmt = mdates.DateFormatter('%d %H:%M:%S', localTZ)
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(h_fmt)
    
    y_min, y_max = ax.get_ylim()
    outliers[componentName] = y_min
    kw = dict(marker='o', linestyle='none', color='r', alpha=0.3)
    ax.plot(outliers[componentName] , label= componentName + '-outlier', **kw)

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

    plt.xlabel('Time (hours)')
    plt.xticks( rotation= 90 )
    plt.ylabel(componentName + ' Component (nT)')
    plt.legend()
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




