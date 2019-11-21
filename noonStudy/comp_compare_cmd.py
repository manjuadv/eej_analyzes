print('This python is script not developed to use with command line arguments.')
print('Procedure should be specified in this file.')


command = 'compare_daily_components'
#command = 'compare_monthly_components'

if command == 'compare_daily_components':
    # This section compare the shape of variation of all three components
    # Magnitude is match to each other other anly only the variation patter in concerned
    import common_DataProcess as processor
    import common_MagdasDB as magdasDB
    import pytz
    import helper_astro as astro
    import numpy as np
    import comp_compare_plot as plotter

    day = '2016-3-9'
    print('Comparing three components for date ' + day)
    parts = day.split("-")
    
    year = parts[0]
    month = parts[1]
    day = parts[2]            
    if len(month) < 2:
        month = '0' + month
    if len(day) < 2:
        day = '0' + day
    
    dataFrame = magdasDB.getMinData('CMB', year, month, day, targetTimeZone=pytz.timezone('Asia/Colombo'))

    component='H'

    unreal_total_field = processor.OutlierFilter(processor.FilterType.UNREAL_TOTAL_FIELD, total_field_min=40000, total_field_max=43000)
    filter_list =  processor.FilterList(unreal_total_field=unreal_total_field)
    outliers = processor.get_outliers_multiple_filter(dataFrame, component, filter_list)
    dataFrame.loc[outliers.index, component] = np.nan
    plotter.component_compare_daily_all(dataFrame, outliers)

if command == 'compare_monthly_components':
    month = day = '2016-3-9'
    print('Comparing three components for month ' + month)