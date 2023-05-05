from abc import ABC, abstractmethod
from typing import List

from CSP.Constraint import Constraint
from CSP.Variable import Variable


class Problem(ABC):

    def __init__(self, constraints: list[Constraint], variables: list[Variable], name=""):
        self.constraints = constraints
        self.variables = variables
        self.name = name

    def calculate_neighbors(self):
        for variable in self.variables:
            for constraint in self.constraints:
                if variable in constraint.variables:
                    for other_var in constraint.variables:
                        if other_var is not variable:
                            variable.neighbors.add(other_var)

    def get_unassigned_variables(self) -> list[Variable]:
        return [x for x in self.variables if not x.has_value]

    def print_assignments(self):
        for variable in self.variables:
            print(f"{variable.name} is set to {variable.value}")

    def get_neighbor_constraints(self, variable: Variable) -> List[Constraint]:
        return [constraint for constraint in self.constraints if variable in constraint.variables]
