from Constraint import *
from ScheduleGenerator import ScheduleGenerator
import helpers

class_dict = helpers.parse_csv()
sg = ScheduleGenerator(class_dict)
print sg.backtrack()
