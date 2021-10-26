from Grid import Grid
from Water import Water
from units import Energy, Mass, Volume, Temperature


class Earth(Grid):
    def __init__(self, shape: tuple, *, parent=None):
        super().__init__(shape, parent=parent)
        for i in range(len(self)):
            self[i] = Water(mass=Mass(), volume=Volume(), temperature=Temperature(), parent=self, index=i)

    def add_energy(self, input_energy: Energy):
        """
        Distribute energy on all the components of the planet uniformly
        :param input_energy:
        :return:
        """
        energy_each = input_energy / len(self)
        for elem in self:
            elem.add_energy(energy_each)

    def compute_average_temperature(self):
        total_temp = sum(elem.temperature for elem in self)
        return total_temp / len(self)

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
