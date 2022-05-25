from models.ABC.celestial_body import CelestialBody
from models.base_class.earth_base import EarthBase
from models.physical_class.grid_chunk import GridChunk


class Earth(EarthBase, CelestialBody):
    """
    Second layer of the Earth model.
    In this layer are all the physical properties and functions of the Earth implemented. It is here that we will add
    new model variables
    """
    albedo: float = 0.3
    CARBON_EMISSIONS_PER_TIME_DELTA: float = 1_000_000  # ppm

    def __init__(self, shape: tuple, radius: float = 6.3781e6, *, parent=None):
        EarthBase.__init__(self, shape, parent=parent)
        CelestialBody.__init__(self,
                               radius)  # The default radius of the earth was found here https://arxiv.org/abs/1510.07674
        self.get_universe().earth = self
        self.get_universe().discover_everything()

    @property
    def average_temperature(self) -> float:
        return sum(x.temperature for x in self.not_nones()) / max(1, self.nb_active_grid_chunks)

    @property
    def total_mass(self):
        return sum(x.total_mass for x in self.not_nones())

    @property
    def composition(self):
        composition_mass_dict = dict()
        total_mass = self.total_mass
        chunk: GridChunk
        for chunk in self.not_nones():
            for component in chunk:
                composition_mass_dict[component.type] = composition_mass_dict.get(component.type,
                                                                                  0) + component.mass / total_mass

        return composition_mass_dict

    @property
    def carbon_flux_to_ocean(self):
        """
        The amount of carbon absorbed at every TIME_DELTA by all the ocean
        :return:
        """
        return 100_000

    @property
    def land_carbon_decay(self):
        """
        The amount of carbon released at every TIME_DELTA due to all the biomass decaying
        :return:
        """
        return 330_000

    @property
    def biosphere_carbon_absorption(self):
        """
        The amount of carbon absorbed at every TIME_DELTA due to all the biomass growing
        :return:
        """
        return 300_000

    def __str__(self):
        res = f"Earth : \n" \
              f"- Mass {self.total_mass}\n" \
              f"- Average temperature: {self.compute_average_temperature()}\n" \
              f"- Composition: \n\t{f'{chr(10) + chr(9)} '.join(str(round(value * 100, 2)) + '% ' + key for key, value in self.composition.items())}"
        return res

    def add_energy(self, input_energy: float):
        """
        Distribute energy on all the components of the planet uniformly
        :param input_energy:
        :return:
        """
        energy_each = input_energy / (self.nb_active_grid_chunks or 1)
        if energy_each:
            for elem in self.not_nones():
                elem.add_energy(energy_each)

    def compute_total_energy(self):
        return sum(elem.energy for elem in self.not_nones())

    def receive_radiation(self, energy: float):
        self.add_energy(energy * (1 - self.albedo))

    def compute_average_temperature(self):
        return sum(x.temperature for x in self.not_nones()) / max(1, self.nb_active_grid_chunks)
