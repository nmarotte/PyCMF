import math
from models.Earth.Components.chunk_component import ChunkComponent
from models.model import Model


class GridChunk(list[ChunkComponent], Model):
    specific_heat_capacity: float
    heat_transfer_coefficient: float
    total_mass: float
    volume: float

    neighbours: list["GridChunk"]

    def __init__(self, components: list[ChunkComponent], volume: float, *, index: int = None, parent=None):
        super(GridChunk, self).__init__()
        self.parent = parent
        self.index = index if index is not None else self.parent.index(self) if self.parent is not None else None

        # If ratio contains some zeros, we remove them from the components, and remove from the ratio
        self.total_mass = sum(c.mass for c in components)
        for i, x in enumerate(components):
            if not math.isclose(x.mass / self.total_mass, 0):
                x.chunk = self
                self.append(x)
        self.volume = volume
        self.neighbours = self.parent.neighbours(self.index) if self.parent else None

        if len(self):
            self.specific_heat_capacity = sum(
                x.specific_heat_capacity * self.ratios[x.component_type] for i, x in enumerate(self)) / len(self)
            self.heat_transfer_coefficient = sum(
                x.heat_transfer_coefficient * self.ratios[x.component_type] for i, x in enumerate(self)) / len(self)

    def compute_component_ratio_dict(self):
        return {component.component_type: ratio for component, ratio in zip(self, self.ratios)}

    def __str__(self):
        res = f"Chunk" + (f" {str(self.index)}\n" if self.index is not None else "\n") + \
              f"Temperature {self.temperature}°C\n" + \
              f"Mass {self.total_mass}kg\n" + \
              f"Composition (mass ratio)\n"
        for component in self:
            res += f"{round(self.ratios[component.component_type] * 100, 2)}% {component.component_type}\n"
        return res

    @property
    def ratios(self) -> dict[str, float]:
        return {c.component_type: c.mass / self.total_mass for c in self}

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
            component.energy = value * self.ratios[component.component_type]

    def update(self):
        joule_per_time_scale = self.heat_transfer_coefficient * self.surface * self.universe.TIME_DELTA
        for n in self.neighbours:
            diff = n.temperature - self.temperature
            if diff:
                self.add_energy(joule_per_time_scale * diff * self.universe.TIME_DELTA)
                n.add_energy(-joule_per_time_scale * diff * self.universe.TIME_DELTA)
        self.tick()

    def deep_copy(self) -> "GridChunk":
        return GridChunk([x.deep_copy() for x in self], self.volume, index=self.index, parent=self.parent)

    def add_energy(self, value: float):
        for component in self:
            component.energy += value * self.ratios[component.component_type]


if __name__ == '__main__':
    water_mass = 1000
    air_mass = 1.29
    components = [
        ChunkComponent(mass=water_mass, temperature=300,
                       component_type="WATER"),
        ChunkComponent(mass=air_mass,
                       temperature=300,
                       component_type="AIR")
    ]
    chunk = GridChunk(components, volume=1)
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
    chunk.temperature = 50
    print(chunk.temperature)
