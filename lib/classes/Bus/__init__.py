# pyright: reportUndefinedVariable=false
from attrs import define, field

from lib.typing import *
from lib.decorators import electric_bus_method as electric


@define
class Bus:
    yid: int = field(init=False)
    connected_buses_yids: list[int] = field(init=False, factory=list[int])

    power_system: "PowerSystem" = field(init=False)
    _min_connected_bus_yid: int = field(init=False)
    _max_connected_bus_yid: int = field(init=False)

    @property
    @electric
    def programmed_current_pu(self):
        return np.conj(S[y] / V[y])

    def define_initial_conditions(self, *_, **__):
        pass
