from timeit import default_timer as timer
from typing import Optional

import numpy

from Earth.Components.grid_component import GridComponent, Unit


class Grid(list[Optional[GridComponent]]):
    def __init__(self, shape: tuple, *, parent=None):
        super().__init__()
        self.shape = shape
        self.parent = parent
        for _ in range(numpy.product(self.shape)):
            self.append(None)

    def __len__(self):
        return numpy.product(self.shape)

    def not_nones(self):
        return (elem for elem in self if elem is not None)

    def by_row(self):
        if len(self.shape) == 1:
            for i in range(self.shape[0]):
                yield self[i]
        elif len(self.shape) == 2:
            for j in range(self.shape[1]):  # Over all the columns, yield the row
                for i in range(self.shape[0]):  # Over all the row, yield one element
                    yield self[i + j * self.shape[0]]
        elif len(self.shape) == 3:
            for k in range(self.shape[2]):
                for j in range(self.shape[1]):
                    for i in range(self.shape[0]):
                        yield self[i + j * self.shape[0] + k * self.shape[1]]

    def by_column(self):
        for i in range(self.shape[0]):  # Over all the rows, yield the column
            for j in range(self.shape[1]):  # Over all the columns, yield one element
                yield self[i + j * self.shape[0]]

    def neighbours(self, index: int) -> list[GridComponent]:
        """
        Yields the neighbouring element of the index, from front top left to back bottom right
        1D : [0,1,2,3,4,5]
        2D: [[0,1], [2,3], [4,5]
        3D: [[[0, 1], [2,3], [4,5]], [[6,7], [8,9], [10,11]]]
        :param index:
        :return:
        """
        # 1D
        if len(self.shape) == 1:
            if index >= 1:  # Left
                yield self[index - 1]
            if index < len(self) - 1:  # Right
                yield self[index + 1]
        # 2D
        elif len(self.shape) == 2:
            if index >= self.shape[0]:  # Top
                yield self[index - self.shape[0]]
            if index % self.shape[0] != 0:  # Left
                yield self[index - 1]
            if (index + 1) % self.shape[0] != 0:  # Right
                yield self[index + 1]
            if index < self.shape[0] * self.shape[1] - self.shape[0]:  # Bot
                yield self[index + self.shape[0]]
        # 3D
        elif len(self.shape) == 3:
            # Front
            if 0 <= index - self.shape[0] * self.shape[1]:
                yield self[index - self.shape[0] * self.shape[1]]
            # Top
            if self.shape[0] <= index % (self.shape[0] * self.shape[1]):
                yield self[index - self.shape[0]]
            # Left
            if 0 < index % self.shape[0]:
                yield self[index - 1]
            # Right
            if 0 < (index + 1) % self.shape[0]:
                yield self[index + 1]
            # Bottom
            if index % (self.shape[0] * self.shape[1]) < self.shape[0] * self.shape[1] - self.shape[0]:
                yield self[index + self.shape[0]]
            # Back
            if index + self.shape[0] * self.shape[1] < numpy.product(self.shape):
                yield self[index + self.shape[0] * self.shape[1]]

    def update(self):
        for elem in self:
            elem.update()


if __name__ == '__main__':
    start = timer()
    # Test neighbours 1D
    shape1D = (15,)
    grid1D = Grid((15,))
    assert list(grid1D.by_row()) == [None] * numpy.product(shape1D)
    for i_test in range(len(grid1D)):
        grid1D[i_test] = i_test
    assert list(grid1D.neighbours(0)) == [1]
    assert list(grid1D.neighbours(7)) == [6, 8]
    assert list(grid1D.neighbours(14)) == [13]

    # Test neighbours 2D
    shape2D = (3, 5)
    grid2D = Grid(shape2D)
    assert list(grid2D.by_row()) == [None] * numpy.product(shape2D)
    for i_test in range(len(grid2D)):
        grid2D[i_test] = i_test
    assert list(grid2D.neighbours(7)) == [4, 6, 8, 10]
    assert list(grid2D.neighbours(0)) == [1, 3]
    assert list(grid2D.neighbours(2)) == [1, 5]
    assert list(grid2D.neighbours(12)) == [9, 13]
    assert list(grid2D.neighbours(14)) == [11, 13]

    # Test neighbours 3D
    shape3D = (2, 3, 4)
    grid3D = Grid(shape3D)
    assert list(grid3D.by_row()) == [None] * numpy.product(shape3D)
    for i_test in range(len(grid3D)):
        grid3D[i_test] = i_test
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
