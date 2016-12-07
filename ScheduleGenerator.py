from Constraint import *
from collections import deque

total_slots = 32
slots_per_semester = 4
class ScheduleGenerator():
    # TODO PREFERENCES!!
    def __init__(self, params, classes, prereqs):
        # [fresh fall 1, fresh fall 2, ..., fresh spring 1, fresh spring 2, ..., senior spring 6]
        self.assignment = [None for _ in xrange(total_slots)]
        self.constraints = [NumCoursesConstraint(), UniqueCoursesConstraint(), OverlappingCoursesConstraint()]
        self.variable_domains = [set() for _ in xrange(total_slots)]
        self.nonbinary_constraint_domains = []
        # courses that can't be changed
        self.fixed = []
        self.classes = classes
        self.params = params
        self.prereqs = prereqs
        self.populate_nonbinary()
        self.process_params()
        self.init_domains()

    # given specific slot, return index
    # Year = [0,1,2,3]; Semester = {0:fall, 1:spring}; Slot=[0,1,2,3,4,5]
    def get_course_index(self, year, semester, slot):
        return 2*slots_per_semester*year + slots_per_semester*semester + slot

    # given specific slot, return course at index
    # Year = [0,1,2,3]; Semester = {0:fall, 1:spring}; Slot=[0,1,2,3,4,5]
    def get_course(self, year, semester, slot):
        return self.assignment[self.get_course_index(year, semester, slot)]

    # TODO add custom constraints
    def process_params(self):
        # Fixing expos course time
        if self.params['expos'] == 0:
            self.assignment[0] = -1
            self.fixed.append(0)
        else:
            self.assignment[4] = -1
            self.fixed.append(4)

        if self.params['math1a']:
            self.nonbinary_constraint_domains.append(helpers.constraint_math1a())
        if self.params['math1b']:
            self.nonbinary_constraint_domains.append(helpers.constraint_math1b())
        
        self.nonbinary_constraint_domains += helpers.constraint_math(self.params['linalg'], self.params['multi'])
        
        id_from_course = {
            "21a": [38, 39, 40, 41, 42, 43],
            "21b": [44, 45, 46, 47],
            "23a": [48],
            "23b": [49],
            "25a": [50],
            "25b": [51],
            "55a": [52],
            "55b": [53]
        }
        for c_name in id_from_course:
            if c_name != self.params['linalg'] and c_name != self.params['multi']:
                for c_id in id_from_course[c_name]:
                    del self.classes[c_id]

        return

    # ALL NONBINARY CONSTRAINTS
    # list of dictionaries for each constraint
    def populate_nonbinary(self):
        self.nonbinary_constraint_domains = [
            helpers.constraint_cs50_cs51_cs61(),
            helpers.constraint_cs121_cs125(),
            helpers.constraint_cs124_cs127_apmth106_apmth107(),
            # helpers.constraint_math(),
            helpers.constraint_gen_ed_ai_cb(),
            helpers.constraint_gen_ed_er(),
            helpers.constraint_gen_ed_sls_spu(),
            helpers.constraint_gen_ed_sw_usw(),
        ]
        print self.nonbinary_constraint_domains
        return

    # initialize domains to all of the classes that meet during the slot's semeste
    # domains - course ids
    def init_domains(self):
        for course in self.classes:
            if self.classes[course]["semester"][0]:
                for slot in self.get_semester_slots(0):
                    self.variable_domains[slot].add(course)
            if self.classes[course]["semester"][1]:
                for slot in self.get_semester_slots(1):
                    self.variable_domains[slot].add(course)


    # checks to see if all constraints satisfied
    # if new_assignment given, check if that assignment's constraints are satisfied
    def validate(self, new_assignment = None, new_constraint_domain = None, all_constraints = True):
        assignment = new_assignment if new_assignment else list(self.assignment)
        constraint_domains = new_constraint_domain if new_constraint_domain else list(self.nonbinary_constraint_domains)
        for constraint in self.constraints:
            if constraint.constraint_type == ConstraintType.BinaryConstraint:
                for x in range(total_slots):
                    for y in range(total_slots):
                        if x != y:
                            # pass 2 slot ids and assignment
                            if not constraint.validate(x, y, assignment):
                                return False
            else:
                if all_constraints and not constraint.validate(assignment):
                    return False
        # now checking constraint domains for nonbinary
        for d_i, domain in enumerate(constraint_domains):
            if len(domain) == 0:
                print "FAILED CONSTRAINT", d_i
                return False
        return True

    # makes a change to assignment and validates that new assignment
    def try_validate(self, slot, value):
        new_assignment = list(self.assignment)
        new_assignment[slot] = value
        nonbinary_constraint_domains = list(self.nonbinary_constraint_domains)
        # check prerequisites
        if value in self.prereqs:
            for prereq in self.prereqs[value]:
                if not prereq in new_assignment:
                    return False

        # print "IN TRY VALIDATE", nonbinary_constraint_domains
        # updating constraint domains
        # TODO AM I SUPPOSED TO DO THIS HERE??
        for cd_i, constraint_domain in enumerate(nonbinary_constraint_domains):
            cd = list(constraint_domain)
            for i, val_dict in enumerate(constraint_domain):
                for slot_i in val_dict:
                    if new_assignment[slot_i] and new_assignment[slot_i] != val_dict[slot_i]:
                        # remove this from domain
                        cd.remove(val_dict)
                        break
            nonbinary_constraint_domains[cd_i] = cd
        return self.validate(new_assignment, nonbinary_constraint_domains, False)

    # get first slot that is unassigned
    # try to fill up 4 classes/semester before adding more
    def select_unassigned(self):
        for year in xrange(4):
            for semester in xrange(2):
                for slot in xrange(slots_per_semester):
                    if self.get_course(year, semester, slot) is None:
                        return self.get_course_index(year, semester, slot)
        return None

    # get indices of all slots for a semester
    # Semester = {0:fall, 1:spring}
    def get_semester_slots(self,semester):
        slots = []
        for year in range(total_slots/(slots_per_semester * 2)):
            for slot in range(slots_per_semester):
                slots.append(self.get_course_index(year, semester, slot))
        return slots

    # i, j are slot indices
    def revise(self, i, j):
        revised = False
        for x in self.variable_domains[i]:
            domain_satisfied = False
            for y in self.variable_domains[j]:
                constraints_satisfied = True
                for c in self.constraints:
                    if c.constraint_type == ConstraintType.BinaryConstraint:
                        new_assignment = list(self.assignment)
                        new_assignment[i] = x
                        new_assignment[j] = y
                        # if a constraint isn't met, then this value of j won't work
                        if not c.validate(i, j, new_assignment):
                            constraints_satisfied = False
                            break
                # if it made it past all constraints, then this domain value works
                if constraints_satisfied:
                    domain_satisfied = True
                    break
            if not domain_satisfied:
                self.variable_domains[i].remove(x)
                # also remove all possible constraint domain options that had val x for slot i
                # for constraint_domain in self.nonbinary_constraint_domains:
                #     for dict_i, val_dict in enumerate(constraint_domain):
                #         if i in val_dict:
                #             if val_dict[i] == x:
                #                 # remove this from domain
                #                 del constraint_domain[dict_i]
                #                 break
                for cd_i, constraint_domain in enumerate(self.nonbinary_constraint_domains):
                    cd = list(constraint_domain)
                    for dict_i, val_dict in enumerate(constraint_domain):
                        if i in val_dict:
                            if val_dict[i] == x:
                                cd.remove(val_dict)
                                break
                    self.nonbinary_constraint_domains[cd_i] = cd
                revised = True
        return revised

    def ac3(self):
        queue = deque()
        # populating all arcs
        for x in range(total_slots):
            for y in range(total_slots):
                if x != y:
                    queue.append((x,y))
        while len(queue):
            i, j = queue.popleft()
            if self.revise(i, j):
                if len(self.variable_domains[i]) == 0:
                    return False
                # if revise removed all of the potential domain values for a nonbinary constraint
                for d_i, c in enumerate(self.nonbinary_constraint_domains):
                    if len(c) == 0:
                        print "FAILED CONSTRAINT IN AC3:", d_i
                        return False
                for k in range(total_slots):
                    if k != j:
                        queue.append((k, i))
        return True

    def backtrack(self):
        if self.validate():
            return self.assignment
        slot_index = self.select_unassigned()
        slot_domain = self.variable_domains[slot_index]
        cur_assignment = list(self.assignment)
        cur_domains = list(self.variable_domains)
        cur_nonbinary_domains = list(self.nonbinary_constraint_domains)
        for value in slot_domain:
            if self.try_validate(slot_index, value):
                self.assignment[slot_index] = value
                print self.assignment
                for cd_i, constraint_domain in enumerate(self.nonbinary_constraint_domains):
                    cd = list(constraint_domain)
                    for i, val_dict in enumerate(constraint_domain):
                        for slot_i in val_dict:
                            if self.assignment[slot_i] and self.assignment[slot_i] != val_dict[slot_i]:
                                # remove this from domain
                                cd.remove(val_dict)
                                break
                    self.nonbinary_constraint_domains[cd_i] = cd
                if self.ac3():
                    result = self.backtrack()
                    if result:
                        return result
            self.assignment = list(cur_assignment)
            self.variable_domains = list(cur_domains)
            self.nonbinary_constraint_domains = list(cur_nonbinary_domains)
        print self.assignment
        return False
