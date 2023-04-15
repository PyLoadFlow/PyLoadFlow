from attrs import define, field

from lib.classes.Bus import Bus

from lib.decorators import bind_methods
from lib.typing import *

from lib.classes.PowerSystem.add_bus import *
from lib.classes.PowerSystem.connect_buses import *
from lib.classes.PowerSystem.allocate_electric_params import *


@bind_methods(
    add_bus,
    add_pq_bus,
    add_pv_bus,
    add_slack_bus,
    allocate_electric_params,
    build_line_series_admittance_pu_diagonal,
    connect_buses_by_id,
    connect_buses,
)
@define
class PowerSystem:
    # main
    number_of_buses: int = field(default=0)
    buses: list[Bus] = []

    # voltage
    bus_voltage_pu: cplv = field(init=False)
    bus_real_voltage_pu: vect = field(init=False)
    bus_imaginary_voltage_pu: vect = field(init=False)

    # power
    bus_programed_apparent_power: cplv = field(init=False)
    bus_programed_real_power: vect = field(init=False)
    bus_programed_reactive_power: vect = field(init=False)

    # admittance
    line_series_admittance_pu: lil_matrix = field(init=False)
    line_series_conductance_pu: lil_matrix = field(init=False)
    line_series_susceptance_pu: lil_matrix = field(init=False)
    line_power_flow_pu: cplm = field(init=False)

    def __init__(self, n):
        self.__attrs_init__(n)

    def __attrs_post_init__(self):
        self.allocate_electric_params()

    def compile(self):
        self.build_line_series_admittance_pu_diagonal()
