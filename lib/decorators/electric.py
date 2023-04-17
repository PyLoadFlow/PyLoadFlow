def electric(func):
    def new_func(self, *args, **kwargs):
        func.__globals__.update(
            {
                "n": self.number_of_buses,
                "P": self.bus_programed_real_power,
                "Q": self.bus_programed_reactive_power,
                "S": self.bus_programed_apparent_power,
                "V": self.bus_voltage_pu,
                "E": self.bus_real_voltage_pu,
                "U": self.bus_imaginary_voltage_pu,
                "Y": self.line_series_admittance_pu,
                "G": self.line_series_conductance_pu,
                "β": self.line_series_susceptance_pu,
            }
        )

        return func(self, *args, **kwargs)

    new_func.__doc__ = func.__doc__
    return new_func

def electric_system_method(func):
    def new_func(self, *args, **kwargs):
        func.__globals__.update(
            {
                "n": self.number_of_buses,
                "P": self.bus_programed_real_power,
                "Q": self.bus_programed_reactive_power,
                "S": self.bus_programed_apparent_power,
                "V": self.bus_voltage_pu,
                "E": self.bus_real_voltage_pu,
                "U": self.bus_imaginary_voltage_pu,
                "Y": self.line_series_admittance_pu,
                "G": self.line_series_conductance_pu,
                "β": self.line_series_susceptance_pu,
            }
        )

        return func(self, *args, **kwargs)

    new_func.__doc__ = func.__doc__
    return new_func

def electric_bus_method(func):
    def new_func(self, *args, **kwargs):
        func.__globals__.update(
            {
                "n": self.power_system.number_of_buses,
                "P": self.power_system.bus_programed_real_power,
                "Q": self.power_system.bus_programed_reactive_power,
                "S": self.power_system.bus_programed_apparent_power,
                "V": self.power_system.bus_voltage_pu,
                "E": self.power_system.bus_real_voltage_pu,
                "U": self.power_system.bus_imaginary_voltage_pu,
                "Y": self.power_system.line_series_admittance_pu,
                "G": self.power_system.line_series_conductance_pu,
                "β": self.power_system.line_series_susceptance_pu,
                "y": self.yid,
            }
        )

        return func(self, *args, **kwargs)

    new_func.__doc__ = func.__doc__
    return new_func
