# pyright: reportUndefinedVariable=false
import numpy as np

from pyloadflow.classes.Bus import Bus
from pyloadflow.decorators import electric_power_system_as_property as electric


"""
Note: for special behaviors at any solving algorithms, the methods bust be named with the algorithm 
initials. eg: A method Bus.faz() used in fast decoupled load flow, must be named Bus.fdlf_faz()
"""


class SlackBus(Bus):
    """
    A bus with a fixed voltage and phase
    """

    def store_in_system(self):
        """
        Saves yid value and register the bus in the main listo to make loops
        """

        self.yid = 0
        self.power_system.buses[0] = self
