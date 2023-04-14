from attrs import define, field

from lib.typing import *


@define
class Bus:
    # yid: int = field(init=False)
    power_system: "PowerSystem" = field(init=False)
    # _min_connected_bus_yid: int = field(init=False)
    # _max_connected_bus_yid: int = field(init=False)

    def define_initial_conditions(self, *_, **__):
        pass
