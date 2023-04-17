from lib.classes.Bus.buses import SlackBus, PVBus, PQBus


def not_slack_buses(self):
    return filter(lambda y: not isinstance(self.buses[y], SlackBus), range(self.number_of_buses))


def pv_buses(self):
    return filter(lambda y: isinstance(self.buses[y], PVBus), range(self.number_of_buses))


def pq_buses(self):
    return filter(lambda y: isinstance(self.buses[y], PQBus), range(self.number_of_buses))
