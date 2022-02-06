from collections.abc import Collection

from models.Earth.Components.chunk_component import ChunkComponent
from modelsv2.ABC.ticking_model import TickingModel
from modelsv2.physical_class.grid_chunk import GridChunk
import modelsv2.physical_class.universe as universe


class TickingGridChunk(TickingModel, GridChunk):
    def __init__(self, components: Collection[ChunkComponent], volume: float, *, index: int = None, parent=None):
        GridChunk.__init__(self, components, volume, index=index, parent=parent)
        TickingModel.__init__(self)

    @TickingModel.on_tick
    def water_evaporation(self):
        if self.water_component is None:
            return
        evaporated_mass = universe.Universe.EVAPORATION_RATE * universe.Universe.TIME_DELTA * self.water_component.mass
        self.water_component.mass -= evaporated_mass
        if self.air_component is None:
            self.air_component = ChunkComponent(evaporated_mass, self.temperature, "AIR")
        else:
            self.air_component.mass += evaporated_mass
