import numpy as np

from ABC.Ticked import Ticked
from Objects.CubeOfWater import CubeOfWater
from Utils import neighbors


class WaterComponent(Ticked):
    volume_each = 1000
    mass_each = 1000
    energy_each_start = 1255200000
    co2_ppmv_each_start = 300

    def __init__(self, shape: tuple = (25, 25, 25), t_stop: int = 300):
        super().__init__(t_stop)
        flat_shape = np.product(shape)
        self.components = np.empty(flat_shape, dtype=CubeOfWater)

        volumes = np.full(flat_shape, fill_value=WaterComponent.volume_each)
        masses = np.full(flat_shape, fill_value=WaterComponent.mass_each)
        energies = np.random.normal(WaterComponent.energy_each_start, 104600000, flat_shape)
        co2_ppmvs = np.random.normal(WaterComponent.co2_ppmv_each_start, 25, flat_shape)

        for i in range(len(self.components)):
            self.components[i] = CubeOfWater(i, volumes[i], masses[i], energies[i], co2_ppmvs[i])
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
