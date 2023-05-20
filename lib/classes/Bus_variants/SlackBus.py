# pyright: reportUndefinedVariable=false
from lib.classes.Bus import Bus


class SlackBus(Bus):
    def store_in_system(self):
        self.yid = 0
        self.power_system.buses[0] = self
