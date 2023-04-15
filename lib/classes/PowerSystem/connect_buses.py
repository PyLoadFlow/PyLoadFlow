def connect_buses_by_id(self, i, j, z, y=0.0j):
    # fulfilling IEEE std. to numerate from 1 and not from 0
    i -= 1
    j -= 1

    # making sure that the buses are different
    if i == j:
        return

    # transforming to admittance
    self.line_series_admittance_pu[i, j] = self.line_series_admittance_pu[j, i] = -1 / z

    # adding shunt susceptance to diagonal
    self.line_series_admittance_pu[i, i] += y / 2
    self.line_series_admittance_pu[j, j] += y / 2


def connect_buses(self, bus_i, bus_j, *args, **kwargs):
    # getting bus_i and bus_j indexes to pass to connect_buses_by_id()
    return self.connect_buses_by_id(self.buses.index(bus_i) + 1, self.buses.index(bus_j) + 1, *args, **kwargs)


def build_line_series_admittance_pu_diagonal(self):
    # calculating self admittances from sum of mutual admittances
    for y in range(self.number_of_buses):
        self.line_series_admittance_pu[y, y] = -self.line_series_admittance_pu[y].sum()  # type: ignore
