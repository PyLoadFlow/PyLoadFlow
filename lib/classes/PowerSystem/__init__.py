from attrs import define, field
from scipy.sparse import lil_matrix

from lib.classes.Bus import Bus

from lib.classes.Bus.buses import SlackBus, PVBus, PQBus
from lib.decorators import electric
from lib.typing import *


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
        self.__attrs_init__(n)  # type: ignore

    def __attrs_post_init__(self):
        self.allocate_electric_params()

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

    def connect_buses(self, bus_i, bus_j, *args, **kwargs):
        # getting busi and busj indexes to pass to connect_buses_by_id()
        return self.connect_buses_by_id(self.buses.index(bus_i) + 1, self.buses.index(bus_j) + 1, *args, **kwargs)

    @electric
    def connect_buses_by_id(self, i, j, z, y=0.0j):
        # fulfilling IEEE std. to numerate from 1 and not from 0
        i -= 1
        j -= 1

        # making sure that the buses are different
        if i == j:
            return

        # transforming to admittance
        Y[i, j] = Y[j, i] = -1 / z

        # adding shunt susceptance to diagonal
        Y[i, i] += y / 2  # type: ignore
        Y[j, j] += y / 2  # type: ignore

    def allocate_electric_params(self):
        n = self.number_of_buses

        # allocate voltages with inicial values of 1
        self.bus_voltage_pu = np.ones(n, dtype=cplx)

        # allocate powers with inicial values of 0
        self.bus_programed_apparent_power = np.empty(n, dtype=cplx)

        # allocate admittances, they are at majority constant zeros, so it's sparse matrix
        self.line_series_admittance_pu = lil_matrix((n, n), dtype=cplx)  # type: ignore

        # initializing empty Ybus diagonal because empty() doesnt warranty zero initial value
        for i in range(n):
            self.line_series_admittance_pu[i, i] = 0

        # V = E + jU
        self.bus_real_voltage_pu = self.bus_voltage_pu.real
        self.bus_imaginary_voltage_pu = self.bus_voltage_pu.imag

        # S = P + jQ
        self.bus_programed_real_power = self.bus_programed_apparent_power.real
        self.bus_programed_reactive_power = self.bus_programed_apparent_power.imag

        # Y = G + jβ
        self.line_series_conductance_pu = self.line_series_admittance_pu.real
        self.line_series_susceptance_pu = self.line_series_admittance_pu.imag

    def compile(self):
        self.build_line_series_admittance_pu_diagonal()

    @electric
    def build_line_series_admittance_pu_diagonal(self):
        # calculating self admittances from sum of mutual admittances
        for y in range(self.number_of_buses):
            Y[y, y] = -Y[y].sum()  # type: ignore
