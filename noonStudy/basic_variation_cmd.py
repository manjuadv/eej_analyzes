import sys

def main():
    printParameterHelp()
    if len(sys.argv) > 1 :
        processArgvs(sys.argv[1:])
    else :
        printInvalidParameterCombError()
        
def processArgvs(argvs):
    
    import numpy as np

    if '-' in argvs[0] :
        parts = argvs[0].split("-")
        comp_list = []
        if len(argvs) > 1:
            # Component was given
            comp_text = str(argvs[1]).capitalize()
            comp_list = list(comp_text)
            print('Plotting components ' + ','.join(comp_list))

        if len(parts) > 2:
            year = parts[0]
            month = parts[1]
            day = parts[2]            
            if len(month) < 2:
                month = '0' + month
            if len(day) < 2:
                day = '0' + day

            if len(comp_list) <1:
                # No component given, use default component(H)
                plotDay(year, month, day)
            elif len(comp_list)==1:
                # Only one component presented
                plotDay(year, month, day, component=comp_list[0])

        else :
            year = parts[0]
            month = parts[1]
            if len(month) < 2:
                month = '0' + month

            if len(comp_list) <1:
                # No component given, use default component(H)
                plotMonth(year, month)
            elif len(comp_list)==1:
                # Only one component presented
                plotMonth(year, month, component=comp_list[0])

    elif len(argvs[0]) == 4 and is_number(argvs[0]):
        year = argvs[0]
        plotYear(year)
    else:
        print('Incorrect combination of parameters. First paramter supposed to be a date.')

def plotYear(year, component="H") :

    import common_DataProcess as processor
    import common_MagdasDB as magdasDB
    import pytz
    import basic_variation_plot as plotter
    import pandas as pd
    import numpy as np

    print('Plotting year : ' + year + ', component : ' + component)
    dataFrame = magdasDB.getMinData('CMB', year, targetTimeZone=pytz.timezone('Asia/Colombo'))

    # outliers_by_abnormal = processor.get_outliers_abnormal_ignore(dataFrame, component,min=40000, max=45000)
    # outliers_by_slope = processor.get_outliers_abnormal_slope_ignore(dataFrame, component,min=40000, max=45000)
    # outliers_zscore = processor.get_outliers_z_score(dataFrame, component, threshold=3)
    # outliers = pd.concat([outliers_by_abnormal, outliers_by_slope, outliers_zscore])
    
    ab_ignore_min_max_filter = processor.OutlierFilter(processor.FilterType.ABNORMAL_IGNORE_BY_MIN_MAX, min=40000, max=45000)
    #ab_ignore_sudden_inc = processor.OutlierFilter(processor.FilterType.ABNORMAL_IGNORE_BY_SUDDEN_INCREASE, threshold=100)
    z_score = processor.OutlierFilter(processor.FilterType.Z_SCORE, threshold=3)
    filter_list =  processor.FilterList(ab_ignore_min_max=ab_ignore_min_max_filter, z_score=z_score)
    outliers = processor.get_outliers_multiple_filter(dataFrame, component, filter_list)

    dataFrame.loc[outliers.index, component] = np.nan

    plotter.yearly_graph(dataFrame, component, outliers=outliers)
    
def plotMonth(year, month, component="H") :

    import common_DataProcess as processor
    import common_MagdasDB as magdasDB
    import pytz
    import basic_variation_plot as plotter
    import pandas as pd
    import numpy as np

    print('Plotting month : ' + year + '-' + month + ', component : ' + component)
    dataFrame = magdasDB.getMinData('CMB', year, month, targetTimeZone=pytz.timezone('Asia/Colombo'))

    # outliers_by_abnormal = processor.get_outliers_abnormal_ignore(dataFrame, component,min=40000, max=45000)
    # outliers_by_slope = processor.get_outliers_abnormal_slope_ignore(dataFrame, component,min=40000, max=45000)
    # outliers_zscore = processor.get_outliers_z_score(dataFrame, component, threshold=3)
    # outliers = pd.concat([outliers_by_abnormal, outliers_by_slope, outliers_zscore])
    
    ab_ignore_min_max_filter = processor.OutlierFilter(processor.FilterType.ABNORMAL_IGNORE_BY_MIN_MAX, min=40000, max=45000)
    ab_ignore_sudden_inc = processor.OutlierFilter(processor.FilterType.ABNORMAL_IGNORE_BY_SUDDEN_INCREASE, threshold=100)
    unreal_total_field = processor.OutlierFilter(processor.FilterType.UNREAL_TOTAL_FIELD, total_field_min=40000, total_field_max=43000)
    z_score = processor.OutlierFilter(processor.FilterType.Z_SCORE, threshold=3)
    # filter_list =  processor.FilterList(ab_ignore_min_max=ab_ignore_min_max_filter, ab_ignore_sudden_inc=ab_ignore_sudden_inc, z_score=z_score)
    # outliers = processor.get_outliers_multiple_filter(dataFrame, component, filter_list)

    filter_list =  processor.FilterList(unreal_total_field=unreal_total_field, z_score=z_score)
    outliers = processor.get_outliers_multiple_filter(dataFrame, component, filter_list)

    dataFrame.loc[outliers.index, component] = np.nan

    plotter.monthly_graph(dataFrame, component, outliers)
    #plotter.monthly_graph(dataFrame, component)

def plotDay(year, month, day, component="H") :

    import common_DataProcess as processor
    import common_MagdasDB as magdasDB
    import numpy as np
    import basic_variation_plot as plotter
    import pytz
    import pandas as pd
    from datetime import timedelta, datetime
    import helper_astro as astro
    import math

    print('Plotting day : ' + year + '-' + month + '-' + day + ', component : ' + component)
    dataFrame = magdasDB.getMinData('CMB', year, month, day, targetTimeZone=pytz.timezone('Asia/Colombo'))
    #outliers_by_abnormal = processor.get_outliers_abnormal_ignore(dataFrame, component,min=40000, max=45000)
    #outliers_by_slope = processor.get_outliers_abnormal_slope_ignore(dataFrame, component,min=40000, max=45000)
    #outliers_zscore = processor.get_outliers_z_score(dataFrame, component, threshold=3)
    #outliers = pd.concat([outliers_by_abnormal, outliers_by_slope, outliers_zscore])
    if component=='H' or component=='F':
        #ab_ignore_min_max_filter = processor.OutlierFilter(processor.FilterType.ABNORMAL_IGNORE_BY_MIN_MAX, min=40000, max=45000)
        #ab_ignore_sudden_inc = processor.OutlierFilter(processor.FilterType.ABNORMAL_IGNORE_BY_SUDDEN_INCREASE, threshold=100)
        #z_score = processor.OutlierFilter(processor.FilterType.Z_SCORE, threshold=3)
        unreal_total_field = processor.OutlierFilter(processor.FilterType.UNREAL_TOTAL_FIELD, total_field_min=40000, total_field_max=43000)
        #filter_list =  processor.FilterList(ab_ignore_min_max=ab_ignore_min_max_filter, ab_ignore_sudden_inc=ab_ignore_sudden_inc, z_score=z_score, unreal_total_field=unreal_total_field)
        filter_list =  processor.FilterList(unreal_total_field=unreal_total_field)
        outliers = processor.get_outliers_multiple_filter(dataFrame, component, filter_list)
        #print(dataFrame.loc[(dataFrame['Date_Time'] > datetime(year=2016,month=3, day=31, hour=11, minute=30, tzinfo=pytz.timezone('Asia/Colombo')))])
        #print(dataFrame.loc[(math.isnan(dataFrame['F']))])
        dataFrame.loc[outliers.index, component] = np.nan
        plotter.daily_graph(dataFrame, component, outliers)
    elif component=='D':
        ab_ignore_min_max_filter = processor.OutlierFilter(processor.FilterType.ABNORMAL_IGNORE_BY_MIN_MAX, min=-10000, max=45000)
        ab_ignore_sudden_inc = processor.OutlierFilter(processor.FilterType.ABNORMAL_IGNORE_BY_SUDDEN_INCREASE, threshold=10)
        z_score = processor.OutlierFilter(processor.FilterType.Z_SCORE, threshold=3)
        filter_list =  processor.FilterList(ab_ignore_min_max=ab_ignore_min_max_filter, ab_ignore_sudden_inc=ab_ignore_sudden_inc, z_score=z_score)
        outliers = processor.get_outliers_multiple_filter(dataFrame, component, filter_list)
        dataFrame.loc[outliers.index, component] = np.nan
        plotter.daily_graph(dataFrame, component, outliers)
        #plotter.daily_graph(dataFrame, component)
    elif component=='Z':
        ab_ignore_min_max_filter = processor.OutlierFilter(processor.FilterType.ABNORMAL_IGNORE_BY_MIN_MAX, min=-10000, max=45000)
        ab_ignore_sudden_inc = processor.OutlierFilter(processor.FilterType.ABNORMAL_IGNORE_BY_SUDDEN_INCREASE, threshold=100)
        #z_score = processor.OutlierFilter(processor.FilterType.Z_SCORE, threshold=3)
        filter_list =  processor.FilterList(ab_ignore_min_max=ab_ignore_min_max_filter, ab_ignore_sudden_inc=ab_ignore_sudden_inc)
        outliers = processor.get_outliers_multiple_filter(dataFrame, component, filter_list)
        dataFrame.loc[outliers.index, component] = np.nan
        plotter.daily_graph(dataFrame, component, outliers)
    #plotter.generate_guassian_fit_curve_for_data(dataFrame, component)
    
def printParameterHelp() :
    print("If there is only one parameter, it should be the target day, month or year")
    print("If there two parameters, it's [date] and [component]")
    print("2016 [year 2016 data to plot]")
    print("2016-3 [year 2016-March data to plot]")
    print("2016-3-12 [year 2016-March-12 data to plot]")
    print("2016-3-12 h [year 2016-March-12 'H' component data to plot]")
    print("2016-3-12 HD [year 2016-March-12 'H' component and 'D' data to plot. Only the plattern is plotted (not real values)]")
    print("")
    print()

def printInvalidParameterCombError() :
    print("Invalid parameter combination")

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
