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
                elem.temperature += temperature_gradiant[(elem.index, neighbour.index)] * self.get_universe().TIME_DELTA
                neighbour.temperature -= temperature_gradiant[(elem.index, neighbour.index)] * self.get_universe().TIME_DELTA
