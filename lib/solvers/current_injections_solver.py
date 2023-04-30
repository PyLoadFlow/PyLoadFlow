import numpy as np

from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve_triangular

from lib.classes.Allocator import Allocator
from lib.decorators import electric_power_system_as_param as electric


@electric
def current_injections_solver(power_system, max_nit, tol):
    # initial configuration
    m = 2 * (n - 1)

    ΔI = lil_matrix((n - 1, 1), dtype=Allocator.complex_dtype)
    J = lil_matrix((m, m), dtype=Allocator.float_dtype)

    ΔIr, ΔIm = ΔI.real, ΔI.imag

    # preparing
    for i, x in enumerate(not_slack_buses):
        i *= 2

        for j, y in enumerate(pq_buses):
            j *= 2

            # J[x,y] = Y'[x,y]
            J[i : i + 2, j : j + 2] = [
                [-G[x, y], +β[x, y]],
                [-β[x, y], -G[x, y]],
            ]

            # yield np.array(
            #     [
            #         [x, y],
            #         [
            #             power_system.line_series_admittance_pu.real[x, y],
            #             power_system.line_series_admittance_pu.imag[x, y],
            #         ],
            #     ]
            # )
            # yield np.array(
            #     [
            #         [- power_system.line_series_conductance_pu[x, y], +β[x, y]],
            #         [-β[x, y], -G[x, y]],
            #     ]
            # )

    # main loop
    for nit in range(max_nit):
        yield J, ΔI
