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

def p(name, value):
    print(name, end=" = ")
    cpprint(value, end="\n\n")


cplx = np.complex128
arr = lambda array: np.array(array, dtype=np.complex128)

Y = arr(
    [
        [20 - 50j, -10 + 20j, -10 + 30j],
        [-10 + 20j, 26 - 52j, -16 + 32j],
        [-10 + 30j, -16 + 32j, 26 - 62j],
    ]
)

V = arr([1.05, 1, 1.04])
p("V", V)

S = arr([0, -4 - 2.5j, 2])
p("S", S)

n = len(V)
p("n", n)

# llenando la mayor parte del jacobiano
J = V.reshape(-1, 1) * Y  # solito llena cada fila en Y por cada fila en V
p("J' = V^T Y", J)

# llenando la diagonal
for x in range(n):
    p("-----------------: x", x)
    p(f"2 J[{x}, {x}]", J[x, x] * 2)
    p(f"V", V)
    p(f"Y[{x}]", Y[x])
    p(f"V dot Y[{x}]", V.dot(Y[x]))
    p(f"V dot Y[{x}] - V[{x}] Y[{x}, {x}]", V.dot(Y[x]) - V[x].conj() * Y[x, x])

    J[x, x] = J[x, x] * 2 + V.dot(Y[x]) - V[x] * Y[x, x]
    p(f"J[{x}, {x}]", J[x, x])

    print("---------------\n\n")


p("J", J)
