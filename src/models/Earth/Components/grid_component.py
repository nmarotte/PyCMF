from abc import ABC
from typing import Optional, Union

from constants import TIME_DELTA
from units import *


class GridComponent(ABC):
    index: int
    volume: Volume
    mass: Mass
    __energy: Energy = 0
    __neighbours: Optional[list["GridComponent"]]

    def __init__(self, volume: Volume = Volume(meters3=1), mass: Mass = Mass(kilograms=1000),
                 temperature: Temperature = Temperature(celsius=21), *, parent=None, index: int = None):
        self.volume = volume
        self.surface = Area(meters2=(volume ** (1 / 3)) ** 2)
        self.mass = mass
        self.temperature = temperature
        self.parent = parent
        # Finds yourself in the list
        self.index = index if index is not None else self.parent and self.parent.index(self)
        self.__neighbours = None

    def __str__(self):
        res = f"""{self.__class__} Component
Volume : {self.volume}
Mass : {self.mass}
Temperature : {self.temperature} ({self.__energy} J)
"""
        return res

    @property
    def temperature(self) -> Temperature:
        value = Temperature(kelvin=self.__energy / (self.specific_heat_capacity * self.mass))
        return value

    @temperature.setter
    def temperature(self, value: Temperature):
        self.__energy = Energy(joules=self.specific_heat_capacity * self.mass * value)

    @property
    def energy(self) -> Energy:
        return self.__energy

    @energy.setter
    def energy(self, value: Energy):
        self.__energy = value

    @property
    @abstractmethod
    def specific_heat_capacity(self) -> float:
        pass

    @property
    @abstractmethod
    def heat_transfer_coefficient(self) -> float:
        pass

    @property
    def neighbours(self):
        if self.__neighbours is None:
            self.__neighbours = self.parent.neighbours(self.index)
        return self.__neighbours

    @neighbours.setter
    def neighbours(self, value: list["GridComponent"]):
        self.__neighbours = value

    def get_diff(self, other: "GridComponent") -> dict[str, Unit]:
        """
        Computes and returns the difference between the physical attributes of two GridComponent
        :param other: the other GridComponent to inspect
        :return:
        """
        return {
            "temperature": (other.temperature - self.temperature),
            "volume": (other.volume - self.volume),
            "mass": (other.mass - self.mass),
        }

    def update(self):
        joule_per_time_scale = self.heat_transfer_coefficient * self.surface * TIME_DELTA
        for n in self.neighbours:
            diff = self.get_diff(n)
            self.energy += joule_per_time_scale * diff["temperature"] * TIME_DELTA
            n.energy -= joule_per_time_scale * diff["temperature"] * TIME_DELTA
