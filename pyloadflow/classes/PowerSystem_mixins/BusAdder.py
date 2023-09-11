import numpy as np

from pyloadflow.classes.Bus import Bus
from pyloadflow.classes.Bus_variants.SlackBus import SlackBus
from pyloadflow.classes.Bus_variants.PQBus import PQBus
from pyloadflow.classes.Bus_variants.PVBus import PVBus


class BusAdder:
    """
    Mixin of PowerSystem to manage bus creation from class instance methods
    """

    def __init__(self):
        self.buses = [None]
        self.pq_buses_yids = np.empty(0, dtype=Bus.index_dtype)
        self.pv_buses_yids = np.empty(0, dtype=Bus.index_dtype)
        self.slack_bus_yid = 0

    def add_slack_bus(self, V=1.0, δ=0.0, pload=0.0, qload=0.0) -> SlackBus:
        """
        Creates a slack bus (fixed voltage magnitude and phase angle)
        IMPORTANT: per now, the SlackBus instance will have the yid 0 in every case

        Args:
            δ (float): voltage phase angle in radians
            V (float): voltage magnitude in pu
            pload (float): load real power magnitude in pu if it exist
            qload (float): load real power magnitude in pu if it exist
        """

        bus = SlackBus(self)
        bus.define_initial_conditions(v_initial=V, phase=δ, pload=pload, qload=qload)
        return bus

    def add_pq_bus(self, P: float, Q=0.0) -> PQBus:
        """
        Creates a pq bus (fixed load or generation real and reactive power)

        Args:
            P (float): load real power magnitude in pu
            Q (float): load reactive power magnitude in pu
        """

        self.pq_buses_yids = np.append(self.pq_buses_yids, [len(self.buses)])
        bus = PQBus(self)
        bus.define_initial_conditions(pload=P, qload=Q)
        return bus

    def add_pv_bus(self, P: float, V=1.0, pload=0.0, qload=0.0, Qmin=-20.0, Qmax=20.0) -> PVBus:
        """
        Creates a pv bus (fixed voltage magnitude and generation real power)

        Args:
            P (float): generated real power magnitude in pu
            V (float): voltage magnitude in pu
            pload (float): load real power magnitude in pu if it exist
            qload (float): load real power magnitude in pu if it exist
            Qmin (float): generated reactive power magnitude min limit in pu
            Qmax (float): generated reactive power magnitude max limit in pu
        """

        self.pv_buses_yids = np.append(self.pv_buses_yids, [len(self.buses)])
        bus = PVBus(self, fixed_voltage=V, limits=(Qmin, Qmax))
        bus.define_initial_conditions(pgen=P, v_initial=V, pload=pload, qload=qload)
        return bus

    def add_load_bus(self, P: float, pf=1.0) -> PQBus:
        """
        Creates a pq bus (fixed load real and reactive power) given real load and power factor

        Args:
            P (float): real power magnitude in pu
            pf (float): power factor as decimal (0~1)
        """

        return self.add_pq_bus(P, P * np.tan(np.arccos(pf)))

    def add_noload_bus(self) -> PQBus:
        """
        Creates a pq bus (fixed load real and reactive power) with P=0 and Q=0"""
        return self.add_pq_bus(0, 0)
