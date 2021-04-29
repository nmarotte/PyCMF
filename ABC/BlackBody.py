from abc import ABC

from ABC.Temperated import Temperated
from Constants import DELTA_T


class BlackBody(Temperated, ABC):
    # https://en.wikipedia.org/wiki/Black_body#Radiative_cooling
    stefan_boltzmann_constant: float = 5.67 * 10 ** (-8)  # [W m^2 K^4]

    def __init__(self, mass: float, area: float, temperature: float, parent_system=None):
        Temperated.__init__(self, mass, area, temperature)
        self.parent_system = parent_system

    def tick(self):
        self.radiate_to(self.parent_system)

    def radiate_to(self, parent_system):
        # todo https://en.wikipedia.org/wiki/Black-body_radiation#:~:text=The%20law%20was%20formulated%20by,is%20the%20Stefan%E2%80%93Boltzmann%20constant.
        power = BlackBody.stefan_boltzmann_constant * (self.temperature**4) * self.area  # [W] = [J s^-1] = [kg m^2 s^-3]
        energy = power * DELTA_T  # [J] = [W] * [s] = [kg m^2 s^-3] * [s] = [kg m^2 s^-2]
        self.energy -= energy
        parent_system.energy += energy
