from models.Earth.Components.grid_component import GridComponent


class Argon(GridComponent):
    specific_heat_capacity = 520.3  # J/kgC
    heat_transfer_coefficient = NotImplemented  # W/m^2K Impossible to find
    ratio: float = 1.0
