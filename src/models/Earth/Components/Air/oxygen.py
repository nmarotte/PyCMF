from models.Earth.Components.grid_component import GridComponent


class Oxygen(GridComponent):
    specific_heat_capacity = 918  # J/kgC
    heat_transfer_coefficient = NotImplemented  # W/m^2K Not Found
    ratio: float = 1.0
