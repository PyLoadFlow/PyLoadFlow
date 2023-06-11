from loadwolf import PowerSystem

# to display
from prettytable import PrettyTable
import numpy as np

# modify this lines to solve with another system
ps = PowerSystem(n=3)

ps.add_slack_bus(V=1.05)
ps.add_pq_bus(P=4, Q=2.5)
ps.add_pv_bus(P=2, V=1.04)

ps.connect_buses_by_IEEE_id(1, 2, z=0.02 + 0.04j)
ps.connect_buses_by_IEEE_id(2, 3, z=0.0125 + 0.025j)
ps.connect_buses_by_IEEE_id(3, 1, z=0.01 + 0.03j)

# Displaying (optional)
buses_table = PrettyTable()
err_table = PrettyTable()

err_table.field_names = "nit", "err"

ps.compile()

# solve system
for nit, err, data in ps.step_by_step(method="cilf", max_nit=16, tol=1e-5):
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
