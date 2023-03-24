from prettyprinter import cpprint
from Bus import *

ps = PowerSystem(n=3)

bus0 = SlackBus(V=1.05, δ=0, system=ps)
bus1 = LoadBus(P=4, Q=2.5, system=ps)
bus2 = GeneratorBus(V=1.04, P=2, system=ps)

bus0.connect(bus1, z=0.02 + 0.04j)
bus1.connect(bus2, z=0.0125 + 0.025j)
bus2.connect(bus0, z=0.01 + 0.03j)

ps.run()

cpprint(bus0)
cpprint(bus1)
cpprint(bus2)
