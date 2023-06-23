# import the library
from pyloadflow import PowerSystem

# define a system
ps = PowerSystem(n=4)

# define the buses
birch = ps.add_slack_bus(pload=0.5, qload=0.3099)
elm = ps.add_load_bus(P=1.7, pf=0.85)
pine = ps.add_load_bus(P=2, pf=0.85)
maple = ps.add_pv_bus(P=3.18, V=1.02, pload=0.8, qload=0.4958)

# connect them
ps.connect_buses_by_IEEE_id(1, 2, z=0.01008 + 0.0504j, y_2=0.05125j)
ps.connect_buses_by_IEEE_id(1, 3, z=0.00744 + 0.0372j, y_2=0.03875j)
ps.connect_buses_by_IEEE_id(2, 4, z=0.00744 + 0.0372j, y_2=0.03875j)
ps.connect_buses_by_IEEE_id(3, 4, z=0.01272 + 0.0636j, y_2=0.06375j)

# run
ps.run()

# Voilà!
print(ps.bus_voltage_pu)
print(ps.bus_apparent_power_pu)
