from models.Earth.Components.chunk_component import ChunkComponent
from models.Earth.Components.grid_chunk import GridChunk
from models.Earth.grid import Grid
from modelsv2.base_model import BaseModel
from src.universe import Universe


class Earth(Grid, BaseModel):
    @BaseModel.on_tick
    def average_temperature(self):
        temperature_gradiant = {}
        # First sweep of finding the temperature difference
        for elem in self.not_nones():
            for neighbour in elem.neighbours:
                if neighbour.index < elem.index:
                    continue  # Already computed the other way around
                temperature_gradiant[(elem.index, neighbour.index)] = neighbour.temperature - elem.temperature
        # Second sweep to apply the difference
        for elem in self.not_nones():
            for neighbour in elem.neighbours:
                if neighbour.index < elem.index:
                    continue  # Already computed the other way around
                elem.temperature += temperature_gradiant[(elem.index, neighbour.index)] * self.universe.TIME_DELTA
                neighbour.temperature -= temperature_gradiant[(elem.index, neighbour.index)] * self.universe.TIME_DELTA


if __name__ == '__main__':
    uni = Universe()
    earth = Earth(shape=(10,10))
    earth.universe = uni
    earth[0] = GridChunk([ChunkComponent(1000, 300, component_type="WATER")], volume=1000, index=0, parent=earth)
    earth[1] = GridChunk([ChunkComponent(1000, 250, component_type="WATER")], volume=1000, index=1, parent=earth)
    earth.update()
    print(earth[0])
    print(earth[1])