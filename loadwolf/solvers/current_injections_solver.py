# pyright: reportUndefinedVariable=false
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

from loadwolf.classes.PowerSystem_mixins.Allocator import Allocator
from loadwolf.decorators import electric_power_system_as_param as electric


@electric
def current_injections_solver(_):
    """
    Solves the system using Current injections method (cilf)

    Args:
        ps (PowerSystem): the system we are trying to solve

    Yields:
        tuple[NDArray, dict]: error vector and specific method data
    """

    ## initial configuration
    m = 2 * (n - 1)

    ΔI = np.empty(n - 1, dtype=Allocator.complex_dtype)
    J = lil_matrix((m, m), dtype=Allocator.float_dtype)
    err = np.empty(m, dtype=Allocator.float_dtype)
    pq_quadrants = (pq_buses - 1) * 2
    pv_quadrants = (pv_buses - 1) * 2

    ## initial jacobian

    # Y' for elems outside diagonal
    # J[x, y] = Y'[x, y]
    for y, j in zip(pq_buses, pq_quadrants):
        for x in buses[y].connected_buses:
            i = (x - 1) * 2

            if x != 0 and x != y:
                J[i : i + 2, j : j + 2] = [
                    [+β[x, y], -G[x, y]],
                    [-G[x, y], -β[x, y]],
                ]

    # main loop
    while True:
        # update error vector
        for y in range(1, n):
            ΔI[y - 1] = buses[y].programmed_current_pu - Y[y].dot(V)

        err[0::2] = ΔI.real
        err[1::2] = ΔI.imag

        # yield data
        yield err, {
            "J": J,
            "ΔI":ΔI,
        }

        # Y' for elems inside diagonal
        # J[x, x] = Y'[x, x] + D'[x]
        for x, i in zip(pq_buses, pq_quadrants):
            if x != 0:
                a, b, c, d = buses[x].cilf_diagonal_quadrant_abcd()

                J[i : i + 2, i : i + 2] = [
                    [+β[x, x] + a, -G[x, x] + b],
                    [-G[x, x] + c, -β[x, x] + d],
                ]

        # Y" for all elems
        # J[x, y] = Y"[x, y] <+ D"[x]>
        for y, j in zip(pv_buses, pv_quadrants):
            for x in buses[y].connected_buses:
                i = (x - 1) * 2

                if x != 0:
                    if x != y:
                        # Y"[x, y]
                        J[i : i + 2, j] = [
                            G[x, y] * U[y] / E[y] + β[x, y],
                            β[x, y] * U[y] / E[y] - G[x, y],
                        ]

                    else:
                        # Y"[y, y] + D"[y]
                        a, b, c, d = buses[x].cilf_diagonal_quadrant_abcd()

                        J[i : i + 2, j : i + 2] = [
                            [G[y, y] * U[y] / E[y] + β[y, y] + a, b],
                            [β[y, y] * U[y] / E[y] - G[y, y] + c, d],
                        ]

        ΔV = spsolve(J.tocsr(), err)

        # applying changes
        U[pq_buses] -= ΔV[pq_quadrants,]
        E[pq_buses] -= ΔV[pq_quadrants + 1,]

        U[pv_buses] -= ΔV[pv_quadrants,]
        Q[pv_buses] -= ΔV[pv_quadrants + 1,]

        for y in pv_buses:
            E[y] = np.sqrt(buses[y].fixed_voltage ** 2 - U[y] ** 2)
