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

        import numpy as np
        import common_DataProcess as processor

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
            print('Collecting data for day ' + year + '-' + month + '-' + day)

            dataFrame = magdasDB.getMinData('CMB', year, month, day, targetTimeZone=pytz.timezone('Asia/Colombo'))
            #outliers = processor.get_outliers_quantile_scale(dataFrame, component, interquartile_range_scale=1.5)
            #outliers = processor.get_outliers_min_max_limit(dataFrame, component, 40000, 40955)
            #outliers = processor.get_outliers_z_score(dataFrame, component, threshold=3)
            #outliers = processor.get_outliers_rolling_medians(dataFrame, component, threshold=1.5)
            normal_distribution_filter = processor.OutlierFilter(processor.FilterType.NORMAL_DISTRIBUTION, SD_range_scalar=3)
            filter_list =  processor.FilterList(normal_disb=normal_distribution_filter)
            outliers = processor.get_outliers_multiple_filter(dataFrame, component, filter_list)
            dataFrame.loc[outliers.index, component] = np.nan # any value can be assigned

            import noon_study_plot as plotter
            plotter.dailyVariationAnalyzes(dataFrame, component, outliers)

            #import pyplotWrap as plotter
            #plotter.dialyCompMaxAndNoon(dataFrame['Date_Time'],dataFrame['H'],'H')

        else :
            year = parts[0]
            month = parts[1]
            if len(month) < 2:
                month = '0' + month
            print('Collecting data for month ' + year + '-' + month)

    elif len(argvs[0]) == 4 and is_number(argvs[0]):
        year = argvs[0]
        print('Collecting data for year ' + year)
    else:
        print('Incorrect combination of parameters. First paramter supposed to be a date.')

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
