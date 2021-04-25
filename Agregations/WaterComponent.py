import numpy as np

from ABC.Ticked import Ticked
from Objects.CubeOfWater import CubeOfWater
from Utils import neighbors


class WaterComponent(Ticked):
    """
    This class could subclass np.ndarray but since it doesn't __init__, it is very complicated to make it work alongside
    Ticked
    """
    volume_each = 1000
    mass_each = 1000
    energy_each_start = 1255200000
    co2_ppmv_each_start = 300

    def __init__(self, shape: tuple = (25, 25, 25), t_stop: int = 300):
        super().__init__(t_stop)
        flat_shape = np.product(shape)
        self.components = np.empty(flat_shape, dtype=CubeOfWater)

        energies = np.random.normal(WaterComponent.energy_each_start, 104600000, flat_shape)
        co2_ppmvs = np.random.normal(WaterComponent.co2_ppmv_each_start, 25, flat_shape)

        for i in range(len(self.components)):
            self.components[i] = CubeOfWater(i, WaterComponent.volume_each, WaterComponent.mass_each, energies[i], co2_ppmvs[i])
            for j in neighbors(i, shape):
                self.components[j].add_neighbor(self.components[i])
                self.components[i].add_neighbor(self.components[j])
        self.components.reshape(shape)

    def tick(self):
        for wc in self.components:
            wc.tick()
        self.one_tick_passed()

    @property
    def flat(self):
        return self.components.flat

    def __iter__(self):
        return self.components.__iter__()
