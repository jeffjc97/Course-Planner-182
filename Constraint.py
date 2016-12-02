# abstract class for constraints
class Constraint():
    def validate(self, assignment):
        return NotImplementedError("implement me!")

# total course length >= 32
class NumCoursesConstraint(Constraint):
    def validate(self, assignment):
        num_courses = 0
        for slot in assignment:
            if assignment[slot]:
                num_courses += 1
        return num_courses >= 32