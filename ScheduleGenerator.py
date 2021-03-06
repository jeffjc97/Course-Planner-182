#
# main code implementing the CSP solving algorithm
#

import sys
import random
from Constraint import *
from collections import deque

total_slots = 32
slots_per_semester = 4


class ScheduleGenerator():
    def __init__(self, params, cs_class_dict, gened_class_dict, prereqs):
        # [fresh fall 1, fresh fall 2, ..., fresh spring 1, fresh spring 2, ..., senior spring 6]
        self.assignment = [None for _ in xrange(total_slots)]
        self.constraints = [NumCoursesConstraint(), UniqueCoursesConstraint(), OverlappingCoursesConstraint()]
        # two deques, one for CS (0), one for GenEds (1)
        self.variable_domains = [(deque(), deque()) for _ in xrange(total_slots)]
        self.nonbinary_constraint_domains = []
        # courses that can't be changed
        self.fixed = []
        self.cs_classes = cs_class_dict
        self.gened_classes = gened_class_dict
        self.params = params
        self.prereqs = prereqs
        self.ai_cb, self.er, self.spu_sls, self.sw_usw = False, False, False, False
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

    def process_params(self):
        # Fixing expos course time
        if self.params['expos'] == 0:
            self.assignment[0] = -1
            self.fixed.append(0)
        else:
            self.assignment[4] = -1
            self.fixed.append(4)

        # if they need math 1a or 1b
        if self.params['math1a']:
            self.nonbinary_constraint_domains.append(helpers.constraint_math1a())
        if self.params['math1b']:
            self.nonbinary_constraint_domains.append(helpers.constraint_math1b())

        # linalg/multi requirements
        self.nonbinary_constraint_domains += helpers.constraint_math(self.params['linalg'], self.params['multi'])

        id_from_course = {
            "MATH21A": [38, 39, 40, 41, 42, 43],
            "MATH21B": [44, 45, 46, 47],
            "MATH23A": [48],
            "MATH23B": [49],
            "MATH25A": [50],
            "MATH25B": [51],
            "MATH55A": [52],
            "MATH55B": [53]
        }
        # removing other courses from domains, as they shouldn't be taking multiple
        for c_name in id_from_course:
            if c_name != self.params['linalg'] and c_name != self.params['multi']:
                for c_id in id_from_course[c_name]:
                    del self.cs_classes[c_id]

        return

    # ALL NONBINARY CONSTRAINTS
    # list of dictionaries for each constraint
    def populate_nonbinary(self):
        self.nonbinary_constraint_domains = [
            # CS concentration requirements
            helpers.constraint_cs50_cs51_cs61(),
            helpers.constraint_cs121_cs125(),
            helpers.constraint_cs124_cs127_apmth106_apmth107(),
        ]
        if self.params["check_gened"]:
            # all constraints concerning gen eds
            self.nonbinary_constraint_domains += [
                helpers.constraint_gen_ed_ai_cb(),
                helpers.constraint_gen_ed_er(),
                helpers.constraint_gen_ed_sls_spu(),
                helpers.constraint_gen_ed_sw_usw()
            ]
        return

    # initialize domains to all of the classes that meet during the slot's semeste
    # domains - course ids
    def init_domains(self):
        # adding CS courses into their respective semester's slots
        for course in self.cs_classes:
            if self.cs_classes[course]["semester"][0]:
                for slot in self.get_semester_slots(0):
                    self.variable_domains[slot][0].append(course)
            if self.cs_classes[course]["semester"][1]:
                for slot in self.get_semester_slots(1):
                    self.variable_domains[slot][0].append(course)

        if self.params["check_gened"]:
            # adding GenEds into their respective semester's slots
            for course in self.gened_classes:
                if self.gened_classes[course]['semester'][0]:
                    for slot in self.get_semester_slots(0):
                        self.variable_domains[slot][1].append(course)
                if self.gened_classes[course]['semester'][1]:
                    for slot in self.get_semester_slots(1):
                        self.variable_domains[slot][1].append(course)

        # prioritizing class preference
        lookup_dict = helpers.get_course_id_dict()
        new_preferred = []
        for slot in self.variable_domains:
            new_preferred += self.params['preferred_classes'] + [self.params['linalg']] + [self.params['multi']]
            if self.params['math1a']:
                for x in range(30, 34):
                    slot[0].remove(x)
                    slot[0].appendleft(x)
            if self.params['math1b']:
                for x in range(34,38):
                    slot[0].remove(x)
                    slot[0].appendleft(x)
            for preference in new_preferred:
                course = lookup_dict[preference]
                if course in slot[0]:
                    slot[0].remove(course)
                    slot[0].appendleft(course)
            for disliked in self.params['disliked_classes']:
                course = lookup_dict[disliked]
                if course in slot[0]:
                    slot[0].remove(course)
                    slot[0].append(course)

    # checks to see if all constraints satisfied
    # if new_assignment given, check if that assignment's constraints are satisfied
    def validate(self, new_assignment=None, new_constraint_domain=None, all_constraints=True):
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
                # print "FAILED CONSTRAINT", d_i, "out of: ", len(constraint_domains)
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

        # updating constraint domains
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
    def get_semester_slots(self, semester):
        slots = []
        for year in range(total_slots/(slots_per_semester * 2)):
            for slot in range(slots_per_semester):
                slots.append(self.get_course_index(year, semester, slot))
        return slots

    # get the number of concentration classes in the semester of the course index
    def get_cs_count(self, index):
        semester_start_index = slots_per_semester * (index / slots_per_semester)
        counter = 0
        for i in range(semester_start_index, semester_start_index + 4):
            if self.assignment[i] and self.assignment[i] != -1 and self.assignment[i] in self.cs_classes:
                counter += 1
        return counter

    # i, j are slot indices
    def revise(self, i, j):
        revised = False
        # checking both CS and GenEd courses in x
        for x in deque(list(self.variable_domains[i][0]) + list(self.variable_domains[i][1])):
            domain_satisfied = False
            # checking both CS and GenEd courses in y
            for y in deque(list(self.variable_domains[j][0]) + list(self.variable_domains[j][1])):
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
                if x in self.variable_domains[i][0]:
                    self.variable_domains[i][0].remove(x)
                else:
                    self.variable_domains[i][1].remove(x)
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

    # AC3 algorithm
    def ac3(self):
        queue = deque()
        # populating all arcs
        for x in range(total_slots):
            for y in range(total_slots):
                if x != y:
                    queue.append((x, y))
        while len(queue):
            i, j = queue.popleft()
            if self.revise(i, j):
                if len(self.variable_domains[0][i]) == 0 and len(self.variable_domains[1][i] == 0):
                    return False
                # if revise removed all of the potential domain values for a nonbinary constraint
                for d_i, c in enumerate(self.nonbinary_constraint_domains):
                    if len(c) == 0:
                        return False
                for k in range(total_slots):
                    if k != j:
                        queue.append((k, i))
        return True

    # backtracking search implementatino
    def backtrack(self):
        if self.validate():
            return self.assignment
        slot_index = self.select_unassigned()
        if self.get_cs_count(slot_index) >= self.params['max']:
            # if we've reached the limit of concentration classes, only select gen eds
            if self.params['check_gened']:
                slot_domain = list(self.variable_domains[slot_index][1])
            else:
                slot_domain = [sys.maxint]

        else:
            # must iterate over both CS and GenEds, so ordering GenEds or CS first with prob 0.5
            slot_domain = list(self.variable_domains[slot_index][0])+list(self.variable_domains[slot_index][1]) if random.random() > 0.3 else list(self.variable_domains[slot_index][1]) + list(self.variable_domains[slot_index][0])

        # iterate through GenEds, removing ones that have been fulfilled
        for course in slot_domain:
            if course in self.gened_classes:
                if (self.gened_classes[course]['gened'] == 'AI' or self.gened_classes[course]['gened'] == 'CB') and self.ai_cb:
                    slot_domain.remove(course)
                elif self.gened_classes[course]['gened'] == 'ER' and self.er:
                    slot_domain.remove(course)
                elif (self.gened_classes[course]['gened'] == 'SPU' or self.gened_classes[course]['gened'] == 'SLS') and self.spu_sls:
                    slot_domain.remove(course)
                elif (self.gened_classes[course]['gened'] == 'SW' or self.gened_classes[course]['gened'] == 'USW') and self.sw_usw:
                    slot_domain.remove(course)

        cur_assignment = list(self.assignment)
        cur_domains = list(self.variable_domains)
        cur_nonbinary_domains = list(self.nonbinary_constraint_domains)
        cur_geneds = list([self.ai_cb, self.er, self.spu_sls, self.sw_usw])

        for value in slot_domain:
            if self.try_validate(slot_index, value):
                self.assignment[slot_index] = value

                print self.assignment
                # check which GenEd has been assigned, and set class variable to True
                if value in self.gened_classes:
                    if self.gened_classes[value]['gened'] == 'AI' or self.gened_classes[value]['gened'] == 'CB':
                        self.ai_cb = True
                    elif self.gened_classes[value]['gened'] == 'ER':
                        self.er = True
                    elif self.gened_classes[value]['gened'] == 'SPU' or self.gened_classes[value]['gened'] == 'SLS':
                        self.spu_sls = True
                    elif self.gened_classes[value]['gened'] == 'SW' or self.gened_classes[value]['gened'] == 'USW':
                        self.sw_usw = True

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
            # reset the GenEd fulfillment class variables because we've reached a dead end
            cur_geneds_copy = list(cur_geneds)
            self.ai_cb = cur_geneds_copy[0]
            self.er = cur_geneds_copy[1]
            self.spu_sls = cur_geneds_copy[2]
            self.sw_usw = cur_geneds_copy[3]
            self.assignment = list(cur_assignment)
            self.variable_domains = list(cur_domains)
            self.nonbinary_constraint_domains = list(cur_nonbinary_domains)
        return False
