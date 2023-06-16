# pyright: reportUndefinedVariable=false
import numpy as np

from pyloadflow.classes.Bus import Bus
from pyloadflow.decorators import electric_power_system_as_property as electric


"""
Note: for special behaviors at any solving algorithms, the methods bust be named with the algorithm 
initials. eg: A method Bus.faz() used in fast decoupled load flow, must be named Bus.fdlf_faz()
"""


class PVBus(Bus):
    """
    A bus with a fixed real power and voltage magnitude and variable reactive power and voltage phase
    """

    def __init__(self, power_system, fixed_voltage):
        """
        Args:
            power_system (lib.classes.PowerSystem.PowerSystem): the system that this bus is connected
            fixed_voltage (float): voltage magnitude in pu
        """

        Bus.__init__(self, power_system)
        self.fixed_voltage = fixed_voltage

    @electric
    def cilf_diagonal_quadrant_abcd(self) -> tuple[float, float, float, float]:
        """
        creates the a, b, c and d parameters that will be added to the diagonal quadrant

        "a" corresponds to the dIr/dU

        "b" corresponds to the dIm/dQ

        "c" corresponds to the dIr/dU

        "d" corresponds to the dIm/dQ

        Returns:
             -> tuple[float, float, float, float]:: a, b, c and d
        """

        V2 = np.abs(V[y]) ** 2

        a = (Q[y] - P[y] * U[y] / E[y]) / V2
        b = U[y] / V2
        c = (P[y] + Q[y] * U[y] / E[y]) / V2
        d = -E[y] / V2

        return a, b, c, d
