from dataclasses import dataclass
from typing import Optional

from Grid import Grid
from units import *

from GridComponent import GridComponent


class Water(GridComponent):
    @staticmethod
    def average(components):
        total_volume = total_mass = total_temperature = 0
        count = 0
        for elem in components:
            total_volume += elem.volume
            total_mass += elem.mass
            total_temperature += elem.temperature
            count += 1
        return total_volume/count, total_mass/count, total_temperature/count

    def __init__(self, volume: Volume = Volume(meters3=1), mass: Mass = Mass(kilograms=1000),
                 temperature: Temperature = Temperature(celsius=21), *, parent: Optional[Grid], index: int = None):
        self.volume = volume
        self.mass = mass
        self.temperature = temperature
        self.parent = parent
        self.index = index if index is not None else self.parent and self.parent.index(self)  # Finds yourself in the list
