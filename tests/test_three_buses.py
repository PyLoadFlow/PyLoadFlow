import numpy as np
from numpy.testing import assert_allclose

from lib import PowerSystem
from lib.classes.Bus import Bus

ps = PowerSystem(n=3)


def test_buses_count():
    ps.add_slack_bus(V=1.05)
    ps.add_pq_bus(P=4, Q=2.5)
    ps.add_pv_bus(V=1.04, P=2)

    ps.connect_buses_by_id(1, 2, z=0.02 + 0.04j)
    ps.connect_buses_by_id(2, 3, z=0.0125 + 0.025j)
    ps.connect_buses_by_id(3, 1, z=0.01 + 0.03j)

    assert ps.number_of_buses == 3


def test_admittance_matrix_before_compile():
    Y = np.array(
        [
            [0.0j, -10 + 20j, -10 + 30j],
            [-10 + 20j, 0, -16 + 32j],
            [-10 + 30j, -16 + 32j, 0],
        ]
    )

    assert_allclose(ps.line_series_admittance_pu.toarray(), Y)


def test_admittance_matrix_after_compile():
    ps.compile()

    Y = np.array(
        [
            [20 - 50j, -10 + 20j, -10 + 30j],
            [-10 + 20j, 26 - 52j, -16 + 32j],
            [-10 + 30j, -16 + 32j, 26 - 62j],
        ]
    )

    assert_allclose(ps.line_series_admittance_pu.toarray(), Y)


def test_inicial_conditions():
    assert ps.bus_voltage_pu[0] == 1.05

    assert ps.bus_programed_apparent_power[1] == -4 - 2.5j

    assert ps.bus_voltage_pu[2] == 1.04
    assert ps.bus_programed_real_power[2] == 2
