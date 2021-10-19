import math

import numpy as np

from ABC.ComponentAggregation import ComponentAggregation
from ABC.Ticked import Ticked
from Objects.CubeOfSoil import CubeOfSoil
from Utils import neighbors_single


class SoilComponent(ComponentAggregation, Ticked):
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
    def full_component(cls, shape: tuple, t_stop: int, density_each: float = 1700, temperature_each: float = 300):
        mass_each = ComponentAggregation.volume_each * density_each
        flat = math.prod(shape)
        temperatures = np.random.normal(temperature_each, 25, flat)
        components = np.empty(flat, dtype=CubeOfSoil)

        for i in range(len(components)):
            components[i] = CubeOfSoil(i, SoilComponent.volume_each, mass_each, temperatures[i])
            for j in neighbors_single(i, shape):
                components[j].add_neighbor(components[i])
                components[i].add_neighbor(components[j])

        return cls(shape, t_stop, data=components)