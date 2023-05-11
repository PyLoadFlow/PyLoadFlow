# pyright: reportGeneralTypeIssues=false
import numpy as np
from numpy.testing import assert_allclose, assert_equal

from lib import PowerSystem
from lib.solvers.current_injections_solver import current_injections_solver

ps = PowerSystem(n=3)

ps.add_slack_bus(V=1.05)
ps.add_pq_bus(P=4, Q=2.5)
ps.add_pv_bus(P=2, V=1.04)

ps.connect_buses_by_IEEE_id(1, 2, z=0.02 + 0.04j)
ps.connect_buses_by_IEEE_id(2, 3, z=0.0125 + 0.025j)
ps.connect_buses_by_IEEE_id(3, 1, z=0.01 + 0.03j)


def test_status_before_compile():
    Y = np.array(
        [
            [0.0j, -10 + 20j, -10 + 30j],
            [-10 + 20j, 0, -16 + 32j],
            [-10 + 30j, -16 + 32j, 0],
        ]
    )

    assert_allclose(ps.line_series_admittance_pu.toarray(), Y)


def test_status_after_compile():
    ps.compile()

    Y = np.array(
        [
            [20 - 50j, -10 + 20j, -10 + 30j],
            [-10 + 20j, 26 - 52j, -16 + 32j],
            [-10 + 30j, -16 + 32j, 26 - 62j],
        ]
    )

    assert_allclose(ps.line_series_admittance_pu.toarray(), Y)

    assert_equal(ps.buses[0].connected_buses, [0, 1, 2])
    assert_equal(ps.buses[1].connected_buses, [0, 1, 2])
    assert_equal(ps.buses[2].connected_buses, [0, 1, 2])


def test_inicial_conditions():
    assert ps.bus_voltage_pu[0] == 1.05

    assert ps.bus_programed_apparent_power[1] == -4 - 2.5j

    assert ps.bus_voltage_pu[2] == 1.04
    assert ps.bus_programed_real_power[2] == 2


def test_bus_currents():
    assert np.allclose(ps.buses[1].programmed_current_pu, -4 + 2.5j)
    assert np.allclose(ps.buses[2].programmed_current_pu, 1.92307692)


def test_filters():
    assert_equal(ps.pq_buses_yids, [1])
    assert_equal(ps.pv_buses_yids, [2])


def test_current_inyections():
    solver = current_injections_solver(ps, 5, 0)

    nit, _, err = next(solver)
    assert nit == 0

    assert_allclose(err.toarray(), [[-2.86], [0.22], [1.38307692], [0.98]])

    nit, J, err = next(solver)
    assert nit == 1

    assert_allclose(
        J.toarray(),
        [
            [-54.5, -22.0, +32, 0],
            [-30.0, +49.5, +16, 0],
            [+32.0, +16.0, -62, 0],
            [+16.0, -32.0, -24.15088757, -0.96153846],
        ],
    )

    assert_allclose(err.toarray(), [[0.0117910297], [0.008545474], [-0.011129543], [-0.0023352042]])

    assert_allclose(ps.bus_voltage_pu, [1.05, 0.9706418 - 0.0458804j, 1.0399615 - 0.00894883j])
    assert_allclose(ps.bus_programed_apparent_power[1:], [-4 - 2.5j, 2 + 1.45755795j])
    
