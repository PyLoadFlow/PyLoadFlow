import numpy as np
from numpy.testing import assert_equal
from lib.classes.Bus import Bus

bus1 = Bus(None, 1)
bus2 = Bus(None, 2)
bus3 = Bus(None, 3)


def test_connected_buses():
    assert bus1.yid == 1

    assert_equal(bus1.connected_buses, [1])

    bus1.connected_buses = np.append(bus1.connected_buses, 2)
    assert_equal(bus1.connected_buses, [1, 2])

    bus1.connected_buses = np.append(bus1.connected_buses, 3)
    assert_equal(bus1.connected_buses, [1, 2, 3])
