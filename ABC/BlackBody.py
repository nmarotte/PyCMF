from abc import abstractmethod, ABC

from ABC.MassBody import MassBody
from Constants import DELTA_T


class BlackBody(MassBody, ABC):
    # https://en.wikipedia.org/wiki/Black_body#Radiative_cooling
    stefan_boltzmann_constant: float = 5.67 * 10 ** (-8)  # [W m^2 K^4]
    area: float

    def __init__(self, area: float, mass: float, temperature: float, parent_system=None):
        super().__init__(mass, temperature)
        self.parent_system = None
        self.area = area

    def tick(self):
        self.radiate_to(self.parent_system)

    def radiate_to(self, parent_system):
        power = BlackBody.stefan_boltzmann_constant * self.temperature * self.area  # [W] = [J s^-1] = [kg m^2 s^-3]
        energy = power * DELTA_T  # [J] = [W] * [s] = [kg m^2 s^-3] * [s] = [kg m^2 s^-2]
        self.remove_energy(energy)
        parent_system.add_energy(energy)
