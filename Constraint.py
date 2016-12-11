import helpers, sys
cs_class_dict = helpers.parse_csv()
gened_class_dict = helpers.parse_geneds_single_dict()

class ConstraintType():
    OverallConstraint = 1
    BinaryConstraint = 2

# abstract class for constraints
class Constraint():
    def validate(self, assignment):
        return NotImplementedError("implement me!")

# total course length >= 32
class NumCoursesConstraint(Constraint):
    def __init__ (self):
        self.constraint_type = ConstraintType.OverallConstraint

    def validate(self, assignment):
        num_courses = 0
        for slot in assignment:
            if slot:
                num_courses += 1
        return num_courses >= 32

class UniqueCoursesConstraint(Constraint):
    def __init__ (self):
        self.constraint_type = ConstraintType.BinaryConstraint

    def validate(self, x, y, assignment):
        if assignment[x] == sys.maxint or assignment[y] == sys.maxint:
            return True
        if not assignment[x] or not assignment[y]:
            return True
        if assignment[x] in cs_class_dict and assignment[y] in cs_class_dict:
            return cs_class_dict[assignment[x]]['class_name'] != cs_class_dict[assignment[y]]['class_name']
        elif assignment[x] in gened_class_dict and assignment[y] in gened_class_dict:
            return gened_class_dict[assignment[x]]['class_name'] != gened_class_dict[assignment[y]]['class_name']
        else:
            return True

class OverlappingCoursesConstraint(Constraint):
    def __init__ (self):
        self.constraint_type = ConstraintType.BinaryConstraint

    def validate(self, x, y, assignment):
        if assignment[x] == sys.maxint or assignment[y] == sys.maxint:
            return True
        if not assignment[x] or not assignment[y]:
            return True
        # check if courses are in same year
        if helpers.get_slot_from_index(x)['year'] == helpers.get_slot_from_index(y)['year']:
            # check if courses are in same semester
            if helpers.get_slot_from_index(x)['semester'] == helpers.get_slot_from_index(y)['semester']:
                # do something
                if assignment[x] in cs_class_dict:
                    x_days = cs_class_dict[assignment[x]]['days']
                    x_cs = True
                else:
                    x_days = gened_class_dict[assignment[x]]['days']
                    x_cs = False

                if assignment[y] in cs_class_dict:
                    y_days = cs_class_dict[assignment[y]]['days']
                    y_cs = True
                else:
                    y_days = gened_class_dict[assignment[y]]['days']
                    y_cs = False
                day_overlap = False
                for day in range(5):
                    if x_days[day] and y_days[day]:
                        day_overlap = True
                        break
                if day_overlap:
                    x_times = cs_class_dict[assignment[x]]['times'] if x_cs else gened_class_dict[assignment[x]]['times']
                    y_times = cs_class_dict[assignment[y]]['times'] if y_cs else gened_class_dict[assignment[y]]['times']
                    if x_times[0] < y_times[0]:
                        if x_times[1] > y_times[0]:
                            return False
                        else:
                            return True
                    elif x_times[0] > y_times[0]:
                        if y_times[1] > x_times[0]:
                            return False
                        else:
                            return True
                    else:
                        return False
                return True
            return True
        return True
