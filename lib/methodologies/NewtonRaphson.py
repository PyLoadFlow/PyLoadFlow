import attrs
import numpy as np
from numpy.typing import NDArray
from errors import ConvergenceError


@attrs.define
class NewtonRaphson:

    Y: NDArray[np.complex128]
    # V*
    V: NDArray[np.complex128]

    nit: int = 0
    max_iterations_number: int = 500
    J: NDArray[np.complex128] = np.array([])

    def build_jacobian(self):

        # not diagonals
        self.J = self.V * self.Y

        # diagonals
        V = self.V.conj()

        for x in range(len(self.V)):
            self.J[x, x] = 2 * self.J[x, x] + V.dot(self.Y[x]) - V[x, x]

        # PV buses

    def loop(self):
        """
        is called till it returns True or max iteration number is exceeded
        """
        raise NotImplementedError(
            "Abstract Newton raphson has no mode to stop iterating"
        )

    def run(self):
        """
        calls loop() method till it returns True or max iteration number is exceeded
        """
        for self.nit in range(self.max_iterations_number):
            if self.loop():
                return

        raise ConvergenceError(self.nit)
