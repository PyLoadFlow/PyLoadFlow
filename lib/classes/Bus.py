import numpy as np


class Bus:
    index_dtype = np.uint8

    def __init__(self, power_system):
        # pointing the power system
        self.power_system = power_system

        # storing
        self.yid = len(self.power_system.buses)
        self.power_system.buses.append(self)

        # allocating connected buses array
        self.connected_buses = np.array([self.yid], dtype=Bus.index_dtype)

    def define_initial_conditions(self, P_load, P_gen=0, Q_gen=0, Q_load=0, V=1, δ=0):
        # initialazing voltage
        self.power_system.bus_real_voltage_pu[self.yid] = V * np.cos(δ)
        self.power_system.bus_imaginary_voltage_pu[self.yid] = V * np.sin(δ)

        # initializing power
        self.power_system.bus_programed_real_power[self.yid] = P_gen - P_load
        self.power_system.bus_programed_reactive_power[self.yid] = Q_gen - Q_load
