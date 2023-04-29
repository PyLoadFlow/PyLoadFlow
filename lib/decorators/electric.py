def electric_power_system_as_self(func):
    def new_func(self, *args, **kwargs):
        func.__globals__.update(
            {
                "buses": self.buses,
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

def electric_power_system_as_param(func):
    def new_func(power_system, *args, **kwargs):
        func.__globals__.update(
            {
                "buses": power_system.buses,
                "n": power_system.number_of_buses,
                "P": power_system.bus_programed_real_power,
                "Q": power_system.bus_programed_reactive_power,
                "S": power_system.bus_programed_apparent_power,
                "V": power_system.bus_voltage_pu,
                "E": power_system.bus_real_voltage_pu,
                "U": power_system.bus_imaginary_voltage_pu,
                "Y": power_system.line_series_admittance_pu,
                "G": power_system.line_series_conductance_pu,
                "β": power_system.line_series_susceptance_pu,
            }
        )

        return func(power_system, *args, **kwargs)

    new_func.__doc__ = func.__doc__
    return new_func

def electric_power_system_as_property(func):
    def new_func(self, *args, **kwargs):
        func.__globals__.update(
            {
                "buses": self.power_system.buses,
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
