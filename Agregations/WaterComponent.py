import math

import numpy as np

from ABC.Ticked import Ticked
from ABC.ComponentAggregation import ComponentAggregation
from Objects.CubeOfWater import CubeOfWater
from Utils import neighbors_single


class WaterComponent(ComponentAggregation, Ticked):
    """
    This class could subclass np.ndarray but since it doesn't __init__, it is very complicated to make it work alongside
    Ticked
    """

    def __init__(self, shape: tuple, t_stop: int, data=None):
        Ticked.__init__(self, t_stop)
        ComponentAggregation.__init__(self, shape)
        if data is not None:
            self.components = data

    @classmethod
    def empty_component(cls, shape, t_stop):
        return cls(shape, t_stop)

    @classmethod
    def full_component(cls, shape: tuple, t_stop: int, density_each: float = 1024, co2_ppmv_each: float = 345):
        flat = math.prod(shape)
        mass_each = ComponentAggregation.volume_each * density_each
        temperatures = np.random.normal(WaterComponent.temperature_each_start, 25, flat)
        co2_ppmvs = np.random.normal(co2_ppmv_each, 25, flat)
        components = np.empty(flat, dtype=CubeOfWater)

        for i in range(len(components)):
            components[i] = CubeOfWater(i, WaterComponent.volume_each, mass_each, temperatures[i], co2_ppmvs[i])
            for j in neighbors_single(i, shape):
                components[j].add_neighbor(components[i])
                components[i].add_neighbor(components[j])

        return cls(shape, t_stop, data=components)
