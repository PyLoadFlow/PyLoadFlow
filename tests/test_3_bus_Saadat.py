# pyright: reportGeneralTypeIssues=false
import numpy as np
from numpy.testing import assert_allclose, assert_equal

from pyloadflow import PowerSystem
from pyloadflow.helpers.apparent_power_mismatch import calculated_apparent_power, apparent_power_mismatch

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

    assert ps.bus_apparent_power_pu[1] == -4 - 2.5j

    assert ps.bus_voltage_pu[2] == 1.04
    assert ps.bus_real_power_pu[2] == 2


def test_bus_currents():
    assert np.allclose(ps.buses[1].programmed_current_pu, -4 + 2.5j)
    assert np.allclose(ps.buses[2].programmed_current_pu, 1.92307692)


def test_filters():
    assert_equal(ps.pq_buses_yids, [1])
    assert_equal(ps.pv_buses_yids, [2])


def test_power_mismatch_before_solve():
    assert_allclose(calculated_apparent_power(ps)[1:], [-1.14 - 2.28j, 0.5616 + 1.0192j])
    assert_allclose(apparent_power_mismatch(ps)[1:], [-2.86 - 0.22j, 1.4384 - 1.0192j])


def test_current_inyections():
    ps.select_solver("current inyections")

    # initial values
    J, err = ps.do_step()

    assert_allclose(err, [-2.86, 0.22, 1.38307692, 0.98])

    # 1st iter
    J, err = ps.do_step()

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
    J, err = ps.do_step()

    assert_allclose(
        J.toarray(),
        [
            [-55.03537607672, -22.03245970122, +32.13767934374, +0],
            [-29.96754029878, +48.96462392328, +15.72464131251, +0],
            [+32.00000000000, +16.00000000000, -60.86022313693, -8.273692714578e-3],
            [+16.00000000000, -32.00000000000, -23.62897611030, -9.615028648042e-1],
        ],
    )

    assert_allclose(ps.bus_voltage_pu, [1.05, 0.970603882582 - 0.045712311458j, 1.039960589497 - 0.009053855154j])

    assert_allclose(err, [-2.165102674923e-08, 3.077805654783e-08, -2.808616046401e-07, -3.181615007009e-07])

    # 3rd iter
    J, err = ps.do_step()

    assert_allclose(
        J.toarray(),
        [
            [-55.03430535157, -22.03104799478, +32.13929535785, +0],
            [-29.96895200522, +48.96569464843, +15.72140928430, +0],
            [+32.00000000000, +16.00000000000, -60.85876863701, -8.370798034479e-3],
            [+16.00000000000, -32.00000000000, -23.62288406276, -9.615020243130e-1],
        ],
    )

    assert_allclose(ps.bus_voltage_pu, [1.05, 0.97060388168 - 0.045712315571j, 1.039960589436 - 0.009053862142j])


def test_current_fast_decoupled():
    ps.bus_voltage_pu[:] = 1.05, 1, 1.04
    ps.bus_apparent_power_pu[:] = 1, -4 - 2.5j, 2

    ps.select_solver("fast decoupled")

    # initial values
    (β_prime, β_dprime), (ΔP, ΔQ), (Δδ, ΔV) = ps.do_step()

    assert_allclose(
        β_prime.toarray(),
        [
            [52, -32],
            [-32, 62],
        ],
    )

    # assert_allclose doesn't work
    assert β_dprime.shape == (1, 1)
    assert β_dprime[0, 0] == 52

    assert_allclose(ΔP, [-2.86, 1.4384])
    assert_allclose(ΔQ, [-0.22])

    assert_allclose(Δδ, [-0.060482517, -0.00890909090])
    assert_allclose(ΔV, [-0.004230769])
