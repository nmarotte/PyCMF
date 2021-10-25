from random import random

from Grid import Grid
from Water import Water
from units import *

if __name__ == '__main__':
    grid = Grid((6, 6, 6))
    for i in range(len(grid)):
        grid[i] = Water(volume=Volume(meters3=100*random()), mass=Mass(kilograms=100*random()),
                        temperature=Temperature(celsius=-5+10*random()), parent=grid, index=i)
    # for elem in grid.by_row():
    #     print(elem.index, elem.temperature)

    averages = Water.average(grid.neighbours(0))
    print(grid[0].volume, grid[0].volume - averages[0])
    print(grid[0].mass, grid[0].mass - averages[1])
    print(grid[0].temperature, grid[0].temperature - averages[2])