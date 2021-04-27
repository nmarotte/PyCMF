from __future__ import annotations

from abc import abstractmethod

from ABC.AreaBody import AreaBody
from ABC.MassBody import MassBody
from Constants import DELTA_T
from abc import ABC


class Temperated(AreaBody, MassBody, ABC):
    @property
    @abstractmethod
    def thermal_conductivity(self) -> float:
        """
        The thermal conductivity of the material
        :return: a constant for the material in Watt per meter Kelvin ( [W m^-1 K^-1] )
        """

    @property
    @abstractmethod
    def specific_heat_capacity(self) -> float:
        """
        The specific heat capacity of the material
        https://en.wikipedia.org/wiki/Heat_capacity#Specific_heat_capacity
        :return: a constant for the material in Joule per kilogram Kelvin ( [J kg^-1 K^-1] )
        """

    def __init__(self, mass: float, area: float, energy: float):
        AreaBody.__init__(self, area)
        MassBody.__init__(self, mass, energy)

    def average_temperature(self, other: Temperated):
        """
        As much as I would like to compute the energy transfer, this is unrealistic. However temperature do transfer
        :param other:
        :return:
        """
        diff = abs(other.temperature - self.temperature)
        rate_of_t_change = self.thermal_diffusivity * self.area * diff * DELTA_T
        rate_of_t_change = rate_of_t_change if self.temperature > other.temperature else -rate_of_t_change
        self.temperature -= rate_of_t_change
        other.temperature += rate_of_t_change


    @property
    @abstractmethod
    def thermal_diffusivity(self) -> float:
        """
        Abstract because it requires the density of the material that depend on the object
        Is computed through thermal conductivity, density and specific heat capacity.
        https://en.wikipedia.org/wiki/Thermal_diffusivity
        :return: return CubeOfMaterial.thermal_conductivity / (self.density * CubeOfMaterial.specific_heat_capacity)
        """

    @property
    def temperature(self):
        """
        The temperature of the system computed via its energy
        Result unit : [K]
        Energy Unit : [J] = [kg m^2 s^-2]
        Calculation :
        [K] = [J] / [J K^-1 kg^-1] * [kg]
                    ^^^^^^^^^^^^^
                    specific heat
                    capacity
        :return:
        """
        return self.energy / (self.specific_heat_capacity * self.mass)  # [K] = [J / ((J K^-1 kg^-1) * kg)]

    @temperature.setter
    def temperature(self, new_t):
        """
        Adds the value to the current temperature and recompute the energy
        :param new_t: the new temperature
        :return:
        """
        self.energy = new_t * self.specific_heat_capacity * self.mass  # [J] = [K] * [J K^-1 kg^-1] * [kg]
