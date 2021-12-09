from abc import ABC
from typing import Optional, Union

from units import *
import constants


class ChunkComponent(ABC):
    """
        A class to represent a component of a chunk.

        ...

        Attributes
        ----------
        index: int
            The position of the attribute in its parent, ranging from 0 to len(parent)
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
        __neighbours: Optional[list[ChunkComponent]]
            List of the neighbouring components of this component
        """

    index: int
    mass: Mass
    specific_heat_capacity: float
    heat_transfer_coefficient: float
    __energy: Energy = 0

    def __init__(self, mass: Mass, temperature: Temperature, *, component_type: str):
        # Information on the component
        self.component_type = component_type

        # Physical properties
        self.mass = mass
        self.specific_heat_capacity = constants.SPECIFIC_HEAT_CAPACITY[self.component_type]
        self.heat_transfer_coefficient = constants.SPECIFIC_HEAT_CAPACITY[self.component_type]

        self.temperature = temperature  # Requires specific heat capacity

    @classmethod
    def init_default(cls, *, component_type: str):
        return cls(mass=Mass(kilograms=1000), temperature=Temperature(celsius=21),
                   component_type=component_type)

    def __str__(self):
        res = f"{self.component_type} Component \n" \
              f"Mass : {self.mass} \n " \
              f"Temperature : {self.temperature} K ({self.__energy / self.mass} J/kg)"
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

    def get_diff(self, other: "ChunkComponent") -> Optional[dict[str, Unit]]:
        """
        Computes and returns the difference between the physical attributes of two GridComponent
        :param other: the other GridComponent to inspect
        :return:
        """
        if other is None:
            return None
        return {
            "temperature": (other.temperature - self.temperature),
            "mass": (other.mass - self.mass),
        }
