import pytest
import numpy as np
import numpy.testing as npt
from prettyprinter import install_extras, cpprint as p
from ._data import *

install_extras(["numpy"])  # type: ignore

# from lib.methodologies.NewtonRaphson import NewtonRaphson

eq = np.array_equiv

VY = V * Y

VY_expected = np.array(
    [
        [21 - 52.5j, -10.5 + 21j, -10.5 + 31.5j],
        [-10 + 20j, 26 - 52j, -16 + 32j],
        [-10.4 + 31.2j, -16.64 + 33.28j, 27.04 - 64.48j],
    ],
    dtype=np.complex128,
)


def test_main():
    assert eq(V, np.array([[1.05], [1], [1.04]]))

    # npt doesn't need assert keyword, because it raises internally
    npt.assert_allclose(VY, VY_expected, rtol=1e-4)
