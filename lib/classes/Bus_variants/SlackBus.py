# pyright: reportUndefinedVariable=false
import numpy as np

from lib.classes.Bus import Bus
from lib.decorators import electric_power_system_as_property as electric


"""
Note: for special behaviors at any solving algorithms, the methods bust be named with the algorithm 
initials. eg: A method Bus.faz() used in fast decoupled load flow, must be named Bus.fdlf_faz()
"""


class SlackBus(Bus):
    def store_in_system(self):
        self.yid = 0
        self.power_system.buses[0] = self
