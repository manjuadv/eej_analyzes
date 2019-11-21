
line_format = '{0}\t{1}\t{2:6.2f}\t{3:6.2f}\t{4:6.2f}\t{5:6.2f}' # 0-UTC_Time 1-Local_Time 2-H 3-D 4-Z 5-F
write_file_format = '{0}_{1}_Generated.txt' # StationCode_MIN_Generated.txt. eg:CMB_Min_Generated.txt
default_read_file_format = '{0}_{1}_Confirmed.txt' # StationCode_MIN_Confirmed.txt. eg:CMB_Min_Confirmed.txt
header = 'UTC_Time'.rjust(25) + '\t' + 'Local_Time'.rjust(25) + '\t' + 'H'.rjust(8) + '\t' + 'D'.rjust(7) + '\t' + 'Z'.rjust(7) + '\t' + 'F'.rjust(7)
base_path = './/Data_Files//Outliers//'

def write_outliers_to_file(station_code, outliers, min_or_sec='Min'):

    import os

    write_file = write_file_format.format(station_code, min_or_sec)
    relative_path = os.path.relpath( base_path + write_file, '.') 

    if os.path.exists(relative_path): 
        #existing_outliers = read_confirmed_outliers(station_code,min_or_sec=min_or_sec, file_name=relative_path)
        #conbined_outlier = existing_outliers.append(outliers)
        print('TODO: concatinating with existing outliers')
        write_df_to_file(relative_path, station_code, outliers, min_or_sec)
    else:
        write_df_to_file(relative_path, station_code, outliers, min_or_sec)

def write_df_to_file(relative_path, station_code, df, min_or_sec='Min'):
    
    import os

    df.sort_index(inplace=True)
    with open(relative_path, 'w') as f:
        f.write("%s\n" % header)
        for index, row in df.iterrows():
            line = line_format.format(index.strftime('%Y-%m-%d %H:%M:%S %z'), row['Date_Time'].strftime('%Y-%m-%d %H:%M:%S %z')
            , row['H'], row['D'], row['Z'], row['F'])
            #print(line)
            f.write("%s\n" % line)

def read_confirmed_outliers(station_code, min_or_sec='Min', file_name=None):
        
    import os
    import pandas as pd

    if file_name is not None:
        relative_path = file_name
    else:
        read_file = default_read_file_format.format(station_code, min_or_sec)
        relative_path = os.path.relpath( './'+ base_path + read_file, '.') 
    outliers_df = pd.read_csv(relative_path, sep='\t', index_col=0, names=['Local_Time','H','D','Z','F'], header=1)
    outliers_df.sort_index(inplace=True)
    #print(outliers_df)
    return outliers_df

            