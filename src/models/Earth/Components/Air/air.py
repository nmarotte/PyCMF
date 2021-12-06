from models.Earth.Components.Air.argon import Argon
from models.Earth.Components.Air.nitrogen import Nitrogen
from models.Earth.Components.Air.oxygen import Oxygen
from models.Earth.Components.grid_component import GridComponent
from models.Earth.Components.water import Water
from units import Volume, Mass, Temperature


class Air(GridComponent):
    specific_heat_capacity = 1012  # J/kgC see bibliography
    heat_transfer_coefficient = 12.5  # W/m^2K
    oxygen: Oxygen
    nitrogen: Nitrogen
    argon: Argon

    def __init__(self, volume: Volume, mass: Mass, temperature: Temperature, *, composition: list[float] = None, ratio=1.0, parent=None, index: int = None):
        super(Air, self).__init__(volume, mass, temperature, ratio=1.0, parent=parent, index=index)
        if composition is None:
            composition = [0.21, 0.78, 0.01]
        if composition[0]:
            self.oxygen = Oxygen(mass=mass/composition[0], temperature=temperature, volume=volume, ratio=composition[0])
        if composition[1]:
            self.nitrogen = Nitrogen(mass=mass/composition[0], temperature=temperature, volume=volume, ratio=composition[1])
        if composition[2]:
            self.argon = Argon(mass=mass/composition[0], temperature=temperature, volume=volume, ratio=composition[2])
