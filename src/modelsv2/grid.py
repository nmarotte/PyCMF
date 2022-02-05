from timeit import default_timer as timer
from typing import Optional, Iterator

import numpy

from models.Earth.Components.grid_chunk import GridChunk
from models.model import Model


class Grid(list[Optional[GridChunk]], Model):
    nb_active_grid_chunks: int = 0

    def __init__(self, shape: tuple, *, parent=None):
        super().__init__()
        self.shape = shape
        self.parent = parent
        self.extend(None for _ in range(numpy.product(self.shape)))

    def __len__(self):
        """
        The size of the Grid is always the static size, not the number of elements inside of it
        :return:
        """
        return numpy.product(self.shape)

    def __setitem__(self, key, value: Optional[GridChunk]):
        """
        Makes sure that we match the number of active grind chunks when changing the Grid
        :param key:
        :param value:
        :return:
        """
        if self[key] is None and value is not None:
            self.nb_active_grid_chunks += 1
        elif self[key] is not None and value is None:
            self.nb_active_grid_chunks -= 1
        super().__setitem__(key, value)
        if value is not None:
            # If we insert an element, we need to recompute its neighbors
            value.neighbours = self.neighbours(value.index)
            for n in value.neighbours:
                n.neighbours = self.neighbours(n.index)

    def not_nones(self) -> Iterator[GridChunk]:
        """
        :return: Iterator containing all the items that are not none
        """
        return (elem for elem in self if elem is not None)

    def get_component_at(self, x, y, z=0):
        return self[x + y * self.shape[0] + z * (self.shape[0] + self.shape[1])]

    def set_component_at(self, component: GridChunk, x, y, z=0):
        self[x + y * self.shape[0] + z * (self.shape[0] + self.shape[1])] = component

    def neighbours(self, index: int) -> list[GridChunk]:
        """
        Yields the neighbouring element of the index, from front top left to back bottom right
        1D : [0,1,2,3,4,5]
        2D: [[0,1], [2,3], [4,5]
        3D: [[[0, 1], [2,3], [4,5]], [[6,7], [8,9], [10,11]]]
        :param index:
        :return:
        """
        res = []
        # 1D
        if len(self.shape) == 1:
            if index >= 1 and self[index - 1] is not None:  # Left
                res.append(self[index - 1])
            if index < len(self) - 1 and self[index + 1] is not None:  # Right
                res.append(self[index + 1])
        # 2D
        elif len(self.shape) == 2:
            if index >= self.shape[0] and self[index - self.shape[0]] is not None:  # Top
                res.append(self[index - self.shape[0]])
            if index % self.shape[0] != 0 and self[index - 1] is not None:  # Left
                res.append(self[index - 1])
            if (index + 1) % self.shape[0] != 0 and self[index + 1] is not None:  # Right
                res.append(self[index + 1])
            if index < self.shape[0] * self.shape[1] - self.shape[0] and self[index + self.shape[0]] is not None:  # Bot
                res.append(self[index + self.shape[0]])
        # 3D
        elif len(self.shape) == 3:
            # Front
            if 0 <= index - self.shape[0] * self.shape[1] and self[index - self.shape[0] * self.shape[1]] is not None:
                res.append(self[index - self.shape[0] * self.shape[1]])
            # Top
            if self.shape[0] <= index % (self.shape[0] * self.shape[1]) and self[index - self.shape[0]] is not None:
                res.append(self[index - self.shape[0]])
            # Left
            if 0 < index % self.shape[0] and self[index - 1] is not None:
                res.append(self[index - 1])
            # Right
            if 0 < (index + 1) % self.shape[0] and self[index + 1] is not None:
                res.append(self[index + 1])
            # Bottom
            if index % (self.shape[0] * self.shape[1]) < self.shape[0] * self.shape[1] - self.shape[0] and self[
                index + self.shape[0]] is not None:
                res.append(self[index + self.shape[0]])
            # Back
            if index + self.shape[0] * self.shape[1] < numpy.product(self.shape) and self[
                index + self.shape[0] * self.shape[1]] is not None:
                res.append(self[index + self.shape[0] * self.shape[1]])
        return res



if __name__ == '__main__':
    start = timer()
    # Test neighbours 1D
    shape1D = (15,)
    grid1D = Grid((15,))
    for i_test in range(len(grid1D)):
        grid1D[i_test] = GridChunk([], 1, parent=grid1D)
    assert list(grid1D.neighbours(0)) == [1]
    assert list(grid1D.neighbours(7)) == [6, 8]
    assert list(grid1D.neighbours(14)) == [13]

    # Test neighbours 2D
    shape2D = (3, 5)
    grid2D = Grid(shape2D)
    for i_test in range(len(grid2D)):
        grid2D[i_test] = GridChunk([], 1, parent=grid2D)
    assert list(grid2D.neighbours(7)) == [4, 6, 8, 10]
    assert list(grid2D.neighbours(0)) == [1, 3]
    assert list(grid2D.neighbours(2)) == [1, 5]
    assert list(grid2D.neighbours(12)) == [9, 13]
    assert list(grid2D.neighbours(14)) == [11, 13]

    # Test neighbours 3D
    shape3D = (2, 3, 4)
    grid3D = Grid(shape3D)
    for i_test in range(len(grid3D)):
        grid3D[i_test] = GridChunk([], 1, parent=grid3D)
    assert list(grid3D.neighbours(0)) == [1, 2, 6]
    assert list(grid3D.neighbours(6)) == [0, 7, 8, 12]
    assert list(grid3D.neighbours(12)) == [6, 13, 14, 18]
    assert list(grid3D.neighbours(18)) == [12, 19, 20]

    assert list(grid3D.neighbours(1)) == [0, 3, 7]
    assert list(grid3D.neighbours(7)) == [1, 6, 9, 13]
    assert list(grid3D.neighbours(13)) == [7, 12, 15, 19]
    assert list(grid3D.neighbours(19)) == [13, 18, 21]

    assert list(grid3D.neighbours(2)) == [0, 3, 4, 8]
    assert list(grid3D.neighbours(8)) == [2, 6, 9, 10, 14]
    assert list(grid3D.neighbours(14)) == [8, 12, 15, 16, 20]
    assert list(grid3D.neighbours(20)) == [14, 18, 21, 22]

    assert list(grid3D.neighbours(3)) == [1, 2, 5, 9]
    assert list(grid3D.neighbours(9)) == [3, 7, 8, 11, 15]
    assert list(grid3D.neighbours(15)) == [9, 13, 14, 17, 21]
    assert list(grid3D.neighbours(21)) == [15, 19, 20, 23]

    assert list(grid3D.neighbours(4)) == [2, 5, 10]
    assert list(grid3D.neighbours(10)) == [4, 8, 11, 16]
    assert list(grid3D.neighbours(16)) == [10, 14, 17, 22]
    assert list(grid3D.neighbours(22)) == [16, 20, 23]

    assert list(grid3D.neighbours(5)) == [3, 4, 11]
    assert list(grid3D.neighbours(11)) == [5, 9, 10, 17]
    assert list(grid3D.neighbours(17)) == [11, 15, 16, 23]
    assert list(grid3D.neighbours(23)) == [17, 21, 22]
    end = timer()
    print(end - start)
