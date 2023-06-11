# pyright: reportUndefinedVariable=false
import numpy as np

from loadwolf.classes.PowerSystem_mixins.Allocator import Allocator
from loadwolf.decorators import electric_power_system_as_self as electric
from loadwolf.errors import ConvergenceError
from loadwolf.solvers import *


class Solver:
    """
    * calls solvers and manage number of iterations
    * checks convergence and evaluates stop criteria
    * give the interfce to make iterations manually
    """

    @electric
    def calculated_apparent_power(self):
        S_calc = np.empty(n, dtype=Allocator.complex_dtype)

        for y in range(n):
            S_calc[y] = Y[y].dot(V)

        return (S_calc * V.conj()).conj()

    @electric
    def apparent_power_mismatch(self):
        return S - self.calculated_apparent_power()

    def step_by_step(self, method="current inyections", max_nit=25, tol=1e-9):
        """
        (generator) Counts number of iterations done and the error gotten from any one, raises if the max nit is exceeded

        Args:
            method ("current inyections" | "cilf" | "fast decoupled" | "fdlf"): method to solve the system. Defaults to "current inyections".
            max_nit (int, optional): max number of iterations. Defaults to 25.
            tol (float, optional): max absolute error allowed to stop iterating. Defaults to 1e-9.

        Raises:
            ConvergenceError: if max_nit is finished and the tol has not been minor

        Yields:
            (int, tuple, dict): a tuple with: the iteration number, current jacobian and error vector
        """
        self.verify()

        self.select_solver(method)

        for nit in range(max_nit + 1):
            err, data = self.do_step()
            max_err = np.abs(err).max()

            yield nit, max_err, data

            if max_err <= tol:
                self.post_solve()
                break

            if nit == max_nit:
                raise ConvergenceError(max_nit, max_err)

    def solve(self, method="current inyections", max_nit=25, tol=1e-9):
        """
        Solves the system inmediatly

        Args:
            method ("current inyections" | "cilf" | "fast decoupled" | "fdlf"): method to solve the system. Defaults to "current inyections"
            max_nit (int, optional): max number of iterations. Defaults to 25
            tol (float, optional): max absolute error allowed to stop iterating. Defaults to 1e-9

        """
        self.verify()

        for _ in self.step_by_step(method, max_nit, tol):
            pass

        self.post_solve()

    def do_step(self):
        """
        Takes the next step value from step_by_step() active solver
        """

        return next(self.solver)

    def select_solver(self, method="current inyections"):
        """
        Selects with solver apply to make iterations

        Args:
            method ("current inyections" | "cilf" | "fast decoupled" | "fdlf"): method to solve the system. Defaults to "current inyections"
        """

        self.solver = {
            "current inyections": current_injections_solver,
            "cilf": current_injections_solver,
            "fast decoupled": fast_decoupled_solver,
            "fdlf": fast_decoupled_solver,
        }[method](self)

    @electric
    def post_solve(self):
        """
        Makes final calculations for every method, at the moment:

        1. calculates the slack bus injected power
        1. calculates the PV buses Q value
        """

        # P and Q for the slack bus
        self.bus_apparent_generation_power_pu[0] = (
            V[0].conj() * Y[0].dot(V)
        ).conj() + self.bus_apparent_load_power_pu[0]

        # Q for PV buses
        self.bus_reactive_generation_power_pu[pv_buses,] = (
            self.calculated_apparent_power()[pv_buses,].imag + self.bus_reactive_load_power_pu[pv_buses,]
        )

    def verify(self):
        pass
