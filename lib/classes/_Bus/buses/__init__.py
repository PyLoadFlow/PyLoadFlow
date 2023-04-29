from lib.classes.Bus import Bus, define
import numpy as np


@define
class SlackBus(Bus):
    def define_initial_conditions(self, V, δ):
        self.power_system.bus_real_voltage_pu[self.yid] = V * np.cos(δ)
        self.power_system.bus_imaginary_voltage_pu[self.yid] = V * np.sin(δ)


@define
class PVBus(Bus):
    fixed_voltage: float

    def define_initial_conditions(self, P):
        self.power_system.bus_programed_real_power[self.yid] = P
        self.power_system.bus_real_voltage_pu[self.yid] = self.fixed_voltage


@define
class PQBus(Bus):
    def define_initial_conditions(self, P, Q):
        self.power_system.bus_programed_real_power[self.yid] = -P
        self.power_system.bus_programed_reactive_power[self.yid] = -Q


@define
class ZIPBus(PQBus):
    # zip: list[float] = [0, 0, 1]
    # ziq: list[float] = [0, 0, 1]
    pass
