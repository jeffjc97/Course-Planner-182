import csv

total_slots = 16

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
                'times': [float(line[8]), float(line[9])],
                'gened': 'concentration'
            }
    return class_dict

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
                            'class_name': geneds[i] + line[4] + line[5],
                            'semester': [line[1] == 'FALL', line[1] == 'SPRING'],
                            'days': [line[11]  == '1', line[11]  == '2', line[11]  == '3', line[11]  == '4', line[11]  == '5'],
                            'times': [line[14].replace(":", "")[0:4], line[15].replace(":", "")[0:4]],
                            'gened': geneds[i]
                        }
                        prev = int(line[0])
    return gen_ed_dict


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

def get_course_id_dict():
    id_dict = {}
    # read in CSV file with all course info
    with open('class_times.csv', 'rb') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)
        for line in csvreader:
            # key: class name, value: course ID
            id_dict[line[0]] = {
                line[10]
            }
    return id_dict

def get_slot_from_index(index):
    year = index / 8
    semester = int(index % 8 >= 4)
    slot = index % 4
    return {
        'year': year,
        'semester': semester,
        'slot': slot
    }

# TODO: Add Stat and Math prereqs once they're added into the general domain
def get_prereqs():
    return {
        # CS61: CS50
        3: [1],
        # CS109A: CS50, STAT110
        6: [1, 63],
        # CS109B: CS109A
        7: [6],
        # CS121: Discrete Math (CS20)
        # CS124: CS50, (CS121, Formal math, AM106, AM107, STAT110 is helpful)
        10: [1],
        # CS125: Comfort with Math 25, 55
        # CS127: (comfort with proofs at the level of CS121, CS124)
        # CS134: (Linear Algebra, Multivariable Calculus, STAT110)
        # 12: [63]
        # CS136: (Applied Math 21b, Computer Science 51 or equivalent, Statistics 110, and one of Computer Science 181, Computer Science 182, Economics 1011a, Economics 1052, or Economics 1056.)
        # CS141: programming experience
        14: [1],
        # CS143: CS50 recommended
        15: [1],
        # CS146: None
        # CS148: CS141
        18: [14],
        # CS152: CS51, CS121
        19: [2, 8],
        # CS153: CS51, CS61
        20: [2, 3],
        # CS161: CS61
        21: [3],
        # CS164: Any four courses numbered 50 or higher
        # CS165: CS51, CS61
        23: [2, 3],
        # CS171: (CS50 programming experience)
        24: [1],
        # CS175: CS51 or CS61 + Linear Algebra
        # CS179: (CS50 programming experience)
        26: [1],
        # CS181: CS51, CS121, STAT110, Linear Algebra, Multivariable Calculus
        27: [2, 8, 63],
        # CS182: CS51, CS121
        28: [2, 8],
        # CS187: CS51, CS121 (not offered)
        # CS189: None
    }

total_slots = 8
# slot_index: course_id
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

# todo 124 125 constraint
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

# Math constraints
def constraint_math():
    constraints = []
    # 21a/b are offered both semesters in weird times;
    # 23a, 25a, 55a --> Fall // 23b, 25b, 55b --> Spring
    # (Multivariable Calculus FALL, Linear Algebra SPRING)
    # (21a, 21b), (21a, 23a), (21a, 25a), (21a, 55a)
    # (23b, 21b), (23b, 23a), (23b, 25a), (23b, 55a)
    # (25b, 21b), (25b, 23a), (25b, 25a), (25b, 55a)
    # (55b, 21b), (55b, 23a), (55b, 25a), (55b, 55a)
    # OR you can take 21b in the fall and 21a in the spring (21b, 21a)

    id_from_course = {
        "21a1": 38,
        "21a2": 39,
        "21a3": 40,
        "21a4": 41,
        "21a5": 42,
        "21a6": 43,
        "21b1": 44,
        "21b2": 45,
        "21b3": 46,
        "21b4": 47,
        "23a": 48,
        "23b": 49,
        "25a": 50,
        "25b": 51,
        "55a": 52,
        "55b": 53
    }
    classes = ["21a", "21b", "23a", "23b", "25a", "25b", "55a", "55b"]

    # 21b/a combination dealt with later
    fall_classes = ['21a', '23a', '25a', '55a']
    spring_classes = ['21b', '23b', '25b', '55b']

    for a in range(total_slots):
        for b in range(a+1, total_slots):
            a_time = get_slot_from_index(a)
            b_time = get_slot_from_index(b)

            # a: fall, b: spring
            if a_time['semester'] == 0 and b_time['semester'] == 1:
                for fall in fall_classes:
                    for spring in spring_classes:
                        if fall == "21a":
                            for x in range(1,7):
                                if spring == "21b":
                                    for y in range(1,5):
                                        constraints.append( {a: id_from_course[fall + str(x)], b: id_from_course[spring + str(y)]} )
                                        # print a, fall + str(x), ", ", b, spring + str(y)
                                else:
                                    constraints.append( {a: id_from_course[fall + str(x)], b: id_from_course[spring]} )
                                    # print a, fall + str(x), ", ", b, spring
                        elif spring == "21b":
                            for y in range(1,5):
                                constraints.append( {a: id_from_course[fall], b: id_from_course[spring + str(y)]} )
                                # print a, fall, ", ", b, spring + str(y)
                        else:
                                constraints.append( {a: id_from_course[fall], b: id_from_course[spring]} )
                                # print a, fall, ", ", b, spring

            # a: Spring, b: Fall, so only 21b,21a
            elif a_time['semester'] == 1 and b_time['semester'] == 0:
                for x in range(1,7):
                    for y in range(1,5):
                        constraints.append( {a: id_from_course['21b' + str(y)], b: id_from_course['21a' + str(x)]} )
    return constraints
# print len(constraint_math())

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

def constraint_gen_ed_sp():
    sp = parse_geneds()[5]
    constraints = []
    for a in range(total_slots):
        a_time = get_slot_from_index(a)
        for course in sp:
            if sp[course]['semester'][a_time['semester']]:
                constraints.append({
                    a: course
                })
    return constraints
