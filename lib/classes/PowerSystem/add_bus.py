import numpy as np

from lib.classes.Bus.buses import SlackBus, PVBus, PQBus


def add_bus(self, bus, *args, **kwargs):
    # giving object reference of his system
    bus.power_system = self
    bus.yid = len(self.buses)
    bus.connected_buses_yids.append(bus.yid)

    # saving initial data
    bus.define_initial_conditions(*args, **kwargs)

    # adding object to the list
    self.buses.append(bus)

    # returning to make able to save into a variable
    return bus


def add_slack_bus(self, V=1.0, δ=0.0):
    return self.add_bus(SlackBus(), V, δ)


def add_pq_bus(self, P, Q=0.0):
    return self.add_bus(PQBus(), P, Q)


def add_pv_bus(self, P, V=1.0):
    return self.add_bus(PVBus(fixed_voltage=V), P)


def add_load_bus(self, P, pf=1.0):
    return self.add_bus(PQBus(), P, P * np.tan(np.arccos(pf)))


def add_noload_bus(self):
    return self.add_bus(PQBus(), 0, 0)
