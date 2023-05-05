from CSP.SudokuVariable import Variable


class Constraint:
    def __init__(self, variables: list[Variable]):
        self.variables = variables

    def is_satisfied(self):
        values = [var.value for var in self.variables if var.value]
        return len(set(values)) == len(values)
