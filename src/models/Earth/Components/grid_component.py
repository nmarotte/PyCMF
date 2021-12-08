from abc import ABC
from typing import Optional, Union

from constants import TIME_DELTA
from units import *

SPECIFIC_HEAT_CAPACITY = {  # [J kg^-1 C^-1]
    "Water": 4184,
    "Air": 1012,
    "Argon": 520.3,
    "Nitrogen": 1040,
    "Oxygen": 918,
    "Land": 830
}

HEAT_TRANSFER_COEFFICIENT = {  # [W m^-2 K^-1]
    "Water": 1000,
    "Air": 12.5,  # 12.5 = 0.78*Nitrogen + 0.21*Oxygen + 0.01*Argon
    "Argon": 1,  # Computed/Made up
    "Nitrogen": 10,  # Computed/Made up
    "Oxygen": 22.3,  # Computed/Made up
    "Land": 250  # Made up
}


class GridComponent(ABC):
    """
        A class to represent a person.

        ...

        Attributes
        ----------
        index: int
            The position of the attribute in its parent, ranging from 0 to len(parent)
        volume: Volume(float)
            The Volume of the component, will be used as m^3
        surface: Area(float)
            The computed Area of the component, will be used in m^2
        mass: Mass(float)
            The Mass of the component, will be used as kg
        specific_heat_capacity:
            The amount of heat that must be added to a material to increase its temperature
            See https://en.wikipedia.org/wiki/Specific_heat_capacity
            Expressed in Joules per Kilograms per Kelvin (Water = 4184 Jkg-1K-1)
        heat_transfer_coefficient:
            Coefficient for Newton's law of Cooling
            See https://en.wikipedia.org/wiki/Heat_transfer_coefficient
            Expressed in Watt per Meter squared per Kelvin
        __energy: Energy(float)
            The molecular kinetic energy of the component. It is used to store and compute the temperature of the
            component
        __neighbours: Optional[list[GridComponent]]
            List of the neighbouring components of this component
        """

    index: int
    volume: Volume
    surface: Area
    mass: Mass
    specific_heat_capacity: float
    heat_transfer_coefficient: float
    __energy: Energy = 0
    __neighbours: Optional[list["GridComponent"]]

    def __init__(self, volume: Volume, mass: Mass, temperature: Temperature, *, component_type: str, parent=None, index: int = None):
        # Information on the component
        self.component_type = component_type

        # Physical properties
        self.volume = volume
        self.surface = Area(meters2=(volume ** (1 / 3)) ** 2)
        self.mass = mass
        self.parent = parent
        self.specific_heat_capacity = SPECIFIC_HEAT_CAPACITY[self.component_type]
        self.heat_transfer_coefficient = SPECIFIC_HEAT_CAPACITY[self.component_type]
        self.temperature = temperature
        # Finds yourself in the list
        self.index = index if index is not None else self.parent and self.parent.index(self)
        self.__neighbours = None

    @classmethod
    def init_default(cls, *, component_type: str, parent=None, index: int = None):
        return cls(volume=Volume(meters3=1), mass=Mass(kilograms=1000), temperature=Temperature(celsius=21),
                   component_type=component_type, parent=parent, index=index)

    def __str__(self):
        res = f"{self.component_type} Component \n" \
              f"Volume : {self.volume} \n" \
              f"Mass : {self.mass} \n " \
              f"Temperature : {self.temperature} K ({self.__energy/self.mass} J/kg)"
        return res

    @property
    def temperature(self) -> Temperature:
        value = Temperature(kelvin=self.energy / (self.specific_heat_capacity * self.mass))
        return value

    @temperature.setter
    def temperature(self, value: Temperature):
        self.energy = Energy(joules=self.specific_heat_capacity * self.mass * value)

    @property
    def energy(self) -> Energy:
        return self.__energy

    @energy.setter
    def energy(self, value: Energy):
        self.__energy = value

    @property
    def neighbours(self):
        if self.__neighbours is None:
            self.__neighbours = self.parent.neighbours(self.index)
        return self.__neighbours

    @neighbours.setter
    def neighbours(self, value: list["GridComponent"]):
        self.__neighbours = value

    def get_diff(self, other: "GridComponent") -> Optional[dict[str, Unit]]:
        """
        Computes and returns the difference between the physical attributes of two GridComponent
        :param other: the other GridComponent to inspect
        :return:
        """
        if other is None:
            return None
        return {
            "temperature": (other.temperature - self.temperature),
            "volume": (other.volume - self.volume),
            "mass": (other.mass - self.mass),
        }

    def update(self):
        joule_per_time_scale = self.heat_transfer_coefficient * self.surface * TIME_DELTA
        for n in self.neighbours:
            diff = self.get_diff(n)
            if diff:
                self.energy += joule_per_time_scale * diff["temperature"] * TIME_DELTA
                n.energy -= joule_per_time_scale * diff["temperature"] * TIME_DELTA
