from CSP.Problem import Problem
from CSP.Variable import Variable
from Sudoku.SudokuConstraint import SudokuConstraint


class SudokuProblem(Problem):
    def __init__(self, grid):
        super().__init__([], [])
        variables = []
        rows = "ABCDEFGHI"
        cols = "123456789"
        domains = set(cols)

        # Create variables
        for r in rows:
            for c in cols:
                name = r + c
                value = int(grid[rows.index(r)][cols.index(c)])
                if value == 0:
                    variable = Variable(list(domains), name)
                else:
                    # For cells that have a default value, their range is limited to the same value
                    variable = Variable([value], name)
                variables.append(variable)

        # Create constraints
        constraints = []
        # row constraints
        for r in rows:
            row_vars = [var for var in variables if var.name[0] == r]
            constraints.append(SudokuConstraint(row_vars))

        # column constraints
        for c in cols:
            col_vars = [var for var in variables if var.name[1] == c]
            constraints.append(SudokuConstraint(col_vars))

        # box constraints
        boxes = [(i, j) for i in range(0, 9, 3) for j in range(0, 9, 3)]
        for box in boxes:
            box_vars = []
            for r in range(box[0], box[0] + 3):
                for c in range(box[1], box[1] + 3):
                    box_vars.append(variables[r * 9 + c])
            constraints.append(SudokuConstraint(box_vars))

        self.constraints = constraints
        self.variables = variables
