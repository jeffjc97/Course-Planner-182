from Constraint import *
from ScheduleGenerator import ScheduleGenerator
import helpers

# class_dict = helpers.parse_csv()
class_dict = helpers.total_class_dict()
id_dict = helpers.get_course_id_dict()
prereqs = helpers.get_prereqs()

params = {
    'math1a': True,
    'math1b': True,
    'linalg': '25a',
    # 21b, 23a, 25a, 55a
    'multi': '25b',
    # 21a, 23b, 25b, 55b
    'expos': 1
}

sg = ScheduleGenerator(params, class_dict, prereqs)

result = sg.backtrack()
# print result

course_names = []
for course_id in result:
    course_names.append(class_dict[course_id]["class_name"])
    
print "FINAL RESULTS", course_names
