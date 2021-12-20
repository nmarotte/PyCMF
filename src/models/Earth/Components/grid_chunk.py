import math
from typing import Union, Optional

from constants import TIME_DELTA
from models.Earth.Components.chunk_component import ChunkComponent
from units import Volume, Temperature, Energy, Mass, Unit, Area


class GridChunk(list[ChunkComponent]):
    specific_heat_capacity: float
    heat_transfer_coefficient: float
    __energy: Energy = None
    total_mass: Mass
    __volume: Volume
    surface: Area

    ratios: dict[str, float] = None

    def __init__(self, components: list[ChunkComponent], volume: Volume, *, index: int = None, parent=None):
        super(GridChunk, self).__init__()
        self.parent = parent
        self.index = index if index is not None else self.parent and self.parent.index(self)

        # If ratio contains some zeros, we remove them from the components, and remove from the ratio
        self.total_mass = sum(c.mass for c in components)
        for i, x in enumerate(components):
            if not math.isclose(x.mass/self.total_mass, 0):
                x.chunk = self
                self.append(x)
        self.ratios = {c.component_type: c.mass/self.mass for c in self}
        self.volume = volume
        self.__neighbours = None

        if len(self):
            self.specific_heat_capacity = sum(x.specific_heat_capacity * self.ratios[x.component_type] for i, x in enumerate(self))/len(self)
            self.heat_transfer_coefficient = sum(x.heat_transfer_coefficient * self.ratios[x.component_type] for i, x in enumerate(self))/len(self)

    def compute_component_ratio_dict(self):
        return {component.component_type: ratio for component, ratio in zip(self, self.ratios)}

    def get_masses(self):
        return {component.component_type: component.mass for component in self}

    def __str__(self):
        res = f"Chunk" + (f" {str(self.index)}\n" if self.index is not None else "\n")
        res += f"- Composition: "
        for component in self:
            res += f"{self.ratios[component.component_type] * 100}% {component.component_type}, "
        res = res[:-2] + "."
        return res

    @property
    def neighbours(self):
        if self.__neighbours is None:
            self.__neighbours = self.parent.neighbours(self.index)
        return self.__neighbours

    @neighbours.setter
    def neighbours(self, value: list["GridChunk"]):
        self.__neighbours = value

    @property
    def volume(self):
        return self.__volume

    @volume.setter
    def volume(self, value: Union[float, Volume]):
        self.__volume = value if isinstance(value, Volume) else Volume(meters3=value)
        self.surface = Area(meters2=(self.__volume ** (1 / 3)) ** 2)

    @property
    def mass(self):
        return self.total_mass

    @mass.setter
    def mass(self, value: Union[float, Mass]):
        for i, component in enumerate(self):
            component.mass = value * self.ratios[component.component_type]

    @property
    def temperature(self) -> Temperature:
        return sum(Temperature(kelvin=c.energy / (c.specific_heat_capacity * c.mass)) for c in self)/len(self)

    @temperature.setter
    def temperature(self, value: Temperature):
        for component in self:
            component.energy = Energy(joules=component.specific_heat_capacity * component.mass * value)

    @property
    def energy(self) -> Energy:
        return sum(c.energy * self.ratios[c.component_type] for c in self)

    @energy.setter
    def energy(self, value: Union[float, Energy]):
        for component in self:
            component.energy = value * self.ratios[component.component_type]

    def get_diff(self, other: "GridChunk") -> Optional[dict[str, Unit]]:
        """
        Computes and returns the difference between the physical attributes of two GridComponent
        :param other: the other GridComponent to inspect
        :return:
        """
        if other is None:
            return None
        return {
            "temperature": (other.temperature - self.temperature),
            "volume": (other.volume - self.volume),
            "mass": (other.mass - self.mass),
        }

    def update(self):
        joule_per_time_scale = self.heat_transfer_coefficient * self.surface * TIME_DELTA
        for n in self.neighbours:
            diff = self.get_diff(n)
            if diff:
                self.energy += joule_per_time_scale * diff["temperature"] * TIME_DELTA
                n.energy -= joule_per_time_scale * diff["temperature"] * TIME_DELTA


if __name__ == '__main__':
    water_mass = 1000
    air_mass = 1.29
    components = [
        ChunkComponent(mass=Mass(kilograms=water_mass), temperature=Temperature(celsius=21),
                       component_type="WATER"),
        ChunkComponent(mass=Mass(kilograms=air_mass),
                       temperature=Temperature(celsius=21),
                       component_type="AIR")
        ]
    chunk = GridChunk(components, volume=Volume(meters3=1))
    print(chunk)
    print(chunk[0])
    print(chunk[1])

    chunk[0].mass -= 500
    print("\n", chunk)
    print(chunk[0])
    print(chunk[1])

    chunk[0].mass += 500
    chunk[0].change_mass(chunk[0].mass - 500)
    print("\n", chunk)
    print(chunk[0])
    print(chunk[1])
    print("-----------")

    chunk[0].change_mass(chunk[0].mass + 500)
    print(chunk.temperature)
    chunk.temperature = Temperature(kelvin=50)
    print(chunk.temperature)
