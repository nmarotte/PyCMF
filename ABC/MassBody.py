from abc import abstractmethod


class MassBody:
    mass: float  # [kg]
    temperature: float  # [K]
    specific_heat_capacity: float  # [j/(kg*K)]

    def __init__(self, mass: float, temperature: float):
        self.mass = mass  # [kg]
        self.temperature = temperature  # [K]

    @property
    @abstractmethod
    def specific_heat_capacity(self) -> float:
        """
        The specific heat capacity of the material in Joules per Kelvin Kilogram
        https://en.wikipedia.org/wiki/Heat_capacity#Specific_heat_capacity
        :return:
        """

    def remove_energy(self, energy):
        temperature_loss = energy / (self.specific_heat_capacity * self.mass)  # [K] = [J / ((J K^-1 kg^-1) * kg)] = [K]
        self.temperature -= temperature_loss

    def add_energy(self, energy):
        temperature_gain = energy / (self.specific_heat_capacity * self.mass)  # [K] = [J / ((J K^-1 kg^-1) * kg)] = [K]
        self.temperature += temperature_gain
