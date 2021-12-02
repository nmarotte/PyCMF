from random import random

from tqdm import tqdm

from models.Earth.Components.water import Water
from models.Earth.earth import Earth
from constants import TIME_DELTA
from units import Temperature
from universe import Universe

if __name__ == '__main__':
    uni = Universe()
    uni.earth = Earth((10, 10, 10), parent=uni)
    for i in range(len(uni.earth)):
        uni.earth[i] = Water(temperature=Temperature(celsius=10 + 20 * random()), parent=uni.earth, index=i)


    print(uni.earth[0].temperature)
    print(uni.earth.average_temperature)
    number_of_steps = int(600 // TIME_DELTA)  # 60 times the number of steps in 1 seconds
    for i in tqdm(range(number_of_steps)):
        uni.update()
    print(uni.earth[0].temperature)
    print(uni.earth.average_temperature)

