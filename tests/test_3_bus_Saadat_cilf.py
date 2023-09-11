# pyright: reportGeneralTypeIssues=false
from numpy.testing import assert_allclose

from pyloadflow import PowerSystem

ps = PowerSystem(n=3)

ps.add_slack_bus(V=1.05)
ps.add_pq_bus(P=4, Q=2.5)
ps.add_pv_bus(P=2, V=1.04)

ps.connect_buses_by_IEEE_id(1, 2, z=0.02 + 0.04j)
ps.connect_buses_by_IEEE_id(2, 3, z=0.0125 + 0.025j)
ps.connect_buses_by_IEEE_id(3, 1, z=0.01 + 0.03j)

ps.compile()
ps.select_solver("current inyections")


def test_inicial_conditions():
    err, _ = ps.do_step()
    
    assert_allclose(ps.buses[1].programmed_current_pu, -4 + 2.5j)
    assert_allclose(ps.buses[2].programmed_current_pu, 1.92307692)

    assert_allclose(err, [-2.86, 0.22, 1.38307692, 0.98])


def test_1st_iteration():
    err, data = ps.do_step()
    J = data["J"]

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


def test_2nd_iteration():
    err, data = ps.do_step()
    J = data["J"]

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


def test_3rd_iteration():
    err, data = ps.do_step()
    J = data["J"]

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

    assert_allclose(err, 0, atol=1e-10)
