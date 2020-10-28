import csv
from enum import IntEnum
import json


class ADVariables(IntEnum):
    SYSTEM_ID = 0
    TAG_NAME = 1
    MOD_BUS_ADDRESS = 4


def read_csv(fileName):
    with open(fileName) as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        next(reader, None)  # skip the headers
        data_read = [row for row in reader]

    return data_read


if __name__ == '__main__':
    csv_data = list(read_csv("../Tags_01_extended.csv"))
    csv_data.remove(csv_data[0])

    usefulRowsOnly = [row for row in csv_data if not row[ADVariables.MOD_BUS_ADDRESS] == ""]

    print(print(json.dumps(usefulRowsOnly)))
