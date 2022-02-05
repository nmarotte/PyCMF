import unittest

from modelsv2.ticking_class.ticking_grid_chunk import TickingGridChunk
from modelsv2.universe import Universe


class TestTickingGridChunkBase(unittest.TestCase):
    def setUp(self):
        self.universe = Universe()

    def test_water_evaporation_no_air(self):
        water_chunk = TickingGridChunk.from_components_tuple((1000, 300, "Water"), volume=1)
        before_water_mass = water_chunk.water_component.mass
        water_chunk.update()
        evaporated_water = before_water_mass * self.universe.TIME_DELTA * self.universe.EVAPORATION_RATE
        self.assertEqual(water_chunk.water_component.mass, before_water_mass - evaporated_water)
        self.assertIsNotNone(water_chunk.air_component)

    def test_water_evaporation_with_air(self):
        water_air_chunk = TickingGridChunk.from_components_tuple((1000, 300, "Water"), (128, 300, "Air"), volume=1)
        before_water_mass = water_air_chunk.water_component.mass
        before_air_mass = water_air_chunk.air_component.mass

        water_air_chunk.update()

        evaporated_water = before_water_mass * self.universe.TIME_DELTA * self.universe.EVAPORATION_RATE

        self.assertEqual(water_air_chunk.water_component.mass, before_water_mass - evaporated_water)
        self.assertEqual(water_air_chunk.air_component.mass, before_air_mass + evaporated_water)


if __name__ == '__main__':
    unittest.main()
