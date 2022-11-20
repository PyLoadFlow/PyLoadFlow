# librería de arreglos super eficientes escrita en c
import numpy as np

# mejor visión de los datos de instancia
from prettyprinter import install_extras, cpprint as p
install_extras(['numpy'])

from helpers import inspect, hr

A = np.arange(1, 10).reshape(3,3)
u = np.arange(1, 4)

inspect('A', A)

# inspect('u', u)

# inspect('u^T', u.reshape(-1,1))

# inspect('u^T * A', u.reshape(-1,1) * A)

B = np.arange(10, 19).reshape(3,3)
inspect('B', B)

inspect('A * B', A * B)
inspect('A ∙ B', A.dot(B))

inspect('A[0] ∙ B[0]', A[0].dot(B[0]))
inspect('A[1] ∙ B[1]', A[1].dot(B[1]))
inspect('A[2] ∙ B[2]', A[2].dot(B[2]))