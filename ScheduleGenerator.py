from Constraint import *

class ScheduleGenerator():
    # TODO PREFERENCES!!
    def __init__(self,classes):
        # [fresh fall 1, fresh fall 2, ..., fresh spring 1, fresh spring 2, ..., senior spring 6]
        self.assignment = [None for _ in xrange(48)]
        self.constraints = [NumCoursesConstraint()]
        self.variable_domains = [set() for _ in xrange(48)]
        self.classes = classes
        self.populate_constraints()
        self.init_domains()

    # given specific slot, return index
    # Year = [0,1,2,3]; Semester = {0:fall, 1:spring}; Slot=[0,1,2,3,4,5]
    def get_course_index(self, year, semester, slot):
        return 12*year + 6*semester + slot

    # given specific slot, return course at index
    # Year = [0,1,2,3]; Semester = {0:fall, 1:spring}; Slot=[0,1,2,3,4,5]
    def get_course(self, year, semester, slot):
        return self.assignment[self.get_course_index(year, semester, slot)]

    # TODO add custom constraints
    def populate_constraints(self):
        return

    # initialize domains to all of the classes that meet during the slot's semeste
    def init_domains(self):
        for course in self.classes:
            if self.classes[course]["fall"]:
                for slot in self.get_semester_slots(0):
                    self.variable_domains[slot].add(course)
            if self.classes[course]["spring"]:
                for slot in self.get_semester_slots(1):
                    self.variable_domains[slot].add(course)


    # checks to see if all constraints satisfied
    # if new_assignment given, check if that assignment's constraints are satisfied
    def validate(self, new_assignment = None):
        assignment = new_assignment if new_assignment else self.assignment
        for constraint in self.constraints:
            if not constraint.validate(assignment):
                return False
        return True

    # makes a change to assignment and validates that new assignment
    def try_validate(self, slot, value):
        new_assignment = list(self.assignment)
        new_assignment[slot] = value
        return self.validate(new_assignment)

    # get first slot that is unassigned
    # try to fill up 4 classes/semester before adding more
    def select_unassigned(self):
        for year in xrange(4):
            for semester in xrange(2):
                for slot in xrange(4):
                    if not self.get_course(year, semester, slot):
                        return self.get_course_index(year, semester, slot)
        for year in xrange(4):
            for semester in xrange(2):
                for slot in xrange(4,6):
                    if not self.get_course(year, semester, slot):
                        return self.get_course_index(year, semester, slot)
        return None

    # get indices of all slots for a semester
    # Semester = {0:fall, 1:spring}
    def get_semester_slots(self,semester):
        slots = []
        for year in range(4):
            for slot in range(6):
                slots.append(self.get_course_index(year, semester, slot))
        return slots

    def ac3(self):
        return False

    def backtrack(self):
        if self.validate():
            return self.assignment
        slot_index = self.select_unassigned()
        slot_domain = self.variable_domains[slot_index]
        cur_assignment = list(self.assignment)
        cur_domains = list(self.variable_domains)
        for value in slot_domain:
            if self.try_validate(slot_index, value):
                self.assignment[slot_index] = value
                if self.ac3:
                    result = self.backtrack()
                    if result:
                        return result
            self.assignment = cur_assignment
            self.variable_domains = cur_domains
        print self.assignment
        return False
