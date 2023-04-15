from lib.classes.Bus.buses import SlackBus, PVBus, PQBus


def add_bus(self, bus, *args, **kwargs):
    # giving object reference of his system
    bus.power_system = self

    # saving initial data
    bus.define_initial_conditions(len(self.buses), *args, **kwargs)

    # adding object to the list
    self.buses.append(bus)

    # returning to make able to save into a variable
    return bus


def add_slack_bus(self, V=1.0, δ=0.0):
    return self.add_bus(SlackBus(), V, δ)


def add_pq_bus(self, P=0.0, Q=0.0):
    return self.add_bus(PQBus(), P, Q)


def add_pv_bus(self, P=0.0, V=1.0, δ=0.0):
    return self.add_bus(PVBus(), P, V, δ)
