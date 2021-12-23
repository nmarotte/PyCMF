from typing import Optional

from tqdm import tqdm

from models.Earth.earth import Earth
from constants import TIME_DELTA
from models.model import Model
from sun import Sun


class Universe(Model):
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
        self.t += 1

    def setup(self, shape=(10, 10, 10)):
        self.earth = Earth(shape, parent=self)
        # self.earth.add_water(Mass(kilograms=1.4e21), Volume(meters3=1.4e21), Temperature(celsius=21))
        self.sun = Sun(parent=self)

    def start_updating(self):
        while True:
            if not self.running:
                break
            print(f"Simulating t={self.t}")
            self.update()
        print("done")

    def get_component_at(self, x: int, y: int, z: int = None):
        return self.earth.get_component_at(x, y, z)



if __name__ == '__main__':
    """
    """
    uni = Universe()
    uni.setup()
    print(uni.earth.average_temperature)
    for i in tqdm(range(int(600*1//TIME_DELTA))):  # Computes for one second of physical time
        uni.update()
    print(uni.earth.average_temperature)