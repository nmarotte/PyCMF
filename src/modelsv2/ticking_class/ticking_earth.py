from modelsv2.ABC.ticking_model import TickingModel
from modelsv2.physical_class.earth import Earth


class TickingEarth(Earth, TickingModel):
    @TickingModel.on_tick
    def average_temperature(self):
        temperature_gradiant = {}
        # First sweep of finding the temperature difference
        for elem in self.not_nones():
            for neighbour in elem.neighbours:
                if neighbour.index < elem.index:
                    continue  # Already computed the other way around
                temperature_gradiant[(elem.index, neighbour.index)] = neighbour.temperature - elem.temperature
        # Second sweep to apply the difference
        for elem in self.not_nones():
            for neighbour in elem.neighbours:
                if neighbour.index < elem.index:
                    continue  # Already computed the other way around
                energy_exchanged = temperature_gradiant[(elem.index, neighbour.index)] * elem.heat_transfer_coefficient * self.get_universe().TIME_DELTA / elem.surface
                elem.energy += energy_exchanged * elem.specific_heat_capacity
                neighbour.energy -= energy_exchanged * elem.specific_heat_capacity
