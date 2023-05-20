# pyright: reportUndefinedVariable=false
from lib.classes.Bus import Bus


class PQBus(Bus):
    @electric
    def cilf_diagonal_quadrant_abcd(self):
        V4 = np.abs(V[y]) ** 4
        a = (Q[y] * (E[y] ** 2 - U[y] ** 2) - 2 * P[y] * U[y] * E[y]) / V4
        b = (P[y] * (U[y] ** 2 - E[y] ** 2) - 2 * Q[y] * U[y] * E[y]) / V4

        return a, b, -b, a
