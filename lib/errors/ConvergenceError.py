class ConvergenceError(Exception):
    def __init__(self, nit):
        super().__init__(
            f"max iteration number exceeded (got {nit}), set obj.max_iterations_number to allow more iterations"
        )
