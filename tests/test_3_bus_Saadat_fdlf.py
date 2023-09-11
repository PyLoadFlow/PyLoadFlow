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
ps.select_solver("fast decoupled")


def test_inicial_conditions():
    _, data = ps.do_step()
    
    β_prime = data["β'"]
    β_dprime = data['β"']
    
    assert ps.bus_voltage_pu[0] == 1.05

    assert ps.bus_apparent_power_pu[1] == -4 - 2.5j

    assert ps.bus_voltage_pu[2] == 1.04
    assert ps.bus_apparent_power_pu[2] == 2
    
    assert_allclose(
        β_prime.toarray(),
        [
            [-52, 32],
            [32, -62],
        ],
    )

    assert_allclose(β_dprime.toarray(), [[-52]])


def test_1st_iteration():
    _, data = ps.do_step()

    ΔP = data["ΔP"]
    ΔQ = data["ΔQ"]
    ΔS = data["ΔS"]
    Δδ = data["Δδ"]
    ΔV = data["Δ|V|"]
    V = data["|V|"]
    # δ = data["δ"]

    assert_allclose(V, [1.05, 1, 1.04])

    assert_allclose(ΔS[1:], [-2.86 - 0.22j, 1.4384 - 1.0192j])
    assert_allclose(ΔP, [-2.86, 1.4384])
    assert_allclose(ΔQ, [-0.22])

    assert_allclose(Δδ, [0.060482517, 0.0089090909])
    assert_allclose(ΔV, [0.004230769])
