from units import Mass, Volume

TIME_DELTA = 0.01  # Can be adjusted to fit the time scale of the simulation
# assert TIME_DELTA < 0.5  # Otherwise might break energy conservation
water_earth_mass = Mass(kilograms=1.4e21)
water_earth_volume = Volume(meters3=1.4e21)

CANVAS_SIZE = (400, 400)
ICON_SIZE = (16, 16)

COMPONENTS = ["WATER", "AIR", "LAND"]
AIR_COMPONENTS = ["NITROGEN", "OXYGEN", "ARGON"]

SPECIFIC_HEAT_CAPACITY = {  # [J kg^-1 C^-1]
    "WATER": 4184,
    "AIR": 1012,
    "ARGON": 520.3,
    "NITROGEN": 1040,
    "OXYGEN": 918,
    "LAND": 830
}

HEAT_TRANSFER_COEFFICIENT = {  # [W m^-2 K^-1]
    "WATER": 1000,
    "AIR": 12.5,  # 12.5 = 0.78*Nitrogen + 0.21*Oxygen + 0.01*Argon
    "ARGON": 1,  # Computed/Made up
    "NITROGEN": 10,  # Computed/Made up
    "OXYGEN": 22.3,  # Computed/Made up
    "LAND": 250  # Made up
}
