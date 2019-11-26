print('This python is script not developed to use with command line arguments.')
print('Procedure should be specified in this file.')


command = 'generate_outliers'
#command = 'check_written_outliers'

if command == 'generate_outliers':

    import common_DataProcess as processor
    import common_MagdasDB as magdasDB
    import pytz

    #outliers = processor.get_outliers_from_specific_file('Data_Files\\Outliers\\one.txt')
    #processor.save_outliers('CMB',outliers)

    dataFrame = magdasDB.getMinData('CMB', '2016', targetTimeZone=pytz.timezone('Asia/Colombo'))
    #outliers = processor.get_outliers_unreal_total_field(dataFrame, min=39000, max=43000)
    ab_ignore_min_max_filter = processor.OutlierFilter(processor.FilterType.ABNORMAL_IGNORE_BY_MIN_MAX, min=40000, max=45000)
    unreal_total_field = processor.OutlierFilter(processor.FilterType.UNREAL_TOTAL_FIELD, total_field_min=40000, total_field_max=43000)
    filter_list =  processor.FilterList(ab_ignore_min_max=ab_ignore_min_max_filter)
        #filter_list =  processor.FilterList(unreal_total_field=unreal_total_field)
    outliers = processor.get_outliers_multiple_filter(dataFrame, 'H', filter_list)

    processor.save_outliers('CMB',outliers)

if command == 'check_written_outliers':

    import common_DataProcess as processor

    #outliers = processor.get_outliers_confirmed_from_file('CMB')
    outliers = processor.get_outliers_from_specific_file('Data_Files\\Outliers\\CMB_Min_Generated.txt')

    print(outliers)