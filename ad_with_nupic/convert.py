import json
import csv


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
            value_type = ['float', 'seconds']
            csvwriter.writerow(value_type)
            count += 2
        else:
            csvwriter.writerow(dp)

    print "Convert {} to {}" .format(json_path, csv_path)

    result.close()


if __name__ == '__main__':
    convert_json_to_csv('1.json')
