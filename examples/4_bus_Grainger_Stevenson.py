from lib import PowerSystem

ps = PowerSystem(n=4)

birch = ps.add_slack_bus()
elm = ps.add_load_bus(P=1.7, pf=0.85)
pine = ps.add_load_bus(P=2, pf=0.85)
maple = ps.add_pv_bus(P=3.18, V=1.02, pload=0.8)

ps.connect_buses_by_IEEE_id(1, 2, z=0.01008 + 0.0504j, y=0.1025j)
ps.connect_buses_by_IEEE_id(1, 3, z=0.00744 + 0.0372j, y=0.0775j)
ps.connect_buses_by_IEEE_id(2, 4, z=0.00744 + 0.0372j, y=0.0775j)
ps.connect_buses_by_IEEE_id(3, 4, z=0.01272 + 0.0636j, y=0.1275j)

ps.run(method="cilf", max_nit=16, tol=1e-5)

print(ps.bus_voltage_pu)
print(ps.bus_programed_apparent_power)
