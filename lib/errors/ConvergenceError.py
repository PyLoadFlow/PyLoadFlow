from attrs import define


@define
class ConvergenceError(Exception):
    message = "max iteration number exceeded set obj.max_iterations_number to allow more iterations"
