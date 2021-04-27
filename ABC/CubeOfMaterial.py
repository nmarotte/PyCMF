from abc import ABC

from ABC.BlackBody import BlackBody
from ABC.Neighbored import Neighbored
from ABC.VolumetricBody import VolumetricBody


class CubeOfMaterial(BlackBody, VolumetricBody, Neighbored, ABC):
    def __init__(self, index: int, volume: float, mass: float, energy: float):
        BlackBody.__init__(self, mass, pow(volume, 2 / 3), energy)
        VolumetricBody.__init__(self, pow(volume, 1 / 3), self.area)
        Neighbored.__init__(self, index)

    @property
    def density(self) -> float:
        return self.mass / self.volume
