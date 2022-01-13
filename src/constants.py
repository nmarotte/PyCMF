water_earth_mass = 1.4e21
water_earth_volume = 1.4e21
earth_radiation_ratio = 00000002.87e-7  # The proportion of the sun's radiation the earth receives
# https://www.quora.com/What-percentage-of-the-suns-energy-actually-ends-up-on-Earth

CANVAS_SIZE = (400, 400)
ICON_SIZE = (16, 16)

COMPONENTS = ["WATER", "AIR", "LAND"]
DEFAULT_MASSES = [1000, 1.29, 1800]
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
