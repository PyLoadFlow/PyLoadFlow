import numpy as np

Y = np.array(
    [
        [20 - 50j, -10 + 20j, -10 + 30j],
        [-10 + 20j, 26 - 52j, -16 + 32j],
        [-10 + 30j, -16 + 32j, 26 - 62j],
    ],
    dtype=np.complex128,
)

V = np.array([1.05, 1, 1.04], dtype=np.complex128).reshape(-1, 1)

S = np.array([0, -4 - 2.5j, 2], dtype=np.complex128).reshape(-1, 1)
