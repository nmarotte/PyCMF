from abc import abstractmethod


class MassBody:
    mass: float  # [kg]
    energy: float  # [J]

    def __init__(self, mass: float, energy: float):
        self.mass = mass  # [kg]
        self.energy = energy  # [J]

    @property
    @abstractmethod
    def specific_heat_capacity(self) -> float:
        """
        The specific heat capacity of the material in Joules per Kelvin Kilogram

        This depends of the type of material, therefore it is a property of the Object and not the Class

        https://en.wikipedia.org/wiki/Heat_capacity#Specific_heat_capacity

        This unit gives us the ability to convert energy to temperature

        :return:
        """

    @property
    def temperature(self):
        """
        The temperature of the system computed via its energy
        Result unit : [K]
        Energy Unit : [J] = [kg m^2 s^-2]
        Calculation :
        [K] = [J] / [J K^-1 kg^-1] * [kg]
                    ^^^^^^^^^^^^^
                    specific heat
                    capacity
        :return:
        """
        return self.energy / (self.specific_heat_capacity * self.mass)  # [K] = [J / ((J K^-1 kg^-1) * kg)]

    @temperature.setter
    def temperature(self, new_t):
        """
        Adds the value to the current temperature and recompute the energy
        :param new_t: the new temperature
        :return:
        """
        self.energy = new_t * self.specific_heat_capacity * self.mass  # [J] = [K] * [J K^-1 kg^-1] * [kg]
