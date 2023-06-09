import numpy as np


def cis(phi):
    """
    converts complex angle to a rectangular unit complex
    """
    return np.cos(phi) + np.sin(phi) * 1j
