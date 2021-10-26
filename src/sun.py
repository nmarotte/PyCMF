import math

from constants import TIME_DELTA
from units import Energy


class Sun:
    """
    Source for the amount of energy radiated by the sun towards earth each second :
    https://www.quora.com/How-many-joules-of-energy-would-be-generated-if-we-harnessed-only-one-tenth-of-the-solar-energy-striking-Earth-on-an-annual-basis
    """
    def __init__(self, total_energy: Energy = Energy(joules=math.inf), energy_radiated_per_second: float = 1.3e17, *, parent=None):
        self.total_energy = total_energy
        self.energy_radiated_per_second = energy_radiated_per_second
        self.parent = parent

    def radiate(self):
        """
        Energy radiated per TIME_DELTA towards the Earth
        :return:
        """
        energy_per_time_delta = self.energy_radiated_per_second * TIME_DELTA
        self.total_energy -= energy_per_time_delta
        return energy_per_time_delta
