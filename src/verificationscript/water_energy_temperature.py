from Earth.Components.water import Water
from units import Mass, Energy, Temperature

if __name__ == '__main__':
    water = Water(mass=Mass(grams=150), temperature=Temperature(celsius=0))
    water.add_energy(Energy(joules=16700))
    print(water.temperature.to_celsius())