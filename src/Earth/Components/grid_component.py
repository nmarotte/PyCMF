from abc import ABC
from typing import Optional, Union

from constants import TIME_DELTA
from units import *


class GridComponent(ABC):
    index: int
    volume: Volume
    mass: Mass
    temperature: Temperature
    __neighbours: Optional[list["GridComponent"]]

    def __init__(self, volume: Volume = Volume(meters3=1), mass: Mass = Mass(kilograms=1000),
                 temperature: Temperature = Temperature(celsius=21), *, parent=None, index: int = None):
        self.volume = volume
        self.surface = Area(meters2=(volume ** (1 / 3)) ** 2)
        self.__mass = mass
        self.__temperature = temperature
        self.parent = parent
        # Finds yourself in the list
        self.index = index if index is not None else self.parent and self.parent.index(self)
        self.__neighbours = None

    @property
    def mass(self):
        return self.__mass

    @mass.setter
    def mass(self, value):
        self.parent.mass += (value - self.mass)
        self.__mass = value

    @property
    def temperature(self):
        return self.__temperature

    @temperature.setter
    def temperature(self, value):
        self.parent.temperature = None  # Invalidate cache to recompute average temperature when needed
        self.__temperature = value

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

    def add_energy(self, input_energy: Union[Energy, float]):
        self.temperature += input_energy / (self.specific_heat_capacity * self.mass)

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

    def compute_step(self) -> list[dict[str, Unit]]:
        return [self.get_diff(n) for n in self.parent.neighbours(self.index)]

    def apply_step(self, deltas: list[dict[str, Unit]]):
        joule_per_time_scale = Energy(joules=self.heat_transfer_coefficient * self.surface * TIME_DELTA)
        for i, n in enumerate(self.neighbours):
            self.add_energy(joule_per_time_scale * deltas[i]["temperature"])
            n.add_energy(-joule_per_time_scale * deltas[i]["temperature"])

    def update(self):
        joule_per_time_scale = Energy(joules=self.heat_transfer_coefficient * self.surface * TIME_DELTA)
        for n in self.neighbours:
            diff = self.get_diff(n)
            self.add_energy(joule_per_time_scale * diff["temperature"])
            n.add_energy(-joule_per_time_scale * diff["temperature"])
