from typing import Collection, Union

from modelsv2.physical_class.chunk_component import ChunkComponent
from modelsv2.base_class.grid_chunk_base import GridChunkBase


class GridChunk(GridChunkBase):
    """
    The physical properties aspect of the GridChunk
    """
    specific_heat_capacity: float
    heat_transfer_coefficient: float
    total_mass: float  # [kg]
    volume: float  # [m3]

    neighbours: list["GridChunk"]

    def __init__(self, components: Collection[ChunkComponent], volume: float, *, index: int = None, parent=None):
        self.volume = volume
        GridChunkBase.__init__(self, components, index=index, parent=parent)

        if not len(self):
            return  # Do not compute specific heat capacity of empty Grid Chunk
        self.specific_heat_capacity = sum(
            component.specific_heat_capacity * self.get_ratio_of_component(component.type)
            for i, component in enumerate(self)) / len(self)

        self.heat_transfer_coefficient = sum(
            component.heat_transfer_coefficient * self.get_ratio_of_component(component.type)
            for i, component in enumerate(self)) / len(self)

    def __str__(self):
        res = f"Chunk" + (f" {str(self.index)}\n" if self.index is not None else "\n") + \
              f"Temperature {self.temperature}°C\n" + \
              f"Mass {self.total_mass}kg\n" + \
              f"Composition (mass ratio)\n"
        for component in self:
            res += f"{round(self.get_ratio_of_component(component) * 100, 2)}% {component.type}\n"
        return res

    def get_ratio_of_component(self, component_type: Union[ChunkComponent, str]):
        if isinstance(component_type, ChunkComponent):
            component_type = component_type.type
        return self[component_type].mass / self.total_mass

    def get_mass_ratio(self):
        return {c.type: c.mass / self.total_mass for c in self}

    @property
    def total_mass(self):
        return sum(component.mass for component in self)

    @property
    def surface(self) -> float:
        # Assuming the chunk is cubic
        # TODO link proof that the limit of the difference between the surface of a cube compared to the surface of a sphere of equivalent radius goes to 0
        # TODO write that the program becomes more and more accurate the smaller the grid chunks are in volume
        return (self.volume ** (1 / 3)) ** 2

    @property
    def temperature(self) -> float:
        return sum(c.energy / (c.specific_heat_capacity * c.mass) for c in self) / max(1, len(self))

    @temperature.setter
    def temperature(self, value: float):
        for component in self:
            component.energy = component.specific_heat_capacity * component.mass * value

    @property
    def energy(self) -> float:
        return sum(c.energy for c in self)

    @energy.setter
    def energy(self, value: float):
        for component in self:
            component.energy = value * self.get_ratio_of_component(component)

    #
    # def update(self):
    #     joule_per_time_scale = self.heat_transfer_coefficient * self.surface * self.universe.TIME_DELTA
    #     for n in self.neighbours:
    #         diff = n.temperature - self.temperature
    #         if diff:
    #             self.add_energy(joule_per_time_scale * diff * self.universe.TIME_DELTA)
    #             n.add_energy(-joule_per_time_scale * diff * self.universe.TIME_DELTA)
    #     self.tick()

    def deep_copy(self, new_index=None, new_parent=None) -> "GridChunk":
        return GridChunk(tuple(component.deep_copy() for component in self),
                         self.volume, index=new_index, parent=new_parent)

    def add_energy(self, value: float):
        for component in self:
            component.energy += value * self.get_ratio_of_component(component)

    @classmethod
    def from_components_tuple(cls, *args: tuple[float, float, str], volume: float, index: int = None, parent=None):
        """
        A quick way of building a GridChunk without having to build the ChunkComponents manually
        :param args: a tuple of the form (mass: float, temperature: float, component_type: str)
        :param volume: volume of the GridChunk
        :param index: its index
        :param parent: its parent
        :return: the instantiated GridChunk object
        """
        return cls(tuple(ChunkComponent(mass=tp[0], temperature=tp[1], component_type=tp[2]) for tp in args),
                   volume, index=index, parent=parent)
