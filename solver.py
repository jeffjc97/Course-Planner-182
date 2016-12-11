#
# code to interface with user and process user preferences
#

from Constraint import *
from ScheduleGenerator import ScheduleGenerator
import helpers

cs_class_dict = helpers.parse_csv()
gened_class_dict = helpers.parse_geneds_single_dict()

# class_dict = helpers.total_class_dict()
id_dict = helpers.get_course_id_dict()
prereqs = helpers.get_prereqs()

# check if course entered is a real course
def valid_courses(course_list):
    for course in course_list:
        if course not in id_dict:
            return False
    return True

# getting user preferences
params = {}

print 'Do you need to take Math 1a? (Type Yes or No)'
math1a = raw_input().lower()
while math1a not in ['yes', 'no']:
    print 'Invalid input. Select from Yes or No'
    math1a = raw_input().lower()
params['math1a'] = 0 if math1a == 'no' else 1

print 'Do you need to take Math 1b? (Type Yes or No)'
math1b = raw_input().lower()
while math1b not in ['yes', 'no']:
    print 'Invalid input. Select from Yes or No'
    math1b = raw_input().lower()
params['math1b'] = 0 if math1b == 'no' else 1

print 'What math do you want to take for Multivariable Calculus? (Type Math21a, Math23b, Math25b, Math55b)'
params['multi'] = raw_input().upper()
while params['multi'] not in ['MATH21A', 'MATH23B', 'MATH25B', 'MATH55B']:
    print 'Invalid input. Select from Math21a, Math23b, Math25b, Math55b'
    params['multi'] = raw_input().upper()

print 'What math do you want to take for Linear Algebra? (Type Math21b, Math23a, Math25a, Math55a)'
params['linalg'] = raw_input().upper()
while params['linalg'] not in ['MATH21B', 'MATH23A', 'MATH25A', 'MATH55A']:
    print 'Invalid input. Select from Math21b, Math23a, Math25a, or Math55a'
    params['linalg'] = raw_input().upper()

print 'What semester to take expos? (Fall or Spring)'
expos = raw_input().lower()
while expos not in ['fall', 'spring']:
    print 'Invalid input. Select from Fall or Spring'
    expos = raw_input().lower()
params['expos'] = 0 if expos == 'fall' else 1

print 'What is the maximum number of concentration courses you want to take per semester? (2, 3, 4)'
params['max'] = raw_input()
while params['max'] not in ['2', '3', '4']:
    print 'Invalid input. Select from 2, 3, or 4'
    params['max'] = raw_input()
params['max'] = int(params['max'])

print 'What CS clases do you want to take? Answer by course name (e.g. "CS182") separated by spaces.'
params['preferred_classes'] = raw_input().upper().split()
while not valid_courses(params['preferred_classes']):
    print 'Invalid input. Answer by course name (e.g. "CS182") separated by spaces.'
    params['preferred_classes'] = raw_input().upper().split()

print 'What CS clases do you not want to take? Answer by course name (e.g. "CS182") separated by spaces.'
params['disliked_classes'] = raw_input().upper().split()
while not valid_courses(params['disliked_classes']) or len(set(params['preferred_classes']) & set(params['disliked_classes'])) != 0:
    print 'Invalid input. Answer by course name (e.g. "CS182") separated by spaces. These courses cannot overlap with your preferred courses.'
    params['disliked_classes'] = raw_input().upper().split()

# hardcoded input, for testing
# params['math1a'] = 0
# params['math1b'] = 1
# params['multi'] = 'MATH23B'
# params['linalg'] = 'MATH23A'
# params['expos'] = 0
# params['max'] = 3
# params['preferred_classes'] = ['CS161']
# params['disliked_classes'] = ['CS108']

# GENERATE SCHEDULE!!
sg = ScheduleGenerator(params, cs_class_dict, gened_class_dict, prereqs)
result = sg.backtrack()

# parse output into nice format
# get course names instead of course IDs
course_names = []
for course_id in result:
    if course_id in cs_class_dict:
        course_names.append(cs_class_dict[course_id]["class_name"])
    elif course_id in gened_class_dict:
        course_names.append(gened_class_dict[course_id]["class_name"])
    else:
        course_names.append("____")

def get_year(x):
    return {
        8: "Freshman Year",
        16: "Sophomore Year",
        24: "Junior Year",
        32: "Senior Year"
    }[x]

# output formatted results
print "Your Course Schedule:\n"
print "                |                Fall                  ||               Spring               "
print "---------------------------------------------------------------------------------------------"
fall, spring = [], []
cur = fall
for i in range(1, helpers.total_slots + 1):
    cur.append(course_names[i-1])
    if i % 8 == 0:
        print '%15s | %8s %8s %8s %8s  || %8s %8s %8s %8s ' % (get_year(i), fall[0], fall[1], fall[2], fall[3], spring[0], spring[1], spring[2], spring[3])
        fall, spring = [], []
        cur = fall
    elif i % 4 == 0:
        cur = spring
