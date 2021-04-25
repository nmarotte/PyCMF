from __future__ import annotations

import numpy as np

from ABC.BlackBody import BlackBody
from ABC.VolumetricBody import VolumetricBody
from Constants import DELTA_T
from functools import cache

from Utils import neighbors


class CubeOfWater(BlackBody, VolumetricBody):
    # Thermal conductivity of water : https://en.wikipedia.org/wiki/List_of_thermal_conductivities
    thermal_conductivity: float = 0.5918  # [W m^-1 K^-1]
    # Specific heat capacity of water : https://en.wikipedia.org/wiki/Specific_heat_capacity
    specific_heat_capacity: float = 4184  # [J kg^-1 K^-1]

    @property
    @cache
    def thermal_diffusivity(self) -> float:
        """
        Thermal diffusivity of water : https://en.wikipedia.org/wiki/Thermal_diffusivity
        Is computed through thermal conductivity, density and specific heat capacity
        Tested 24/04/2021 and gives a very good result compared to the list
        :return:
        """
        return CubeOfWater.thermal_conductivity / (self.density * CubeOfWater.specific_heat_capacity)

    @property
    @cache
    def co2_diffusivity(self) -> float:
        """
        The ability of the CO2 to spread
        :return: a constant
        """
        return 0.00014

    @property
    @cache
    def density(self) -> float:
        return self.mass / self.volume

    index: int
    neighbors: list[CubeOfWater]

    def __init__(self, index: int, volume: float, mass: float, energy: float, co2_ppmv: float = 300):
        BlackBody.__init__(self, pow(volume, 2 / 3), mass, energy)
        VolumetricBody.__init__(self, pow(volume, 1 / 3), self.area)
        self.index = index
        self.co2_ppmv = co2_ppmv  # In Part Per Million Volume
        self.neighbors = []

    def __repr__(self):
        return str(f"Température : {round(self.temperature, 2)}, CO2 PPMV : {round(self.co2_ppmv, 2)}")

    def add_neighbor(self, neighbor: CubeOfWater):
        self.neighbors.append(neighbor)

    def tick(self):
        for neighbor in self.neighbors:
            self.average_temperature(neighbor)
            self.average_co2(neighbor)

    def average_temperature(self, other: CubeOfWater):
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

    def average_co2(self, other: CubeOfWater):
        diff = abs(other.co2_ppmv - self.co2_ppmv)
        rate_of_co2_change = self.co2_diffusivity * self.area * diff * DELTA_T
        rate_of_co2_change = rate_of_co2_change if self.co2_ppmv > other.co2_ppmv else -rate_of_co2_change

        self.co2_ppmv -= rate_of_co2_change
        other.co2_ppmv += rate_of_co2_change
