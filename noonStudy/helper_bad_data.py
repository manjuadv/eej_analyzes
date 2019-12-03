
def get_sun_rise_noon_peak_bad_data_days(station_code, utc_start_time=None, utc_end_time=None):
    import pandas as pd
    import os

    file_name = '{0}.txt'.format(station_code)
    relative_path = os.path.relpath( './'+ './/Data_Files//Bad_data_points//noon_study//sun_rise_noon_peak//' + file_name, '.')

    if not os.path.exists(relative_path): 
        print('Error : File not exists. [' + relative_path + ']')
        return pd.DataFrame()
    print('Reading Dst data from file : ' + relative_path)
    #outliers_df = pd.read_csv(relative_path, sep='\t', index_col=0, names=['Local_Time','H','D','Z','F'], header=1)
    dst_data = pd.read_csv(relative_path, sep='\t', index_col=0, names=['Day'], header=0, parse_dates=[0]
    ,date_parser=dateparse)
    dst_data.sort_index(inplace=True)
    return dst_data.loc[(dst_data.index > utc_start_time) & (dst_data.index < utc_end_time)]

def dateparse (datetime_str):  
    import datetime
    return datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S %z')