from Constraint import *
from ScheduleGenerator import ScheduleGenerator
import helpers

# class_dict = helpers.parse_csv()
class_dict = helpers.total_class_dict()
id_dict = helpers.get_course_id_dict()
prereqs = helpers.get_prereqs()
# manual input
preferred_classes = [62]
disliked_classes = [2]
sg = ScheduleGenerator(class_dict, prereqs, preferred_classes, disliked_classes)

result = sg.backtrack()

course_names = []
for course_id in result:
    course_names.append(class_dict[course_id]["class_name"])

print "FINAL RESULTS", course_names
