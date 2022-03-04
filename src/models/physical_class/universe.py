import math
from typing import TYPE_CHECKING

from models.ABC.ticking_model import TickingModel
from models.physical_class.sun import Sun

if TYPE_CHECKING:
    from models.ABC.celestial_body import CelestialBody
from models.base_class.universe_base import UniverseBase
from models.physical_class.earth import Earth


class Universe(UniverseBase, TickingModel):
    """
    Singleton class that will contain all other models
    """
    TIME_DELTA: float = 0.01
    EVAPORATION_RATE: float = 0.0001

    def __init__(self):
        super().__init__()

    def __str__(self):
        res = ""
        if self.sun is not None:
            res += f"{self.sun.__str__()}\n"
        if self.earth is not None:
            res += f"{self.earth.__str__()}\n"
        return res

    def discover_everything(self):
        """
        Exchange 1 virtual photon with every celestial body contained in the universe so that we can know if they can
        see each other in a direct line of sight or not
        :return:
        """
        for obj1 in self:
            for obj2 in self:
                if obj1 is obj2 or obj1 is None or obj2 is None:
                    continue
                obj1.discover(obj2)

    def get_component_at(self, x: int, y=0, z=0):
        return self.earth.get_component_at(x, y, z)

    @staticmethod
    def radiate_inside(energy_radiation_per_time_delta: float, *, source: "CelestialBody"):
        for celestial_body in source.objects_in_line_of_sight:
            solid_angle = source.solid_angle(celestial_body)
            celestial_body.receive_radiation(energy_radiation_per_time_delta * solid_angle / (4 * math.pi))

    @staticmethod
    def distance_between(object1: "CelestialBody", object2: "CelestialBody"):
        if isinstance(object1, Sun) and isinstance(object2, Earth) or isinstance(object1, Earth) and isinstance(object2, Sun):
            return 1.496e11

    def update_all(self):
        for elem in self:
            elem.update()
        self.update()

    def __update_loop(self):
        while True:
            if not self.__running:
                break
            print(f"Simulating t={self._t}")
            self.update_all()
        print("done")

    def start_simulation(self):
        self.__running = True
        self.__update_loop()

    def stop_updating(self):
        self.__running = False

    def resume_updating(self):
        self.__running = True
        self.__update_loop()

    def pause_updating(self):
        self.__running = False
