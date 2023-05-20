# pyright: reportUndefinedVariable=false
from lib.classes.Bus import Bus


class PVBus(Bus):
    def __init__(self, power_system, fixed_voltage):
        Bus.__init__(self, power_system)
        self.fixed_voltage = fixed_voltage

    @electric
    def cilf_diagonal_quadrant_abcd(self):
        V2 = np.abs(V[y]) ** 2

        a = (Q[y] - P[y] * U[y] / E[y]) / V2
        b = U[y] / V2
        c = (P[y] + Q[y] * U[y] / E[y]) / V2
        d = -E[y] / V2

        return a, b, c, d
