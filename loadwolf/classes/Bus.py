# pyright: reportUndefinedVariable=false
import numpy as np

from loadwolf.decorators import electric_power_system_as_property as electric

"""
Note: for special behaviors at any solving algorithms, the methods bust be named with the algorithm 
initials. eg: A method Bus.faz() used in fast decoupled load flow, must be named Bus.fdlf_faz()
"""


class Bus:
    """
    Stores the bus configurations and behaviors for any solving algorithm.
    """

    index_dtype = np.uint16

    def __init__(self, power_system):
        # pointing the power system
        self.power_system = power_system
        self.store_in_system()

        # allocating connected buses array
        self.connected_buses = np.array([self.yid], dtype=Bus.index_dtype)

    def store_in_system(self):
        """
        Saves yid value and register the bus in the main listo to make loops
        """

        self.yid = len(self.power_system.buses)
        self.power_system.buses.append(self)

    @electric
    def define_initial_conditions(self, pload=0.0, pgen=0.0, qgen=0.0, qload=0.0, v_initial=1.0, phase=0.0):
        """
        Writes the initial values to initialize all the data matrices (doesn't fixes them),
        default params makes a plain start.

        Args:
            pload (float, optional): load real power magnitude in pu. Defaults to 0.0.
            pgen (float, optional): generated real power magnitude in pu. Defaults to 0.0.
            qgen (float, optional): generated reactive power magnitude in pu. Defaults to 0.0.
            qload (float, optional): load reactive power magnitude in pu. Defaults to 0.0.
            v_initial (float, optional): initial voltage magnitude in pu. Defaults to 1.0.
            phase (float, optional): initial voltage phase in radians. Defaults to 0.0.
        """

        # initialazing voltage
        E[y] = v_initial * np.cos(phase)
        U[y] = v_initial * np.sin(phase)

        # initializing power
        self.power_system.bus_apparent_generation_power_pu[y] = pgen + qgen * 1j
        self.power_system.bus_apparent_load_power_pu[y] = pload + qload * 1j

    def store_connected_bus_yid(self, yid):
        """
        Registers the connection between this bus and another to make loops
        """

        self.connected_buses = np.append(self.connected_buses, [yid])

    @property
    @electric
    def programmed_current_pu(self):
        return np.conj(S[y] / V[y])
