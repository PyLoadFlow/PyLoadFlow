from lib.decorators.electric import electric_power_system_as_self as electric


class BusConnector:
    @electric
    def connect_buses_by_id(self, i, j, z, y=0.0j):
        # making sure that the buses are different
        if i == j:
            return

        # transforming to admittance
        Y[i, j] = Y[j, i] = -1 / z

        # adding shunt susceptance to diagonal
        Y[i, i] += y / 2
        Y[j, j] += y / 2

        # storing connected buses into two buses
        buses[i].store_connected_bus_yid(j)
        buses[j].store_connected_bus_yid(i)

    def connect_buses_by_IEEE_id(self, i, j, *args, **kwargs):
        # fulfilling IEEE std. to numerate from 1 and not from 0
        return self.connect_buses_by_id(i - 1, j - 1, *args, **kwargs)

    @electric
    def build_line_series_admittance_pu_diagonal(self):
        # calculating self admittances from sum of mutual admittances
        for y in range(n):
            Y[y, y] = -Y[y].sum()
