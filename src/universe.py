from random import random
from typing import Optional
from tqdm import tqdm

from Earth import Earth
from Water import Water
from constants import TIME_DELTA
from sun import Sun
from units import Temperature, Mass, Volume


class Universe:
    def __init__(self):
        self.earth: Optional[Earth] = None
        self.sun: Optional[Sun] = None

    def update(self, *, skip_earth=False, skip_sun=False):
        if not skip_earth and self.earth:
            self.earth.update()
        if not skip_sun and self.sun:
            input_energy = self.sun.radiate()
            self.earth.add_energy(input_energy)


if __name__ == '__main__':
    """
    """
    uni = Universe()
    uni.earth = Earth((10, 10, 10), parent=uni)
    uni.earth.add_water(Mass(kilograms=1.4e21), Volume(meters3=1.4e21), Temperature(celsius=21))
    uni.sun = Sun(parent=uni)
    print(uni.earth.compute_average_temperature())
    for i in tqdm(range(int(1//TIME_DELTA))):  # Computes for one second of physical time
        uni.update()
    print(uni.earth.compute_average_temperature())
