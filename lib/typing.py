import numpy as np
from numpy.typing import NDArray
from scipy.sparse import lil_matrix

double = np.float64
cplx = np.complex128

vect = lil_matrix | NDArray[double]
mtrx = lil_matrix | NDArray[double]

cplm = lil_matrix | NDArray[cplx]
cplv = lil_matrix | NDArray[cplx]
