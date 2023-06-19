from pyloadflow import PowerSystem

# to display
from prettytable import PrettyTable
import numpy as np

# config
ps = PowerSystem(n=39)


ps.add_slack_bus(V=0.982, pload=0.092, qload=0.046)  # first element needs to be the slack one
ps.add_noload_bus()
ps.add_pq_bus(P=3.22, Q=0.024)
ps.add_pq_bus(P=5, Q=1.84)
ps.add_noload_bus()
ps.add_noload_bus()
ps.add_pq_bus(P=2.338, Q=0.84)
ps.add_pq_bus(P=5.22, Q=1.76)
ps.add_noload_bus()
ps.add_noload_bus()
ps.add_noload_bus()
ps.add_pq_bus(P=0.075, Q=0.88)
ps.add_noload_bus()
ps.add_noload_bus()
ps.add_pq_bus(P=3.2, Q=1.53)
ps.add_pq_bus(P=3.29, Q=0.323)
ps.add_noload_bus()
ps.add_pq_bus(P=1.58, Q=0.3)
ps.add_noload_bus()
ps.add_pq_bus(P=6.28, Q=1.03)
ps.add_pq_bus(P=2.74, Q=1.15)
ps.add_noload_bus()
ps.add_pq_bus(P=2.475, Q=0.846)
ps.add_pq_bus(P=3.086, Q=-0.92)
ps.add_pq_bus(P=2.240, Q=0.472)
ps.add_pq_bus(P=1.390, Q=0.170)
ps.add_pq_bus(P=2.810, Q=0.755)
ps.add_pq_bus(P=2.060, Q=0.276)
ps.add_pq_bus(P=2.835, Q=0.269)
ps.add_pv_bus(P=2.5, V=1.0475)
ps.add_noload_bus()
ps.add_pv_bus(P=6.50, V=0.9831)
ps.add_pv_bus(P=6.32, V=0.9972)
ps.add_pv_bus(P=5.08, V=1.0123)
ps.add_pv_bus(P=6.50, V=1.0493)
ps.add_pv_bus(P=5.60, V=1.0635)
ps.add_pv_bus(P=5.40, V=1.0278)
ps.add_pv_bus(P=8.30, V=1.0265)
ps.add_pv_bus(P=10.0, V=1.03, pload=11.04, qload=2.5)


ps.connect_buses_by_IEEE_id(31, 2, z=0.0035 + 0.0411j, y_2=0.6987j)
ps.connect_buses_by_IEEE_id(31, 39, z=0.001 + 0.025j, y_2=0.75j)

ps.connect_buses_by_IEEE_id(2, 3, z=0.0013 + 0.0151j, y_2=0.2572j)
ps.connect_buses_by_IEEE_id(2, 25, z=0.007 + 0.0086j, y_2=0.146j)

ps.connect_buses_by_IEEE_id(3, 4, z=0.0013 + 0.0213j, y_2=0.2214j)
ps.connect_buses_by_IEEE_id(3, 18, z=0.0011 + 0.0133j, y_2=0.2138j)

ps.connect_buses_by_IEEE_id(4, 5, z=0.0008 + 0.0128j, y_2=0.1342j)
ps.connect_buses_by_IEEE_id(4, 14, z=0.0008 + 0.0129j, y_2=0.1382j)

ps.connect_buses_by_IEEE_id(5, 6, z=0.0002 + 0.0026j, y_2=0.0434j)
ps.connect_buses_by_IEEE_id(5, 8, z=0.0008 + 0.0112j, y_2=0.1476j)

ps.connect_buses_by_IEEE_id(6, 7, z=0.0006 + 0.0092j, y_2=0.113j)
ps.connect_buses_by_IEEE_id(6, 11, z=0.0007 + 0.0082j, y_2=0.1389j)

ps.connect_buses_by_IEEE_id(7, 8, z=0.0004 + 0.0046j, y_2=0.0780j)
ps.connect_buses_by_IEEE_id(8, 9, z=0.0023 + 0.0363j, y_2=0.3804j)
ps.connect_buses_by_IEEE_id(9, 39, z=0.001 + 0.0250j, y_2=1.2000j)

ps.connect_buses_by_IEEE_id(10, 11, z=0.0004 + 0.0043j, y_2=0.079j)
ps.connect_buses_by_IEEE_id(10, 13, z=0.0004 + 0.0043j, y_2=0.079j)

ps.connect_buses_by_IEEE_id(13, 14, z=0.0009 + 0.0101j, y_2=0.1723j)
ps.connect_buses_by_IEEE_id(14, 15, z=0.0018 + 0.0217j, y_2=0.3660j)
ps.connect_buses_by_IEEE_id(15, 16, z=0.0009 + 0.0094j, y_2=0.1710j)

ps.connect_buses_by_IEEE_id(16, 17, z=0.0007 + 0.0089j, y_2=0.1342j)
ps.connect_buses_by_IEEE_id(16, 19, z=0.0016 + 0.0195j, y_2=0.3040j)
ps.connect_buses_by_IEEE_id(16, 21, z=0.0008 + 0.0135j, y_2=0.2548j)
ps.connect_buses_by_IEEE_id(16, 24, z=0.0003 + 0.0059j, y_2=0.0680j)

ps.connect_buses_by_IEEE_id(17, 18, z=0.0007 + 0.0082j, y_2=0.1319j)
ps.connect_buses_by_IEEE_id(17, 27, z=0.0013 + 0.0173j, y_2=0.3216j)

ps.connect_buses_by_IEEE_id(21, 22, z=0.0008 + 0.0140j, y_2=0.2565j)
ps.connect_buses_by_IEEE_id(22, 23, z=0.0006 + 0.0096j, y_2=0.1846j)
ps.connect_buses_by_IEEE_id(23, 24, z=0.0022 + 0.0350j, y_2=0.3610j)
ps.connect_buses_by_IEEE_id(25, 26, z=0.0032 + 0.0323j, y_2=0.5130j)

ps.connect_buses_by_IEEE_id(26, 27, z=0.0014 + 0.0147j, y_2=0.2396j)
ps.connect_buses_by_IEEE_id(26, 28, z=0.0043 + 0.0474j, y_2=0.7802j)
ps.connect_buses_by_IEEE_id(26, 29, z=0.0057 + 0.0625j, y_2=1.0290j)

ps.connect_buses_by_IEEE_id(28, 29, z=0.0014 + 0.0151j, y_2=0.2490j)

ps.connect_buses_with_taps_by_IEEE_id(12, 11, z=0.0016 + 0.0435j, a=1.006)
ps.connect_buses_with_taps_by_IEEE_id(12, 13, z=0.0016 + 0.0435j, a=1.006)

ps.connect_buses_with_taps_by_IEEE_id(6, 1, z=0.0250j, a=1.070)
ps.connect_buses_with_taps_by_IEEE_id(10, 32, z=0.02j, a=1.070)

ps.connect_buses_with_taps_by_IEEE_id(19, 33, z=0.0007 + 0.0142j, a=1.070)
ps.connect_buses_with_taps_by_IEEE_id(20, 34, z=0.0009 + 0.0180j, a=1.009)

ps.connect_buses_with_taps_by_IEEE_id(22, 35, z=0.0143j, a=1.025)
ps.connect_buses_by_IEEE_id(23, 36, z=0.0005 + 0.0272j)
ps.connect_buses_with_taps_by_IEEE_id(25, 37, z=0.0006 + 0.0232j, a=1.025)
ps.connect_buses_with_taps_by_IEEE_id(2, 30, z=0.0181j, a=1.025)
ps.connect_buses_with_taps_by_IEEE_id(29, 38, z=0.0008 + 0.0156j, a=1.025)
ps.connect_buses_with_taps_by_IEEE_id(19, 20, z=0.0007 + 0.0138j, a=1.06)


# Displaying (optional)
np.set_printoptions(precision=4)
buses_table = PrettyTable()
err_table = PrettyTable()

err_table.field_names = "nit", "err"

ps.compile()

# np.savetxt(f"__resultfiles/Ybus.csv", ps.line_series_admittance_pu.toarray(), delimiter=",", fmt="%.4f")

# solve system
for nit, err, data in ps.step_by_step(method="cilf", max_nit=16, tol=1e-5):
    # print()
    # break

    # if nit == 1:
    # # if nit >= 1 or nit <= 4:
    #     np.savetxt(f"__resultfiles/B_1_{nit}.csv", data["β'"].toarray(), delimiter=",", fmt="%.4f")
    #     np.savetxt(f"__resultfiles/B_2_{nit}.csv", data['β"'].toarray(), delimiter=",", fmt="%.4f")

    if nit == 16:
        # np.savetxt(f"__resultfiles/jacobiano_{nit}.csv", data["J"].toarray(), delimiter=",", fmt="%.4f")
        break

    err_table.add_row([nit, err])

print(err_table)

buses_table.add_column("Num", np.arange(1, ps.number_of_buses + 1))
buses_table.add_column("Voltage [pu]", np.abs(ps.bus_voltage_pu))
buses_table.add_column("phase [deg]", np.angle(ps.bus_voltage_pu, deg=True))
buses_table.add_column("P Gen. [pu]", ps.bus_real_generation_power_pu)
buses_table.add_column("Q Gen. [pu]", ps.bus_reactive_generation_power_pu)
buses_table.add_column("P Load [pu]", ps.bus_real_load_power_pu)
buses_table.add_column("Q Load [pu]", ps.bus_reactive_load_power_pu)

print(buses_table)
