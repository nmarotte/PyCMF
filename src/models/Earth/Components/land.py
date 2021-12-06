from models.Earth.Components.grid_component import GridComponent


class Land(GridComponent):
    specific_heat_capacity = 830  # J/kgC see bibliography
    heat_transfer_coefficient = 250  # W/m^2K inventing numbers
    ratio: float
