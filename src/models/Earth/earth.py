from models.Earth.grid import Grid
from models.Earth.Components.water import Water
from constants import water_earth_volume, water_earth_mass
from units import Energy, Mass, Volume, Temperature
import PyQt5.QtGui as QtGui


class Earth(Grid):
    def __init__(self, shape: tuple, *, temperature=Temperature(celsius=21), populate=True, parent=None):
        super().__init__(shape, parent=parent)
        if populate:
            for i in range(len(self)):
                self[i] = Water(mass=water_earth_mass/len(self), volume=water_earth_volume/len(self), temperature=temperature, parent=self, index=i)

    @classmethod
    def from_qimage(cls, qimage: QtGui.QImage):
        return cls(shape=(qimage.size().width(), qimage.size().height()))

    @property
    def total_mass(self) -> Mass:
        return Mass(kilograms=sum(x.mass for x in self))

    @property
    def average_temperature(self) -> Temperature:
        return Temperature(kelvin=sum(x.temperature for x in self)/len(self))
        
    @property
    def composition(self):
        water = 0
        rest = 0
        for elem in self:
            if isinstance(elem, Water):
                water += 1
        return {"water": water/len(self), "rest": rest/len(self)}

    def __str__(self):
        res = f"""Earth : 
- Mass {self.total_mass}
- Average temperature: {self.average_temperature}
- Composition: {self.composition['water'] * 100}% Water"""
        return res

    def add_energy(self, input_energy: Energy):
        """
        Distribute energy on all the components of the planet uniformly
        :param input_energy:
        :return:
        """
        energy_each = input_energy / len(self)
        for elem in self:
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
