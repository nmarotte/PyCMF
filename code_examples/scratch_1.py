from typing import Iterable

import numpy as np


# Classic OOP implementation, very easy to write
class StandaloneCube:
    top_left_back_point: np.array
    size: int

    def __init__(self, top_left_back_point: tuple[int, int, int], size: int):
        self.top_left_back_point = np.array(top_left_back_point)
        self.size = size

    def push_up(self, amount: int):
        self.top_left_back_point[1] = max(0, self.top_left_back_point[1] - amount)


# Heavier OOP-interface, FP-backend. but faster access
class Cube:
    def __init__(self, top_left_back_point: tuple[int, int, int], size: int):
        self.__index = CubeHandler.get_next_index()
        CubeHandler.top_left_back_points[self.__index] = top_left_back_point
        CubeHandler.sizes[self.__index] = size
        CubeHandler.instances[self.__index] = self

    @staticmethod
    def batch_push_up(indexes: Iterable[int], amount: int):
        CubeHandler.top_left_back_points = np.apply_along_axis()
        for i in indexes:
            CubeHandler.top_left_back_points[i][1] = max(0, CubeHandler.top_left_back_points[i][1] - amount)

    def push_up(self, amount: int):
        if self is None:
            self = CubeHandler.instances
        if isinstance(self, Cube):
            self = [self]
        for cube in self:
            if cube is None:
                continue
            cube.top_left_back_point[1] = max(0, cube.top_left_back_point[1] - amount)

    @property
    def top_left_back_point(self):
        return CubeHandler.top_left_back_points[self.__index]

    @top_left_back_point.setter
    def top_left_back_point(self, value: tuple[int, int, int]):
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
    instances: np.array = np.empty(dtype=Cube, shape=20)
    top_left_back_points: np.array = np.empty(dtype=int, shape=(200, 3))
    sizes: np.array = np.empty(dtype=int, shape=200)

    @staticmethod
    def get_next_index():
        index = np.where(CubeHandler.instances == None)[0]
        if not index.size > 0:
            # Extending the arrays
            CubeHandler.top_left_back_points = np.append(CubeHandler.top_left_back_points,
                                                         np.empty_like(CubeHandler.top_left_back_points), axis=0)
            CubeHandler.sizes = np.append(CubeHandler.sizes, np.empty_like(CubeHandler.sizes))
            CubeHandler.instances = np.append(CubeHandler.instances, np.empty_like(CubeHandler.instances))
            index = np.where(CubeHandler.instances == None)[0]
        return index[0]


if __name__ == '__main__':
    cubes = np.empty(shape=200, dtype=Cube)
    for i in range(21):
        cubes[i] = Cube(np.random.randint(100, size=3), 200)

    print(cubes[0].top_left_back_point)
    print(cubes[15].top_left_back_point)
    Cube.batch_push_up(range(10, 25), 5)
    print(cubes[0].top_left_back_point)
    print(cubes[15].top_left_back_point)

    # print("Removing the first 10 cubes of the array. Showing index 10 and 11")
    # print(cubes[10].top_left_back_point)
    # print(cubes[11].top_left_back_point)
    # cubes = cubes[10:]
    # print("They are now indexes 0 and 1\n")
    # print("Showing index 0 and 1")
    # print(cubes[0].top_left_back_point)
    # print(cubes[1].top_left_back_point)
    # Cube.push_up(cubes, 5)
    # print("Pushing up all cubes with a value of 5")
    # print(cubes[0].top_left_back_point)
    # print(cubes[1].top_left_back_point)
    # print("\nApplying push_up of value 20 to all cubes with indexes between 10 and 19 included")
    # print(list(x.top_left_back_point[1] for x in cubes[10:20]))
    # Cube.push_up(cubes[10:20], 20)
    # print(list(x.top_left_back_point[1] for x in cubes[10:20]))
    # print(cubes[11].top_left_back_point)
    # print("Applying push_up of value 5 to one particular cube of index 15")
    # print(cubes[15].top_left_back_point)
    # cubes[15].push_up(amount=5)
    # print(cubes[15].top_left_back_point)
    # input()
    #
    # cubes = []
    # test_points = np.random.randint(100, size=(200, 3))
    # for p in test_points:
    #     cubes.append(StandaloneCube(p, 100))
    # print(cubes[10].top_left_back_point)
    # print(cubes[11].top_left_back_point)
    # cubes = cubes[10:]
    # print(cubes[0].top_left_back_point)
    # print(cubes[1].top_left_back_point)
    # input()
