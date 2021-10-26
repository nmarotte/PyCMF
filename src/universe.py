from random import random
from typing import Optional

from Earth import Earth
from Water import Water
from constants import TIME_DELTA
from sun import Sun
from units import Temperature, Mass


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
    If we assume that the earth has 10 * 10 * 10 * 1000000000000000000 = 1e21 kilograms of water, each second that the 
    sun shines on earth, we have
    """
    uni = Universe()
    earth = Earth((10, 10, 10), parent=uni)
    for i in range(len(earth)):
        earth[i] = Water(mass=Mass(kilograms=1000000000000000000), temperature=Temperature(celsius=21 * random()), parent=earth, index=i)
    uni.earth = earth
    uni.sun = Sun(parent=uni)
    print(earth.compute_average_temperature())
    for i in range(int(1//TIME_DELTA)):
        uni.update()
    print(earth.compute_average_temperature())