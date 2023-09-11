# pyright: reportUndefinedVariable=false
import numpy as np
from enum import Enum


from pyloadflow.classes.Bus_variants.PQBus import PQBus
from pyloadflow.decorators import electric_power_system_as_property as electric


"""
Note: for special behaviors at any solving algorithms, the methods bust be named with the algorithm 
initials. eg: A method Bus.faz() used in fast decoupled load flow, must be named Bus.fdlf_faz()
"""


class PVModes(Enum):
    PV = 0
    PQ = 1


class PVBus(PQBus):
    """
    A bus with a fixed real power and voltage magnitude and variable reactive power and voltage phase
    """

    def __init__(self, power_system, fixed_voltage, limits=(-20.0, 20.0)):
        """
        Args:
            power_system (lib.classes.PowerSystem.PowerSystem): the system that this bus is connected
            fixed_voltage (float): voltage magnitude in pu
        """

        PQBus.__init__(self, power_system)
        self.fixed_voltage = fixed_voltage
        self.mode = PVModes.PV
        self.limits = limits

    @electric
    def cilf_quadrant(self, x: int):
        """
        Creates the matrix that will be added to any outside diagonal quadrant

        Parameters:
            x (int): The x value for which the cilf quadrant will be calculated.

        Returns:
            list: The matrix
        """

        # in case of PV bus exceeded limits of power generation
        if self.mode == PVModes.PQ:
            return super().cilf_quadrant(x)

        # normally...
        return [
            [G[x, y] * U[y] / E[y] + β[x, y], 0],
            [β[x, y] * U[y] / E[y] - G[x, y], 0],
        ]

    @electric
    def cilf_diagonal_quadrant(self):
        """
        creates the a, b, c and d parameters that will be added to the diagonal quadrant

        "a" corresponds to the dIr/dU

        "b" corresponds to the dIm/dQ

        "c" corresponds to the dIr/dU

        "d" corresponds to the dIm/dQ

        Returns:
            -> list[list[float, float], list[float, float]]
        """

        # in case of PV bus exceeded limits of power generation
        if self.mode == PVModes.PQ:
            return super().cilf_diagonal_quadrant()

        # normally...
        V2 = np.abs(V[y]) ** 2

        a = (Q[y] - P[y] * U[y] / E[y]) / V2
        b = U[y] / V2
        c = (P[y] + Q[y] * U[y] / E[y]) / V2
        d = -E[y] / V2

        return [
            [a, b],
            [c, d],
        ]

    @electric
    def cilf_after_iteration(self):
        """
        Hook to execute after every iteration of the current injections solver
        """
        if self.mode == PVModes.PV:
            E[y] = np.sqrt(self.fixed_voltage**2 - U[y] ** 2)

    def switch_to_pq(self):
        # in case of PV bus exceeded limits of power generation: transform this bus to PQ type
        self.mode = PVModes.PQ

        # add this bus to the list of PQ buses
        self.power_system.pq_buses_yids = np.append(self.power_system.pq_buses_yids, self.yid)

        # remove this bus from the list of PV buses
        self.power_system.pv_buses_yids = self.power_system.pv_buses_yids[self.power_system.pv_buses_yids != self.yid]
