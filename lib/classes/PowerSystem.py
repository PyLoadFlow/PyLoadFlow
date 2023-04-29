from lib.classes.Allocator import Allocator
from lib.classes.BusList import BusList
from lib.classes.BusConnector import BusConnector


class PowerSystem(Allocator, BusList, BusConnector):
    def __init__(self, n):
        Allocator.__init__(self,n)
        BusList.__init__(self)
        BusConnector.__init__(self)
        
    def compile(self):
        self.build_line_series_admittance_pu_diagonal()
        
        for bus in self.buses:
            bus.connected_buses.sort()
