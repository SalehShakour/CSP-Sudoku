from CSP.Constraint import Constraint


class SudokuConstraint(Constraint):
    def __init__(self, variables):
        super().__init__(variables)

    def is_satisfied(self):
        values = [var.value for var in self.variables if var.value]
        return len(set(values)) == len(values)
