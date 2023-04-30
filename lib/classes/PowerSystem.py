import numpy as np

from lib.classes.Allocator import Allocator
from lib.classes.BusManager import BusManager
from lib.classes.BusConnector import BusConnector


class PowerSystem(Allocator, BusManager, BusConnector):
    complex_dtype = np.complex128
    float_dtype = np.float64

    def __init__(self, n):
        Allocator.__init__(self, n)
        BusManager.__init__(self)
        BusConnector.__init__(self)

    def compile(self):
        self.build_line_series_admittance_pu_diagonal()

        for bus in self.buses:
            bus.connected_buses.sort()
