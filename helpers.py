#
# general helper functions used throughout the code
#

import csv

total_slots = 32


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
                'days': [line[3] == 'TRUE', line[4]  == 'TRUE', line[5] == 'TRUE', line[6] == 'TRUE', line[7] == 'TRUE'],
                'times': [float(line[8]), float(line[9])],
                'gened': 'concentration'
            }
    return class_dict


# converting time from csv to usable format
# '1430' -> 14.5
def convert_time(time):
    a = int(time)
    decimal_hour = float(a % 100) / 60
    hour = a / 100
    return hour + decimal_hour


# parse CSVs for all gen eds and return a single dictionary
def parse_geneds_single_dict():
    geneds = ["AI", "CB", "EMR", "ER", "SLS", "SP", "SPU", "SW", "USW"]
    gen_ed_dict = {}
    for i in range(len(geneds)):
        with open(geneds[i] + '.csv', 'rb') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader, None)
            prev = None
            for line in csvreader:
                # mark with catalog number
                if not line[11] == "":
                    if line[0] == "":
                        gen_ed_dict[prev]['days'][int(line[11]) - 1] = True
                    else:
                        gen_ed_dict[int(line[0])] = {
                            'class_name': geneds[i] + line[4],
                            'semester': [line[1] == 'FALL', line[1] == 'SPRING'],
                            'days': [line[11] == '1', line[11] == '2', line[11] == '3', line[11] == '4', line[11] == '5'],
                            'times': [convert_time(line[14].replace(":", "")[0:4]), convert_time(line[15].replace(":", "")[0:4])],
                            'gened': geneds[i]
                        }
                        prev = int(line[0])
    return gen_ed_dict


# parse CSVs for all gen eds and returns a list of dictionaries
def parse_geneds():
    geneds = ["AI", "CB", "EMR", "ER", "SLS", "SP", "SPU", "SW", "USW"]
    ai_dict, cb_dict, emr_dict, er_dict, sls_dict, sp_dict, spu_dict, sw_dict, usw_dict = {}, {}, {}, {}, {}, {}, {}, {}, {}
    dicts = [ai_dict, cb_dict, emr_dict, er_dict, sls_dict, sp_dict, spu_dict, sw_dict, usw_dict]
    class_dict = {}
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
                            'class_name': geneds[i] + line[4],
                            'semester': [line[1] == 'FALL', line[1] == 'SPRING'],
                            'days': [line[11] == '1', line[11] == '2', line[11] == '3', line[11] == '4', line[11] == '5'],
                            'times': [convert_time(line[14].replace(":", "")[0:4]), convert_time(line[15].replace(":", "")[0:4])],
                            'gened': geneds[i]
                        }
                        prev = int(line[0])
    return dicts


# create a dictionary keyed by class name and valued by course ID for easy lookups
def get_course_id_dict():
    id_dict = {}
    # read in CSV file with all course info
    with open('class_times.csv', 'rb') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)
        for line in csvreader:
            # key: class name, value: course ID
            id_dict[line[0]] = int(line[10])
    return id_dict


# get Year, Semester and Slot from a slot index
# ex. 3 -> Freshman fall, slot 4
def get_slot_from_index(index):
    year = index / 8
    semester = int(index % 8 >= 4)
    slot = index % 4
    return {
        'year': year,
        'semester': semester,
        'slot': slot
    }


# get prerequisite course IDs for each course
def get_prereqs():
    return {
        # CS61: CS50
        3: [1],
        # CS109A: CS50, STAT110
        6: [1, 63],
        # CS109B: CS109A
        7: [6],
        # CS121: Discrete Math (CS20)
        10: [1],
        # CS141: programming experience
        14: [1],
        # CS143: CS50 recommended
        15: [1],
        # CS148: CS141
        18: [14],
        # CS152: CS51, CS121
        19: [2, 8],
        # CS153: CS51, CS61
        20: [2, 3],
        # CS161: CS61
        21: [3],
        # CS165: CS51, CS61
        23: [2, 3],
        # CS171: (CS50 programming experience)
        24: [1],
        # CS179: (CS50 programming experience)
        26: [1],
        # CS181: CS51, CS121, STAT110
        27: [2, 8, 63],
        # CS182: CS51, CS121
        28: [2, 8],
    }


# creating constraint domains
# must take 2 of the 3 classes
def constraint_cs50_cs51_cs61():
    constraints = []
    id_from_course = {
        50: 1,
        51: 2,
        61: 3
    }
    for a in range(total_slots):
        for b in range(a + 1, total_slots):
            a_time = get_slot_from_index(a)
            b_time = get_slot_from_index(b)
            # b will always be a bigger slot, either later year or same year
            if a_time['year'] < b_time['year']:
                # if they're both in the fall and one is before the other, always do 50 first
                if a_time['semester'] == 0 and b_time['semester'] == 0:
                    constraints.append({
                        a: id_from_course[50],
                        b: id_from_course[61]
                    })
                # else if one's in the spring and one's in the fall, either 50 or 61 in the fall and 51 in the spring
                elif a_time['semester'] == 0 and b_time['semester'] == 1:
                    constraints.append({
                        a: id_from_course[50],
                        b: id_from_course[51]
                    })
                    constraints.append({
                        a: id_from_course[61],
                        b: id_from_course[51]
                    })
                elif a_time['semester'] == 1 and b_time['semester'] == 0:
                    constraints.append({
                        a: id_from_course[51],
                        b: id_from_course[61]
                    })
            elif a_time['year'] == b_time['year']:
                if a_time['semester'] == 0 and b_time['semester'] == 0:
                    constraints.append({
                        a: id_from_course[50],
                        b: id_from_course[61]
                    })
                elif a_time['semester'] == 0 and b_time['semester'] == 1:
                    constraints.append({
                        a: id_from_course[50],
                        b: id_from_course[51]
                    })
                    constraints.append({
                        a: id_from_course[61],
                        b: id_from_course[51]
                    })
                # shouldn't happen
                elif a_time['semester'] == 1 and b_time['semester'] == 0:
                    constraints.append({
                        a: id_from_course[51],
                        b: id_from_course[61]
                    })
    return constraints

# creating constraint domains
# must take 1 of the 2 courses
def constraint_cs121_cs125():
    constraints = []
    id_from_course = {
        121: 8,
        125: 9,
    }
    for a in range(total_slots):
        a_time = get_slot_from_index(a)
        if a_time['semester'] == 0:
            constraints.append({
                a: id_from_course[121]
            })
            constraints.append({
                a: id_from_course[125]
            })
    return constraints


# creating constraint domains
# must take 1 of the 4 courses
def constraint_cs124_cs127_apmth106_apmth107():
    constraints = []
    id_from_course = {
        124: 10,
        127: 11,
        106: 55,
        107: 56
    }
    for a in range(total_slots):
        a_time = get_slot_from_index(a)
        if a_time['semester'] == 1:
            constraints.append({
                a: id_from_course[124]
            })
            constraints.append({
                a: id_from_course[127]
            })
            constraints.append({
                a: id_from_course[106]
            })
            constraints.append({
                a: id_from_course[107]
            })
    return constraints


# creating constraint domains
# given a user's input of which courses they want to take, create constraint
# must take one lin alg class and one multi class
def constraint_math(linalg, multi):
    # linalg: 21b, 23a, 25a, 55a
    # multi: 21a, 23b, 25b, 55b

    constraints = []
    id_from_course = {
        "MATH21A": [38, 39, 40, 41, 42, 43],
        "MATH21B": [44, 45, 46, 47],
        "MATH23A": [48],
        "MATH23B": [49],
        "MATH25A": [50],
        "MATH25B": [51],
        "MATH55A": [52],
        "MATH55B": [53]
    }

    fall_classes = ['MATH21A', 'MATH23A', 'MATH25A', 'MATH55A']
    linalg_sem = 0 if linalg in fall_classes else 1
    multi_sem = 0 if multi in fall_classes else 1
    if linalg == 'MATH21B':
        linalg_sem = 2
    if multi == 'MATH21A':
        multi_sem = 2

    # linalg constraints
    linalg_constraints = []
    for a in range(total_slots):
        a_time = get_slot_from_index(a)
        if a_time['semester'] == linalg_sem or linalg_sem == 2:
            for c_id in id_from_course[linalg]:
                linalg_constraints.append({
                    a: c_id
                })

    # multi constraints
    multi_constraints = []
    for a in range(total_slots):
        a_time = get_slot_from_index(a)
        if a_time['semester'] == multi_sem or multi_sem == 2:
            for c_id in id_from_course[multi]:
                multi_constraints.append({
                    a: c_id
                })

    return [linalg_constraints, multi_constraints]


# creating constraint domains
# must take 1 course from these gen ed categories
def constraint_gen_ed_ai_cb():
    ai, cb = parse_geneds()[:2]
    constraints = []
    for a in range(total_slots):
        a_time = get_slot_from_index(a)
        for course in ai:
            if ai[course]['semester'][a_time['semester']]:
                constraints.append({
                    a: course
                })
        for course in cb:
            if cb[course]['semester'][a_time['semester']]:
                constraints.append({
                    a: course
                })
    return constraints


# creating constraint domains
# must take 1 course from these gen ed categories
def constraint_gen_ed_er():
    er = parse_geneds()[3]
    constraints = []
    for a in range(total_slots):
        a_time = get_slot_from_index(a)
        for course in er:
            if er[course]['semester'][a_time['semester']]:
                constraints.append({
                    a: course
                })
    return constraints


# creating constraint domains
# must take 1 course from these gen ed categories
def constraint_gen_ed_sls_spu():
    geneds = parse_geneds()
    sls, spu = geneds[4], geneds[6]
    constraints = []
    for a in range(total_slots):
        a_time = get_slot_from_index(a)
        for course in sls:
            if sls[course]['semester'][a_time['semester']]:
                constraints.append({
                    a: course
                })
        for course in spu:
            if spu[course]['semester'][a_time['semester']]:
                constraints.append({
                    a: course
                })
    return constraints


# creating constraint domains
# must take 1 course from these gen ed categories
def constraint_gen_ed_sw_usw():
    sw, usw = parse_geneds()[7:]
    constraints = []
    for a in range(total_slots):
        a_time = get_slot_from_index(a)
        for course in sw:
            if sw[course]['semester'][a_time['semester']]:
                constraints.append({
                    a: course
                })
        for course in usw:
            if usw[course]['semester'][a_time['semester']]:
                constraints.append({
                    a: course
                })
    return constraints


# creating constraint domains
# must take 1 course from these gen ed categories
def constraint_gen_ed_sp():
    sp = parse_geneds()[5]
    constraints = [30, 31, 32, 33]
    for a in range(total_slots):
        a_time = get_slot_from_index(a)
        for course in sp:
            if sp[course]['semester'][a_time['semester']]:
                constraints.append({
                    a: course
                })
    return constraints


# creating constraint domains
# given a user's input of whether or not they need Math 1a, create constraint
def constraint_math1a():
    constraints = []
    # only freshman fall
    for a in range(total_slots):
        for ci in range(30, 34):
            constraints.append({
                a: ci
            })
    return constraints


# creating constraint domains
# given a user's input of whether or not they need Math 1b, create constraint
def constraint_math1b():
    constraints = []
    # only freshman fall
    for a in range(total_slots):
        for ci in range(34, 38):
            constraints.append({
                a: ci
            })
    return constraints
