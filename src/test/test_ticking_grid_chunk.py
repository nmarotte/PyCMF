import unittest

from models.Earth.Components.chunk_component import ChunkComponent
from modelsv2.ticking_class.ticking_grid_chunk import TickingGridChunk
from modelsv2.universe import Universe


class TestTickingGridChunkBase(unittest.TestCase):
    def setUp(self):
        self.universe = Universe()
        self.a_water_component = ChunkComponent(1000, 300, "Water")
        self.an_air_component = ChunkComponent(128, 300, "Air")
        self.a_land_component = ChunkComponent(1800, 300, "Land")

        self.water_chunk = TickingGridChunk([self.a_water_component], volume=1)
        self.water_air_chunk = TickingGridChunk([self.a_water_component, self.an_air_component], volume=1)

    def test_water_evaporation(self):
        before_water_mass = self.water_chunk.water_component.mass
        self.water_chunk.update()
        evaporated_water = before_water_mass * self.universe.TIME_DELTA * self.universe.EVAPORATION_RATE
        self.assertEqual(self.water_chunk.water_component.mass, before_water_mass - evaporated_water)


if __name__ == '__main__':
    unittest.main()
