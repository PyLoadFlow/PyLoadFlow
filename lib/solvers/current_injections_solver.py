# pyright: reportUndefinedVariable=false, reportGeneralTypeIssues=warning
from lib.typing import *

# from scipy.sparse.linalg import spsolve_triangular

from lib.decorators import electric_system_method as electric


@electric
def current_injections_solver(self, max_nit, tol):
    # initial configuration
    m = 2 * (n - 1)

    ΔI = lil_matrix((n - 1, 1), dtype=cplx)
    J = lil_matrix((m, m))

    ΔIr, ΔIm = ΔI.real, ΔI.imag

    # preparing jacobian
    # building diagonal outside elements
    for x, i in enumerate(self.not_slack_buses()):
        i *= 2

        for y, j in enumerate(self.not_slack_buses()):
            j *= 2

            # J[x,y] = Y'[x,y]
            J[i : i + 2, j : j + 2] = [
                [-G[x, y], β[x, y]],
                [-β[x, y], -G[x, y]],
            ]

    # starting main loop
    for nit in range(1, max_nit + 1):
        # getting current unbalances
        for i, y in enumerate(self.not_slack_buses()):
            ΔI[i] = self.buses[y].programmed_current_pu - Y[y].dot(V)

        # checking max current unbalance
        if np.abs(ΔI.tocsc().max()) <= tol:
            return ΔI
            # return nit

        # for x, i in enumerate(self.not_slack_buses()):
        #     i *= 2

        #     for j, y in zip(PV_QUADRANTS, PV_BUSES):
        #         J[i : i + 2, j] = [
        #             G[x, y] * U[y] / E[y] + β[x, y],
        #             β[x, y] * U[y] / E[y] - G[x, y],
        #         ]

    return ΔI
