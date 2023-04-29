import numpy as np

from lib.classes.Bus import Bus, SlackBus, PQBus, PVBus
from lib.decorators.electric import electric_power_system_as_self as electric

class BusList:
    
    def __init__(self):
        self.buses = []
        
    def add_bus(self, *args, **kwargs):
        return Bus(power_system=self, *args, **kwargs)
    
    
    def add_slack_bus(self, V=1.0, δ=0.0):
        return SlackBus(self, 0, V_pu=V, δ_rad=δ)


    def add_pq_bus(self, P, Q=0.0):
        return PQBus(self, P_load_pu=P, Q_load_pu=Q)


    def add_pv_bus(self, P, V=1.0):
        return PVBus(self, fixed_voltage=V, P_gen_pu=P)


    def add_load_bus(self, P, pf=1.0):
        return PQBus(self, P_load_pu=P, Q_load_pu=P * np.tan(np.arccos(pf)))


    def add_noload_bus(self):
        return PQBus(self)


