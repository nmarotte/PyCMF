from typing import Optional

from Earth.grid import Grid
from Earth.Components.water import Water
from constants import TIME_DELTA, STEFAN_BOLTZMANN
from units import Energy, Mass, Volume, Temperature, Unit, Area


class Earth(Grid):
    __mass: Optional[Mass]
    __temperature: Optional[Temperature]
    __surface: Optional[Area]

    def __init__(self, shape: tuple, surface: Area = Area(meters2=510.1e9), *, parent=None):
        super().__init__(shape, parent=parent)
        for i in range(len(self)):
            self[i] = Water(mass=Mass(kilograms=1000), volume=Volume(meters3=1), temperature=Temperature(celsius=21), parent=self, index=i)
        self.__mass = None
        self.__temperature = None
        self.__surface = surface

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

    def black_body_radiate(self):
        heat = STEFAN_BOLTZMANN * self.temperature**4 * self.__surface * TIME_DELTA
        print(heat, self.__temperature)
        self.__temperature -= heat
        return heat

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

    def update(self):
        self.black_body_radiate()
        super(Earth, self).update()
