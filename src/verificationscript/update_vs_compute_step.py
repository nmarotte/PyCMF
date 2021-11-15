from tqdm import tqdm

from Earth.Components.water import Water
from Earth.earth import Earth
from constants import TIME_DELTA
from sun import Sun
from units import Mass, Temperature, Volume
from universe import Universe

if __name__ == '__main__':
    uni = Universe()
    uni.earth = Earth((10, 10, 10), parent=uni)
    uni.earth.add_water(Mass(kilograms=1.4e21), Volume(meters3=1.4e21), Temperature(celsius=21))
    uni.sun = Sun(parent=uni)
    print(uni)
    for i in tqdm(range(int(60 // TIME_DELTA))):  # Computes for 60 seconds of physical time
        uni.update()
    print(uni.earth.temperature)

    uni = Universe()
    uni.earth = Earth((10, 10, 10), parent=uni)
    uni.earth.add_water(Mass(kilograms=1.4e21), Volume(meters3=1.4e21), Temperature(celsius=21))
    uni.sun = Sun(parent=uni)
    print(uni.earth.temperature)
    for i in tqdm(range(int(60 // TIME_DELTA))):  # Computes for 60 seconds of physical time
        deltas = uni.compute_step()
        uni.apply_step(deltas)
    print(uni.earth.temperature)
