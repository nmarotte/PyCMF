from abc import abstractmethod


class Unit(float):
    precision = 25
    epsilon = 1 / (10 ** precision)  # We recommend matching epsilon and the precision

    @property
    @abstractmethod
    def default(self):
        """Specifies the default unit of the Unit class, for example seconds for Time, meters for Distance, ..."""

    def __eq__(self, other):
        # Either they are equal, or they are very close to each other
        return super(Unit, self).__eq__(other) or abs(self - other) <= self.epsilon

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return round(self - other, self.precision) >= self.epsilon

    def __lt__(self, other):
        return round(other - self, self.precision) >= self.epsilon

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __truediv__(self, other) -> "Unit":
        return self.__class__(**{self.default: super().__truediv__(other)})

    def copy(self):
        return self.__class__(**{self.default: self})


class Temperature(Unit):
    default = "kelvin"

    def __new__(cls, *, celsius: float = None, kelvin: float = None, fahrenheit: float = None):
        return super().__new__(cls, Temperature.to_kelvin(celsius=celsius, kelvin=kelvin, fahrenheit=fahrenheit))

    @staticmethod
    def to_kelvin(*, kelvin: float = None, celsius: float = None, fahrenheit: float = None):
        if kelvin is not None:
            return round(kelvin, Temperature.precision)
        if celsius is not None:
            return round(celsius + 273.15, Temperature.precision)
        if fahrenheit is not None:
            return round((fahrenheit + 459.67) * (5 / 9), Temperature.precision)
        return 0.0

    def to_celsius(self):
        return self - 273.15

    def to_fahrenheit(self):
        return (self - 273.15) * (9 / 5) + 32


class Mass(Unit):
    default = "kilograms"

    def __new__(cls, *, kilograms: float = None, grams: float = None, pounds: float = None):
        return super().__new__(cls, Mass.to_kilograms(kilograms=kilograms, grams=grams, pounds=pounds))

    @staticmethod
    def to_kilograms(*, kilograms: float = None, grams: float = None, pounds: float = None):
        if kilograms is not None:
            return round(kilograms, Mass.precision)
        if grams is not None:
            return round(grams / 1000, Mass.precision)
        if pounds is not None:
            return round(pounds / 2.20462, Mass.precision)
        return 0.0

    def to_grams(self):
        return 1000 * self

    def to_pounds(self):
        return self * 2.20462


class Distance(Unit):
    default = "meters"

    def __new__(cls, *, meters: float = None, yards: float = None, feet: float = None, inches: float = None):
        if meters is not None:
            return super().__new__(cls, round(meters, Distance.precision))
        if yards is not None:
            return super().__new__(cls, round(yards / 1.0936, Distance.precision))
        if feet is not None:
            return super().__new__(cls, round(feet / 3.2808, Distance.precision))
        if inches is not None:
            return super().__new__(cls, round(inches / 39.370, Distance.precision))
        return super().__new__(cls, 0.0)


class Area(Unit):
    default = "meters2"

    def __new__(cls, *, meters2: float = None, yards2: float = None, feet2: float = None, inches2: float = None):
        if meters2 is not None:
            return super().__new__(cls, round(meters2, Area.precision))
        if yards2 is not None:
            return super().__new__(cls, round(yards2 / (1.0936 ** 2), Area.precision))
        if feet2 is not None:
            return super().__new__(cls, round(feet2 / (3.2808 ** 2), Area.precision))
        if inches2 is not None:
            return super().__new__(cls, round(inches2 / (39.370 ** 2), Area.precision))
        return super().__new__(cls, 0.0)

    def to_yards2(self):
        return self * (1.0936 ** 2)

    def to_feet2(self):
        return self * (3.2808 ** 2)

    def to_inches2(self):
        return self * (39.370 ** 2)


class Volume(Unit):
    default = "meters3"

    def __new__(cls, *, meters3: float = None, yards3: float = None, feet3: float = None, inches3: float = None):
        if meters3 is not None:
            return super().__new__(cls, round(meters3, Area.precision))
        if yards3 is not None:
            return super().__new__(cls, round(yards3 / (1.0936 ** 3), Area.precision))
        if feet3 is not None:
            return super().__new__(cls, round(feet3 / (3.2808 ** 3), Area.precision))
        if inches3 is not None:
            return super().__new__(cls, round(inches3 / (39.370 ** 3), Area.precision))
        return super().__new__(cls, 0.0)

    def to_yards3(self):
        return self * (1.0936 ** 3)

    def to_feet(self):
        return self * (3.2808 ** 3)

    def to_inches3(self):
        return self * (39.370 ** 3)


class Time(Unit):
    default = "seconds"

    def __new__(cls, *, seconds: float = None, minutes: float = None, hours: float = None, days: float = None):
        if seconds is not None:
            return super().__new__(cls, round(seconds, Time.precision))
        if minutes is not None:
            return super().__new__(cls, round(minutes * 60, Time.precision))
        if hours is not None:
            return super().__new__(cls, round(hours * 3600, Time.precision))
        if days is not None:
            return super().__new__(cls, round(days * 86400, Time.precision))
        return super().__new__(cls, 0.0)


class Energy(Unit):
    default = "joules"

    def __new__(cls, *, joules: float = None):
        if joules is not None:
            return super().__new__(cls, round(joules, Energy.precision))
        return super().__new__(cls, 0.0)


if __name__ == '__main__':
    unitA = Unit(5.0000000001)
    unitB = Unit(5)
    assert unitA == unitB
    unitA = Unit(5.01)
    assert unitA > unitB

    c = Temperature(celsius=50)
    k = Temperature(kelvin=323.15)
    f = Temperature(fahrenheit=122)
    assert c == k == f

    c1 = Temperature(celsius=0)
    assert c1 == Temperature(kelvin=273.15)

    kg = Mass(kilograms=1)
    g = Mass(grams=1000)
    lb = Mass(pounds=2.20462)
    assert kg == g == lb

    m = Distance(meters=100)
    y = Distance(yards=109.36133)
    ft = Distance(feet=328.08399)
    inch = Distance(inches=3937.0079)
    assert m == y == ft == inch

    m2 = Area(meters2=100)
    y2 = Area(yards2=119.59900)
    ft2 = Area(feet2=1076.3910)
    inch2 = Area(inches2=155000.31)
    assert m2 == y2 == ft2 == inch2

    s = Time(seconds=986321)
    mi = Time(minutes=16438.683333333334)
    h = Time(hours=273.97805555555556)
    d = Time(days=11.415752314814815)
    assert s == mi == h == d

    s = Time(seconds=986321)
    assert isinstance(s / 500, Time)

    m = Mass(kilograms=1)
    m2 = m.copy()
    m += 1
    assert m == 2
    assert m2 == 1
