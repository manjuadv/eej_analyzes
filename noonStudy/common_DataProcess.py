import numpy as np
import enum

class FilterType(enum.Enum):
    ABNORMAL_IGNORE_BY_MIN_MAX = 'Abnormal ignore by min max'
    UNREAL_TOTAL_FIELD = 'Unreal total field'
    ABNORMAL_IGNORE_BY_SUDDEN_INCREASE = 'Abnormal ignore by sudden increase'
    Z_SCORE = 'Z-score'
    NORMAL_DISTRIBUTION = 'Normal distribution'
    QAUANTILE = 'quantile'
    ROLLING_MEDIANS = 'Rolling Medians'

class OutlierFilter():
    def __init__(self, filter_type, **kwargs):
        self.__dict__.update(kwargs)
        self.filter_type = filter_type

class FilterList():
    def __init__(self, ab_ignore_min_max=None, ab_ignore_sudden_inc=None, 
    z_score=None, normal_disb=None, quantile=None, rolling_medians=None, unreal_total_field=None):
        self.ab_ignore_min_max = ab_ignore_min_max
        self.ab_ignore_sudden_inc = ab_ignore_sudden_inc
        self.z_score = z_score
        self.normal_disb = normal_disb
        self.quantile = quantile
        self.rolling_medians = rolling_medians
        self.unreal_total_field = unreal_total_field

def get_outliers_multiple_filter(data_frame, component, filter_list):
    import pandas as pd
    from scipy import stats
    import math

    print('Started : get_outliers_multiple_filter')

    if filter_list.z_score is not None:
        data_frame[component + '_z'] = np.abs(stats.zscore(data_frame[component]))
        print('Z-score calculation done.')
    if filter_list.normal_disb is not None:
        mean = data_frame[component].mean()
        std = data_frame[component].std()
        print('Mean and std calculation done.')
    if filter_list.quantile is not None:
        q1 = data_frame[component].quantile(0.25)
        q3 = data_frame[component].quantile(0.75)
        iqr = q3-q1 #Interquartile range
        fence_low  = q1 - filter_list.quantile.interquartile_range_scale*iqr
        fence_high = q3 + filter_list.quantile.interquartile_range_scale*iqr
        print('quantile calculation done.')
    if filter_list.rolling_medians is not None:
        from pandas import rolling_median
        data_frame['r_median'] = rolling_median(data_frame[component], window=3, center=True).fillna(method='bfill').fillna(method='ffill')
        data_frame['r_median_diff'] = np.abs(data_frame[component] - data_frame['r_median'])
        print('Rolling calculation done.')

    index_list_to_drop = []
    for index, row in data_frame.iterrows():
        if filter_list.ab_ignore_min_max is not None:
            if row[component]< filter_list.ab_ignore_min_max.min or row[component]> filter_list.ab_ignore_min_max.max:
                index_list_to_drop.append(index)
        if filter_list.unreal_total_field is not None:
            if math.isnan(row['F']) or row['F'] < filter_list.unreal_total_field.total_field_min or row['F']> filter_list.unreal_total_field.total_field_max:
                index_list_to_drop.append(index)
        if filter_list.ab_ignore_sudden_inc is not None:
            int_index = data_frame.index.get_loc(index)
            if int_index > 1 and abs(row[component] - data_frame.iloc[int_index - 1][component]) > filter_list.ab_ignore_sudden_inc.threshold:
                index_list_to_drop.append(index)
        if filter_list.z_score is not None:
            if row[component + '_z'] > filter_list.z_score.threshold:
                index_list_to_drop.append(index)
        if filter_list.normal_disb is not None:
            if (row[component] < (mean - filter_list.normal_disb.SD_range_scalar * std)) or (row[component] > (mean + filter_list.normal_disb.SD_range_scalar * std)):
                index_list_to_drop.append(index)
        if filter_list.quantile is not None:
            if (row[component] < fence_low) or (row[component] > fence_high):
                index_list_to_drop.append(index)
        if filter_list.rolling_medians is not None:
            if row['r_median_diff'] > filter_list.rolling_medians.threshold:         
                index_list_to_drop.append(index)
            
    result = data_frame.loc[index_list_to_drop]
    print('Done : get_outliers_multiple_filter')
    return result

def save_outliers(station_code, outliers_df):

    import common_file as file_acces
    if outliers_df.empty:
        print('No data set is empty')
        return
    elif len(outliers_df)<1:
        print('No data set is empty')
        return

    file_acces.write_outliers_to_file(station_code, outliers_df)

def get_outliers_from_file(station_code, min_or_sec='Min'):

    import common_file as file_access

    outliers = file_access.read_confirmed_outliers(station_code, min_or_sec)

    return outliers



# def get_outliers_min_max_limit(df_in, col_name, min=0, max = 100000):
#     print('Started : get_outliers_min_max_limit')
#     df_out = df_in.loc[(df_in[col_name] < min) | (df_in[col_name] > max)]
#     print('Done : get_outliers_min_max_limit')
#     return df_out

# def get_outliers_abnormal_ignore(data_frame, component, min=0, max = 100000):
#     import pandas as pd
#     print('Started : get_outliers_abnormal_ignore')
#     index_list_to_drop = []
#     for index, row in data_frame.iterrows():
#         if row[component]< min or row[component]>max:
#             index_list_to_drop.append(index)
#             # More logic can be integrated here
#     result = data_frame.loc[index_list_to_drop]
#     print('Done : get_outliers_abnormal_ignore')
#     return result

# def get_outliers_abnormal_slope_ignore(data_frame, component, min=0, max = 100000):
#     import pandas as pd

#     print('Started : get_outliers_abnormal_slope_ignore')
#     index_list_to_drop = []
#     for index, row in data_frame.iterrows():
#         int_index = data_frame.index.get_loc(index)
#         if int_index > 1 and abs(data_frame.iloc[int_index][component] - data_frame.iloc[int_index - 1][component]) > 100:
#             index_list_to_drop.append(index)
#             # More logic can be integrated here
#     result = data_frame.loc[index_list_to_drop]
#     print('Done : get_outliers_abnormal_slope_ignore')
#     return result

# def get_outliers_median(df_in, col_name):
#     print('Started : get_outliers_median')
#     df_out = df_in.loc[(df_in[col_name] < 40860) | (df_in[col_name] > 40980)]
#     print('Done : get_outliers_median')
#     return df_out

# def get_outliers_quantile_scale(df_in, col_name, interquartile_range_scale = 1.5):
#     import numpy as np

#     print('Started : get_outliers_quantile_scale')

#     q1 = df_in[col_name].quantile(0.25)
#     q3 = df_in[col_name].quantile(0.75)
#     iqr = q3-q1 #Interquartile range
#     fence_low  = q1-interquartile_range_scale*iqr
#     fence_high = q3+interquartile_range_scale*iqr
#     df_out = df_in.loc[(df_in[col_name] < fence_low) | (df_in[col_name] > fence_high)]
#     print('Done : get_outliers_quantile_scale')
#     return df_out

# def get_outliers_z_score(dataFrame, component, threshold = 3):
#     from scipy import stats
#     import numpy as np

#     print('Started : get_outliers_z_score')

#     dataFrame[component + '_z'] = np.abs(stats.zscore(dataFrame[component]))
#     #print(dataFrame)
#     df_out = dataFrame.loc[(dataFrame[component + '_z'] > threshold)]
#     print('Done : get_outliers_z_score')
#     return df_out

# def get_outliers_rolling_medians(dataFrame, component, threshold = 3):
#     from pandas import rolling_median

#     print('Started : get_outliers_rolling_medians')

#     dataFrame['r_median'] = rolling_median(dataFrame[component], window=3, center=True).fillna(method='bfill').fillna(method='ffill')
#     dataFrame['diff'] = np.abs(dataFrame[component] - dataFrame['r_median'])
#     df_out = dataFrame.loc[(dataFrame['diff'] > threshold)]
#     print('Done : get_outliers_rolling_medians')
#     return df_out

# def get_outliers_normal_distribution(dataFrame, component, SD_range_scalar = 2):
#     import numpy as np

#     print('Started : get_outliers_normal_distribution')
#     mean = dataFrame[component].mean()
#     std = dataFrame[component].std()
#     df_out = dataFrame.loc[(dataFrame[component] < (mean - SD_range_scalar * std)) | (dataFrame[component] > (mean + SD_range_scalar * std))]
#     print('Done : get_outliers_normal_distribution')
#     return df_out