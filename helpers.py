import csv

# creates dictionary containing all information about courses
def parse_csv():
    class_dict = {}
    # read in CSV file with all course info
    with open('class_times.csv', 'rb') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)
        for line in csvreader:
            class_dict[line[0]] = {
                'semester': [bool(line[1]), bool(line[2])],
                'days': [bool(line[3]), bool(line[4]), bool(line[5]), bool(line[6]), bool(line[7])],
                'times': [float(line[8]), float(line[9])]
            }
    return class_dict

def get_slot_from_index(index):
    year = index / 12
    semester = int(index % 12 >= 6)
    slot = index % 6
    return {
        'year': year,
        'semester': semester,
        'slot': slot
    }

