import pytest
import numpy as np

eq = np.array_equal

u = np.array([1, 2, 3])
v = np.array([[1], [2], [3]])

A = np.array(
    [
        [2, 3, 4],
        [3, 4, 5],
        [4, 5, 6],
    ]
)

B = np.array(
    [
        [1, 2, 3],
        [2, 4, 6],
        [3, 6, 9],
    ]
)

vA = np.array(
    [
        [2, 3, 4],
        [6, 8, 10],
        [12, 15, 18],
    ]
)


def test_vector_vertical():
    # u is horizontal and v is vertical
    assert not eq(u, v)

    assert eq(u + v, A)

    assert eq(u * v, B)

    assert eq(v * A, vA)
