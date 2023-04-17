def connect_buses_by_id(self, i, j, z, y=0.0j):
    # making sure that the buses are different
    if i == j:
        return

    # transforming to admittance
    self.line_series_admittance_pu[i, j] = self.line_series_admittance_pu[j, i] = -1 / z

    # adding shunt susceptance to diagonal
    self.line_series_admittance_pu[i, i] += y / 2
    self.line_series_admittance_pu[j, j] += y / 2

    # storaging connected buses into two buses
    self.buses[i].connected_buses_yids.append(j)
    self.buses[j].connected_buses_yids.append(i)


def connect_buses_by_IEEE_id(self, i, j, *args, **kwargs):
    # fulfilling IEEE std. to numerate from 1 and not from 0
    return self.connect_buses_by_id(i - 1, j - 1, *args, **kwargs)


def connect_buses(self, bus_i, bus_j, *args, **kwargs):
    if not isinstance(bus_i, int):
        bus_i = bus_i.yid

    if not isinstance(bus_j, int):
        bus_j = bus_j.yid

    # getting bus_i and bus_j indexes to pass to connect_buses_by_id()
    return self.connect_buses_by_id(bus_i, bus_j, *args, **kwargs)
    # return self.connect_buses_by_id(self.buses.index(bus_i), self.buses.index(bus_j), *args, **kwargs)


def build_line_series_admittance_pu_diagonal(self):
    # calculating self admittances from sum of mutual admittances
    for y in range(self.number_of_buses):
        self.line_series_admittance_pu[y, y] = -self.line_series_admittance_pu[y].sum()  # type: ignore
