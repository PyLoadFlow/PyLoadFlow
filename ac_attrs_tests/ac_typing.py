import attrs
from helpers import *


@attrs.define
class Node:
    value: int
    children: "list[Node]" = []

    def faz(self, foo: float):
        return self.children[0].faz(foo / 3)


a = Node(1)
b = Node(2)
c = Node(3)

a.children = [b, c]
b.children = [a, c]

p(a)
