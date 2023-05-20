def electric_power_system_as_self(func):
    def new_func(self, *args, **kwargs):
        func.__globals__.update(
            {
                "buses": self.buses,
                "n": self.number_of_buses,
                "S": self.bus_programed_apparent_power,
                "P": self.bus_programed_apparent_power.real,
                "Q": self.bus_programed_apparent_power.imag,
                "V": self.bus_voltage_pu,
                "E": self.bus_voltage_pu.real,
                "U": self.bus_voltage_pu.imag,
                "Y": self.line_series_admittance_pu,
                "G": self.line_series_admittance_pu.real,
                "β": self.line_series_admittance_pu.imag,
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
                "S": power_system.bus_programed_apparent_power,
                "P": power_system.bus_programed_apparent_power.real,
                "Q": power_system.bus_programed_apparent_power.imag,
                "V": power_system.bus_voltage_pu,
                "E": power_system.bus_voltage_pu.real,
                "U": power_system.bus_voltage_pu.imag,
                "Y": power_system.line_series_admittance_pu,
                "G": power_system.line_series_admittance_pu.real,
                "β": power_system.line_series_admittance_pu.imag,
                "pq_buses": power_system.pq_buses_yids,
                "pv_buses": power_system.pv_buses_yids,
                "slack_bus": power_system.slack_bus_yid,
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
                "S": self.power_system.bus_programed_apparent_power,
                "P": self.power_system.bus_programed_apparent_power.real,
                "Q": self.power_system.bus_programed_apparent_power.imag,
                "V": self.power_system.bus_voltage_pu,
                "E": self.power_system.bus_voltage_pu.real,
                "U": self.power_system.bus_voltage_pu.imag,
                "Y": self.power_system.line_series_admittance_pu,
                "G": self.power_system.line_series_admittance_pu.real,
                "β": self.power_system.line_series_admittance_pu.imag,
                "y": self.yid,
            }
        )

        return func(self, *args, **kwargs)

    new_func.__doc__ = func.__doc__
    return new_func
