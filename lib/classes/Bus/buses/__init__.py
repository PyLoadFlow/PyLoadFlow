from lib.classes.Bus import Bus, define
import numpy as np


@define
class SlackBus(Bus):
    def define_initial_conditions(self, y, V, δ):
        self.power_system.bus_real_voltage_pu[y] = V * np.cos(δ)
        self.power_system.bus_imaginary_voltage_pu[y] = V * np.sin(δ)


@define
class PVBus(Bus):
    def define_initial_conditions(self, y, P, V, δ=0):
        self.power_system.bus_programed_real_power[y] = P
        self.power_system.bus_real_voltage_pu[y] = V * np.cos(δ)
        self.power_system.bus_imaginary_voltage_pu[y] = V * np.sin(δ)


@define
class PQBus(Bus):
    def define_initial_conditions(self, y, P, Q):
        self.power_system.bus_programed_real_power[y] = -P
        self.power_system.bus_programed_reactive_power[y] = -Q


@define
class ZIPBus(PQBus):
    # zip: list[float] = [0, 0, 1]
    # ziq: list[float] = [0, 0, 1]
    pass
