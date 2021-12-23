import math
import random
from typing import Union, Iterable

import PyQt5.QtGui as QtGui

from constants import CANVAS_SIZE
from models.Earth.Components.chunk_component import ChunkComponent
from models.Earth.Components.grid_chunk import GridChunk
from models.Earth.grid import Grid
from other.utils import index_to_2D, color_from_ratio, ComponentColor, ChunkData


class Earth(Grid):
    total_temperature: float = 0

    def __init__(self, shape: tuple, *, parent=None):
        super().__init__(shape, parent=parent)

    def set_component_at(self, component: GridChunk, x, y, z=None):
        self.total_temperature += component.temperature
        super().set_component_at(component, x, y, z)

    @classmethod
    def from_qimage(cls, qimage: QtGui.QImage, chunk_data_stack: list[ChunkData]):
        res = cls(shape=(qimage.size().width(), qimage.size().height()))
        for y in range(qimage.size().height()):
            for x in range(qimage.size().width()):
                if qimage.pixelColor(x, y) == QtGui.QColor("black"):
                    continue
                ratio = ComponentColor.DICT[qimage.pixelColor(x, y).rgb()]
                chunk_data = [x for x in chunk_data_stack if x.ratios == ratio][0]
                components = []
                if not math.isclose(chunk_data["WATER"].ratio, 0):
                    components.append(ChunkComponent(component_type="WATER", mass=chunk_data["WATER"].mass * chunk_data["WATER"].ratio,
                                                     temperature=chunk_data["WATER"].temperature))
                if not math.isclose(chunk_data["AIR"].ratio, 0):
                    components.append(ChunkComponent(component_type="AIR", mass=chunk_data["AIR"].mass * chunk_data["AIR"].ratio,
                                                     temperature=chunk_data["AIR"].temperature))
                if not math.isclose(chunk_data["LAND"].ratio, 0):
                    components.append(ChunkComponent(component_type="LAND", mass=chunk_data["LAND"].mass * chunk_data["LAND"].ratio,
                                                     temperature=chunk_data["LAND"].temperature))
                chunk = GridChunk(components=components, volume=1, parent=res,
                                  index=x + y * qimage.size().width())
                res.set_component_at(chunk, x, y)
        return res

    def to_qimage(self):
        image = QtGui.QImage(*CANVAS_SIZE, QtGui.QImage.Format_RGB32)
        for i, elem in enumerate(self):
            if elem is None:
                color = QtGui.QColor("black")
            else:
                color = color_from_ratio(elem.compute_component_ratio_dict())
            image.setPixel(*index_to_2D(i, CANVAS_SIZE), color.rgb())
        return image

    @property
    def total_mass(self) -> float:
        return sum(x.total_mass for x in self if x is not None)

    @property
    def average_temperature(self) -> float:
        return (self.total_temperature/self.nb_active_grid_chunks) if self.nb_active_grid_chunks else 0

    @property
    def composition(self):
        composition_mass_dict = dict()
        total_mass = self.total_mass
        for chunk in self.not_nones():
            for component_type, mass in chunk.get_masses().items():
                composition_mass_dict[component_type] = composition_mass_dict.get(component_type, 0) + mass / total_mass

        return composition_mass_dict

    def __str__(self):
        res = f"""Earth : 
- Mass {self.total_mass}
- Average temperature: {self.average_temperature}
- Composition: \n\t{f'{chr(10) + chr(9)} '.join(str(round(value * 100, 2)) + "% " + key for key, value in self.composition.items())}"""
        return res

    def add_energy(self, input_energy: float):
        """
        Distribute energy on all the components of the planet uniformly
        :param input_energy:
        :return:
        """
        energy_each = input_energy / len(self)
        for elem in self:
            if elem is not None:
                elem.energy += energy_each

    def add_water(self, total_mass: float, total_volume: float, temperature: float):
        """
        Adds a certain mass and volume of water to the component with the given temperature
        :param total_mass:
        :param total_volume:
        :param temperature:
        :return:
        """
        mass_each = total_mass / len(self)
        volume_each = total_volume / len(self)
        for elem in self:
            elem.mass = mass_each.copy()
            elem.volume = volume_each.copy()
            elem.temperature = temperature.copy()


if __name__ == '__main__':
    earth = Earth(shape=(400, 400))
    water_component = ChunkComponent(mass=1000, temperature=300,component_type="WATER")
    air_component = ChunkComponent(mass=1.29, temperature=300, component_type="AIR")
    land_component = ChunkComponent(mass=1700, temperature=300,component_type="LAND")
    components = [water_component, air_component, land_component]
    empty_chance = 3
    for _ in range(16000):  # 10%
        earth[random.randint(0, 400 * 400 - 1)] = GridChunk(
            components=components,
            volume=1000)
    image = earth.to_qimage()
    image.save("test.png", "PNG", -1)
    print(ComponentColor.DICT.__sizeof__())
