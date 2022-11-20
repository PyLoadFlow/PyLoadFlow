import attrs
from helpers import *


@attrs.define
class Node:
    value: int

    def call(self):
        self.faz()  # reconoce si Node o SubNode es quien llama
        self.__faz()  # no lo reconoce y siempre llama al de Node

    def faz(self):
        print("foo")

    def __faz(self):
        print("foo")


@attrs.define
class SubNode(Node):
    def faz(self):
        print("bar")

    def __faz(self):
        print("bar")


a = Node(1)
b = SubNode(4)

a.call()
b.call()
