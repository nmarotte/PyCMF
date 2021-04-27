from __future__ import annotations

from abc import abstractmethod

from ABC.AreaBody import AreaBody
from Constants import DELTA_T


class Temperated(AreaBody):
    thermal_conductivity: float  # [W m^-1 K^-1]
    specific_heat_capacity: float  # [J kg^-1 K^-1]

    def __init__(self, temperature: float, area: float):
        super().__init__(area)
        self.temperature = temperature

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
