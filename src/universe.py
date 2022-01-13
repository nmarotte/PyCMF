from typing import Optional, TYPE_CHECKING


from models.model import Model
if TYPE_CHECKING:
    from models.Earth.earth import Earth
    from sun import Sun


class Universe(Model):
    """
    Singleton class that will contain all other models
    """
    earth: Optional["Earth"] = None
    sun: Optional["Sun"] = None
    TIME_DELTA: float = 0.01

    def __new__(cls, *args, **kwargs):
        if Model.universe is None:
            Model.universe = super(Universe, cls).__new__(cls, *args, **kwargs)
        return Model.universe

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

    def radiate_inside(self, energy_per_time_delta: float, earth_radiation_ratio: float):
        self.earth.add_energy(energy_per_time_delta * earth_radiation_ratio * (1-self.earth.albedo))

    def radiate_towards_earth(self, energy: float):
        self.earth.receive_radiation(energy)
