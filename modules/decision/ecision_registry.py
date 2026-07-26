from .decision_office import DecisionOffice


class DecisionRegistry:
    """
    Central access point for all decision services.
    """

    def __init__(self):
        self.office = DecisionOffice()

    def get_office(self) -> DecisionOffice:
        return self.office