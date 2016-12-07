from Constraint import *
from ScheduleGenerator import ScheduleGenerator
import helpers

# class_dict = helpers.parse_csv()
class_dict = helpers.total_class_dict()
id_dict = helpers.get_course_id_dict()
prereqs = helpers.get_prereqs()

def valid_courses(course_list):
    for course in course_list:
        if course not in id_dict:
            return False
    return True

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
    math1a = raw_input().lower()
params['math1b'] = 0 if math1b == 'no' else 1

print 'What math do you want to take for Multivariable Calculus? (Type 21a, 23b, 25b, 55b)'
params['multi'] = raw_input()
while params['multi'] not in ['21a', '23b', '25b', '55b']:
    print 'Invalid input. Select from 21a, 23b, 25b, or 55b'
    params['multi'] = raw_input()

print 'What math do you want to take for Linear Algebra? (Type 21b, 23a, 25a, 55a)'
params['linalg'] = raw_input()
while params['linalg'] not in ['21b', '23a', '25a', '55a']:
    print 'Invalid input. Select from 21b, 23a, 25a, or 55a'
    params['linalg'] = raw_input()

print 'What semester to take expos? (Fall or Spring)'
expos = raw_input().lower()
while expos not in ['fall', 'spring']:
    print 'Invalid input. Select from Fall or Spring'
    expos = raw_input().lower()
params['expos'] = 0 if expos == 'fall' else 1

print 'What clases do you want to take? Answer by course name (e.g. "CS182") separated by spaces.'
params['preferred_classes'] = raw_input().upper().split()
while not valid_courses(params['preferred_classes']):
    print 'Invalid input. Answer by course name (e.g. "CS182") separated by spaces.'
    params['preferred_classes'] = raw_input().upper().split()

print 'What clases do you not want to take? Answer by course name (e.g. "CS182") separated by spaces.'
params['disliked_classes'] = raw_input().upper().split()
while not valid_courses(params['disliked_classes']) or len(set(params['preferred_classes']) & set(params['disliked_classes'])) != 0:
    print 'Invalid input. Answer by course name (e.g. "CS182") separated by spaces. These courses cannot overlap with your preferred courses.'
    params['disliked_classes'] = raw_input().upper().split()

# manual input
preferred_classes = [1]
disliked_classes = [62]
sg = ScheduleGenerator(params, class_dict, prereqs)

result = sg.backtrack()

course_names = []
for course_id in result:
    course_names.append(class_dict[course_id]["class_name"])



def get_year(x):
    return {
        8: "Freshman Year",
        16: "Sophomore Year",
        24: "Junior Year",
        32: "Senior Year"
    }[x]

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
