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
    import MagdasDB as magdasDB
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
            print('Collecting data for day ' + year + '-' + month + '-' + day)

            dataFrame = magdasDB.getMinData('CMB', year, month, day, targetTimeZone=pytz.timezone('Asia/Colombo'))
            #print(dataFrame)

            import dataProcess as processor
            dataFrame, outliers = processor.get_outliers_quantile(dataFrame, component)
            #print(dataFrame[dataFrame[component] == None])

            import plotter
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
