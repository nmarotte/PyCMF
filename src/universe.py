from typing import Optional

from tqdm import tqdm

from Earth.earth import Earth
from constants import TIME_DELTA
from sun import Sun
from units import Temperature, Mass, Volume


class Universe:
    def __init__(self):
        self.earth: Optional[Earth] = None
        self.sun: Optional[Sun] = None

    def __str__(self):
        res = ""
        if self.sun is not None:
            res += f"{self.sun.__str__()}\n"
        if self.earth is not None:
            res += f"{self.earth.__str__()}\n"
        return res

    def compute_step(self, *, skip_earth=False, skip_sun=False):
        deltas = {"earth": None, "sun": None}
        if not skip_earth and self.earth:
            deltas["earth"] = self.earth.compute_step()
        if not skip_sun and self.sun:
            deltas["sun"] = self.sun.compute_step()
        return deltas

    def apply_step(self, deltas, *, skip_earth=False, skip_sun=False):
        if not skip_earth and self.earth:
            self.earth.apply_step(deltas["earth"])
        if not skip_sun and self.sun:
            self.sun.apply_step(deltas["sun"])
            self.earth.add_energy(deltas["sun"]["energy"])

    def update(self, *, skip_earth=False, skip_sun=False):
        deltas = self.compute_step(skip_earth=skip_earth, skip_sun=skip_sun)
        self.apply_step(deltas, skip_earth=skip_earth, skip_sun=skip_sun)


if __name__ == '__main__':
    """
    """
    uni = Universe()
    uni.earth = Earth((10, 10, 10), parent=uni)
    uni.earth.add_water(Mass(kilograms=1.4e21), Volume(meters3=1.4e21), Temperature(celsius=21))
    uni.sun = Sun(parent=uni)
    print(uni.earth.temperature)
    for i in tqdm(range(int(1//TIME_DELTA))):  # Computes for one second of physical time
        uni.update()
    print(uni.earth.temperature)