import urllib.request
import datetime as datetime
import pytz as pytz
import numpy as np
import pandas as pd
import os

def main():
    #download_provisional_dst_data(2015)
    #download_provisional_dst_data(2016)
    #download_realtime_dst_data(2017)
    #download_realtime_dst_data(2018)
    download_realtime_dst_data(2019)
        
def download_provisional_dst_data(year):
    url_format = "http://wdc.kugi.kyoto-u.ac.jp/dst_provisional/{0}/index.html"
    download_month = datetime.datetime(year, 1, 1)
    data_frame = download_dst_from_url(url_format.format(download_month.strftime('%Y%m')), year, 1)
    
    for month in range(2, 13):
        download_month = datetime.datetime(year, month, 1)
        data_frame = data_frame.append(download_dst_from_url(url_format.format(download_month.strftime('%Y%m')), year, month))

    data_frame.sort_index(inplace=True)
    append_dst_data_frame(data_frame, year)

def download_realtime_dst_data(year):
    url_format = "http://wdc.kugi.kyoto-u.ac.jp/dst_realtime/{0}/index.html"
    download_month = datetime.datetime(year, 1, 1)
    data_frame = download_dst_from_url(url_format.format(download_month.strftime('%Y%m')), year, 1)
    
    for month in range(2, 13):
        download_month = datetime.datetime(year, month, 1)
        data_frame = data_frame.append(download_dst_from_url(url_format.format(download_month.strftime('%Y%m')), year, month))

    data_frame.sort_index(inplace=True)
    append_dst_data_frame(data_frame, year)

def download_dst_from_url(url, year, month):
    print('Downloading data from {0}'.format(url))
    fp = urllib.request.urlopen(url)
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(fp,features="html5lib")
    local_tz = pytz.timezone('Asia/Colombo')
    dataSet = {'UTC_Time' : [], 'Local_Time' : [],'Dst' : []}
    for i, line in enumerate(soup.pre.text.splitlines()):
        #print(line)
        if i > 6 :
            line_parts = line.split()
            if len(line_parts) != 25:
                line = line.replace('-', ' -')
            line_parts = line.split()
            if len(line_parts) > 24:
                for h in range(1, 25):
                    utc_time = datetime.datetime(year, month, int(line_parts[0]), (int(h)-1), 0, 0, 0, tzinfo=pytz.UTC)
                    dataSet['UTC_Time'] = np.append(dataSet['UTC_Time'], utc_time)
                    dataSet['Local_Time'] = np.append(dataSet['Local_Time'], datetime.datetime.astimezone(utc_time, local_tz))
                    dataSet['Dst'] = np.append(dataSet['Dst'], int(line_parts[h]))
            elif len(line_parts) != 0:
                print('Error : All hours not represented in following line.')
                print (line)
                break


    data_frame = pd.DataFrame(data=dataSet, index=dataSet['UTC_Time'], columns=['Local_Time','Dst'])
    data_frame.sort_index(inplace=True)
    return data_frame


def append_dst_data_frame(data_frame, year):
    if data_frame.empty:
        return
    base_path = '..//..//noonStudy//Data_Files//Dst//'
    relative_path = os.path.relpath( base_path + 'Dst_{0}.txt'.format(year), '.') 

    line_format = '{0}\t{1}\t{2:6.2f}'
    header = 'UTC_Time'.rjust(25) + '\t' + 'Local_Time'.rjust(25) + '\t' + 'Dst'.rjust(8)
    with open(relative_path, 'w') as f:
        f.write("%s\n" % header)
        for index, row in data_frame.iterrows():
            line = line_format.format(index.strftime('%Y-%m-%d %H:%M:%S %z'), row['Local_Time'].strftime('%Y-%m-%d %H:%M:%S %z'), row['Dst'])
            f.write("%s\n" % line)

if __name__ == "__main__":
    main()
