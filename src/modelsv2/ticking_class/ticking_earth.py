import math

from modelsv2.ABC.ticking_model import TickingModel
from modelsv2.physical_class.earth import Earth


class TickingEarth(Earth, TickingModel):
    def __init__(self, shape: tuple, radius: float = 6.3781e6, *, parent=None):
        Earth.__init__(self, shape, radius, parent=parent)
        TickingModel.__init__(self)

    @TickingModel.on_tick
    def average_temperature(self):
        temperature_gradiant = {}
        # First sweep of finding the temperature difference
        for elem in self.not_nones():
            for neighbour in elem.neighbours:
                if neighbour.index < elem.index or math.isclose(neighbour.temperature - elem.temperature, 0):
                    continue  # Already computed the other way around
                temperature_gradiant[(elem.index, neighbour.index)] = neighbour.temperature - elem.temperature
        # Second sweep to apply the difference
        for elem in self.not_nones():
            for neighbour in elem.neighbours:
                if neighbour.index < elem.index or (elem.index, neighbour.index) not in temperature_gradiant:
                    continue  # Already computed the other way around
                energy_exchanged = temperature_gradiant[(elem.index, neighbour.index)] * elem.heat_transfer_coefficient * self.get_universe().TIME_DELTA / elem.surface
                elem.add_energy(energy_exchanged * elem.specific_heat_capacity)
                neighbour.add_energy(-energy_exchanged * elem.specific_heat_capacity)
