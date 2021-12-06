from models.Earth.Components.grid_component import GridComponent


class Water(GridComponent):
    specific_heat_capacity = 4184  # J/kgC see bibliography
    heat_transfer_coefficient = 1000  # W/m^2K
    ratio: float
