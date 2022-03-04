import unittest


class TestTickingUniverse(unittest.TestCase):
    pass

    # def test_universe_profiling(self):
    #     # Uncomment to profile the update loop for around 70s
    #     earth = TickingEarth(shape=(40, 40))
    #     for i in range(40*40):
    #         earth[i] = TickingGridChunk.from_components_tuple((1000, random.randint(273, 300), "WATER"), volume=1, index=0, parent=earth)
    #     sun = TickingSun()
    #     for i in range(500):
    #         sun.get_universe().update_all()
