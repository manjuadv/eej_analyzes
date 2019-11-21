print('This python is script not developed to use with command line arguments.')
print('Procedure should be specified in this file.')


#command = 'generate_outliers'
command = 'check_written_outliers'

if command == 'generate_outliers':

    import common_DataProcess as processor
    import common_MagdasDB as magdasDB
    import pytz

    dataFrame = magdasDB.getMinData('CMB', '2016', '03', '31', targetTimeZone=pytz.timezone('Asia/Colombo'))

    processor.save_outliers('CMB',dataFrame)

if command == 'check_written_outliers':

    import common_file as file_access

    outliers = file_access.read_confirmed_outliers('CMB','Min')

    print(outliers)