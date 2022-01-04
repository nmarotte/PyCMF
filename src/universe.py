from typing import Optional

from tqdm import tqdm

from models.Earth.earth import Earth
from constants import TIME_DELTA, CANVAS_SIZE
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
        if not skip_sun and self.sun is not None:
            self.sun.update()
        if not skip_earth and self.earth is not None:
            self.earth.update()
        self.tick()

    def start_updating(self):
        while True:
            if not self.running:
                break
            print(f"Simulating t={self.t}")
            self.update()
        print("Simulation stopped")

    def get_component_at(self, x: int, y: int, z: int = None):
        return self.earth.get_component_at(x, y, z)

    def radiate_inside(self, energy_per_time_delta: float):
        self.earth.add_energy(energy_per_time_delta * 00000002.87e-7 * (1-self.earth.albedo))


if __name__ == '__main__':
    """
    """
    uni = Universe()
    uni.earth = Earth(shape=CANVAS_SIZE, parent=uni)
    uni.sun = Sun(parent=uni)
    print(uni.earth.average_temperature)
    for i in tqdm(range(int(600*1//TIME_DELTA))):  # Computes for one second of physical time
        uni.update()
    print(uni.earth.average_temperature)