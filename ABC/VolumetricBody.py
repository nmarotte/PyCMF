from ABC.AreaBody import AreaBody


class VolumetricBody(AreaBody):
    volume: float  # [m^3]

    def __init__(self, depth: float, area: float):
        super().__init__(area)
        self.volume = depth * area  # [m^3] = [m] * [m^2]
