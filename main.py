import random

from models.physical_class.earth import Earth
from models.physical_class.grid_chunk import GridChunk
from models.physical_class.sun import Sun
from models.physical_class.universe import Universe
from models.ticking_class.ticking_earth import TickingEarth
from models.ticking_class.ticking_sun import TickingSun

if __name__ == "__main__":
    universe = Universe()
    universe.sun = TickingSun()  # Can be replace with Sun()
    universe.earth = TickingEarth(shape=(400, 400))  # Can be replace with Earth(shape=(400, 400))
    universe.discover_everything()

    # Fills the earth with random GridChunk of water
    filling_density = 0.1
    for i in range(len(universe.earth)):
        if random.randint(0, int(1/filling_density)):
            continue
        universe.earth[i] = GridChunk.from_components_tuple((1000, 300+random.randint(-10, 10), "WATER"), volume=1, index=0, parent=universe.earth)

    print(universe)
    if isinstance(universe.earth, TickingEarth) and isinstance(universe.sun, TickingSun):
        for i in range(10):
            universe.update_all()
        print(universe)