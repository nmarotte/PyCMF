from models.Earth.Components.chunk_component import ChunkComponent
from models.Earth.Components.grid_chunk import GridChunk
from models.Earth.grid import Grid
from modelsv2.base_class.earth_base import EarthBase
from modelsv2.base_model import BaseModel
from src.universe import Universe


class Earth(EarthBase, BaseModel):
    albedo: float = 0

    # @classmethod
    # def from_qimage(cls, qimage: QtGui.QImage, temperatures: list[float], masses: list[float]):
    #     res = cls(shape=(qimage.size().width(), qimage.size().height()))
    #     for y in range(qimage.size().height()):
    #         for x in range(qimage.size().width()):
    #             if qimage.pixelColor(x, y) == QtGui.QColor("black"):
    #                 continue
    #             ratios = ComponentColor.DICT[qimage.pixelColor(x, y).rgb()]
    #             components = []
    #             if not math.isclose(ratios[0], 0):
    #                 components.append(
    #                     ChunkComponent(component_type="WATER", mass=masses[0] * ratios[0], temperature=temperatures[0]))
    #             if not math.isclose(ratios[1], 0):
    #                 components.append(
    #                     ChunkComponent(component_type="AIR", mass=masses[1] * ratios[1], temperature=temperatures[1]))
    #             if not math.isclose(ratios[2], 0):
    #                 components.append(
    #                     ChunkComponent(component_type="LAND", mass=masses[1] * ratios[2], temperature=temperatures[2]))
    #             chunk = GridChunk(components=components, volume=1, parent=res,
    #                               index=x + y * res.shape[1])
    #             res.set_component_at(chunk, x, y)
    #     return res
    #
    # def to_qimage(self):
    #     image = QtGui.QImage(*CANVAS_SIZE, QtGui.QImage.Format_RGB32)
    #     for i, elem in enumerate(self):
    #         if elem is None:
    #             color = QtGui.QColor("black")
    #         else:
    #             color = color_from_ratio(elem.get_mass_ratio())
    #         image.setPixel(*index_to_2D(i, CANVAS_SIZE), color.rgb())
    #     return image

    @property
    def average_temperature(self) -> float:
        return sum(x.temperature for x in self.not_nones()) / max(1, self.nb_active_grid_chunks)

    @property
    def total_mass(self):
        return sum(x.total_mass for x in self.not_nones())

    @property
    def composition(self):
        composition_mass_dict = dict()
        total_mass = self.total_mass
        chunk: GridChunk
        for chunk in self.not_nones():
            for component in chunk:
                composition_mass_dict[component.type] = composition_mass_dict.get(component.type, 0) + component.mass / total_mass

        return composition_mass_dict

    def __str__(self):
        res = f"Earth : \n" \
              f"- Mass {self.total_mass}\n" \
              f"- Average temperature: {self.average_temperature}\n" \
              f"- Composition: \n\t{f'{chr(10) + chr(9)} '.join(str(round(value * 100, 2)) + '% ' + key for key, value in self.composition.items())}"
        return res

    def add_energy(self, input_energy: float):
        """
        Distribute energy on all the components of the planet uniformly
        :param input_energy:
        :return:
        """
        energy_each = input_energy / (self.nb_active_grid_chunks or 1)
        if energy_each:
            for elem in self.not_nones():
                elem.energy += energy_each

    def receive_radiation(self, energy: float):
        self.add_energy(energy * (1 - self.albedo))


if __name__ == '__main__':
    uni = Universe()
    earth = Earth(shape=(10,10))
    earth.universe = uni
    earth[0] = GridChunk([ChunkComponent(1000, 300, component_type="WATER")], volume=1000, index=0, parent=earth)
    earth[1] = GridChunk([ChunkComponent(1000, 250, component_type="WATER")], volume=1000, index=1, parent=earth)
    earth.update()
    print(earth[0])
    print(earth[1])