from constants import TIME_DELTA
from units import *

from Earth.Components.grid_component import GridComponent


class Water(GridComponent):
    specific_heat_capacity = 4200  # J/kgC
    heat_transfer_coefficient = 1000  # W/m^2K

    def get_diff(self, other: GridComponent) -> dict[str, Unit]:
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

    def compute_step(self) -> list[dict[str, Unit]]:
        return [self.get_diff(n) for n in self.parent.neighbours(self.index)]

    def apply_step(self, deltas: list[dict[str, Unit]]):
        joule_per_time_scale = Energy(joules=self.heat_transfer_coefficient * self.surface * TIME_DELTA)
        for i, n in enumerate(self.neighbours):
            self.add_energy(joule_per_time_scale * deltas[i]["temperature"])
            n.add_energy(-joule_per_time_scale * deltas[i]["temperature"])

    def update(self):
        joule_per_time_scale = Energy(joules=self.heat_transfer_coefficient * self.surface * TIME_DELTA)
        for n in self.neighbours:
            diff = self.get_diff(n)
            self.add_energy(joule_per_time_scale * diff["temperature"])
            n.add_energy(-joule_per_time_scale * diff["temperature"])

    def add_energy(self, input_energy: Energy):
        self.temperature += input_energy / (self.specific_heat_capacity * self.mass)


if __name__ == '__main__':
    water1 = Water(temperature=Temperature(kelvin=300), parent=None)
    water2 = Water(temperature=Temperature(kelvin=320), parent=None)
    water2._neighbours.append(water1)
    water1._neighbours.append(water2)
    print(water1.temperature)
    for i in range(60):
        water1.update()
        print(water1.temperature)
