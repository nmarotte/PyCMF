from abc import ABC


class AreaBody(ABC):
    def __init__(self, area: float):
        self.area: float = area  # [m^2]

