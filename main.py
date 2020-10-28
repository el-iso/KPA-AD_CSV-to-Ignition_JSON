import csv

def read_csv(fileName):
    with open(fileName) as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        # next(reader, None)  # skip the headers
        data_read = [row for row in reader]

    return data_read

if __name__ == '__main__':
    csv_data = read_csv("../Tags_01_extended.csv")
    print(csv_data)


