from dataclasses import dataclass

from Grid import Grid
from units import *

from GridComponent import GridComponent


class Water(GridComponent):
    def __init__(self, volume: Volume = Volume(meters3=1),
                 mass: Mass = Mass(kilograms=1000),
                 temperature: Temperature = Temperature(celsius=21), *, parent: Grid, index: int = None):
        self.volume = volume
        self.mass = mass
        self.temperature = temperature
        self.parent = parent
        self.index = index or self.parent.index(self)  # Finds yourself in the list
