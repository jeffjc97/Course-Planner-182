from Constraint import *

class ScheduleGenerator():
    # TODO PREFERENCES!!
    def __init__(self):
        self.assignment = [None for _ in xrange(48)]

        # {
        #     'f11': None, 'f12': None, 'f13': None, 'f14': None, 'f15': None, 'f16': None,
        #     'f21': None, 'f22': None, 'f23': None, 'f24': None, 'f25': None, 'f26': None,
        #     'f31': None, 'f32': None, 'f33': None, 'f34': None, 'f35': None, 'f36': None,
        #     'f41': None, 'f42': None, 'f43': None, 'f44': None, 'f45': None, 'f46': None,
        #     's11': None, 's12': None, 's13': None, 's14': None, 's15': None, 's16': None,
        #     's21': None, 's22': None, 's23': None, 's24': None, 's25': None, 's26': None,
        #     's31': None, 's32': None, 's33': None, 's34': None, 's35': None, 's36': None,
        #     's41': None, 's42': None, 's43': None, 's44': None, 's45': None, 's46': None,
        # }
        self.constraints = [NumCoursesConstraint()]
        self.populate_constraints()

    # Year = [0,1,2,3]; Semester = {0:fall, 1:spring}; Slot=[0,1,2,3,4,5]
    def get_course(year, semester, slot):
        return self.assignment[12*year + 6*semester + slot]

    def get_course_index(year, semester, slot):
        return 12*year + 6*semester + slot

    def populate_constraints(self):
        return

    def validate(self):
        for constraint in self.constraints:
            if not constraint.validate(self.assignment):
                return False
        return True

    def select_unassigned(self):
        for year in xrange(4):
            for semester in xrange(2):
                for slot in xrange(4):
                    if not get_course(year, semester, slot):
                        return get_course_index(year, semester, slot)
        for year in xrange(4):
            for semester in xrange(2):
                for slot in xrange(4,6):
                    if not get_course(year, semester, slot):
                        return get_course_index(year, semester, slot)
        return None

    def backtrack(self):
        if self.validate():
            return self.assignment
        course_index = self.select_unassigned()
        

