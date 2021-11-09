from abc import ABC, abstractmethod
from units import *


class GridComponent(ABC):
    index: int
    volume: Volume
    mass: Mass
    temperature: Temperature
    _neighbours: list

    def __init__(self, volume: Volume = Volume(meters3=1), mass: Mass = Mass(kilograms=1000),
                 temperature: Temperature = Temperature(celsius=21), *, parent = None, index: int = None):
        self.volume = volume
        self.mass = mass
        self.temperature = temperature
        self.parent = parent
        self.index = index if index is not None else self.parent and self.parent.index(self)  # Finds yourself in the list
        self._neighbours = []

    @property
    def neighbours(self):
        if not self._neighbours:
            self._neighbours = self.parent.neighbours(self.index)
        return self._neighbours

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def add_energy(self, input_energy: Energy):
        pass

    @abstractmethod
    def compute_step(self):
        pass
