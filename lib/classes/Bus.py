import numpy as np

from lib.decorators import electric_power_system_as_property as electric


class Bus:
    index_dtype = np.uint16

    def __init__(self, power_system):
        # pointing the power system
        self.power_system = power_system
        self.store_in_system()

        # allocating connected buses array
        self.connected_buses = np.array([self.yid], dtype=Bus.index_dtype)

    def store_in_system(self):
        self.yid = len(self.power_system.buses)
        self.power_system.buses.append(self)

    @electric
    def define_initial_conditions(self, pload=0.0, pgen=0.0, qgen=0.0, qload=0.0, v_initial=1.0, phase=0.0):
        # initialazing voltage
        E[y] = v_initial * np.cos(phase)
        U[y] = v_initial * np.sin(phase)

        # initializing power
        P[y] = pgen - pload
        Q[y] = qgen - qload

    def store_connected_bus_yid(self, yid):
        self.connected_buses = np.append(self.connected_buses, [yid])

    @property
    @electric
    def programmed_current_pu(self):
        return np.conj(S[y] / V[y])


class SlackBus(Bus):
    pass


class PQBus(Bus):
    pass


class PVBus(Bus):
    def __init__(self, power_system, fixed_voltage):
        Bus.__init__(self, power_system)
        self.fixed_voltage = fixed_voltage


class ZIPBus(PQBus):
    pass
