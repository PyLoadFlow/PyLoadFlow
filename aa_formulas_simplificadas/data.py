# fmt: off
import numpy as np

Y = np.array((
    (53.8516, 22.3606, 31.6227),
    (22.3606, 58.1377, 35.7770),
    (31.6227, 35.7770, 67.2309),
))

theta = np.array((
    (-1.9029, 2.0344, 1.8925), 
    (2.0344, -1.1071, 2.0344), 
    (1.8925, 2.0344, -1.1737)
))

V = np.ones(3)
delta = np.zeros(3)
P = np.zeros(3)
Q = np.zeros(3)

# Nodo 1 (compensador)
V[0] = 1.05

# Nodo 2
P[1] = -4
Q[1] = -2.5

# Nodo 3
P[2] = 2
V[2] = 1.04
