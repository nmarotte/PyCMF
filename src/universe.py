from typing import Optional

from tqdm import tqdm

from Earth.earth import Earth
from constants import TIME_DELTA
from sun import Sun
from units import Temperature, Mass, Volume


class Universe:
    earth: Optional[Earth] = None
    sun: Optional[Sun] = None

    def __str__(self):
        res = ""
        if self.sun is not None:
            res += f"{self.sun.__str__()}\n"
        if self.earth is not None:
            res += f"{self.earth.__str__()}\n"
        return res

    def update(self, *, skip_earth=False, skip_sun=False):
        radiation = None
        if not skip_sun and self.sun is not None:
            radiation = self.sun.radiate()
        if not skip_earth and self.earth is not None:
            self.earth.update()
            if radiation:
                self.earth.add_energy(radiation)


if __name__ == '__main__':
    """
    """
    uni = Universe()
    uni.earth = Earth((10, 10, 10), parent=uni)
    uni.earth.add_water(Mass(kilograms=1.4e21), Volume(meters3=1.4e21), Temperature(celsius=21))
    uni.sun = Sun(parent=uni)
    print(uni.earth.average_temperature)
    for i in tqdm(range(int(1//TIME_DELTA))):  # Computes for one second of physical time
        uni.update()
    print(uni.earth.average_temperature)