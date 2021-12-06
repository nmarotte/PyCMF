from models.Earth.Components.Air.air import Air
from models.Earth.Components.land import Land
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
    def from_qimage(cls, qimage: QtGui.QImage, air_color: QtGui.QColor, water_color: QtGui.QColor, land_color: QtGui.QColor):
        res = cls(shape=(qimage.size().width(), qimage.size().height()), populate=False)
        for y in range(qimage.size().height()):
            for x in range(qimage.size().width()):
                if qimage.pixelColor(x, y) == air_color:
                    component = Air.init_default(parent=res, index=x+y*qimage.size().width())
                elif qimage.pixelColor(x, y) == water_color:
                    component = Water.init_default(parent=res, index=x+y*qimage.size().width())
                elif qimage.pixelColor(x, y) == land_color:
                    component = Land.init_default(parent=res, index=x+y*qimage.size().width())
                else:
                    continue
                res.set_component_at(component, x, y)

        return res

    @property
    def total_mass(self) -> Mass:
        return Mass(kilograms=sum(x.mass for x in self if x is not None))

    @property
    def average_temperature(self) -> Temperature:
        count = 0
        temperature = 0
        for x in self:
            if x is not None:
                count += 1
                temperature += x.temperature
        return Temperature(kelvin=(temperature/count) if count else 0)
        
    @property
    def composition(self):
        water, air, land = 0, 0, 0
        rest = 0
        for elem in self:
            if isinstance(elem, Water):
                water += 1
            elif isinstance(elem, Air):
                air += 1
            elif isinstance(elem, Land):
                land += 1
            else:
                rest += 1
        return {"water": water/len(self),
                "air": air / len(self),
                "land": land / len(self),
                "rest": rest/len(self)}

    def __str__(self):
        composition = self.composition
        res = f"""Earth : 
- Mass {self.total_mass}
- Average temperature: {self.average_temperature}
- Composition: {composition['water'] * 100}% Water, {composition['air'] * 100}% Air, {composition['land'] * 100}% Land."""
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
