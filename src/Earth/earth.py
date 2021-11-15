from typing import Optional

from Earth.grid import Grid
from Earth.Components.water import Water
from units import Energy, Mass, Volume, Temperature


class Earth(Grid):
    __mass: Optional[Mass]
    __temperature: Optional[Temperature]

    def __init__(self, shape: tuple, *, parent=None):
        super().__init__(shape, parent=parent)
        for i in range(len(self)):
            self[i] = Water(mass=Mass(), volume=Volume(), temperature=Temperature(), parent=self, index=i)
        self.__mass = None
        self.__temperature = None

    @property
    def mass(self) -> Mass:
        if self.__mass is None:
            self.__mass = Mass(kilograms=sum(x.mass for x in self))
        return self.__mass

    @mass.setter
    def mass(self, value):
        self.__mass = value

    @property
    def temperature(self) -> Temperature:
        if self.__temperature is None:
            self.__temperature = Temperature(celsius=sum(x.temperature for x in self)/len(self))
        return self.__temperature

    @temperature.setter
    def temperature(self, value):
        self.__temperature = value
        
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
- Mass {self.__mass}
- Average temperature: {self.temperature}
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
            elem.add_energy(energy_each)

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
