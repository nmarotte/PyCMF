import numpy as np


def neighbors_single(index_single: int, shape: tuple):
    if len(shape) not in [3,2]:
        raise NotImplemented
    index_multi = np.unravel_index(index_single, shape)
    for dim in range(len(shape)):
        if index_multi[dim] > 0:
            yield np.ravel_multi_index([im - 1 if i == dim else im for i, im in enumerate(index_multi)], shape)


def neighbors_multi(index_multi: int, shape: tuple):
    if len(shape) not in [2]:
        raise NotImplemented
    i, j = index_multi

    # Top Row
    if i-1 >= 0:
        yield i-1, j

    # Middle Row
    if j-1 >= 0:
        yield i, j-1

