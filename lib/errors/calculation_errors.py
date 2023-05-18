"""
    Errors to raise when calculations are imposible to solve
"""


class ConvergenceError(Exception):
    """Raise it when max iterations number are more than allowed ones"""

    def __init__(self, max_nit, err):
        self.message = f"Max number of iterations has exceeded, got {max_nit} with an error of {err}"
