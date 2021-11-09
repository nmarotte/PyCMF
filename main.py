from random import random
from time import time_ns

from Earth.grid import Grid
from Earth.Components.water import Water
from units import *

class Boat:
    displacement_tonnage: float
    weight: float
    length: float
    capacity: float
    objects_on_board: list[object]

    def load(self, objects: object):
        pass

    def unload(self) -> list[object]:
        pass

    def anchor(self):
        pass

    def set_sail(self):
        pass

if __name__ == '__main__':
    grid = Grid((10, 10, 10))
    for i in range(len(grid)):
        grid[i] = Water(temperature=Temperature(celsius=21*random()), parent=grid, index=i)
    for i in range(100):
        start = time_ns() / (10 ** 9)
        grid.update()
        # print(f"Updating {len(grid)} water temperature, took {time_ns() / (10 ** 9) - start} seconds")
    for elem in grid:
        print(elem.temperature)