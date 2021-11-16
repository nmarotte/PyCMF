from units import Mass, Volume

TIME_DELTA = 1  # Can be adjusted to fit the time scale of the simulation
# assert TIME_DELTA < 0.5  # Otherwise might break energy conservation
water_earth_mass = Mass(kilograms=1.4e21)
water_earth_volume = Volume(meters3=1.4e21)
