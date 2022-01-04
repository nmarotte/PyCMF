import math

from constants import TIME_DELTA
from models.model import Model


class Sun(Model):
    """
    Source for the amount of energy radiated by the sun towards earth each second :
    https://www.quora.com/How-many-joules-of-energy-would-be-generated-if-we-harnessed-only-one-tenth-of-the-solar-energy-striking-Earth-on-an-annual-basis
    """

    def update(self):
        """
        Update function for the Sun.

        Behavior :
            Updates the amount of energy contained in the sun
            Radiate that energy outward
        :return:
        """
        energy_per_time_delta = self.energy_radiated_per_second * TIME_DELTA
        self.parent.radiate_inside(energy_per_time_delta)
        self.tick()

    def __init__(self, total_energy: float = math.inf, energy_radiated_per_second: float = 3.8e26, *, parent=None):
        self.total_energy = total_energy
        self.energy_radiated_per_second = energy_radiated_per_second
        self.parent = parent

    def __str__(self):
        res = f"Sun :\n"
        if self.total_energy != math.inf:
            res += f"- Total energy remaining {self.total_energy} J\n"
        res += f"- Radiating {self.energy_radiated_per_second} J/s towards the earth"
        if self.parent is not None:
            res += f"\n- Located in {self.parent.__class__}"
        return res
