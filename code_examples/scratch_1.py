import numpy as np

# Classic OOP implementation, very easy to write
class StandaloneCube:
    def __init__(self, top_left_back: tuple[int, int, int], size: int):
        self.top_left_back = top_left_back
        self.size = size


# Heavier OOP-interface, FP-backend. but faster access
class Cube:
    def __init__(self, top_left_back: tuple[int, int, int], size: int):
        self.__index = CubeHandler.get_next_index()
        self.__index = np.where(CubeHandler.instances == None)[0][0]
        CubeHandler.top_left_back_points[self.__index] = top_left_back
        CubeHandler.sizes[self.__index] = size
        CubeHandler.instances[self.__index] = self

    def push_up(self=None, *, amount: int):
        def f(a):
            return a[0], max(0, a[1]-amount), a[2]
        CubeHandler.top_left_back_points = np.apply_along_axis(f, 1, CubeHandler.top_left_back_points)

    @property
    def top_left_back(self):
        return CubeHandler.top_left_back_points[self.__index]

    @top_left_back.setter
    def top_left_back(self, value: tuple[int, int, int]):
        CubeHandler.top_left_back_points[self.__index] = value

    @property
    def size(self):
        return CubeHandler.sizes[self.__index]

    @size.setter
    def size(self, value: int):
        CubeHandler.sizes[self.__index] = value

    def __del__(self):
        CubeHandler.top_left_back_points[self.__index] = np.array([-1, -1, -1])
        CubeHandler.sizes[self.__index] = -1
        CubeHandler.instances[self.__index] = None


class CubeHandler:
    instances: np.array = np.empty(dtype=Cube, shape=200)
    top_left_back_points: np.array = np.empty(dtype=int, shape=(200, 3))
    sizes: np.array = np.empty(dtype=int, shape=200)

    @staticmethod
    def get_next_index():
        index = np.where(CubeHandler.instances == None)
        if not index:
            # Extending the arrays
            CubeHandler.top_left_back_points = np.append(CubeHandler.top_left_back_points,
                                                         np.empty_like(CubeHandler.top_left_back_points))
            CubeHandler.sizes = np.append(CubeHandler.sizes, np.empty_like(CubeHandler.sizes))
            CubeHandler.instances = np.append(CubeHandler.instances, np.empty_like(CubeHandler.instances))
            index = np.where(CubeHandler.instances == None)
        return index


if __name__ == '__main__':
    cubes = []
    test_points = np.random.randint(100, size=(200, 3))
    for p in test_points:
        cubes.append(Cube(p, 100))
    print(cubes[10].top_left_back)
    print(cubes[11].top_left_back)
    cubes = cubes[10:]
    print()
    print(cubes[0].top_left_back)
    print(cubes[1].top_left_back)
    Cube.push_up(amount=5)
    print(cubes[0].top_left_back)
    print(cubes[1].top_left_back)
    print()

    print(cubes[15].top_left_back)
    cubes[15].push_up(amount=5)
    print(cubes[15].top_left_back)
    input()

    cubes = []
    test_points = np.random.randint(100, size=(200, 3))
    for p in test_points:
        cubes.append(StandaloneCube(p, 100))
    print(cubes[10].top_left_back)
    print(cubes[11].top_left_back)
    cubes = cubes[10:]
    print(cubes[0].top_left_back)
    print(cubes[1].top_left_back)
    input()

    # test_points = np.random.randint(100, size=(200, 3))
    # test_size = 100
    # cubes = []
    # standalone_cubes = []
    # for p in test_points:
    #     cubes.append(Cube(p, test_size))
    #     standalone_cubes.append(StandaloneCube(p, test_size))
    # print(cubes[10].top_left_back)
    # cubes = cubes[10:20]
    # print(cubes[0].top_left_back)
