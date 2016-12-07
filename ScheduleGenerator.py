from Constraint import *
from collections import deque

total_slots = 8
class ScheduleGenerator():
    # TODO PREFERENCES!!
    def __init__(self,classes):
        # [fresh fall 1, fresh fall 2, ..., fresh spring 1, fresh spring 2, ..., senior spring 6]
        self.assignment = [None for _ in xrange(total_slots)]
        self.constraints = [NumCoursesConstraint(), UniqueCoursesConstraint(), OverlappingCoursesConstraint()]
        self.variable_domains = [set() for _ in xrange(total_slots)]
        self.nonbinary_constraint_domains = [helpers.constraint_cs50_cs51_cs61(), helpers.constraint_cs121_cs125(), helpers.constraint_cs124_cs127_apmth106_apmth107(), helpers.constraint_math()]
        # helpers.constraint_cs121_cs125(), helpers.constraint_cs124_cs127_apmth106_apmth107()
        self.classes = classes
        self.populate_constraints()
        self.populate_nonbinary()
        self.init_domains()

    # given specific slot, return index
    # Year = [0,1,2,3]; Semester = {0:fall, 1:spring}; Slot=[0,1,2,3,4,5]
    def get_course_index(self, year, semester, slot):
        return 8*year + 4*semester + slot

    # given specific slot, return course at index
    # Year = [0,1,2,3]; Semester = {0:fall, 1:spring}; Slot=[0,1,2,3,4,5]
    def get_course(self, year, semester, slot):
        return self.assignment[self.get_course_index(year, semester, slot)]

    # TODO add custom constraints
    def populate_constraints(self):
        return

    # ALL NONBINARY CONSTRAINTS
    # list of dictionaries for each constraint
    def populate_nonbinary(self):
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
        assignment = new_assignment if new_assignment else self.assignment
        constraint_domains = new_constraint_domain if new_constraint_domain else self.nonbinary_constraint_domains
        print "MATH CONSTRAINT"
        print assignment
        print constraint_domains[3]
        if assignment == [1, 4, 38, 8, None, None, None, None]:
            print "========================================="
            print "-"
            print "-"
            print "-"
            print "-fuck"
            print "-"
            print "-"
            print "-"
            print "-"
            print "-"
            print constraint_domains
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
                # print assignment
                # print "CONSTRAINT", d_i, "FAILED"
                return False
        return True

    # makes a change to assignment and validates that new assignment
    def try_validate(self, slot, value):
        new_assignment = list(self.assignment)
        new_assignment[slot] = value
        nonbinary_constraint_domains = list(self.nonbinary_constraint_domains)
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
        # print "TRY VALIDATE"
        return self.validate(new_assignment, nonbinary_constraint_domains, False)

    # get first slot that is unassigned
    # try to fill up 4 classes/semester before adding more
    def select_unassigned(self):
        for year in xrange(4):
            for semester in xrange(2):
                for slot in xrange(4):
                    if not self.get_course(year, semester, slot):
                        return self.get_course_index(year, semester, slot)
        return None

    # get indices of all slots for a semester
    # Semester = {0:fall, 1:spring}
    def get_semester_slots(self,semester):
        slots = []
        for year in range(total_slots/8):
            for slot in range(4):
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
                        print "CONSTRAINT", d_i, "FAILED IN AC3"
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
            # print slot_index
            # print value

            if self.try_validate(slot_index, value):
                # print "BACKTRACK TRY VALIDATE TRUE"
                self.assignment[slot_index] = value
                # print "BEFORE:"
                # print self.nonbinary_constraint_domains
                for cd_i, constraint_domain in enumerate(self.nonbinary_constraint_domains):
                    cd = list(constraint_domain)
                    for i, val_dict in enumerate(constraint_domain):
                        for slot_i in val_dict:
                            if self.assignment[slot_i] and self.assignment[slot_i] != val_dict[slot_i]:
                                # remove this from domain
                                cd.remove(val_dict)
                                break
                    self.nonbinary_constraint_domains[cd_i] = cd
                # print self.assignment
                # print "AFTER:"
                # print self.nonbinary_constraint_domains
                if self.ac3():
                    result = self.backtrack()
                    if result:
                        return result
            # print "COULDN'T USE", value, "IN SLOT", slot_index
            self.assignment = list(cur_assignment)
            self.variable_domains = list(cur_domains)
            print "REVERTING DOMAIN"
            print cur_nonbinary_domains[3]
            self.nonbinary_constraint_domains = list(cur_nonbinary_domains)
        print self.assignment
        return False
