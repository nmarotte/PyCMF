import numpy as np

from ABC.Ticked import Ticked
from ABC.ComponentAggregation import ComponentAggregation
from Objects.CubeOfWater import CubeOfWater
from Utils import neighbors


class WaterComponent(ComponentAggregation, Ticked):
    """
    This class could subclass np.ndarray but since it doesn't __init__, it is very complicated to make it work alongside
    Ticked
    """

    def __init__(self, shape: tuple, t_stop: int, density_each:float = 999.7, co2_ppmv_each:float = 345):
        mass_each = ComponentAggregation.volume_each * density_each
        Ticked.__init__(self, t_stop)
        ComponentAggregation.__init__(self, shape)

        temperatures = np.random.normal(WaterComponent.temperature_each_start, 25, len(self.flat))
        co2_ppmvs = np.random.normal(co2_ppmv_each, 25, len(self.flat))

        for i in range(len(self.components)):
            self.components[i] = CubeOfWater(i, WaterComponent.volume_each, mass_each, temperatures[i], co2_ppmvs[i])
            for j in neighbors(i, shape):
                self.components[j].add_neighbor(self.components[i])
                self.components[i].add_neighbor(self.components[j])
        self.components.reshape(shape)

