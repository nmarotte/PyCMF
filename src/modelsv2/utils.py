from dataclasses import dataclass

from modelsv2.ABC.celestial_body import CelestialBody


@dataclass
class EnergyRadiation:
    """Class for keeping track of an item in inventory."""
    source: CelestialBody
    amount_per_time_delta: float
