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
                plotDay(year, month, day)

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
    pass
    
def plotMonth(year, month, component="H") :
    pass

def plotDay(year, month, day) :

    import common_DataProcess as processor
    import common_MagdasDB as magdasDB
    import pytz
    import helper_astro as astro
    import numpy as np
    import comp_compare_plot as plotter

    dataFrame = magdasDB.getMinData('CMB', year, month, day, targetTimeZone=pytz.timezone('Asia/Colombo'))

    component='H'

    unreal_total_field = processor.OutlierFilter(processor.FilterType.UNREAL_TOTAL_FIELD, total_field_min=40000, total_field_max=43000)
    filter_list =  processor.FilterList(unreal_total_field=unreal_total_field)
    outliers = processor.get_outliers_multiple_filter(dataFrame, component, filter_list)
    dataFrame.loc[outliers.index, component] = np.nan
    plotter.component_compare_daily_all(dataFrame, outliers)
    
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
