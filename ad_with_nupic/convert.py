import json
import csv
from datetime import datetime


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

    for dp in datapoints:
        if count == 0:
            header = ['value', 'timestamp']
            csvwriter.writerow(header)
            count += 1
        elif count == 1:
            value_type = ['float', 'datetime']
            tmp = ['T', ]
            csvwriter.writerow(value_type)
            csvwriter.writerow(tmp)
            count += 2
        else:
            if dp[0] == 'null':
                continue
            else:
                tmp = [dp[0], datetime.fromtimestamp(
                    int(dp[1])).strftime('%Y-%m-%d %H:%M:%S')]
                csvwriter.writerow(tmp)
                del tmp

    print "Convert {} to {} " .format(json_path, csv_path)

    result.close()


if __name__ == '__main__':
    convert_json_to_csv('1.json')
