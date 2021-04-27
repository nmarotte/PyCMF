from ABC.CubeOfMaterial import CubeOfMaterial


class CubeOfSoil(CubeOfMaterial):
    # Thermal conductivity of Soil : https://www.researchgate.net/publication/297856519_Soil_Thermal_Conductivity_Effects_of_Density_Moisture_Salt_Concentration_and_Organic_Matter
    thermal_conductivity: float = 0.5  # [W m^-1 K^-1]
    # Specific Heat Capacity of Soil : https://www.e-education.psu.edu/earth103/node/1005
    specific_heat_capacity: float = 830  # [J kg^-1 K^-1]

    @property
    def thermal_diffusivity(self) -> float:
        return CubeOfSoil.thermal_conductivity / (self.density * CubeOfSoil.specific_heat_capacity)

    def __init__(self, index: int, volume: float, mass: float, energy: float):
        CubeOfMaterial.__init__(self, index, volume, mass, energy)

    def tick(self):
        for neighbor in self.neighbors:
            self.average_temperature(neighbor)
