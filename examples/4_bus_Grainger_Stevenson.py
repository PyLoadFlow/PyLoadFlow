from loadwolf import PowerSystem

# to display
from prettytable import PrettyTable
import numpy as np

# config
ps = PowerSystem(n=4)

birch = ps.add_slack_bus(pload=0.5, qload=0.3099)
elm = ps.add_load_bus(P=1.7, pf=0.85)
pine = ps.add_load_bus(P=2, pf=0.85)
maple = ps.add_pv_bus(P=3.18, V=1.02, pload=0.8, qload=0.4958)

ps.connect_buses_by_IEEE_id(1, 2, z=0.01008 + 0.0504j, y_2=0.05125j)
ps.connect_buses_by_IEEE_id(1, 3, z=0.00744 + 0.0372j, y_2=0.03875j)
ps.connect_buses_by_IEEE_id(2, 4, z=0.00744 + 0.0372j, y_2=0.03875j)
ps.connect_buses_by_IEEE_id(3, 4, z=0.01272 + 0.0636j, y_2=0.06375j)

# Displaying (optional)
buses_table = PrettyTable()
err_table = PrettyTable()

err_table.field_names = "nit", "err"

ps.compile()

# solve system
for nit, err, data in ps.step_by_step(method="fdlf", max_nit=16, tol=1e-5):
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
