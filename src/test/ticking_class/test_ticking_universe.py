import math
import random
import unittest

from modelsv2.physical_class.universe import Universe
from modelsv2.ticking_class.ticking_earth import TickingEarth
from modelsv2.ticking_class.ticking_grid_chunk import TickingGridChunk
from modelsv2.ticking_class.ticking_sun import TickingSun


class TestTickingUniverse(unittest.TestCase):
    pass

    # def test_universe_profiling(self):
    #     # Uncomment to profile the update loop for around 70s
    #     earth = TickingEarth(shape=(40, 40))
    #     for i in range(40*40):
    #         earth[i] = TickingGridChunk.from_components_tuple((1000, random.randint(273, 300), "WATER"), volume=1, index=0, parent=earth)
    #     sun = TickingSun()
    #     for i in range(500):
    #         sun.get_universe().update_all()
