from __future__ import annotations
from abc import ABC
from collections import Collection

from ABC.BlackBody import BlackBody
from ABC.Neighbored import Neighbored
from ABC.VolumetricBody import VolumetricBody
from Constants import DELTA_T


class CubeOfMaterial(BlackBody, VolumetricBody, Neighbored, ABC):
    def __init__(self, index: int, volume: float, mass: float, temperature: float):
        BlackBody.__init__(self, mass, pow(volume, 2 / 3), temperature)
        VolumetricBody.__init__(self, pow(volume, 1 / 3), self.area)
        Neighbored.__init__(self, index)

    @property
    def density(self) -> float:
        return self.mass / self.volume

    def average_temperature(self):
        """
        Averages the temperature of the cube given its surrounding
        :return:
        """
        average = sum([n.temperature for n in self.neighbors]) / len(self.neighbors)
        diff = average - self.temperature
        self.temperature += diff * DELTA_T * self.heat_transfer_factor
