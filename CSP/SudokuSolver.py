import time
from typing import Optional
from PriorityQueue import PriorityQueue
from CSP.SudokuProblem import Problem
from CSP.SudokuVariable import Variable


class Solver:
    def __init__(self, problem: Problem):
        self.problem = problem

    def is_finished(self) -> bool:
        return all([x.is_satisfied() for x in self.problem.constraints]) and len(
            self.problem.get_unassigned_variables()) == 0

    def solve(self):
        self.problem.calculate_neighbors()
        start = time.time()
        result = self.backtracking()
        end = time.time()
        time_elapsed = (end - start) * 1000
        if result:
            print(f'Solved after {time_elapsed} ms')
        else:
            print(f'Failed to solve after {time_elapsed} ms')

    def backtracking(self):
        if len(self.problem.get_unassigned_variables()) == 0:
            return True

        # MRV: minimum remaining value
        var = self.select_unassigned_variable()

        # least constraining value
        queue = self.order_domain_values(var)

        while queue.size > 0:
            var.value = queue.dequeue()
            if self.is_consistent(var) and self.forward_check(var):
                result = self.backtracking()
                if result:
                    return True

            var.value = None

        return False

    def select_unassigned_variable(self) -> Optional[Variable]:
        unassigned_variables = self.problem.get_unassigned_variables()
        return min(unassigned_variables, key=lambda x: len(x.domain))

    def order_domain_values(self, var: Variable):
        queue = PriorityQueue()
        for value in var.domain:
            var.value = value
            contract = 0
            for neighbor in var.neighbors:
                if not neighbor.has_value:
                    for other_var_candidate in neighbor.domain:
                        neighbor.value = other_var_candidate
                        if not self.is_consistent(neighbor):
                            contract += 1
                        neighbor.value = None
            queue.enqueue_with_priority(contract, value)
            var.value = None
        return queue

    def forward_check(self, var):
        for neighbor in var.neighbors:
            if not neighbor.has_value:
                for other_var_candidate in neighbor.domain:
                    neighbor.value = other_var_candidate
                    if not self.is_consistent(neighbor):
                        neighbor.domain.remove(other_var_candidate)
                        if len(neighbor.domain) == 0:
                            return False
                    neighbor.value = None

        return True

    def is_consistent(self, var: Variable):
        for constraint in self.problem.constraints:
            if var in constraint.variables and not constraint.is_satisfied():
                return False
        return True
