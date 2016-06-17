import json
import csv
from datetime import datetime

import swarm_description
from swarm_description import set_swarm_description

MAX = 0.0
MIN = 0.0


def convert_json_to_csv(json_path, csv_path='test.csv'):
    # open input json file

    with open(json_path) as data_file:
        data = json.load(data_file)

    datapoints = data[0]['datapoints']

    # open a file for writing

    result = open(csv_path, 'w')

    # create the csv writer object

    csvwriter = csv.writer(result)

    count = 0
    global MAX, MIN

    for dp in datapoints:
        if count == 0:
            header = ['value', 'timestamp']
            csvwriter.writerow(header)
            count += 1
        elif count == 1:
            value_type = ['float', 'datetime']
            tmp = ['', 'T']
            csvwriter.writerow(value_type)
            csvwriter.writerow(tmp)
            count += 2
        else:
            if dp[0] is None:
                continue
            else:
                if MAX <= float(dp[0]):
                    MAX = float(dp[0])
                if MIN > float(dp[0]):
                    MIN = float(dp[0])
                tmp = [dp[0], datetime.fromtimestamp(
                    int(dp[1])).strftime('%Y-%m-%d %H:%M:%S')]
                csvwriter.writerow(tmp)
                del tmp

    print "Convert {} to {}. Max Value = {} and Min Value = {}" \
        . format(json_path, csv_path, MAX, MIN)

    set_swarm_description(csv_path, MAX, MIN)

    result.close()

if __name__ == '__main__':
    convert_json_to_csv('test.json')
