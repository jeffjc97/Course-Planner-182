import csv

# creates dictionary containing all information about courses
def parse_csv():
    class_dict = {}
    # read in CSV file with all course info
    with open('class_times.csv', 'rb') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)
        for line in csvreader:
            class_dict[int(line[10])] = {
                'class_name': line[0],
                'semester': [line[1] == 'TRUE', line[2] == 'TRUE'],
                'days': [line[3]  == 'TRUE', line[4]  == 'TRUE', line[5]  == 'TRUE', line[6]  == 'TRUE', line[7]  == 'TRUE'],
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

