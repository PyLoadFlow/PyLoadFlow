# pyright: reportUndefinedVariable=false
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import splu

from lib.classes.PowerSystem_mixins.Allocator import Allocator
from lib.decorators import electric_power_system_as_param as electric


@electric
def fast_decoupled_solver(_):
    pass
