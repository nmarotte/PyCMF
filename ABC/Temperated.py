from __future__ import annotations

from abc import abstractmethod
from functools import cache

from ABC.AreaBody import AreaBody
from ABC.MassBody import MassBody
from Constants import DELTA_T
from abc import ABC


class Temperated(AreaBody, MassBody, ABC):
    @property
    @abstractmethod
    def thermal_conductivity(self) -> float:
        """
        The ability of the material to conduct heat.
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

    @property
    @abstractmethod
    def density(self) -> float:
        """
        The density of the material
        In this class because it is necessary for the computation of thermal_diffusivity
        :return:
        """

    def __init__(self, mass: float, area: float, temperature: float):
        AreaBody.__init__(self, area)
        energy = temperature * self.specific_heat_capacity * mass
        MassBody.__init__(self, mass, energy)

    def average_temperature(self, other: Temperated):
        """
        As much as I would like to compute the energy transfer, this is unrealistic. However temperature do transfer
        :param other:
        :return:
        """
        diff = abs(other.temperature - self.temperature)
        rate_of_t_change = self.thermal_diffusivity * self.area * diff * DELTA_T  # [m^2 s^-1] * [m^2] * [t] * s
        rate_of_t_change = rate_of_t_change if self.temperature > other.temperature else -rate_of_t_change
        self.temperature -= rate_of_t_change
        other.temperature += rate_of_t_change

    @property
    @cache
    def thermal_diffusivity(self) -> float:
        """
        Abstract because it requires the density of the material that depend on the object
        Is computed through thermal conductivity, density and specific heat capacity.
        https://en.wikipedia.org/wiki/Thermal_diffusivity
        [m^2 s^-1] = [W m^-1 K^-1] * [m^3 kg^-1] * [J^-1 kg^1 K^1]
                   = [W] * [m^2] * [kg^-1 m^-2 s^2]
                   = [kg m^2 s^-3] * [kg^-1 s^2]
                   = [m^2 s^-1]
        :return:
        """
        return self.thermal_conductivity / (self.density * self.specific_heat_capacity)

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
        self.set_energy(new_t * self.specific_heat_capacity * self.mass)  # [J] = [K] * [J K^-1 kg^-1] * [kg]

