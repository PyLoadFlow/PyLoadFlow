import numpy as np

from lib.classes.PowerSystem_mixins.Allocator import Allocator
from lib.classes.PowerSystem_mixins.BusAdder import BusAdder
from lib.classes.PowerSystem_mixins.BusConnector import BusConnector
from lib.classes.PowerSystem_mixins.Solver import Solver


class PowerSystem(Allocator, BusAdder, BusConnector, Solver):
    complex_dtype = np.complex128
    float_dtype = np.float64

    def __init__(self, n):
        Allocator.__init__(self, n)
        BusAdder.__init__(self)
        BusConnector.__init__(self)
        Solver.__init__(self)

    def compile(self):
        self.build_line_series_admittance_pu_diagonal()

        for bus in self.buses:
            bus.connected_buses.sort()

    def run(self, *args, **kwargs):
        self.compile()
        self.solve(*args, **kwargs)
