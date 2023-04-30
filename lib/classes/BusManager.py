from itertools import chain
import numpy as np

from lib.classes.Bus import Bus, SlackBus, PQBus, PVBus

# from lib.decorators.electric import electric_power_system_as_self as electric


class BusManager:
    def __init__(self):
        self.buses = []
        self.pq_buses_yids = np.empty(0, dtype=Bus.index_dtype)
        self.pv_buses_yids = np.empty(0, dtype=Bus.index_dtype)
        self.slack_bus_yid = 0

    def add_bus(self, *args, **kwargs):
        bus = Bus(power_system=self)
        bus.define_initial_conditions(*args, **kwargs)
        return bus

    def add_slack_bus(self, V=1.0, δ=0.0):
        bus = SlackBus(self)
        bus.define_initial_conditions(v_initial=V, phase=δ)
        return bus

    def add_pq_bus(self, P, Q=0.0):
        self.pq_buses_yids = np.append(self.pq_buses_yids, [len(self.buses)])
        bus = PQBus(self)
        bus.define_initial_conditions(pload=P, qload=Q)
        return bus

    def add_pv_bus(self, P, V=1.0):
        self.pv_buses_yids = np.append(self.pv_buses_yids, [len(self.buses)])
        bus = PVBus(self, fixed_voltage=V)
        bus.define_initial_conditions(pgen=P, v_initial=V)
        return bus

    def add_load_bus(self, P, pf=1.0):
        return self.add_pq_bus(P, P * np.tan(np.arccos(pf)))

    def add_noload_bus(self):
        return PQBus(self)
        
    @property
    def not_slack_buses_yids(self):
        return chain(self.pq_buses_yids, self.pv_buses_yids)
