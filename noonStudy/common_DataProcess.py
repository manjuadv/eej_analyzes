import numpy as np

def get_outliers_min_max_limit(df_in, col_name, min=0, max = 100000):
    df_out = df_in.loc[(df_in[col_name] < min) | (df_in[col_name] > max)]
    return df_out

def get_outliers_abnormal_ignore(data_frame, component, min=0, max = 100000):
    import pandas as pd
    #new_df = pd.DataFrame(columns=['Date_Time','H','D','Z','F'])
    index_list_to_drop = []
    for index, row in data_frame.iterrows():
        #print (str(index) + ' : ' + str(row['H']) + ',' + str(row['D']))
        if row[component]< 40860 or row[component]>40940:
            index_list_to_drop.append(index)
    return data_frame.drop(index_list_to_drop)


def get_outliers_median(df_in, col_name):
    df_out = df_in.loc[(df_in[col_name] < 40860) | (df_in[col_name] > 40980)]
    return df_out

def get_outliers_quantile_scale(df_in, col_name, interquartile_range_scale = 1.5):
    import numpy as np
    q1 = df_in[col_name].quantile(0.25)
    q3 = df_in[col_name].quantile(0.75)
    iqr = q3-q1 #Interquartile range
    fence_low  = q1-interquartile_range_scale*iqr
    fence_high = q3+interquartile_range_scale*iqr
    df_out = df_in.loc[(df_in[col_name] < fence_low) | (df_in[col_name] > fence_high)]
    return df_out

def get_outliers_z_score(dataFrame, component, threshold = 3):
    from scipy import stats
    import numpy as np
    dataFrame[component + '_z'] = np.abs(stats.zscore(dataFrame[component]))
    print('z-score')
    print(dataFrame)
    df_out = dataFrame.loc[(dataFrame[component + '_z'] > threshold)]
    return df_out

def get_outliers_rolling_medians(dataFrame, component, threshold = 3):
    from pandas import rolling_median

    dataFrame['r_median'] = rolling_median(dataFrame[component], window=3, center=True).fillna(method='bfill').fillna(method='ffill')
    dataFrame['diff'] = np.abs(dataFrame[component] - dataFrame['r_median'])
    df_out = dataFrame.loc[(dataFrame['diff'] > threshold)]
    return df_out

def get_outliers_normal_distribution(dataFrame, component, SD_range_scalar = 2):
    import numpy as np
    mean = dataFrame[component].mean()
    std = dataFrame[component].std()
    df_out = dataFrame.loc[(dataFrame[component] < (mean - SD_range_scalar * std)) | (dataFrame[component] > (mean + SD_range_scalar * std))]
    return df_out