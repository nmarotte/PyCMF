from typing import Optional

from modelsv2.base_model import BaseModel
from modelsv2.physical_class.earth import Earth
from sun import Sun


class Universe(BaseModel):
    """
    Singleton class that will contain all other models
    """
    earth: Optional[Earth] = None
    sun: Optional[Sun] = None
    TIME_DELTA: float = 0.01
    EVAPORATION_RATE: float = 0.0001

    def __new__(cls, *args, **kwargs):
        if BaseModel.universe is None:
            BaseModel.universe = super(Universe, cls).__new__(cls, *args, **kwargs)
        return BaseModel.universe

    def __str__(self):
        res = ""
        if self.sun is not None:
            res += f"{self.sun.__str__()}\n"
        if self.earth is not None:
            res += f"{self.earth.__str__()}\n"
        return res

    # def update(self, *, skip_earth=False, skip_sun=False):
    #     if not skip_sun and self.sun is not None:
    #         self.sun.update()
    #     if not skip_earth and self.earth is not None:
    #         self.earth.update()
    #     self.tick()

    def start_updating(self):
        while True:
            if not self.running:
                break
            print(f"Simulating t={self.t}")
            self.update()
        print("Simulation stopped")

    # def radiate_inside(self, energy_per_time_delta: float, earth_radiation_ratio: float):
    #     self.earth.add_energy(energy_per_time_delta * earth_radiation_ratio * (1-self.earth.albedo))
    #
    # def radiate_towards_earth(self, energy: float):
    #     self.earth.receive_radiation(energy)

if __name__ == '__main__':
    uni = Universe()
    uni.update()

