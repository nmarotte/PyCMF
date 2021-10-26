from random import random
from time import time_ns

from Grid import Grid
from Water import Water
from units import *

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