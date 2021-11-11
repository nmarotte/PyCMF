from random import random

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
    for i in range(len(uni.earth)):
        uni.earth[i] = Water(temperature=Temperature(celsius=10 + 20 * random()), parent=uni.earth, index=i)

    for elem in uni.earth:
        print(elem.temperature)
    print(uni.earth.compute_average_temperature())
    number_of_steps = int(6000 // TIME_DELTA)  # 60 times the number of steps in 1 seconds
    for i in tqdm(range(number_of_steps)):
        deltas = uni.compute_step()
        uni.apply_step(deltas)
    for elem in uni.earth:
        print(elem.temperature)
    print(uni.earth.compute_average_temperature())

