import math

from models.Earth.Components.chunk_component import ChunkComponent
from models.Earth.Components.grid_chunk import GridChunk
from models.Earth.grid import Grid
from units import Energy, Mass, Volume, Temperature
import PyQt5.QtGui as QtGui


class Earth(Grid):
    def __init__(self, shape: tuple, *, parent=None):
        super().__init__(shape, parent=parent)

    @classmethod
    def from_qimage(cls, qimage: QtGui.QImage, color_dict_ratio: dict[int, list[float]]):
        res = cls(shape=(qimage.size().width(), qimage.size().height()))
        for y in range(qimage.size().height()):
            for x in range(qimage.size().width()):
                if qimage.pixelColor(x,y) == QtGui.QColor("black"):
                    continue
                color = qimage.pixelColor(x, y)
                ratio = color_dict_ratio[color.rgb()]
                components = []
                if ratio[0]:
                    components.append(ChunkComponent(component_type="Water", mass=Mass(kilograms=1000), temperature=Temperature(celsius=21)))
                if ratio[1]:
                    components.append(ChunkComponent(component_type="Air", mass=Mass(kilograms=1.29), temperature=Temperature(celsius=21)))
                if ratio[2]:
                    components.append(ChunkComponent(component_type="Land", mass=Mass(kilograms=1700), temperature=Temperature(celsius=21)))
                chunk = GridChunk(components=components,
                                  ratios=[x for x in ratio if x], volume=Volume(meters3=1), parent=res, index=x+y*qimage.size().width())
                res.set_component_at(chunk, x, y)
        return res

    @property
    def total_mass(self) -> Mass:
        return Mass(kilograms=sum(x.mass for x in self if x is not None))

    @property
    def average_temperature(self) -> Temperature:
        count = 0
        temperature = 0
        for x in self.not_nones():
            count += 1
            temperature += x.temperature
        return Temperature(kelvin=(temperature/count) if count else 0)

    @property
    def composition(self):
        composition_mass_dict = dict()
        total_mass = self.total_mass
        for chunk in self.not_nones():
            for component_type, mass in chunk.get_masses().items():
                composition_mass_dict[component_type] = composition_mass_dict.get(component_type, 0) + mass/total_mass

        return composition_mass_dict

    def __str__(self):
        res = f"""Earth : 
- Mass {self.total_mass}
- Average temperature: {self.average_temperature}
- Composition: {' '.join(str(round(value * 100, 2)) + "% " + key for key, value in self.composition.items())}"""
        return res

    def add_energy(self, input_energy: Energy):
        """
        Distribute energy on all the components of the planet uniformly
        :param input_energy:
        :return:
        """
        energy_each = input_energy / len(self)
        for elem in self:
            if elem is not None:
                elem.energy += energy_each

    def add_water(self, total_mass: Mass, total_volume: Volume, temperature: Temperature):
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
