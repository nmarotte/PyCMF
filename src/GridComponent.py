from abc import ABC, abstractmethod

from units import *


class GridComponent(ABC):
    index: int
    volume = Volume
    mass = Mass
    temperature = Temperature

    @staticmethod
    @abstractmethod
    def average(components):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def add_energy(self, input_energy: Energy):
        pass
