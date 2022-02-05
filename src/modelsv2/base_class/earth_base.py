from typing import Optional, Iterator

import numpy

from modelsv2.base_model import BaseModel
from modelsv2.physical_class.grid_chunk import GridChunk


class EarthBase(list[Optional[GridChunk]], BaseModel):
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

    def get_component_at(self, x, y=0, z=0):
        return self[x + y * self.shape[0] + z * (self.shape[0] + self.shape[1])]

    def set_component_at(self, component: GridChunk, x, y=0, z=0):
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
