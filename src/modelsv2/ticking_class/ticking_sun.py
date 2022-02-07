from modelsv2.physical_class.sun import Sun
from modelsv2.ABC.ticking_model import TickingModel


class TickingSun(Sun, TickingModel):
    def __init__(self):
        Sun.__init__(self)
        TickingModel.__init__(self)

    @TickingModel.on_tick
    def radiate_energy_outwards(self):
        """
        Update function for the Sun.

        Behavior :
            Updates the amount of energy contained in the sun
            Radiate that energy outward
        :return:
        """
        energy_per_time_delta = self.energy_radiated_per_second * self.get_universe().TIME_DELTA
        self.get_universe().radiate_inside(energy_per_time_delta, source=self)
