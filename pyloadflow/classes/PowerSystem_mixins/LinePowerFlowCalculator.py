from pyloadflow.decorators.electric import electric_power_system_as_self as electric


class LinePowerFlowCalculator:
    @property
    @electric
    def line_voltage_pu(self):
        return V - V.reshape(-1, 1)
