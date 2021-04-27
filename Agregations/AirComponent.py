import numpy as np

from ABC.ComponentAggregation import ComponentAggregation
from ABC.Ticked import Ticked
from Objects.CubeOfAir import CubeOfAir
from Utils import neighbors


class AirComponent(ComponentAggregation, Ticked):
    """
        This class could subclass np.ndarray but since it doesn't __init__, it is very complicated to make it work alongside
        Ticked
        """
    density = 1.225  # [kg m^-3]
    mass_each = ComponentAggregation.volume_each * density
    co2_ppmv_each_start = 300

    def __init__(self, shape: tuple, t_stop: int):
        Ticked.__init__(self, t_stop)
        ComponentAggregation.__init__(self, shape)

        temperatures = np.random.normal(AirComponent.temperature_each_start, 25, len(self.flat))

        for i in range(len(self.components)):
            self.components[i] = CubeOfAir(i, AirComponent.volume_each, AirComponent.mass_each, temperatures[i])
            for j in neighbors(i, shape):
                self.components[j].add_neighbor(self.components[i])
                self.components[i].add_neighbor(self.components[j])
        self.components.reshape(shape)
