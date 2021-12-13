import math
from typing import Union, Optional

from constants import TIME_DELTA
from models.Earth.Components.chunk_component import ChunkComponent
from units import Volume, Temperature, Energy, Mass, Unit, Area


class GridChunk(list[ChunkComponent]):
    specific_heat_capacity: float
    heat_transfer_coefficient: float
    __energy: Energy = None
    __mass: Mass
    __volume: Volume
    surface: Area

    __ratios: dict[str, float] = None

    def __init__(self, components: list[ChunkComponent], volume: Volume, *, ratios: dict[str, float] = None, index: int = None, parent=None):
        # If ratio contains some zeros, we remove them from the components, and remove from the ratio
        components = [x for i, x in enumerate(components) if not math.isclose(ratios[x.component_type], 0)]
        ratios = {key: x for key, x in ratios.items() if not math.isclose(x, 0)}
        super(GridChunk, self).__init__()
        self.__ratios = ratios
        self.extend(components)
        self.parent = parent
        self.index = index if index is not None else self.parent and self.parent.index(self)

        self.__mass = sum(c.mass for c in components)
        self.main_component = self.compute_main_component()
        self.volume = volume
        self.__neighbours = None

        if len(self):
            self.specific_heat_capacity = sum(x.specific_heat_capacity * self.ratios[x.component_type] for i, x in enumerate(self))/len(self)
            self.heat_transfer_coefficient = sum(x.heat_transfer_coefficient * self.ratios[x.component_type] for i, x in enumerate(self))/len(self)

    @property
    def ratios(self) -> dict[str, float]:
        if self.__ratios is None:
            self.__ratios = {c.component_type: c.mass/self.mass for c in self}
        return self.__ratios

    @ratios.setter
    def ratios(self, value: dict[str, float]):
        if len(value) != len(self):
            raise Exception(f"Cannot set {len(value)} ratios to a chunk with {len(self)} items")
        for component in self:
            temperature = component.temperature.copy()
            component.mass = (component.mass/self.ratios[component.component_type]) * value[component.component_type]
            component.temperature = temperature
        self.__ratios = value

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

    def compute_main_component(self):
        component = None
        max_ratio = 0
        for i, component in enumerate(self):
            if self.ratios[component.component_type] > max_ratio:
                component = component
                max_ratio = self.ratios[component.component_type]
        return component

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
        return self.__mass

    @mass.setter
    def mass(self, value: Union[float, Mass]):
        self.__mass = Mass(kilograms=0)
        for i, component in enumerate(self):
            component.mass = value * self.ratios[component.component_type]
            self.__mass += component.mass

    @property
    def temperature(self) -> Temperature:
        value = Temperature(kelvin=self.energy / (self.specific_heat_capacity * self.mass))
        return value

    @temperature.setter
    def temperature(self, value: Temperature):
        self.__energy = Energy(joules=self.specific_heat_capacity * self.mass * value)

    @property
    def energy(self) -> Energy:
        if self.__energy is None:
            self.__energy = sum(c.energy for c in self)
        return self.__energy

    @energy.setter
    def energy(self, value: Union[float, Energy]):
        self.__energy = Energy(joules=0)
        for component in self:
            component.energy = value * self.ratios[component.component_type]
            self.__energy += component.energy

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

    chunk.ratios = [0.5, 0.5]
    print("\n", chunk)
    print(chunk[0])
    print(chunk[1])
