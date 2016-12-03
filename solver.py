from constraint import *
from scheduleGenerator import ScheduleGenerator
import helpers

class_dict = helpers.parse_csv()
sg = ScheduleGenerator(class_dict)
print sg.backtrack()
