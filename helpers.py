import csv

def parse_csv():
    class_dict = {}
    # read in CSV file with all course info
    with open('class_times.csv', 'rb') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)
        for line in csvreader:
            class_dict[line[0]] = {
                'fall': bool(line[1]),
                'spring': bool(line[2]),
                'mon': bool(line[3]),
                'tues': bool(line[4]),
                'wed': bool(line[5]),
                'thurs': bool(line[6]),
                'fri': bool(line[7]),
                'start_time': float(line[8]),
                'end_time': float(line[9])
            }
    return class_dict
