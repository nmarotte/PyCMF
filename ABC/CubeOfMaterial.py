from abc import ABC

from ABC.BlackBody import BlackBody
from ABC.Neighbored import Neighbored
from ABC.Temperated import Temperated
from ABC.VolumetricBody import VolumetricBody


class CubeOfMaterial(BlackBody, VolumetricBody, Neighbored, Temperated, ABC):
    def __init__(self, index: int, volume: float, mass: float, energy: float):
        BlackBody.__init__(self, pow(volume, 2 / 3), mass, energy)
        VolumetricBody.__init__(self, pow(volume, 1 / 3), self.area)
        Neighbored.__init__(self, index)
        Temperated.__init__(self, self.temperature, self.area)

    @property
    def density(self) -> float:
        return self.mass / self.volume
