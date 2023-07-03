# pyright: reportUndefinedVariable=false
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

from pyloadflow.classes.PowerSystem_mixins.Allocator import Allocator
from pyloadflow.decorators import electric_power_system_as_param as electric


@electric
def current_injections_solver(ps):
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
    ΔV = None

    ## initial jacobian

    # Y' for elems outside diagonal
    # J[x, y] = Y'[x, y]
    for y, j in zip(pq_buses, pq_quadrants):
        for x in buses[y].connected_buses:
            i = (x - 1) * 2

            if x != 0 and x != y:
                J[i : i + 2, j : j + 2] = buses[y].cilf_quadrant(x)

    # main loop
    while True:
        # update error vector
        for y in range(1, n):
            ΔI[y - 1] = buses[y].programmed_current_pu - (Y[y] @ V)

        err[0::2] = ΔI.real
        err[1::2] = ΔI.imag

        # yield data
        yield err, {
            "J": J,
            "ΔI": ΔI,
            "ΔV": ΔV,
        }

        # Y' for elems inside diagonal
        # J[x, x] = Y'[x, x] + D'[x]
        for x, i in zip(pq_buses, pq_quadrants):
            if x != 0:
                J[i : i + 2, i : i + 2] = np.array(buses[x].cilf_quadrant(x)) + buses[x].cilf_diagonal_quadrant()

        # Y" for all PV elems
        # J[x, y] = Y"[x, y] <+ D"[x]>
        for y, j in zip(pv_buses, pv_quadrants):
            for x in buses[y].connected_buses:
                i = (x - 1) * 2

                if x != 0:
                    if x != y:
                        # Y"[x, y]
                        J[i : i + 2, j : j + 2] = buses[y].cilf_quadrant(x)

                    else:
                        # Y"[y, y] + D"[y]
                        J[i : i + 2, i : i + 2] = (
                            np.array(buses[y].cilf_quadrant(y)) + buses[y].cilf_diagonal_quadrant()
                        )

        ΔV = spsolve(J.tocsr(), err)

        # applying changes
        U[pq_buses] -= ΔV[pq_quadrants,]
        E[pq_buses] -= ΔV[pq_quadrants + 1,]

        U[pv_buses] -= ΔV[pv_quadrants,]
        Q[pv_buses] -= ΔV[pv_quadrants + 1,]

        for y in range(n):
            buses[y].cilf_after_iteration()
