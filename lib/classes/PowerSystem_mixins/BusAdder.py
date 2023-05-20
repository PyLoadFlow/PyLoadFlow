from itertools import chain
import numpy as np

from lib.classes.Bus import Bus
from lib.classes.Bus_variants.SlackBus import SlackBus
from lib.classes.Bus_variants.PQBus import PQBus
from lib.classes.Bus_variants.PVBus import PVBus


class BusAdder:
    """Mixin of PowerSystem to manage bus creation from class instance methods"""

    def __init__(self):
        self.buses = [None]
        self.pq_buses_yids = np.empty(0, dtype=Bus.index_dtype)
        self.pv_buses_yids = np.empty(0, dtype=Bus.index_dtype)
        self.slack_bus_yid = 0

    def add_slack_bus(self, V=1.0, δ=0.0):
        """Creates a slack bus (fixed voltage magnitude and phase angle)
        IMPORTANT: per now, the SlackBus instance will have the yid 0 in every case

        Args:
            δ (float): voltage phase angle in radians
            V (float): voltage magnitude in pu
        """
        bus = SlackBus(self)
        bus.define_initial_conditions(v_initial=V, phase=δ)
        return bus

    def add_pq_bus(self, P: float, Q=0.0):
        """Creates a pq bus (fixed load or generation real and reactive power)

        Args:
            P (float): real power magnitude in pu
            Q (float): reactive power magnitude in pu
        """
        self.pq_buses_yids = np.append(self.pq_buses_yids, [len(self.buses)])
        bus = PQBus(self)
        bus.define_initial_conditions(pload=P, qload=Q)
        return bus

    def add_pv_bus(self, P: float, V=1.0):
        """Creates a pv bus (fixed voltage magnitude and generation real power)

        Args:
            P (float): real power magnitude in pu
            V (float): voltage magnitude in pu
        """
        self.pv_buses_yids = np.append(self.pv_buses_yids, [len(self.buses)])
        bus = PVBus(self, fixed_voltage=V)
        bus.define_initial_conditions(pgen=P, v_initial=V)
        return bus

    def add_load_bus(self, P: float, pf=1.0):
        """Creates a pq bus (fixed load real and reactive power) given real load and power factor

        Args:
            P (float): real power magnitude in pu
            pf (float): power factor as decimal (0~1)
        """
        return self.add_pq_bus(P, P * np.tan(np.arccos(pf)))

    def add_noload_bus(self):
        """Creates a pq bus (fixed load real and reactive power) with P=0 and Q=0"""
        return PQBus(self)
