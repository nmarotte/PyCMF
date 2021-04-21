from WaterBody import WaterBody


class Earth:
    def __init__(self, shape_water_component=(5, 5, 5)):
        self.water_bodies = WaterBody.generate_as_shape(shape_water_component)


if __name__ == '__main__':
    terre = Earth()
    print(terre.water_bodies)
    for i in range(1):
        for wb in terre.water_bodies.flat:
            wb.tick()

    print(terre.water_bodies)
