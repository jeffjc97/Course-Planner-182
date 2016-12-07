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


print 'What math do you want to take? (Type 21, 23, 25, or 55)'
math_preference = int(raw_input())
while math_preference not in [21, 23, 25, 55]:
    print 'Invalid input. Select from 21, 23, 25, or 55'
    math_preference = int(raw_input())

print 'What semester to take expos? (Fall or Spring)'
expos_preference = raw_input().lower()
while expos_preference not in ['fall', 'spring']:
    print 'Invalid input. Select from Fall or Spring'
    expos_preference = raw_input().lower()

print 'What clases do you want to take? Answer by course name (e.g. "CS182") separated by spaces.'
preferred_classes = raw_input().upper().split()
while not valid_courses(preferred_classes):
    print 'Invalid input. Answer by course name (e.g. "CS182") separated by spaces.'
    preferred_classes = raw_input().upper().split()

print 'What clases do you not want to take? Answer by course name (e.g. "CS182") separated by spaces.'
disliked_classes = raw_input().upper().split()
while not valid_courses(disliked_classes) or len(set(preferred_classes) & set(disliked_classes)) != 0:
    print 'Invalid input. Answer by course name (e.g. "CS182") separated by spaces. These courses cannot overlap with your preferred courses.'
    disliked_classes = raw_input().upper().split()

# manual input
preferred_classes = [1]
disliked_classes = [62]
sg = ScheduleGenerator(class_dict, prereqs, preferred_classes, disliked_classes, math_preference, expos_preference)

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
