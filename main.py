from tqdm import tqdm

from models.Earth.earth import Earth
from sun import Sun
from units import *
from universe import Universe

if __name__ == '__main__':
    universe = Universe()
    universe.earth = Earth((10, 10, 10), parent=universe)
    universe.sun = Sun(parent=universe)
    universe.earth.add_water(Mass(kilograms=1.4e21), Volume(meters3=1.4e21), Temperature(celsius=21))
    print(universe.earth.average_temperature)
    print(universe.earth[0].temperature)
    for i in tqdm(range(60*60*24)):
        universe.update(skip_sun=True)
    print(universe.earth.average_temperature)
    print(universe.earth[0].temperature)