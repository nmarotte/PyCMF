from Grid import Grid
from units import Energy


class Earth(Grid):
    def add_energy(self, input_energy: Energy):
        energy_each = input_energy/len(self)
        for elem in self:
            elem.add_energy(energy_each)

    def compute_average_temperature(self):
        total_temp = sum(elem.temperature for elem in self)
        return total_temp/len(self)
