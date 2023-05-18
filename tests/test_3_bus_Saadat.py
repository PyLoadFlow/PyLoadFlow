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
    ps.select_solver("current inyections")

    # initial values
    err, J = ps.do_step()

    assert_allclose(err, [-2.86, 0.22, 1.38307692, 0.98])

    # 1st iter
    err, J = ps.do_step()

    assert_allclose(
        J.toarray(),
        [
            [-54.5, -22.0, +32, 0],
            [-30.0, +49.5, +16, 0],
            [+32.0, +16.0, -62, 0],
            [+16.0, -32.0, -24.15088757, -0.96153846],
        ],
    )

    assert_allclose(ps.bus_voltage_pu, [1.05, 0.970641799809 - 0.045880404203j, 1.039961498572 - 0.00894882604j])

    assert_allclose(err, [0.011791029677, 0.008545474001, -0.011129542951, -0.002335204221])

    # 2nd iter
    err, J = ps.do_step()

    assert_allclose(
        J.toarray(),
        [
            [-55.03430535157, -22.03104799478, +32.13929535785, 0],
            [-29.96895200522, +48.96569464843, +15.72140928430, 0],
            [+32.00000000000, +16.00000000000, -60.85876863701, -8.370798034479e-03],
            [+16.00000000000, -32.00000000000, -23.62288406276, -9.615020243130e-01],
        ],
    )

    assert_allclose(ps.bus_voltage_pu, [1.05, 0.970603882582 - 0.045712311458j, 1.039960589497 - 0.009053855154j])

    assert_allclose(err, [-2.165102674923e-08, 3.077805654783e-08, -2.808616046401e-07, -3.181615007009e-07])
