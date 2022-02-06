import unittest

from modelsv2.physical_class.grid_chunk import GridChunk
from modelsv2.ticking_class.ticking_earth import TickingEarth


class TestTickingEarth(unittest.TestCase):
    def setUp(self):
        self.earth = TickingEarth(shape=(10, 10))
        self.earth[0] = GridChunk.from_components_tuple((1000, 300, "WATER"), volume=1000, index=0, parent=self.earth)
        self.earth[1] = GridChunk.from_components_tuple((1000, 250, "WATER"), volume=1000, index=1, parent=self.earth)

    def test_temperature_balance(self):
        temperature_before = [x.temperature for x in self.earth.not_nones()]
        difference = (self.earth[1].temperature - self.earth[0].temperature) * self.earth.get_universe().TIME_DELTA
        self.earth.update()
        self.assertEqual([x.temperature for x in self.earth.not_nones()],
                         [temperature_before[0] + difference, temperature_before[1] - difference])

    def test_temperature_balance_fail(self):
        temperature_before = [x.temperature for x in self.earth.not_nones()]
        difference = (self.earth[1].temperature - self.earth[0].temperature) * self.earth.get_universe().TIME_DELTA
        self.earth.update()
        self.assertNotEqual([x.temperature for x in self.earth.not_nones()],
                            [temperature_before[0] + 3 * difference, temperature_before[1] - difference])
