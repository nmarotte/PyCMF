from units import Mass, Volume

TIME_DELTA = 0.01  # Can be adjusted to fit the time scale of the simulation
# assert TIME_DELTA < 0.5  # Otherwise might break energy conservation
water_earth_mass = Mass(kilograms=1.4e21)
water_earth_volume = Volume(meters3=1.4e21)

COMPONENTS = ["Water", "Air", "Land"]
AIR_COMPONENTS = ["Nitrogen", "Oxygen", "Argon"]

SPECIFIC_HEAT_CAPACITY = {  # [J kg^-1 C^-1]
    "Water": 4184,
    "Air": 1012,
    "Argon": 520.3,
    "Nitrogen": 1040,
    "Oxygen": 918,
    "Land": 830
}

HEAT_TRANSFER_COEFFICIENT = {  # [W m^-2 K^-1]
    "Water": 1000,
    "Air": 12.5,  # 12.5 = 0.78*Nitrogen + 0.21*Oxygen + 0.01*Argon
    "Argon": 1,  # Computed/Made up
    "Nitrogen": 10,  # Computed/Made up
    "Oxygen": 22.3,  # Computed/Made up
    "Land": 250  # Made up
}
