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
