from Constraint import *
from ScheduleGenerator import ScheduleGenerator
import helpers

class_dict = helpers.parse_csv()
id_dict = helpers.get_course_id_dict()
prereqs = helpers.get_prereqs()
sg = ScheduleGenerator(class_dict, prereqs)

result = sg.backtrack()
# print result

course_names = []
for course_id in result:
    course_names.append(class_dict[course_id]["class_name"])
    
print "FINAL RESULTS", course_names
