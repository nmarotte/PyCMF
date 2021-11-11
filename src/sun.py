import math

from constants import TIME_DELTA
from units import Energy, Unit


class Sun:
    """
    Source for the amount of energy radiated by the sun towards earth each second :
    https://www.quora.com/How-many-joules-of-energy-would-be-generated-if-we-harnessed-only-one-tenth-of-the-solar-energy-striking-Earth-on-an-annual-basis
    """
    def __init__(self, total_energy: Energy = Energy(joules=math.inf), energy_radiated_per_second: float = 1.3e17, *, parent=None):
        self.total_energy = total_energy
        self.energy_radiated_per_second = energy_radiated_per_second  # Energy radiated towards the earth ! Not total amount radiated by the sun
        self.parent = parent

    def radiate(self):
        """
        Energy radiated per TIME_DELTA towards the Earth
        :return:
        """
        energy_per_time_delta = self.energy_radiated_per_second * TIME_DELTA
        self.total_energy -= energy_per_time_delta
        return energy_per_time_delta

    def compute_step(self) -> dict[str, Unit]:
        """
        The change that has to be applied to the sun at each step
        energy : the amount of energy to be removed from the sun and added to the objects being radiated by the sun
        :return:
        """
        return {"energy": self.energy_radiated_per_second * TIME_DELTA}

    def apply_step(self, deltas: dict[str, Unit]):
        """
        What happens to the sun at each time step, it doesn't do anything on the sun since its changed are not
        relevant on such small time scales

        :param deltas: dict containing the energy to remove from the sun
        :return:
        """
        return NotImplemented

    def update(self) -> dict[str, Unit]:
        deltas = self.compute_step()
        self.apply_step(deltas)
        return deltas
