from abc import ABC, abstractmethod

from ABC.MassBody import MassBody


class Star(MassBody, ABC):
    @property
    @abstractmethod
    def specific_heat_capacity(self) -> float:
        """
        Not sure if this will be necessary
        Composition of the sun : https://solarsystem.nasa.gov/solar-system/sun/in-depth/
        Heat capacity per element : https://en.wikipedia.org/wiki/Heat_capacities_of_the_elements_(data_page)
        :return:
        """
