from __future__ import annotations

from functools import cache

from ABC.CubeOfMaterial import CubeOfMaterial
from Constants import DELTA_T


class CubeOfWater(CubeOfMaterial):
    # Thermal conductivity of water : https://en.wikipedia.org/wiki/List_of_thermal_conductivities
    thermal_conductivity: float = 0.5918  # [W m^-1 K^-1]
    # Specific heat capacity of water : https://en.wikipedia.org/wiki/Specific_heat_capacity
    specific_heat_capacity: float = 4184  # [J kg^-1 K^-1]
    # TODO CO2 diffusivity of Water : ???
    co2_diffusivity = 0.00014

    def __init__(self, index: int, volume: float, mass: float, temperature: float, co2_ppmv: float = 300):
        CubeOfMaterial.__init__(self, index, volume, mass, temperature)
        self.co2_ppmv = co2_ppmv  # In Part Per Million Volume

    def tick(self):
        for neighbor in self.neighbors:
            self.average_temperature(neighbor)
            self.average_co2(neighbor)

    def average_co2(self, other: CubeOfWater):
        diff = abs(other.co2_ppmv - self.co2_ppmv)
        rate_of_co2_change = CubeOfWater.co2_diffusivity * self.area * diff * DELTA_T
        rate_of_co2_change = rate_of_co2_change if self.co2_ppmv > other.co2_ppmv else -rate_of_co2_change

        self.co2_ppmv -= rate_of_co2_change
        other.co2_ppmv += rate_of_co2_change
