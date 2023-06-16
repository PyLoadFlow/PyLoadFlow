from pyloadflow.classes.PowerSystem_mixins.Allocator import Allocator
from pyloadflow.classes.PowerSystem_mixins.BusAdder import BusAdder
from pyloadflow.classes.PowerSystem_mixins.BusConnector import BusConnector
from pyloadflow.classes.PowerSystem_mixins.Solver import Solver
from pyloadflow.errors import NotCompiledSystemError


class PowerSystem(Allocator, BusAdder, BusConnector, Solver):
    """
    Main program class to do all power flow calculations
    """

    def __init__(self, n: int):
        """
        Args:
            n (int): Number of system buses
        """
        self.__compiled = False

        Allocator.__init__(self, n)
        BusAdder.__init__(self)
        BusConnector.__init__(self)
        Solver.__init__(self)

    def compile(self):
        """
        Verifies the power system data and does previous calculations
        """
        self.__compiled = True

        self.build_line_series_admittance_pu_diagonal()

        self.bus_apparent_power_pu = self.bus_apparent_generation_power_pu - self.bus_apparent_load_power_pu

        for bus in self.buses:
            bus.connected_buses.sort()  # type: ignore

    def verify(self):
        """
        Verifies the power system was compiled to start calculations
        """
        if not self.__compiled:
            raise NotCompiledSystemError()

    def run(self, method="current inyections", max_nit=25, tol=1e-9):
        """
        Shortcut to compile() and solve() methods. Highly recommended

        Args:
            method ("current inyections" | "cilf" | "fast decoupled" | "fdlf"): Method to solve the system. Defaults to "current inyections".
            max_nit (int, optional): Max number of iterations. Defaults to 25.
            tol (float, optional): Max absolute error allowed to stop iterating. Defaults to 1e-9.

        Raises:
            ConvergenceError: If max_nit is exceeded and the tol has not been minor
        """

        self.compile()
        self.solve(method, max_nit, tol)
