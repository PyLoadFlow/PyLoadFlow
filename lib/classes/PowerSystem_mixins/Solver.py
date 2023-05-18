import numpy as np

from lib.solvers import *
from lib.errors import ConvergenceError


class Solver:
    def solving_steps(self, method="current inyections", max_nit=25, tol=1e-9):
        self.select_solver(method)

        for nit in range(max_nit + 1):
            errv, J = self.do_step()

            yield nit, J, errv

            if err := np.abs(errv).max() <= tol:
                break

            if nit == max_nit:
                raise ConvergenceError(max_nit, err)

    def solve(self, *args, **kwargs):
        for _ in self.solving_steps(*args, **kwargs):
            pass

    def do_step(self):
        return next(self.solver)
    
    def select_solver(self, method):
        self.solver = {
            "current inyections": current_injections_solver,
            "ci": current_injections_solver,
            "fast decoupled": fast_decoupled_solver,
            "fdlf": fast_decoupled_solver,
        }[method](self)
