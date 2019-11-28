
line_format = '{0}\t{1}\t{2:6.2f}\t{3:6.2f}\t{4:6.2f}\t{5:6.2f}' # 0-UTC_Time 1-Date_Time 2-H 3-D 4-Z 5-F
write_file_format = '{0}_{1}_Generated.txt' # StationCode_MIN_Generated.txt. eg:CMB_Min_Generated.txt
default_read_file_format = '{0}_{1}_Confirmed.txt' # StationCode_MIN_Confirmed.txt. eg:CMB_Min_Confirmed.txt
manual_outlier_file_format = '{0}_{1}_Manual_Removed.txt' # StationCode_MIN_Manual_Removed.txt. eg:CMB_Min_Manual_Removed.txt
manual_outlier_confirmed_file_format = '{0}_{1}_Manual_Removed.txt' #'{0}_{1}_Manual_Confirmed.txt'
header = 'UTC_Time'.rjust(25) + '\t' + 'Date_Time'.rjust(25) + '\t' + 'H'.rjust(8) + '\t' + 'D'.rjust(7) + '\t' + 'Z'.rjust(7) + '\t' + 'F'.rjust(7)
base_path = './/Data_Files//Outliers//'

def write_outliers_to_file(station_code, outliers, min_or_sec='Min'):
    import os

    write_file = write_file_format.format(station_code, min_or_sec)
    relative_path = os.path.relpath( base_path + write_file, '.') 
    marked_outliers = mark_as_outlier(outliers.copy(deep=True))

    save_to_file(relative_path, marked_outliers, station_code, min_or_sec)

def write_manual_outliers_to_file(station_code, outliers, min_or_sec='Min', comp_name = None):
    import os

    write_file = manual_outlier_file_format.format(station_code, min_or_sec)
    relative_path = os.path.relpath( base_path + write_file, '.')
    marked_outliers = mark_as_outlier(outliers.copy(deep=True), comp_name = comp_name)

    save_to_file(relative_path, marked_outliers, station_code, min_or_sec)

def save_to_file(relative_path, marked_outliers, station_code, min_or_sec):
    import os

    if os.path.exists(relative_path): 
        existing_outliers = read_outliers_from_file(relative_path)
        conbined_outliers = concatinate_outliers(existing_outliers, marked_outliers)
        write_df_to_file(relative_path, station_code, conbined_outliers, min_or_sec)
    else:
        write_df_to_file(relative_path, station_code, marked_outliers, min_or_sec)

def mark_as_outlier(outliers, comp_name = None):
    if comp_name is None:
        # mark all columns as outlires (as True)
        outliers['H'] = True
        outliers['D'] = True
        outliers['Z'] = True
        outliers['F'] = True
        return outliers
    else:
        # mark only the given column as outliers (as True)
        outliers[comp_name] = True
        return outliers

def concatinate_outliers(existing_outliers, new_outliers):
    
    for index, row in new_outliers.iterrows():
        if index in existing_outliers.index:
            if row['H']==True:
                existing_outliers.loc[index, 'H'] = True
            if row['D']==True:
                existing_outliers.loc[index, 'D'] = True
            if row['Z']==True:
                existing_outliers.loc[index, 'Z'] = True
            if row['F']==True:
                existing_outliers.loc[index, 'F'] = True
        else:
            existing_outliers = existing_outliers.append(row)
    
    return existing_outliers


def write_df_to_file(relative_path, station_code, df, min_or_sec='Min'):    
    import os

    df.sort_index(inplace=True)
    with open(relative_path, 'w') as f:
        f.write("%s\n" % header)
        for index, row in df.iterrows():
            #line = line_format.format(index.strftime('%Y-%m-%d %H:%M:%S %z'), row['Date_Time'].strftime('%Y-%m-%d %H:%M:%S %z')
            #, row['H'], row['D'], row['Z'], row['F'])
            line = line_format.format(index.strftime('%Y-%m-%d %H:%M:%S %z'), row['Date_Time'].strftime('%Y-%m-%d %H:%M:%S %z'), row['H'], row['D'], row['Z'], row['F'])
            #print(line)
            f.write("%s\n" % line)

def read_confirmed_outliers(station_code, min_or_sec='Min', comp_name=None):        
    import os

    confirmed_file = default_read_file_format.format(station_code, min_or_sec)
    relative_path_confirmed_file = os.path.relpath( './'+ base_path + confirmed_file, '.')
    confirmded_file_outliers = read_outliers_from_file(relative_path_confirmed_file, comp_name)

    manual_file = manual_outlier_confirmed_file_format.format(station_code, min_or_sec)
    relative_path_manual_file = os.path.relpath( './'+ base_path + manual_file, '.')
    manual_removed_outliers = read_outliers_from_file(relative_path_manual_file, comp_name)

    to_appended = manual_removed_outliers.loc[~manual_removed_outliers.index.isin(confirmded_file_outliers.index)]
    confirmed_and_manual_outliers = confirmded_file_outliers.append(to_appended)

    return confirmed_and_manual_outliers

def read_outliers_from_file(relative_path, comp_name = None):
    import pandas as pd
    import os

    if not os.path.exists(relative_path): 
        print('Error : File not exists. [' + relative_path + ']')
        return pd.DataFrame()
    print('Reading outliers from file : ' + relative_path)
    #outliers_df = pd.read_csv(relative_path, sep='\t', index_col=0, names=['Local_Time','H','D','Z','F'], header=1)
    outliers_df = pd.read_csv(relative_path, sep='\t', index_col=0, names=['Date_Time','H','D','Z','F'], header=0, parse_dates=[0]
    ,date_parser=dateparse)
    outliers_df.sort_index(inplace=True)
    if comp_name is None:
        return outliers_df
    else:
        return outliers_df.loc[outliers_df[comp_name]==True]

def dateparse (datetime_str):  
    import datetime
    return datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S %z')