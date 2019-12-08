print('This python is script not developed to use with command line arguments.')
print('Procedure should be specified in this file.')


#command = 'generate_outliers'
#command = 'check_written_outliers'
#command = 'outliers_generation_verify'
#command = 'generate_manual_remove_file'
command = 'read_ee_index_data'

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
    filter_list =  processor.FilterList(ab_ignore_min_max=ab_ignore_min_max_filter, unreal_total_field=unreal_total_field)
        #filter_list =  processor.FilterList(unreal_total_field=unreal_total_field)
    outliers = processor.get_outliers_multiple_filter(dataFrame, 'H', filter_list)

    processor.save_outliers('CMB',outliers)

if command == 'check_written_outliers':

    import common_DataProcess as processor

    #outliers = processor.get_outliers_confirmed_from_file('CMB')
    outliers = processor.get_outliers_from_specific_file('Data_Files\\Outliers\\CMB_Min_Generated.txt')

    print(outliers)

if command == 'outliers_generation_verify':
    import common_DataProcess as processor
    import common_MagdasDB as magdasDB

    #outliers = processor.get_outliers_from_specific_file('Data_Files\\Outliers\\two.txt')
    outliers = processor.get_outliers_from_specific_file('Data_Files\\Outliers\\one.txt')
    #outliers = processor.get_outliers_from_specific_file('Data_Files\\Outliers\\CMB_Min_Confirmed.txt')
    #print(outliers.loc[outliers.index.duplicated(keep=False)])
    processor.save_manual_outliers('CMB',outliers)

if command == 'generate_manual_remove_file':
    import common_MagdasDB  as magdasDB
    import pytz
    import common_DataProcess as processor
    
    # Outliers are saved in a file called 'CMB_Min_Manual_Removed.txt'
    # But outliers are read-back from a file called 'CMB_Min_Manual_Confirmed.txt'. 
    # Generated outlier data should be coppied to 'CMB_Min_Manual_Confirmed.txt' so outliers become active


    # Removing of month 2016-03 outlier values. 
    processor.save_manual_outliers('CMB', '2016-03-03 08:08:00','2016-03-03 09:05:00')
    processor.save_manual_outliers('CMB', '2016-03-03 15:10:00',targetTimeZone=pytz.timezone('Asia/Colombo'))
    processor.save_manual_outliers('CMB', '2016-03-03 15:11:00', '2016-03-03 15:12:00', targetTimeZone=pytz.timezone('Asia/Colombo'))
    processor.save_manual_outliers('CMB', '2016-03-03 15:15:00', '2016-03-03 15:16:00', targetTimeZone=pytz.timezone('Asia/Colombo'))
    processor.save_manual_outliers('CMB', '2016-03-31 10:51:00', '2016-03-31 10:53:00', targetTimeZone=pytz.timezone('Asia/Colombo'))

    # Removing of month 2016-04 outlier values.    
    processor.save_manual_outliers('CMB', '2016-04-06 04:56:00','2016-04-06 05:15:00')
    
    # Removing of month 2016-05 outlier values.    
    processor.save_manual_outliers('CMB', '2016-05-26 01:45:00', '2016-05-26 01:46:00')
    processor.save_manual_outliers('CMB', '2016-05-26 09:39:00', targetTimeZone=pytz.timezone('Asia/Colombo'))
    processor.save_manual_outliers('CMB', '2016-05-26 15:25:00','2016-05-26 15:27:00')
    processor.save_manual_outliers('CMB', '2016-05-26 18:29:00')

    # Removing of month 2016-09 outlier values.    
    processor.save_manual_outliers('CMB', '2016-09-26 14:44:00', targetTimeZone=pytz.timezone('Asia/Colombo'))

    # Removing of month 2016-12 outlier values.    
    processor.save_manual_outliers('CMB', '2016-12-01 06:26:00')
    processor.save_manual_outliers('CMB', '2016-12-01 12:02:00', '2016-12-01 12:04:00', targetTimeZone=pytz.timezone('Asia/Colombo'))

if command=='read_ee_index_data':
    import common_MagdasDB as magdasDB
    import pytz as pytz
    import matplotlib.pyplot as plt
    import numpy as np
    import common_DataProcess as processor
    from datetime import datetime

    df_ee_index = magdasDB.getEEIndex('CMB',year='2016')
    #outliers = processor.get_outliers_confirmed_in_range('CMB', utc_start_time=df_ee_index.index.values[0], utc_end_time=df_ee_index.index.values[-1])
    df_ee_index = processor.get_ee_index_data_in_range(df_ee_index, datetime(year=2016,month=1, day=1), datetime(year=2016, month=12, day=31, hour=23, minute=59))

    #df_ee_index = df_ee_index.loc[df_ee_index.EUEL<99000]
    print(df_ee_index)
    fig, axs = plt.subplots(4, 1, sharex=True)
    fig.subplots_adjust(hspace=0)
    axs[0].plot(df_ee_index.index, df_ee_index['EUEL'], label='EUEL')
    axs[1].plot(df_ee_index.index, df_ee_index['ER'], label='ER')
    axs[2].plot(df_ee_index.index, df_ee_index['EDst6h'], label='EDst6h')
    axs[3].plot(df_ee_index.index, df_ee_index['EDst1h'], label='EDst1h')
    axs[0].legend()
    axs[1].legend()
    axs[2].legend()
    axs[3].legend()
    #plt.plot(df_ee_index.index, df_ee_index['EUEL'])
    plt.show()