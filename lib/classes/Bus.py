import numpy as np


class Bus:
    index_dtype = np.uint16

    def __init__(self, power_system, P_load_pu=0.0, P_gen_pu=0.0, Q_gen_pu=0.0, Q_load_pu=0.0, V_pu=1.0, δ_rad=0.0):
        # pointing the power system
        self.power_system = power_system

        # storing
        self.yid = len(self.power_system.buses)
        self.power_system.buses.append(self)

        # allocating connected buses array
        self.connected_buses = np.array([self.yid], dtype=Bus.index_dtype)

        # initialazing voltage
        self.power_system.bus_real_voltage_pu[self.yid] = V_pu * np.cos(δ_rad)
        self.power_system.bus_imaginary_voltage_pu[self.yid] = V_pu * np.sin(δ_rad)

        # initializing power
        self.power_system.bus_programed_real_power[self.yid] = P_gen_pu - P_load_pu
        self.power_system.bus_programed_reactive_power[self.yid] = Q_gen_pu - Q_load_pu
        
    def store_connected_bus_yid(self,yid):
        self.connected_buses = np.append(self.connected_buses, [yid])


class SlackBus(Bus):
    pass


class PQBus(Bus):
    pass


class PVBus(Bus):
    def __init__(self, power_system, fixed_voltage, *args, **kwargs):
        Bus.__init__(self,power_system, V_pu=fixed_voltage,*args, **kwargs)
        self.fixed_voltage = fixed_voltage


class ZIPBus(PQBus):
    pass
