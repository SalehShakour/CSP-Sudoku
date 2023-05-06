from CSP.SudokuVariable import Variable
from CSP.SudokuConstraint import Constraint


class Problem:
    def __init__(self, grid, constraints=None, variables: list[Variable] = None, name=""):
        if constraints is None:
            constraints = []
        self.grid = grid
        self.constraints = constraints
        self.variables = variables
        self.name = name
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
            constraints.append(Constraint(row_vars))

        # column constraints
        for c in cols:
            col_vars = [var for var in variables if var.name[1] == c]
            constraints.append(Constraint(col_vars))

        # box constraints
        boxes = [(i, j) for i in range(0, 9, 3) for j in range(0, 9, 3)]
        for box in boxes:
            box_vars = []
            for r in range(box[0], box[0] + 3):
                for c in range(box[1], box[1] + 3):
                    box_vars.append(variables[r * 9 + c])
            constraints.append(Constraint(box_vars))

        self.constraints = constraints
        self.variables = variables

    def get_unassigned_variables(self) -> list[Variable]:
        return [x for x in self.variables if not x.has_value]

    # check valid or invalid
    def check(self):
        arr = self.grid

        def check_true(arr, row=0, col=0):
            if row == 9:
                return True
            if col == 9:
                return check_true(arr, row + 1, 0)
            if arr[row][col] != 0:
                return check_true(arr, row, col + 1)
            for num in range(1, 10):
                if (num not in arr[row] and
                        all(num != arr[i][col] for i in range(9)) and
                        all(num != arr[i // 3 + row // 3 * 3][col // 3 * 3 + i % 3] for i in range(9))):
                    arr[row][col] = num
                    if check_true(arr, row, col + 1):
                        return True
                    arr[row][col] = 0
            return False

        arr_copy = [row[:] for row in arr]
        check_true(arr_copy)
        return arr_copy

    def print_assignments(self):
        for i in self.check():
            print(i)

    def calculate_neighbors(self):
        for variable in self.variables:
            for constraint in self.constraints:
                if variable in constraint.variables:
                    for other_var in constraint.variables:
                        if other_var.name is not variable.name:
                            variable.neighbors.add(other_var)
