from constraint import *
from scheduleGenerator import ScheduleGenerator
import helpers

# dictionary containing all information about courses
class_dict = helpers.parse_csv()
sg = ScheduleGenerator(class_dict)
print sg.backtrack()
