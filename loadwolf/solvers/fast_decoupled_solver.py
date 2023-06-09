# pyright: reportUndefinedVariable=false
import numpy as np
from scipy.sparse import csc_matrix, lil_matrix
from scipy.sparse.linalg import splu

from loadwolf.decorators import electric_power_system_as_param as electric
from loadwolf.helpers.math_helpers import cis


@electric
def pq_slice(_):
    """
    Fills the β" matrix because scipy hasn't matrix slicing
    """

    # creating a matrix of (number of pq elems) x (number of pq elems)
    β_dprime = lil_matrix((len(pq_buses), len(pq_buses)))

    # filling row by row
    for x, row in enumerate(β[pq_buses,]):
        β_dprime[x] = row.todense()[:, pq_buses]

    # converting to a constant csc matrix
    return β_dprime.tocsc()


@electric
def fast_decoupled_solver(ps):
    """
    Solves the system using Fast decoupled method (fdlf)

    Args:
        ps (PowerSystem): the system we are trying to solve

    Yields:
        tuple[NDArray, dict]: error vector and specific method data
    """

    # taking β' and β" from main β matrix
    β_prime = csc_matrix(β[1:, 1:])
    β_dprime = pq_slice(ps)  # needed, scipy can't do this easily

    # preparing L and U matrices to solve changing only results vector
    β_prime_lu = splu(β_prime)
    β_dprime_lu = splu(β_dprime)

    while True:
        # saving current |V| and δ to work in polars
        V_polar = np.abs(V)
        δ = np.angle(V)

        # taking |V| in not slack buses and |V| in pq buses
        V_prime = V_polar[1:]
        V_dprime = V_polar[pq_buses,]

        # calculating power mismatches
        ΔS = ps.apparent_power_mismatch()
        ΔP = ΔS[1:].real
        ΔQ = ΔS[pq_buses,].imag

        # solving the main jacobian system
        # Δδ = [β']⁻¹ ∙ (ΔP / |V|)
        Δδ = β_prime_lu.solve(ΔP / V_prime)

        # Δ|V| = [β"]⁻¹ ∙ (ΔQ / |V|)
        ΔV = β_dprime_lu.solve(ΔQ / V_dprime)

        yield (Δδ.max(), ΔV.max()), {
            "β'": β_prime,
            'β"': β_dprime,
            "ΔP": ΔP,
            "ΔQ": ΔQ,
            "Δδ": Δδ,
            "Δ|V|": ΔV,
            "|V|": V_polar,
            "δ": δ,
        }

        # updating
        V_polar[pq_buses,] -= ΔV
        δ[1:] -= Δδ

        V[:] = V_polar * cis(δ)
