# pyright: reportUndefinedVariable=false
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

from lib.classes.Allocator import Allocator
from lib.decorators import electric_power_system_as_param as electric


@electric
def current_injections_solver(_, max_nit, tol):
    ## initial configuration
    m = 2 * (n - 1)

    ΔI = lil_matrix((n - 1, 1), dtype=Allocator.complex_dtype)
    J = lil_matrix((m, m), dtype=Allocator.float_dtype)
    err = lil_matrix((m, 1), dtype=Allocator.float_dtype)
    pq_quadrants = (pq_buses - 1) * 2
    pv_quadrants = (pv_buses - 1) * 2

    ## initial jacobian

    # Y' for elems outside diagonal
    # J[x, y] = Y'[x, y]
    for y in pq_buses:
        j = (y - 1) * 2

        for x in buses[y].connected_buses:
            i = (x - 1) * 2

            if x != 0 and x != y:
                J[i : i + 2, j : j + 2] = [
                    [+β[x, y], -G[x, y]],
                    [-G[x, y], -β[x, y]],
                ]

    # main loop
    for nit in range(max_nit + 1):
        # current inyections
        for y in range(1, n):
            ΔI[y - 1] = np.conj(S[y] / V[y]) - Y[y].dot(V)

        err[0::2] = ΔI.real
        err[1::2] = ΔI.imag

        # starting with this to show initial conditions
        yield nit, J, err

        # Y' for elems inside diagonal
        # J[x, x] = Y'[x, x] + D'[x]
        for x, i in zip(pq_buses, pq_quadrants):
            # i = (x - 1) * 2

            if x != 0:
                V4 = np.abs(V[x]) ** 4
                a = (Q[x] * (E[x] ** 2 - U[x] ** 2) - 2 * P[x] * U[x] * E[x]) / V4
                b = (P[x] * (U[x] ** 2 - E[x] ** 2) - 2 * Q[x] * U[x] * E[x]) / V4
                c = -b
                d = a

                J[i : i + 2, i : i + 2] = [
                    [+β[x, x], -G[x, x]],
                    [-G[x, x], -β[x, x]],
                ]

                J[i : i + 2, i : i + 2] += lil_matrix(
                    [
                        [a, b],
                        [c, d],
                    ]
                )

        # Y" for all elems
        # J[x, y] = Y"[x, y] + D"[x]
        for y in pv_buses:
            j = (y - 1) * 2

            for x in buses[y].connected_buses:
                i = (x - 1) * 2

                if x != 0:
                    # Y"[x, y]
                    J[i : i + 2, j] = [
                        G[x, y] * U[y] / E[y] + β[x, y],
                        β[x, y] * U[y] / E[y] - G[x, y],
                    ]

                    # D"[x]
                    if x == y:
                        J[i : i + 2, i : i + 2] += lil_matrix(
                            [
                                [Q[y] - P[y] * U[y] / E[y], U[y]],
                                [P[y] + Q[y] * U[y] / E[y], -E[y]],
                            ]
                        ) / (np.abs(V[x]) ** 2)

        ΔV = spsolve(J.tocsr(), err.tocsr())

        # applying changes
        U[pq_buses] -= ΔV[pq_quadrants,]
        E[pq_buses] -= ΔV[pq_quadrants + 1,]

        U[pv_buses] -= ΔV[pv_quadrants,]
        Q[pv_buses] -= ΔV[pv_quadrants + 1,]

        for y in pv_buses:
            E[y] = np.sqrt(buses[y].fixed_voltage ** 2 - U[y] ** 2)
