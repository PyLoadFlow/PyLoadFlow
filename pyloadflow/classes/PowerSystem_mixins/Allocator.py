import numpy as np
from scipy.sparse import lil_matrix


class Allocator:
    """Mixin of PowerSystem to allocate the numpy/scipy arrays"""

    complex_dtype = np.complex128
    float_dtype = np.float64
    indexing_dtype = np.uint32
    lite_complex_dtype = np.complex64

    def __init__(self, n: int):
        """
        Args:
            n (int): number of system buses
        """
        self.allocate_electric_params(n)

    def allocate_electric_params(self, n):
        """
        Creates the numpy/scipy arrays that will be used for all calculations (it doesn't inititialices all them)
        """

        self.number_of_buses = n

        # allocate voltages with inicial values of 1
        self.bus_voltage_pu = np.empty(n, dtype=Allocator.complex_dtype)

        # allocate powers
        self.bus_apparent_power_pu = np.empty([])
        self.bus_apparent_generation_power_pu = np.empty(n, dtype=Allocator.complex_dtype)
        self.bus_apparent_load_power_pu = np.empty(n, dtype=Allocator.complex_dtype)

        # allocate admittances with inicial values of 0
        self.line_series_admittance_pu = lil_matrix((n, n), dtype=Allocator.complex_dtype)

        # V = E + jU
        self.bus_real_voltage_pu = self.bus_voltage_pu.real
        self.bus_imaginary_voltage_pu = self.bus_voltage_pu.imag

        # S = P + jQ
        self.bus_real_generation_power_pu = self.bus_apparent_generation_power_pu.real
        self.bus_reactive_generation_power_pu = self.bus_apparent_generation_power_pu.imag

        self.bus_real_load_power_pu = self.bus_apparent_load_power_pu.real
        self.bus_reactive_load_power_pu = self.bus_apparent_load_power_pu.imag

        # Y = G + jβ
        self.line_series_conductance_pu = self.line_series_admittance_pu.real
        self.line_series_susceptance_pu = self.line_series_admittance_pu.imag
