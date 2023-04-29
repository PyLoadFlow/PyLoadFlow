from lib.classes.Allocator import Allocator
from lib.classes.BusList import BusList


class PowerSystem(Allocator, BusList):
    def __init__(self, n):
        Allocator(n)
