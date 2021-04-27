from ABC.AreaBody import AreaBody
from abc import ABC


class VolumetricBody(AreaBody, ABC):
    def __init__(self, depth: float, area: float):
        super().__init__(area)
        self.volume: float = depth * area  # [m^3] = [m] * [m^2]
