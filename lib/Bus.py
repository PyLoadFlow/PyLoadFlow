import attrs
from PowerSystem import PowerSystem


@attrs.define
class Bus:
    system: PowerSystem
    connected_buses: list[int] = []
    _id: int = -1

    def __attrs_post_init__(self):
        # generating id from all system connected buses
        self._id = self.system.add(self)

        # considerating self admittance
        self.connected_buses.append(self._id)

    def connect(self, bus: "Bus", y=0j, z=0j):
        """sugar for PowerSystem.connect(bus1, bus2)"""
        self.system.connect(self, bus, z, y)
        return self


@attrs.define
class SlackBus(Bus):
    V: float = 1
    δ: float = 0


@attrs.define
class LoadBus(Bus):
    P: float = 0
    Q: float = 0
    zip: list[float] = [0, 0, 1]
    ziq: list[float] = [0, 0, 1]


@attrs.define
class GeneratorBus(Bus):
    V: float = 1
    P: float = 0
