import numpy as np

SLACK, PQ, PV = range(3)

BUS_TYPES = PQ, PV, PQ, SLACK, PV, PQ

n = len(BUS_TYPES)
J = np.zeros([n * 2 - 2, n * 2 - 2])


def non_slack_buses():
    for y, type in enumerate(BUS_TYPES):
        if type is not SLACK:
            yield y


def pq_buses():
    for y, type in enumerate(BUS_TYPES):
        if type is PQ:
            yield y


def pv_buses():
    for y, type in enumerate(BUS_TYPES):
        if type is PV:
            yield y


def slack_bus():
    for y, type in enumerate(BUS_TYPES):
        if type is SLACK:
            return y


def quadrants(gen):
    y_slack = slack_bus()
    has_passed_slack = 0

    for y in gen:
        yield y + has_passed_slack, (y + has_passed_slack) * 2

        if y > y_slack:
            has_passed_slack = -1


print("PQ Buses: ", list(pq_buses()))
print("PV Buses: ", list(pv_buses()))
print("Slack Bus: ", slack_bus())


# Getting main jacobian
for y, i in quadrants(pq_buses()):
    print(f"ΔI[{y}]:V[{y}]", end=",\t")
    J[i : i + 2, i : i + 2] = y

for y, i in quadrants(pv_buses()):
    print(f"ΔI[{y}]:V[{y}]", end=",\t")
    J[i : i + 2, i : i + 2] = y

print()
print(J)
