# pyright: reportUndefinedVariable=false
from loadwolf.decorators.electric import electric_power_system_as_self as electric


class BusConnector:
    """Mixin of PowerSystem to build branch impedance matrix"""

    @electric
    def connect_buses_by_id(self, i: int, j: int, z: complex, y=0.0j, y_2=0.0j, y_i=0.0j, y_j=0.0j):
        """Writes outside diagonal values for the branch impedance matrix, saves shunt impedance and registers buses mutual connection

        Args:
            i (int): index from first bus i to connect to the bus j
            j (int): index from first bus j to connect to the bus i
            z (complex): branch impedance between buses (i) and (j)
            y (complex): shunt impedance along the line between buses (i) and (j). Defaults to 0.0j.
            y_2 (complex): same that (y), but for for already divided data. Defaults to 0.0j.
        """
        # making sure that the buses are different
        if i == j:
            return

        # transforming to admittance
        Y[i, j] = Y[j, i] = -1 / z

        # adding shunt susceptance to diagonal
        Y[i, i] += y / 2 + y_2 + y_i
        Y[j, j] += y / 2 + y_2 + y_j

        # storing connected buses into two buses
        buses[i].store_connected_bus_yid(j)
        buses[j].store_connected_bus_yid(i)

    def connect_buses_by_IEEE_id(self, i: int, j: int, z: complex, y=0.0j, y_2=0.0j):
        """Same than connect_buses_by_id, but counts from 1 and not from 0 as arrays do

        Writes outside diagonal values for the branch impedance matrix, saves shunt impedance and registers buses mutual connection


        Args:
            i (int): index from first bus i to connect to the bus j
            j (int): index from first bus j to connect to the bus i
            z (complex): branch impedance between buses (i) and (j)
            y (complex): shunt impedance along the line between buses (i) and (j). Defaults to 0.0j.
        """
        # fulfilling IEEE std. to numerate from 1 and not from 0
        return self.connect_buses_by_id(i - 1, j - 1, z, y, y_2)

    @electric
    def build_line_series_admittance_pu_diagonal(self):
        """Calculates diagonal inside values"""
        # calculating self admittances from sum of mutual admittances
        for y in range(n):
            Y[y, y] = -Y[y].sum()
