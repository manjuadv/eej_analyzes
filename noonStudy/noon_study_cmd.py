import sys
#import DbUtility as dbUtils
#import DBread as dbRead
import pytz

def main():
    printParameterHelp()
    if len(sys.argv) > 1 :
        processArgvs(sys.argv[1:])
    else :
        print('No parameter provided. Please check the instructions.')

def processArgvs(argvs):
    import common_MagdasDB as magdasDB
    if argvs[0] == "stl" :
        magdasDB.printStationList()
    elif '-' in argvs[0] :

        component  = 'H'
        parts = argvs[0].split("-")
        if len(parts) > 2:
            year = parts[0]
            month = parts[1]
            day = parts[2]            
            if len(month) < 2:
                month = '0' + month
            if len(day) < 2:
                day = '0' + day

            daily_noon_analyze(year, month, day, component)
        else :
            year = parts[0]
            month = parts[1]
            if len(month) < 2:
                month = '0' + month

            monthly_noon_peak_analyze(year, month, component)

    elif len(argvs[0]) == 4 and is_number(argvs[0]):
        year = argvs[0]
        component  = 'H'
        yearly_noon_peak_analyze(year, component)
    else:
        print('Incorrect combination of parameters. First paramter supposed to be a date.')

def yearly_noon_peak_analyze(year, component):
    
    import numpy as np
    import common_DataProcess as processor
    import noon_study_plot as plotter
    import common_MagdasDB as magdasDB
            
    print('Collecting data for year ' + year )

    dataFrame = magdasDB.getMinData('CMB', year, targetTimeZone=pytz.timezone('Asia/Colombo'))
    
    outliers = processor.get_outliers_confirmed_in_range('CMB', utc_start_time=dataFrame.index.values[0], utc_end_time=dataFrame.index.values[-1])
    dataFrame.loc[dataFrame.index.isin(outliers.index), ['H','D','Z','F']] = np.nan

    dst_data = processor.read_dst_data_in_range(dataFrame.index.values[0], dataFrame.index.values[-1])

    plotter.yearly_sun_rise_peak_variatoin(dataFrame, component, outliers, dst_data)

def monthly_noon_peak_analyze(year, month, component):
    
    import numpy as np
    import common_DataProcess as processor
    import noon_study_plot as plotter
    import common_MagdasDB as magdasDB
            
    print('Collecting data for month ' + year + '-' + month)

    dataFrame = magdasDB.getMinData('CMB', year, month, targetTimeZone=pytz.timezone('Asia/Colombo'))
    
    # unreal_total_field = processor.OutlierFilter(processor.FilterType.UNREAL_TOTAL_FIELD, total_field_min=40000, total_field_max=43000)
    # z_score = processor.OutlierFilter(processor.FilterType.Z_SCORE, threshold=3)
    # filter_list =  processor.FilterList(unreal_total_field=unreal_total_field, z_score=z_score)
    # outliers = processor.get_outliers_multiple_filter(dataFrame, component, filter_list)

    # dataFrame.loc[outliers.index, ['H','D','Z','F']] = np.nan
    outliers = processor.get_outliers_confirmed_in_range('CMB', utc_start_time=dataFrame.index.values[0], utc_end_time=dataFrame.index.values[-1])
    dataFrame.loc[dataFrame.index.isin(outliers.index), ['H','D','Z','F']] = np.nan

    dst_data = processor.read_dst_data_in_range(dataFrame.index.values[0], dataFrame.index.values[-1])
    #print(dst_data)

    plotter.montly_peak_noon_height_variatoin(dataFrame, component, outliers, dst_data)
    #plotter.montly_sun_rise_peak_variatoin(dataFrame, component, outliers, dst_data)

def daily_noon_analyze(year, month, day, component):
    
    import numpy as np
    import common_DataProcess as processor
    import common_MagdasDB as magdasDB

    print('Collecting data for day ' + year + '-' + month + '-' + day)

    dataFrame = magdasDB.getMinData('CMB', year, month, day, targetTimeZone=pytz.timezone('Asia/Colombo'))

    if (dataFrame.index == '2017-09-07 03:26:00 +0000').any():
        dataFrame.loc['2017-09-07 03:26:00 +0000', component] = np.nan
    if (dataFrame.index == '2017-09-07 03:27:00 +0000').any():
        dataFrame.loc['2017-09-07 03:27:00 +0000', component] = np.nan
    if (dataFrame.index == '2017-09-09 03:57:00 +0000').any():
        dataFrame.loc['2017-09-09 03:57:00 +0000', component] = np.nan
    if (dataFrame.index == '2017-09-09 03:58:00 +0000').any():
        dataFrame.loc['2017-09-09 03:58:00 +0000', component] = np.nan
    if (dataFrame.index == '2017-09-09 12:13:00 +0000').any():
        dataFrame.loc['2017-09-09 12:13:00 +0000', component] = np.nan
    if (dataFrame.index == '2017-09-09 13:08:00 +0000').any():
        dataFrame.loc['2017-09-09 13:08:00 +0000', component] = np.nan

    #print(dataFrame.loc['2017-09-07 18:09:00 +0000'])
    #print(dataFrame[dataFrame.apply(lambda x: (not (np.isreal(x[component]))), axis=1)])
    #print(dataFrame[dataFrame.apply(lambda x: (not (np.isreal(x['F']))), axis=1)])
    #print(dataFrame['F'].isnull())
    #outliers = processor.get_outliers_quantile_scale(dataFrame, component, interquartile_range_scale=1.5)
    #outliers = processor.get_outliers_min_max_limit(dataFrame, component, 40000, 40955)
    #outliers = processor.get_outliers_z_score(dataFrame, component, threshold=3)
    #outliers = processor.get_outliers_rolling_medians(dataFrame, component, threshold=1.5)
    # normal_distribution_filter = processor.OutlierFilter(processor.FilterType.NORMAL_DISTRIBUTION, SD_range_scalar=3)
    # filter_list =  processor.FilterList(normal_disb=normal_distribution_filter)
    # outliers = processor.get_outliers_multiple_filter(dataFrame, component, filter_list)

    # import pandas as pd
    # unreal_total_field_filter = processor.OutlierFilter(processor.FilterType.UNREAL_TOTAL_FIELD, total_field_min=40000, total_field_max=43000)
    # ab_ignore_min_max_filter = processor.OutlierFilter(processor.FilterType.ABNORMAL_IGNORE_BY_MIN_MAX, min=40700, max=45000)
    # filter_list =  processor.FilterList(ab_ignore_min_max=ab_ignore_min_max_filter)
    # outliers = processor.get_outliers_multiple_filter(dataFrame, component, filter_list)

    outliers = processor.get_outliers_confirmed_in_range('CMB', utc_start_time=dataFrame.index.values[0], utc_end_time=dataFrame.index.values[-1])

    dataFrame.loc[dataFrame.index.isin(outliers.index), component] = np.nan # any value can be assigned

    import noon_study_plot as plotter
    plotter.dailyVariationAnalyzes(dataFrame, component, outliers)

    #import pyplotWrap as plotter
    #plotter.dialyCompMaxAndNoon(dataFrame['Date_Time'],dataFrame['H'],'H')

def printParameterHelp() :
    print('Commands and examples')
    print('-----------------------')
    print("stl : station list")
    print("[yyyy-mm-dd (day), yyyy-mm(month), yyyy(year)]: graph of the given period")
    print("[prediod] [c]: component")
    print()


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

if __name__ == "__main__":
    main()
