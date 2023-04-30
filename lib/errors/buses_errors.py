"""
    Errors to raise in user bus-defining uncompleted requirements
"""


class SlackBusNotDefinedError:
    """Raise it when buses system doesnt have a slack bus to reference"""

    def __init__(self):
        self.message = "No Slack bus was provided, needed to solve systems"


class DoubleSlackBusDefinitionError:
    """Raise it when buses system doesnt have a slack bus to reference"""

    def __init__(self):
        self.message = "System has already an slack bus, got"
