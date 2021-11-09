import datetime
from time import time_ns
from tqdm import tqdm

from Earth.earth import Earth
from sun import Sun
from units import Temperature, Mass, Volume
from universe import Universe

if __name__ == '__main__':
    """
    This script verifies the behavior of the sun's energy radiation towards the earth. With accurate values for the quantity 
    of water on earth, and the amount of energy received from the sun, we should get accurate results, that is the earth should not 
    gain a lot of energy each second (temperature should remain pretty stable
    
    Source for weight of water on earth : https://hypertextbook.com/facts/1998/AvijeetDut.shtml
    Source for the amount of energy radiated by the sun towards earth each second : 
    https://www.quora.com/How-many-joules-of-energy-would-be-generated-if-we-harnessed-only-one-tenth-of-the-solar-energy-striking-Earth-on-an-annual-basis
    
    """
    nb_iter = 100

    initial_water_temperature = Temperature(celsius=21)
    simulation_duration_total = 0
    after_total = 0
    print(f"Temperature at the beginning of the simulation : {initial_water_temperature}°K ")
    for n in tqdm(range(nb_iter)):
        uni = Universe()
        uni.earth = Earth((1, 1, 1), parent=uni)
        uni.earth.add_water(Mass(kilograms=1.4e21), Volume(meters3=1.4e21), initial_water_temperature)
        uni.sun = Sun()
        start = time_ns()
        for i in range(24 * 60 * 60):
            uni.update(skip_earth=True)
        stop = time_ns()
        simulation_duration_total += stop - start
        after_total += uni.earth.compute_average_temperature()
    simulation_duration_average = simulation_duration_total / nb_iter
    after_average = after_total / nb_iter
    print(f"Total simulation time for {nb_iter} runs : {simulation_duration_total / (10 ** 9)} seconds")
    print(f"Simulation time {simulation_duration_average / (10 ** 9)} seconds per 24 hours\n")

    print(f"Average temperature after 24 hours of simulating the sun's impact on earth {nb_iter} times : {after_average}°K ")
    print(f"The temperature increase of sun's energy radiation on Earth over 24 hours is {after_average - initial_water_temperature}°K\n")

    print(f"Average Ratio simulation time over real time : `{datetime.timedelta(seconds=24 * 60 * 60 / (simulation_duration_average / (10 ** 9)))}` "
          f"(one second of running the program computes X seconds of real world physics) ")
