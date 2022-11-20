# librería de arreglos super eficientes escrita en c
import numpy as np

# datos iniciales del ejercicio
from data import *

# funciones de apoyo para resolverlo
from helpers import *

# main
def iterate(i):
    print(f"iteración {i}:\n")

    alpha = delta - delta.reshape(-1, 1) + theta

    sin_alpha = np.sin(alpha)  # type: ignore
    cos_alpha = np.cos(alpha)  # type: ignore

    u = V * Y

    A, B = calc_A_or_B(u, cos_alpha, sin_alpha)

    # fmt: off
    Jacob = np.array((
        (calc_H(1, 1, sin_alpha, B),  calc_H(1, 2, sin_alpha, B),  calc_N(1, 1, cos_alpha, A)),
        (calc_H(2, 1, sin_alpha, B),  calc_H(2, 2, sin_alpha, B),  calc_N(2, 1, cos_alpha, A)),
        (calc_J(1, 1, cos_alpha, A),  calc_J(1, 2, cos_alpha, A),  calc_L(1, 1, sin_alpha, B)),
    ))

    H = np.array((
        (0, 0, 0),
        (0, calc_H(1, 1, sin_alpha, B), calc_H(1, 2, sin_alpha, B)),
        (0, calc_H(2, 1, sin_alpha, B), calc_H(2, 2, sin_alpha, B)),
    ))

    J = np.array((
        (calc_J(2, 2, cos_alpha, A), 0, 0),
        (0, calc_J(1, 1, cos_alpha, A), calc_J(1, 2, cos_alpha, A)),
        (0, 0,calc_J(2, 2, cos_alpha, A)),
    ))
    # fmt: on

    dPQ = calc_dPQ(J, H, sin_alpha, cos_alpha)

    dV = np.linalg.solve(Jacob, dPQ)

    delta[1] += dV[0]
    delta[2] += dV[1]
    V[1] += dV[2]

    # inspect("α", alpha)
    # inspect("u", u)
    # inspect("sin(α)", sin_alpha)
    # inspect("cos(α)", cos_alpha)
    # inspect("A", A)
    # inspect("B", B)
    inspect("Jacobiano", Jacob)
    # inspect("J", J)
    # inspect("H", H)
    inspect("dPQ", dPQ)
    # inspect("dV", dV)

    inspect("err = max(dPQ)", f"{dPQ.max() * 100}%")

    inspect("P", P)
    inspect("Q", Q)
    inspect("V", V)
    inspect("delta", delta)


iterate(1)
iterate(2)
iterate(3)
