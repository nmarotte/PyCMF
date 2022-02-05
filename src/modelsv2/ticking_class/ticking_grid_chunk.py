from collections.abc import Collection

from models.Earth.Components.chunk_component import ChunkComponent
from modelsv2.tickable_model import TickableModel
from modelsv2.physical_class.grid_chunk import GridChunk


class TickingGridChunk(TickableModel, GridChunk):
    def __init__(self, components: Collection[ChunkComponent], volume: float, *, index: int = None, parent=None):
        GridChunk.__init__(self, components, volume, index=index, parent=parent)
        TickableModel.__init__(self)

    @TickableModel.on_tick
    def water_evaporation(self):
        if self.water_component is None:
            return
        evaporated_mass = self.universe.EVAPORATION_RATE * self.universe.TIME_DELTA * self.water_component.mass
        self.water_component.mass -= evaporated_mass
        if self.air_component is None:
            self.air_component = ChunkComponent(evaporated_mass, self.temperature, "AIR")
        else:
            self.air_component.mass += evaporated_mass
