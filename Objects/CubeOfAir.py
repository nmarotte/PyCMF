from ABC.CubeOfMaterial import CubeOfMaterial


class AirComposition(dict):
    def __init__(self, **kwargs):
        super().__init__()
        self['N'] = 0.7803
        self['O'] = 0.21
        self['Ar'] = 0.0093
        self['CO2'] = 0.0004
        self.update(kwargs)


class CubeOfAir(CubeOfMaterial):
    # Thermal conductivity of Air https://en.wikipedia.org/wiki/List_of_thermal_conductivities
    # /!\ TODO : this could be made more accurate by being dependant of the composition of the atsmosphere
    thermal_conductivity = 0.025  # [W m^-1 K^-1]
    specific_heat_capacity = 1000.35  # [J kg^-1 K^-1]

    def __init__(self, index: int, volume: float, mass: float, temperature: float):
        CubeOfMaterial.__init__(self, index, volume, mass, temperature)
        self.composition = AirComposition()

    def tick(self):
        self.average_temperature(self.neighbors)
