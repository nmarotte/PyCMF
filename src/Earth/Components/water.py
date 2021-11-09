from constants import TIME_DELTA
from units import *

from Earth.Components.grid_component import GridComponent


class Water(GridComponent):
    specific_heat_capacity = 4200  # J/kgC

    def get_diff(self, other: GridComponent) -> dict[str, float]:
        """
        Computes and returns the difference between the physical attributes of two GridComponent
        :param other: the other GridComponent to inspect
        :param time_scale:
        :return:
        """
        return {
            "temperature": (other.temperature - self.temperature),
            "volume": (other.volume - self.volume),
            "mass": (other.mass - self.mass),
        }

    def compute_step(self) -> list[dict[str, float]]:
        return [self.get_diff(n) for n in self.parent.neighbours(self.index)]

    def update(self, time_scale=TIME_DELTA):
        for n in self._neighbours:
            diff = self.get_diff(n)
            self.temperature += time_scale * diff["temperature"]/2
            n.temperature -= time_scale * diff["temperature"]/2

    def add_energy(self, input_energy: Energy):
        self.temperature += input_energy / (self.specific_heat_capacity * self.mass)


if __name__ == '__main__':
    water1 = Water(temperature=Temperature(kelvin=300), parent=None)
    water2 = Water(temperature=Temperature(kelvin=320), parent=None)
    water2._neighbours.append(water1)
    water1._neighbours.append(water2)
    print(water1.temperature)
    for i in range(200000):
        water1.update(time_scale=0.001)
        print(water1.temperature)
