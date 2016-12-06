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

def parse_geneds():
    geneds = ["AI", "CB", "EMR", "ER", "SLS", "SP", "SPU", "SW", "USW"]
    ai_dict, cb_dict, emr_dict, er_dict, sls_dict, sp_dict, spu_dict, sw_dict, usw_dict = {}, {}, {}, {}, {}, {}, {}, {}, {}
    dicts = [ai_dict, cb_dict, emr_dict, er_dict, sls_dict, sp_dict, spu_dict, sw_dict, usw_dict]

    for i in range(len(geneds)):
        with open(geneds[i] + '.csv', 'rb') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader, None)
            class_dict = dicts[i]
            prev = None
            for line in csvreader:
                # mark with catalog number
                if not line[11] == "":
                    if line[0] == "":
                        class_dict[prev]['days'][int(line[11]) - 1] = True
                    else:
                        class_dict[int(line[0])] = {
                            'class_name': geneds[i] + line[4] + line[5],
                            'semester': [line[1] == 'FALL', line[1] == 'SPRING'],
                            'days': [line[11]  == '1', line[11]  == '2', line[11]  == '3', line[11]  == '4', line[11]  == '5'],
                            'times': [line[14].replace(":", "")[0:4], line[15].replace(":", "")[0:4]]
                        }
                        prev = int(line[0])
    return dicts

def get_slot_from_index(index):
    year = index / 12
    semester = int(index % 12 >= 6)
    slot = index % 6
    return {
        'year': year,
        'semester': semester,
        'slot': slot
    }
