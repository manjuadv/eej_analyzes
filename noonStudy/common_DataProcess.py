import numpy as np

def get_outliers_min_max_limit(df_in, col_name, min=0, max = 100000):
    print('Started : get_outliers_min_max_limit')
    df_out = df_in.loc[(df_in[col_name] < min) | (df_in[col_name] > max)]
    print('Done : get_outliers_min_max_limit')
    return df_out

def get_outliers_abnormal_ignore(data_frame, component, min=0, max = 100000):
    import pandas as pd
    print('Started : get_outliers_abnormal_ignore')
    index_list_to_drop = []
    for index, row in data_frame.iterrows():
        if row[component]< min or row[component]>max:
            index_list_to_drop.append(index)
            # More logic can be integrated here
    result = data_frame.loc[index_list_to_drop]
    print('Done : get_outliers_abnormal_ignore')
    return result

def get_outliers_abnormal_slope_ignore(data_frame, component, min=0, max = 100000):
    import pandas as pd

    print('Started : get_outliers_abnormal_slope_ignore')
    index_list_to_drop = []
    for index, row in data_frame.iterrows():
        int_index = data_frame.index.get_loc(index)
        if int_index > 1 and abs(data_frame.iloc[int_index][component] - data_frame.iloc[int_index - 1][component]) > 100:
            index_list_to_drop.append(index)
            # More logic can be integrated here
    result = data_frame.loc[index_list_to_drop]
    print('Done : get_outliers_abnormal_slope_ignore')
    return result

def get_outliers_median(df_in, col_name):
    print('Started : get_outliers_median')
    df_out = df_in.loc[(df_in[col_name] < 40860) | (df_in[col_name] > 40980)]
    print('Done : get_outliers_median')
    return df_out

def get_outliers_quantile_scale(df_in, col_name, interquartile_range_scale = 1.5):
    import numpy as np

    print('Started : get_outliers_quantile_scale')

    q1 = df_in[col_name].quantile(0.25)
    q3 = df_in[col_name].quantile(0.75)
    iqr = q3-q1 #Interquartile range
    fence_low  = q1-interquartile_range_scale*iqr
    fence_high = q3+interquartile_range_scale*iqr
    df_out = df_in.loc[(df_in[col_name] < fence_low) | (df_in[col_name] > fence_high)]
    print('Done : get_outliers_quantile_scale')
    return df_out

def get_outliers_z_score(dataFrame, component, threshold = 3):
    from scipy import stats
    import numpy as np

    print('Started : get_outliers_z_score')

    dataFrame[component + '_z'] = np.abs(stats.zscore(dataFrame[component]))
    df_out = dataFrame.loc[(dataFrame[component + '_z'] > threshold)]
    print('Done : get_outliers_z_score')
    return df_out

def get_outliers_rolling_medians(dataFrame, component, threshold = 3):
    from pandas import rolling_median

    print('Started : get_outliers_rolling_medians')

    dataFrame['r_median'] = rolling_median(dataFrame[component], window=3, center=True).fillna(method='bfill').fillna(method='ffill')
    dataFrame['diff'] = np.abs(dataFrame[component] - dataFrame['r_median'])
    df_out = dataFrame.loc[(dataFrame['diff'] > threshold)]
    print('Done : get_outliers_rolling_medians')
    return df_out

def get_outliers_normal_distribution(dataFrame, component, SD_range_scalar = 2):
    import numpy as np

    print('Started : get_outliers_normal_distribution')
    mean = dataFrame[component].mean()
    std = dataFrame[component].std()
    df_out = dataFrame.loc[(dataFrame[component] < (mean - SD_range_scalar * std)) | (dataFrame[component] > (mean + SD_range_scalar * std))]
    print('Done : get_outliers_normal_distribution')
    return df_out