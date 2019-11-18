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
        if len(parts) > 2:
            year = parts[0]
            month = parts[1]
            day = parts[2]            
            if len(month) < 2:
                month = '0' + month
            if len(day) < 2:
                day = '0' + day
            plotDay(year, month, day)

        else :
            year = parts[0]
            month = parts[1]
            if len(month) < 2:
                month = '0' + month
            plotMonth(year, month)

    elif len(argvs[0]) == 4 and is_number(argvs[0]):
        year = argvs[0]
        plotYear(year)
    else:
        print('Incorrect combination of parameters. First paramter supposed to be a date.')

def plotYear(year, component="H") :
    print('Plotting year : ' + year + ', component : ' + component)
    
def plotMonth(year, month, component="H") :
    print('Plotting month : ' + year + '-' + month + ', component : ' + component)

def plotDay(year, month, day, component="H") :

    import dataProcess as processor
    import MagdasDB as magdasDB
    import numpy as np
    import plotter
    import pytz

    print('Plotting month : ' + year + '-' + month + '-' + day + ', component : ' + component)
    dataFrame = magdasDB.getMinData('CMB', year, month, day, targetTimeZone=pytz.timezone('Asia/Colombo'))
    # outliers = processor.get_outliers_rolling_medians(dataFrame, component, threshold=1.5)
    # dataFrame.loc[outliers.index, component] = np.nan # any value can be assigned
    # plotter.daily_graph(dataFrame, component, outliers)
    outliers = processor.get_outliers_abnormal_ignore(dataFrame, component)
    #plotter.generate_guassian_fit_curve_for_data(dataFrame, component)
    
def printParameterHelp() :
    print("If there is only one parameter, it should be the target daay, month or year")
    print("year, eg : 2016")
    print("month of an year, eg : 2016-3")
    print("day of a month of an year, eg : 2016-3-12")
    print(":c : component. If not specified, default component H taken. eg : :c dh (To graph both 'D' and 'H' components)")
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
