import numpy as np
import numpy.typing as npt

# mejor visión de los datos
from prettyprinter import install_extras, cpprint as p

install_extras(["numpy"])  # type: ignore

from data import *


def hr():
    print("-------------------------")


def inspect(name, value):
    print(name, end=" = ")
    p(value, end="\n\n")


def calc_A_or_B(u, cos_alpha, sin_alpha):
    n = len(u)
    A = np.empty(n)
    B = np.empty(n)

    A[0] = B[0] = 0

    for x in range(1, n):
        A[x] = u[x].dot(cos_alpha[x]) - V[x] * Y[x, x] * cos_alpha[x, x]
        B[x] = u[x].dot(sin_alpha[x]) - V[x] * Y[x, x] * sin_alpha[x, x]

    return A, B


def calc_H(x, y, sin_alpha, B):
    if x is not y:
        return -V[x] * V[y] * Y[x, y] * sin_alpha[x, y]

    return V[x] * B[x]


def calc_J(x, y, cos_alpha, A):
    return calc_H(x, y, cos_alpha, A)


def calc_N(x, y, cos_alpha, A):
    if x is not y:
        return V[x] * Y[x, y] * cos_alpha[x, y]

    return A[x] + V[x] * Y[x, x] * cos_alpha[x, x] * 2


def calc_L(x, y, sin_alpha, B):
    return -calc_N(x, y, sin_alpha, B)


def calc_P_or_Q(x, J, f_alpha):
    return J[x, x] + V[x] ** 2 * Y[x, x] * f_alpha[x, x]


def calc_dPQ(J, H, sin_alpha, cos_alpha):
    dPQ = np.empty(3)

    # por ahora, se quedarán las iteraciones estáticas
    dPQ[0] = P[1] - calc_P_or_Q(1, J, cos_alpha)
    dPQ[2] = Q[1] + calc_P_or_Q(1, H, sin_alpha)
    
    dPQ[1] = P[2] - calc_P_or_Q(2, J, cos_alpha)

    return dPQ
