# pyright: reportUndefinedVariable=false
import numpy as np

from pyloadflow.classes.Bus import Bus
from pyloadflow.decorators import electric_power_system_as_property as electric


"""
Note: for special behaviors at any solving algorithms, the methods bust be named with the algorithm 
initials. eg: A method Bus.faz() used in fast decoupled load flow, must be named Bus.fdlf_faz()
"""


class PQBus(Bus):
    """
    A bus with a fixed real and reactive power and variable voltage magnitude and phase
    """

    @electric
    def cilf_quadrant(self, x: int):
        return [
            [+β[x, y], -G[x, y]],
            [-G[x, y], -β[x, y]],
        ]

    @electric
    def cilf_diagonal_quadrant(self):
        """
        creates the a, b, c and d matrix that will be added to the diagonal quadrant

        "a" corresponds to the dIr/dU

        "b" corresponds to the dIm/dE

        "c" corresponds to the dIr/dU

        "d" corresponds to the dIm/dE

        Returns:
            tuple[float, float, float, float]:: a, b, c and d
        """

        V4 = np.abs(V[y]) ** 4
        a = (Q[y] * (E[y] ** 2 - U[y] ** 2) - 2 * P[y] * U[y] * E[y]) / V4
        b = (P[y] * (U[y] ** 2 - E[y] ** 2) - 2 * Q[y] * U[y] * E[y]) / V4

        return [
            [+a, b],
            [-b, a],
        ]
