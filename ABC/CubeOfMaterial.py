from abc import ABC
from functools import cache

from ABC.BlackBody import BlackBody
from ABC.Neighbored import Neighbored
from ABC.VolumetricBody import VolumetricBody


class CubeOfMaterial(BlackBody, VolumetricBody, Neighbored, ABC):
    def __init__(self, index: int, volume: float, mass: float, temperature: float):
        BlackBody.__init__(self, mass, pow(volume, 2 / 3), temperature)
        VolumetricBody.__init__(self, pow(volume, 1 / 3), self.area)
        Neighbored.__init__(self, index)

    @property
    @cache
    def density(self) -> float:
        return self.mass / self.volume
