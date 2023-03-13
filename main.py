import numpy as np
from prettyprinter import cpprint, install_extras

install_extras(["numpy", "attrs"])  # type: ignore


def _(name, value="__usename__"):
    print(name, end=" = ")

    if value == "__usename__":
        cpprint(globals()[name], end="\n\n")
        return

    cpprint(value, end="\n\n")


SLACK, PQ, PV = range(3)

"""
    *********************************
    
    Initial data
    
    Touch any values in this part to modify power systems
    
    *********************************
"""
Y = np.array(
    [
        [20 - 50j, -10 + 20j, -10 + 30j],
        [-10 + 20j, 26 - 52j, -16 + 32j],
        [-10 + 30j, -16 + 32j, 26 - 62j],
    ],
    dtype=np.complex128,
)

B = np.zeros([3, 3])

V = np.array([1.05, 1 + 0j, 1.04])

S = np.array([0, -4 - 2.5j, 2])

zip_ = np.array(
    [
        [0, 0, 0],  # for bus 0
        [0, 0, 1],  # for bus 1
        [0, 0, 1],  # for bus 2
    ]
)

ziq = np.array(
    [
        [0, 0, 0],  # for bus 0
        [0, 0, 1],  # for bus 1
        [0, 0, 1],  # for bus 2
    ]
)

BUS_TYPES = SLACK, PQ, PV

bus = np.array(
    [
        [1, 2],  # for bus 0
        [0, 2],  # for bus 1
        [0, 1],  # for bus 2
    ]
)


"""
    *********************************
    
    Computed values to start
    
    this code will be internally added to class implementations and must be extendable to
    any power system model
    
    *********************************
"""
n = len(Y)
# _2n = n * 2 - 1

NON_SLACK_BUSES = filter(lambda y: y is not SLACK, BUS_TYPES)
PQ_BUSES = filter(lambda y: y is PQ, BUS_TYPES)
PV_BUSES = filter(lambda y: y is PV, BUS_TYPES)

# E and U are linked to V, same P, Q, G and B
E, U = V.real, V.imag
P, Q = S.real, S.imag
G, B = Y.real, Y.imag

dIm = np.empty(n)
dIr = np.empty(n)
dI = np.empty(n)
dE = np.empty(n)
dU = np.empty(n)
dQ = np.empty(n)

I = np.empty(n)

J = np.empty(n)

variables = []
functions = []

for y in PQ_BUSES:
    functions.append(["dIm", y, dIm])
    functions.append(["dIr", y, dIr])

    variables.append(["E", y, E])
    variables.append(["U", y, U])


for y in PV_BUSES:
    functions.append(["dIm", y, dIm])
    functions.append(["dIr", y, dIr])

    variables.append(["U", y, U])
    variables.append(["Q", y, Q])

"""
    main algorithm
"""

for nit in range(1):
    # calculating current unbalance
    for y in NON_SLACK_BUSES:
        i_calc = 0 + 0j
        v = np.abs(V[y])

        az, ai, ap = zip_[y]
        bz, bi, bq = ziq[y]

        p = P[y] * (az * v**2 + ai * v + ap)
        q = Q[y] * (bz * v**2 + bi * v + bq)

        for x in bus[y]:
            i_calc += V[x] * (0.5j * _B[x, y] - Y[x, y]) + V[y] * Y[x, y]

        dI[y] = (p - 1j * q) / np.conj(V[y]) - i_calc

    _("dI")

    # check convergence
    if dI.max() < 1e-9:
        break

    for f_name, y, F in functions:
        for x_name, x, X in variables:

            if f_name == "dIm":
                if x_name == "E":
                    if x is not y:
                        pass


def __():

    ZIP_POTENCES = ((2,), (1,), (1,))

    # calculating zip polynomial factors
    P_FACTORS = zip_ * P.reshape(-1, 1)
    Q_FACTORS = ziq * Q.reshape(-1, 1)
    for y in NON_SLACK_BUSES:
        pass

    # getting zip model potences
    v = abs(V)
    vp = (v**ZIP_POTENCES).transpose()
    p = vp * P_FACTORS
    q = vp * Q_FACTORS
    _("P_FACTORS")
    _("Q_FACTORS")
    _("vp")
    _("p")
    _("q")

    # correcting real PV voltajes
    for t, y in enumerate(BUS_TYPES):
        if t == PV:
            E[y] = np.sqrt(abs(V[y]) ** 2 - U[y] ** 2)
