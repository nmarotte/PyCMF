from ABC.Star import Star


class Sun(Star):
    @property
    def specific_heat_capacity(self) -> float:
        """
        Composition of the sun : https://solarsystem.nasa.gov/solar-system/sun/in-depth/
        Heat capacity per element : https://en.wikipedia.org/wiki/Heat_capacities_of_the_elements_(data_page)
        :return: a constant
        """
        return 14304 * 0.706 + 5193 * 0.274
