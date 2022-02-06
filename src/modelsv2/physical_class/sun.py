import math

from modelsv2.ABC.celestial_body import CelestialBody
from modelsv2.base_class.sun_base import SunBase


class Sun(SunBase, CelestialBody):
    def receive_radiation(self, energy: float):
        raise NotImplementedError("No behaviour set for the Sun receiving radiation")

    # def update(self):
    #     """
    #     Update function for the Sun.
    #
    #     Behavior :
    #         Updates the amount of energy contained in the sun
    #         Radiate that energy outward
    #     :return:
    #     """
    #     energy_per_time_delta = self.energy_radiated_per_second * self.universe.TIME_DELTA
    #     self.universe.radiate_towards_earth(energy_per_time_delta * self.earth_radiation_ratio)
    #     self.tick()

    def __init__(self, total_energy: float = math.inf, energy_radiated_per_second: float = 3.8e26,
                 earth_radiation_ratio: float = 00000002.87e-7, radius: float = 6.957e8):
        self.total_energy = total_energy
        self.energy_radiated_per_second = energy_radiated_per_second
        self.earth_radiation_ratio = earth_radiation_ratio  # https://socratic.org/questions/how-much-of-the-total-energy-that-leaves-the-sun-makes-it-to-earth-why
        CelestialBody.__init__(self, radius)
        self.get_universe().sun = self

    def __str__(self):
        res = f"Sun :\n"
        if self.total_energy != math.inf:
            res += f"- Total energy remaining {self.total_energy} J\n"
        else:
            res += f"- Infinite amount of energy"
        res += f"- Radiating {self.energy_radiated_per_second} J/s outwards"
        res += f"- Of which {100*self.earth_radiation_ratio} % will reach the earth"
        return res

