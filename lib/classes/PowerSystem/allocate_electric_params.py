from lib.typing import *


def allocate_electric_params(self):
    n = self.number_of_buses

    # allocate voltages with inicial values of 1
    self.bus_voltage_pu = np.ones(n, dtype=cplx)

    # allocate powers with inicial values of 0
    self.bus_programed_apparent_power = np.empty(n, dtype=cplx)

    # allocate admittances, they are at majority constant zeros, so it's sparse matrix
    self.line_series_admittance_pu = lil_matrix((n, n), dtype=cplx)  # type: ignore

    # V = E + jU
    self.bus_real_voltage_pu = self.bus_voltage_pu.real
    self.bus_imaginary_voltage_pu = self.bus_voltage_pu.imag

    # S = P + jQ
    self.bus_programed_real_power = self.bus_programed_apparent_power.real
    self.bus_programed_reactive_power = self.bus_programed_apparent_power.imag

    # Y = G + jβ
    self.line_series_conductance_pu = self.line_series_admittance_pu.real
    self.line_series_susceptance_pu = self.line_series_admittance_pu.imag
