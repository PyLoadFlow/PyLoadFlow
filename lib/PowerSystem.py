import attrs
import numpy as np
from numpy.typing import NDArray
from prettyprinter import install_extras

install_extras(["numpy", "attrs"])  # type: ignore

# from errors import ConvergenceError


@attrs.define
class PowerSystem:
    n: int
    buses: list = []
    Y: NDArray = np.empty(0)
    V: NDArray = np.empty(0)
    ΔI: NDArray = np.empty(0)

    def __attrs_post_init__(self):
        # allocating
        self.Y = np.empty([self.n, self.n], dtype=np.complex128)
        self.V = np.empty(self.n)
        self.ΔI = np.empty(self.n)

    def add(self, bus):
        self.buses.append(bus)
        return len(self.buses) - 1

    def connect(self, bus1, bus2, z, y=0j):
        i = bus1._id
        j = bus2._id

        # transforming to admittance
        self.Y[i, j] = self.Y[j, i] = 1 / z

        # adding shunt susceptance to diagonal
        self.Y[i, i] += y / 2
        self.Y[j, j] += y / 2

        # saving new connected bus data
        if not i in bus1.connected_buses:
            bus1.connected_buses.append(i)

        if not j in bus2.connected_buses:
            bus2.connected_buses.append(j)

    def build_Ybus_diagonal(self):
        # calculating self admittances from sum of mutual admittances
        for i in range(self.n):
            self.Y[i, i] = -self.Y[i].sum()

    def build_absV_vector(self):
        for i in range(self.n):
            self.V[i] = self.buses[i].V if hasattr(self.buses[i], "V") else 1

    def run(self, max_nit=25, tol=1e-9):
        """Starts calculating nodal voltages

        Args:
            max_nit (int, optional): maximum allowed iterations before raise. Defaults to 25.
            tol (float, optional): maximum allowed current unbalance tolerated. Defaults to 1e-9.
        """

        self.build_Ybus_diagonal()
        self.build_absV_vector()
        max_nit *= tol
