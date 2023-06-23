# pyloadflow

A simple and powerful load calculations library for python 3

Solve power systems with

- [x] Current Injections (cilf)
- [x] Fast Decoupled method (fdlf)

## Get started

Let's Solve the 3-bus Hadi Saadat power system

```python
from pyloadflow import PowerSystem

ps = PowerSystem(n=3)

ps.add_slack_bus(V=1.05)
ps.add_pq_bus(P=4, Q=2.5)
ps.add_pv_bus(P=2, V=1.04)

ps.connect_buses_by_IEEE_id(1, 2, z=0.02 + 0.04j)
ps.connect_buses_by_IEEE_id(2, 3, z=0.0125 + 0.025j)
ps.connect_buses_by_IEEE_id(3, 1, z=0.01 + 0.03j)

ps.run()

# Voilà!
print(ps.bus_voltage_pu)
print(ps.bus_apparent_power_pu)
```

Result:

```bash
[1.05      +0.j         0.97060388-0.04571232j 1.03996059-0.00905386j]
[2.18422834+1.40851505j         -4.-2.5j         2.+1.46176925j]
```

Proyecto de tesis de Luis Miguel Pintor Olivares

Asesorado por:
- M. en C. Alejandro Villegas Ortega
- Lic. Blanca Marina Feregrino Leyva
- M. en C. Sergio Baruch Barragán Gómez
