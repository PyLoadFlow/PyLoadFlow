# pyright: reportGeneralTypeIssues=false
import numpy as np
from numpy.testing import assert_allclose, assert_equal

from pyloadflow import PowerSystem

ps = PowerSystem(n=3)

ps.add_slack_bus(V=1.05)
ps.add_pq_bus(P=4, Q=2.5)
ps.add_pv_bus(P=2, V=1.04)

ps.connect_buses_by_IEEE_id(1, 2, z=0.02 + 0.04j)
ps.connect_buses_by_IEEE_id(2, 3, z=0.0125 + 0.025j)
ps.connect_buses_by_IEEE_id(3, 1, z=0.01 + 0.03j)


def test_Ybus():
    Y = np.array(
        [
            [0.0j, -10 + 20j, -10 + 30j],
            [-10 + 20j, 0, -16 + 32j],
            [-10 + 30j, -16 + 32j, 0],
        ]
    )

    assert_allclose(ps.line_series_admittance_pu.toarray(), Y)

    ps.compile()

    Y = np.array(
        [
            [20 - 50j, -10 + 20j, -10 + 30j],
            [-10 + 20j, 26 - 52j, -16 + 32j],
            [-10 + 30j, -16 + 32j, 26 - 62j],
        ]
    )

    assert_allclose(ps.line_series_admittance_pu.toarray(), Y)


def test_bus_connection_relations():
    assert_equal(ps.buses[0].connected_buses, [0, 1, 2])
    assert_equal(ps.buses[1].connected_buses, [0, 1, 2])
    assert_equal(ps.buses[2].connected_buses, [0, 1, 2])


def test_PVPQ_recognition():
    assert_equal(ps.pq_buses_yids, [1])
    assert_equal(ps.pv_buses_yids, [2])


def test_inicial_conditions():
    assert ps.bus_voltage_pu[0] == 1.05

    assert ps.bus_apparent_power_pu[1] == -4 - 2.5j

    assert ps.bus_voltage_pu[2] == 1.04
    assert ps.bus_apparent_power_pu[2] == 2


def test_bus_voltages_solved():
    ps.solve()

    assert_allclose(ps.bus_voltage_pu, [1.05, 0.97060388168 - 0.045712315571j, 1.039960589436 - 0.009053862142j])
