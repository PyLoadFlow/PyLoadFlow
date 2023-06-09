"""
    Errors to raise when user forgotten some important steps
"""


class NotCompiledSystemError(Exception):
    """Raise it when user didn't compiled the system and started calculating"""

    def __init__(self):
        self.message = f"System was not compiled, this would raise convergence errors"
