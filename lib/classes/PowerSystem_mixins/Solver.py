import numpy as np

from lib.solvers import *
from lib.errors import ConvergenceError


class Solver:
    """
    * calls solvers and manage number of iterations
    * checks convergence and evaluates stop criteria
    * give the interfce to make iterations manually
    """

    def solving_steps(self, method="current inyections", max_nit=25, tol=1e-9):
        """
        (generator) Counts number of iterations done and the error gotten from any one, raises if the max nit is exceeded

        Args:
            method ("current inyections" | "cilf" | "fast decoupled" | "fdlf"): method to solve the system. Defaults to "current inyections".
            max_nit (int, optional): max number of iterations. Defaults to 25.
            tol (float, optional): max absolute error allowed to stop iterating. Defaults to 1e-9.

        Raises:
            ConvergenceError: if max_nit is finished and the tol has not been minor

        Yields:
            (int, lil_matrix, NDArray): a tuple with: the iteration number, current jacobian and error vector
        """
        self.select_solver(method)

        for nit in range(max_nit + 1):
            errv, J = self.do_step()

            yield nit, J, errv

            if err := np.abs(errv).max() <= tol:
                break

            if nit == max_nit:
                raise ConvergenceError(max_nit, err)

    def solve(self, method="current inyections", max_nit=25, tol=1e-9):
        """
        Solves the system inmediatly

        Args:
            method ("current inyections" | "cilf" | "fast decoupled" | "fdlf"): method to solve the system. Defaults to "current inyections".
            max_nit (int, optional): max number of iterations. Defaults to 25.
            tol (float, optional): max absolute error allowed to stop iterating. Defaults to 1e-9.

        """

        for _ in self.solving_steps(method, max_nit, tol):
            pass

    def do_step(self):
        """Takes the next step value from solving_steps() active solver"""
        return next(self.solver)

    def select_solver(self, method):
        """Selects with solver apply to make iterations"""
        self.solver = {
            "current inyections": current_injections_solver,
            "cilf": current_injections_solver,
            "fast decoupled": fast_decoupled_solver,
            "fdlf": fast_decoupled_solver,
        }[method](self)
