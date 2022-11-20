import numpy as np
import numpy.typing as npt
from colorama import Fore

# mejor visión de los datos
from prettyprinter import install_extras, cpprint as p

install_extras(["numpy", "attrs"])  # type: ignore


def hr():
    print("-------------------------")


def inspect(name, value):
    print(name, end=" = ")
    p(value, end="\n\n")
