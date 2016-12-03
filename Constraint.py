import helpers
class_dict = helpers.parse_csv()

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
        if not assignment[x] or not assignment[y]:
            return True
        return class_dict[assignment[x]]['class_name'] != class_dict[assignment[y]]['class_name']

class OverlappingCoursesConstraint(Constraint):
    def __init__ (self):
        self.constraint_type = ConstraintType.BinaryConstraint

    def validate(self, x, y, assignment):
        if not assignment[x] or not assignment[y]:
            return True
        if helpers.get_slot_from_index(x)['semester'] == helpers.get_slot_from_index(y)['semester']:
            # do something
            if class_dict[assignment[x]]['times'][0] < class_dict[assignment[y]]['times'][0]:
                first_class = x
                second_class = y
            elif class_dict[assignment[x]]['times'][0] > class_dict[assignment[y]]['times'][0]:
                first_class = y
                second_class = x
            else:
                return False
            if class_dict[assignment[first_class]]['times'][1] > class_dict[assignment[second_class]]['times'][0]:
                return False
            else:
                return True
        else:
            return True
