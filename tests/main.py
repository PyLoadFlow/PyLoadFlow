# from prettyprinter import cpprint
# from Bus import *

# ps = PowerSystem(n=3)

# bus0 = SlackBus(V=1.05, δ=0, system=ps)
# bus1 = LoadBus(P=4, Q=2.5, system=ps)
# bus2 = GeneratorBus(V=1.04, P=2, system=ps)

# bus0.connect(bus1, z=0.02 + 0.04j, y=1.6e-4j)
# bus1.connect(bus2, z=0.0125 + 0.025j, y=1.6e-4j)
# bus2.connect(bus0, z=0.01 + 0.03j, y=1.6e-4j)

# ps.compile()  # previous calcs
# ps.solve(tol=1e-9, max_nit=6)

# cpprint(bus0)
# cpprint(bus1)
# cpprint(bus2)
