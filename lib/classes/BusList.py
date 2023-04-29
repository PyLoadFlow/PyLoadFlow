from lib.classes.Bus import Bus
from lib.decorators.electric import electric

class BusList:
    def __init__(self):
        self.buses = []
        
    def add_bus(self, bus, *args, **kwargs):
        # giving object reference of his system
        bus.power_system = self
        bus.yid = len(self.buses)
        bus.connected_buses_yids.append(bus.yid)

        # adding object to the list
        self.buses.append(bus)

        # saving initial data
        bus.define_initial_conditions(*args, **kwargs)

        # returning to make able to save into a variable
        return bus
        

