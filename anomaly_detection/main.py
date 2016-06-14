__author__ = 'huanpc'

from pyculiarity import detect_ts
import pandas as pd
import json
import os
import datetime

def detect_anomaly():
    twitter_example_data = pd.read_csv('1.csv',usecols=['timestamp', 'count'])
    results = detect_ts(twitter_example_data,
                        max_anoms=0.02,
                        direction='both', only_last='day')
    print results['anoms'].iloc[:,1]

def convert_raw_data():
    with open("./1.json") as data_file:
        json_data = json.load(data_file)
        data_points = json_data[0]['datapoints']
        try:
            dir = os.path.dirname("./1.csv")
            if not os.path.exists(dir):
                os.makedirs(dir)
            f = open("./1.csv", 'w')
            f.write('"", '+'"timestamp"'+', "count" \n')
            index = 0
            for item in data_points:
                index+=1
                f.write('"'+str(index)+'"'+', '+str(convert_timestamp_to_datetime(item[1]))+', '+str(item[0])+'\n')
        finally:
            f.close()
            return


def convert_timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')


def write_to_file(file_path,data):
    try:
        dir = os.path.dirname(file_path)
        if not os.path.exists(dir):
            os.makedirs(dir)
        f = open(file_path, 'w')
        f.write(data+'\n')
        f.close()
        return True
    except:
        return False

if __name__ == '__main__':
    # convert from json to csv
    convert_raw_data()
    # run dectect
    # detect_anomaly()
