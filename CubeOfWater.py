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
    def density(self) -> float:
        return self.mass / self.volume

    index: int
    neighbors: list[CubeOfWater]
    co2_diffusivity: float = 1  # TODO Find a value

    def __init__(self, index: int, volume: float, mass: float, temperature: float, co2_ppmv: float = 300):
        BlackBody.__init__(self, pow(volume, 2 / 3), mass, temperature)
        VolumetricBody.__init__(self, pow(volume, 1 / 3), self.area)
        self.index = index
        self.co2_ppmv = co2_ppmv  # In Part Per Million Volume
        self.neighbors = []

    def __repr__(self):
        return str(f"Température : {round(self.temperature, 2)}, CO2 PPMV : {round(self.co2_ppmv, 2)}")

    @staticmethod
    def generate_as_shape(shape: tuple):
        flat_shape = np.product(shape)
        volumes = np.full(flat_shape, fill_value=1000)
        masses = np.full(flat_shape, fill_value=1000)
        temperatures = np.random.normal(300, 25, flat_shape)
        co2_ppmvs = np.random.normal(300, 25, flat_shape)
        res = np.empty(flat_shape, dtype=CubeOfWater)
        for i in range(len(res)):
            res[i] = CubeOfWater(i, volumes[i], masses[i], temperatures[i], co2_ppmvs[i])
            for j in neighbors(i, shape):
                res[j].add_neighbor(res[i])
                res[i].add_neighbor(res[j])
        res.reshape(shape)
        # for i in range(shape[0]):
        #     for j in range(shape[1]):
        #         for k in range(shape[2]):
        #             index = i * shape[0] * shape[1] + j * shape[2] + k
        #
        #             wb = CubeOfWater(index, volumes[i,j,k], masses[i,j,k], temperatures[i,j,k], co2_ppmvs[i,j,k])
        #             if i > 0:
        #                 wb.add_neighbor(res[i - 1, j, k])
        #                 res[i - 1, j, k].add_neighbor(wb)
        #             if j > 0:
        #                 wb.add_neighbor(res[i, j - 1, k])
        #                 res[i, j - 1, k].add_neighbor(wb)
        #             if k > 0:
        #                 wb.add_neighbor(res[i, j, k - 1])
        #                 res[i, j, k - 1].add_neighbor(wb)
        #             res[i, j, k] = wb
        return res

    def add_neighbor(self, neighbor: CubeOfWater):
        self.neighbors.append(neighbor)

    def tick(self):
        for neighbor in self.neighbors:
            self.average_temperature(neighbor)
            self.average_co2(neighbor)

    def average_temperature(self, other: CubeOfWater):
        diff = abs(other.temperature - self.temperature)
        rate_of_t_change = self.thermal_diffusivity * self.area * diff * DELTA_T
        rate_of_t_change = rate_of_t_change if self.temperature > other.temperature else -rate_of_t_change
        self.temperature -= rate_of_t_change
        other.temperature += rate_of_t_change

    def average_co2(self, other: CubeOfWater):
        diff = abs(other.co2_ppmv - self.co2_ppmv)
        rate_of_co2_change = CubeOfWater.co2_diffusivity * self.area * diff * DELTA_T
        rate_of_co2_change = rate_of_co2_change if self.co2_ppmv > other.co2_ppmv else -rate_of_co2_change

        self.co2_ppmv -= rate_of_co2_change
        other.co2_ppmv += rate_of_co2_change
