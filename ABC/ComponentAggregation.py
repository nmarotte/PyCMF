import numpy as np
from abc import ABC


class ComponentAggregation(ABC):
    # All cells will start at 300 K
    # With a volume of 1000 m^3 (1 000 000 litres)
    temperature_each_start = 300
    volume_each = 0.001

    def __init__(self, shape: tuple):
        flat_shape = np.product(shape)
        self.components = np.empty(flat_shape, dtype=self.__class__)
        self.shape = shape

    def tick(self):
        for wc in self.components:
            wc.tick()

    @property
    def flat(self):
        return self.components.flat

    def __iter__(self):
        return self.components.__iter__()
